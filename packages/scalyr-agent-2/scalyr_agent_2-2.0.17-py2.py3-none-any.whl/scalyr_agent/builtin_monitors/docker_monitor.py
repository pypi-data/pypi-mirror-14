# Copyright 2014 Scalyr Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------
# author:  Imron Alston <imron@imralsoftware.com>

__author__ = 'imron@imralsoftware.com'

import datetime
import logging
import os
import re
import socket
import stat
import struct
import sys
import time
import threading
from scalyr_agent import ScalyrMonitor, define_config_option
import scalyr_agent.util as scalyr_util
import scalyr_agent.json_lib as json_lib
import scalyr_agent.scalyr_logging as scalyr_logging
from scalyr_agent.json_lib import JsonObject
from scalyr_agent.json_lib import JsonConversionException, JsonMissingFieldException
from scalyr_agent.log_watcher import LogWatcher
from scalyr_agent.monitor_utils.server_processors import LineRequestParser
from scalyr_agent.monitor_utils.server_processors import RequestSizeExceeded
from scalyr_agent.monitor_utils.server_processors import RequestStream

from scalyr_agent.util import StoppableThread

from scalyr_agent.util import RunState

global_log = scalyr_logging.getLogger(__name__)

__monitor__ = __name__

define_config_option(__monitor__, 'module',
                     'Always ``scalyr_agent.builtin_monitors.docker_monitor``',
                     convert_to=str, required_option=True)

define_config_option( __monitor__, 'container_name',
                     'Optional (defaults to scalyr-agent). Defines the name given to the container running the scalyr-agent\n'
                     'You should make sure to specify this same name when creating the docker container running scalyr\n'
                     'e.g. docker run --name scalyr-agent ...',
                     convert_to=str, default='scalyr-agent')

define_config_option( __monitor__, 'api_socket',
                     'Optional (defaults to /var/scalyr/docker.sock). Defines the unix socket used to communicate with the docker API.\n'
                     'Note:  You need to map the host\'s /run/docker.sock to the same value as specified here, using the -v parameter, e.g.\n'
                     '\tdocker run -v /run/docker.sock:/var/scalyr/docker.sock ...',
                     convert_to=str, default='/var/scalyr/docker.sock')

define_config_option( __monitor__, 'docker_log_prefix',
                     'Optional (defaults to docker). Prefix added to the start of all docker logs. ',
                     convert_to=str, default='docker')

define_config_option( __monitor__, 'max_previous_lines',
                     'Optional (defaults to 5000). The maximum number of lines to read backwards from the end of the stdout/stderr logs\n'
                     'when starting to log a containers stdout/stderr.',
                     convert_to=int, default=5000)

define_config_option( __monitor__, 'log_timestamps',
                     'Optional (defaults to False). If true, stdout/stderr logs will contain docker timestamps at the beginning of the line\n',
                     convert_to=bool, default=False)

class DockerRequest( object ):

    def __init__( self, sock_file, max_request_size=64*1024 ):
        self.__socket = socket.socket( socket.AF_UNIX, socket.SOCK_STREAM )
        self.__socket.connect( sock_file )
        self.__line_request = LineRequestParser( max_request_size, eof_as_eol=True )
        self.__request_stream = RequestStream( self.__socket, self.__line_request.parse_request, max_request_size, max_request_size )
        self.__headers = []

    def get( self, path ):
        endpoint = "GET %s HTTP/1.0\r\n\r\n" % path
        self.__socket.sendall( endpoint )
        self.__read_headers()
        return self

    def response_body( self ):

        result = ""
        while not self.__request_stream.at_end():
            line = self.__request_stream.read_request()
            if line != None:
                result += line

        return result

    def readline( self ):
        #Make sure the headers have been read - this might not be the case for some queries
        #even if __read_headers() has already been called
        if len( self.__headers ) == 0:
            self.__read_headers()
            return None

        return self.__request_stream.read_request()

    def __read_headers( self ):
        """reads HTTP headers from the request stream, leaving the stream at the first line of data"""
        self.response_code = 400
        self.response_message = "Bad request"

        #first line is response code
        line = self.__request_stream.read_request()
        if not line:
            return

        match = re.match( '^(\S+) (\d+) (.*)$', line.strip() )
        if not match:
            return

        if match.group(1).startswith( 'HTTP' ):
            self.response_code = int( match.group(2) )
            self.response_message = match.group(3)
            self.__headers = []
            while not self.__request_stream.at_end():
                line = self.__request_stream.read_request()
                if line == None:
                    break
                else:
                    cur_line = line.strip()
                    if len( cur_line ) == 0:
                        break
                    else:
                        self.__headers.append( cur_line )

class DockerLogger( object ):
    def __init__( self, socket_file, cid, name, stream, log_path, config, last_request=None, max_log_size=20*1024*1024, max_log_rotations=2 ):
        self.__socket_file = socket_file
        self.cid = cid
        self.name = name
        self.stream = stream
        self.log_path = log_path
        self.stream_name = name + "-" + stream

        self.__max_previous_lines = config.get( 'max_previous_lines' )
        self.__log_timestamps = config.get( 'log_timestamps' )

        self.__last_request_lock = threading.Lock()

        self.__last_request = time.time()
        if last_request:
            self.__last_request = last_request

        self.__logger = logging.Logger( cid + '.' + stream )

        self.__log_handler = logging.handlers.RotatingFileHandler( filename = log_path, maxBytes = max_log_size, backupCount = max_log_rotations )
        formatter = logging.Formatter()
        self.__log_handler.setFormatter( formatter )
        self.__logger.addHandler( self.__log_handler )
        self.__logger.setLevel( logging.INFO )

        self.__thread = StoppableThread( target=self.process_request, name="Docker monitor logging thread for %s" % (name + '.' + stream) )

    def start( self ):
        self.__thread.start()

    def stop( self, wait_on_join=True, join_timeout=5 ):
        self.__thread.stop( wait_on_join=wait_on_join, join_timeout=join_timeout )

    def last_request( self ):
        self.__last_request_lock.acquire()
        result = self.__last_request
        self.__last_request_lock.release()
        return result

    def process_request( self, run_state ):
        request = DockerRequest( self.__socket_file )
        request.get( '/containers/%s/logs?%s=1&follow=1&tail=%d&timestamps=1' % (self.cid, self.stream, self.__max_previous_lines) )

        epoch = datetime.datetime.utcfromtimestamp( 0 )

        while run_state.is_running():
            line = request.readline()
            while line:
                line = self.strip_docker_header( line )
                dt, log_line = self.split_datetime_from_line( line )
                if not dt:
                    global_log.error( 'No timestamp found on line: \'%s\'', line )
                else:
                    timestamp = scalyr_util.seconds_since_epoch( dt, epoch )

                    #see if we log the entire line including timestamps
                    if self.__log_timestamps:
                        log_line = line

                    #check to make sure timestamp is >= to the last request
                    #Note: we can safely read last_request here because we are the only writer
                    if timestamp >= self.__last_request:
                        self.__logger.info( log_line.strip() )

                        #but we need to lock for writing
                        self.__last_request_lock.acquire()
                        self.__last_request = timestamp
                        self.__last_request_lock.release()

                line = request.readline()
            run_state.sleep_but_awaken_if_stopped( 0.1 )

        # we are shutting down, so update our last request to be slightly later than it's current
        # value to prevent duplicate logs when starting up again.
        self.__last_request_lock.acquire()

        #can't be any smaller than 0.01 because the time value is only saved to 2 decimal places
        #on disk
        self.__last_request += 0.01

        self.__last_request_lock.release()

    def strip_docker_header( self, line ):
        """Docker prepends some lines with an 8 byte header.  The first 4 bytes a byte containg the stream id
        0, 1 or 2 for stdin, stdout and stderr respectively, followed by 3 bytes of padding.

        The next 4 bytes contain the size of the message.

        This function checks for the existence of the the 8 byte header and if the length field matches the remaining
        length of the line then it strips the first 8 bytes.

        If the lengths don't match or if an expected stream type is not found then the line is left alone
        """

        # the docker header has a stream id, which is a single byte, followed by 3 bytes of padding
        # and then a 4-byte int in big-endian (network) order
        fmt = '>B3xI'
        size = struct.calcsize( fmt )

        # make sure the length of the line has as least as many bytes required by the header
        if len( line ) >= size:
            stream, length = struct.unpack( fmt, line[0:size] )

            # We expect a value of 0, 1 or 2 for stream.  Anything else indicates we don't have
            # a docker header
            # We also expect length to be the length of the remaining line
            if stream in [ 0, 1, 2 ] and len( line[size:] ) == length:
                #We have a valid docker header, so strip it
                line = line[size:]

        return line


    def split_datetime_from_line( self, line ):
        """Docker timestamps are in RFC3339 format: 2015-08-03T09:12:43.143757463Z, with everything up to the first space
        being the timestamp.
        """
        log_line = line
        dt = datetime.datetime.utcnow()
        pos = line.find( ' ' )
        if pos > 0:
            dt = scalyr_util.rfc3339_to_datetime( line[0:pos] )
            log_line = line[pos+1:]

        return (dt, log_line)




class DockerMonitor( ScalyrMonitor ):
    """Monitor plugin for docker containers

    This plugin accesses the Docker API to detect all containers running on a given host, and then logs messages from stdin and stdout
    to Scalyr servers.
    """

    def __get_socket_file( self ):
        """Gets the Docker API socket file and validates that it is a UNIX socket
        """
        #make sure the API socket exists and is a valid socket
        api_socket = self._config.get( 'api_socket' )
        try:
            st = os.stat( api_socket )
            if not stat.S_ISSOCK( st.st_mode ):
                raise Exception()
        except:
            raise Exception( "The file '%s' specified by the 'api_socket' configuration option does not exist or is not a socket.\n\tPlease make sure you have mapped the docker socket from the host to this container using the -v parameter.\n\tNote: Due to problems Docker has mapping symbolic links, you should specify the final file and not a path that contains a symbolic link, e.g. map /run/docker.sock rather than /var/run/docker.sock as on many unices /var/run is a symbolic link to the /run directory." % api_socket )

        return api_socket

    def __get_scalyr_container_id( self, socket_file ):
        """Gets the container id of the scalyr-agent container
        If the config option container_name is empty, then it is assumed that the scalyr agent is running
        on the host and not in a container and None is returned.
        """
        result = None
        name = self._config.get( 'container_name' )

        if name:
            request = DockerRequest( socket_file ).get( "/containers/%s/json" % name )

            if request.response_code == 200:
                json = json_lib.parse( request.response_body() )
                result = json['Id']

            if not result:
                raise Exception( "Unabled to find a matching container id for container '%s'.  Please make sure that a container named '%s' is running." % (name, name) )

        return result

    def __get_running_containers( self, socket_file ):
        """Gets a dict of running containers that maps container id to container name
        """
        request = DockerRequest( socket_file ).get( "/containers/json" )

        result = {}
        if request.response_code == 200:
            json = json_lib.parse( request.response_body() )
            for container in json:
                cid = container['Id']
                if not cid == self.container_id:
                    try:
                        containerRequest = DockerRequest( socket_file ).get( "/containers/%s/json" % cid )
                        if containerRequest.response_code == 200:
                            body = containerRequest.response_body()
                            containerJson = json_lib.parse( body )

                            result[cid] = containerJson['Name'].lstrip( '/' )
                    except:
                        result[cid] = cid
        return result

    def __create_log_config( self, parser, path, attributes ):

        return { 'parser': parser,
                 'path': path,
                 'attributes': attributes
               }

    def __get_docker_logs( self, containers ):
        result = []

        attributes = None
        try:
            attributes = JsonObject( { "monitor": "agentDocker" } )
            if self.__host_hostname:
                attributes['serverHost'] = self.__host_hostname

        except Exception, e:
            self._logger.error( "Error setting monitor attribute in DockerMonitor" )
            raise

        prefix = self._config.get( 'docker_log_prefix' ) + '-'

        for cid, name in containers.iteritems():
            path =  prefix + name + '-stdout.log'
            log_config = self.__create_log_config( parser='dockerStdout', path=path, attributes=attributes )
            result.append( { 'cid': cid, 'stream': 'stdout', 'log_config': log_config } )

            path = prefix + name + '-stderr.log'
            log_config = self.__create_log_config( parser='dockerStderr', path=path, attributes=attributes )
            result.append( { 'cid': cid, 'stream': 'stderr', 'log_config': log_config } )

        return result

    def _initialize( self ):
        data_path = ""
        self.__host_hostname = ""
        if self._global_config:
            data_path = self._global_config.agent_data_path

            if self._global_config.server_attributes:
                if 'serverHost' in self._global_config.server_attributes:
                    self.__host_hostname = self._global_config.server_attributes['serverHost']
                else:
                    self._logger.info( "no server host in server attributes" )
            else:
                self._logger.info( "no server attributes in global config" )

        self.__checkpoint_file = os.path.join( data_path, "docker-checkpoints.json" )

        self.__socket_file = self.__get_socket_file()
        self.__checkpoints = {}
        self.container_id = self.__get_scalyr_container_id( self.__socket_file )
        self.__log_watcher = None
        self.__start_time = time.time()

    def set_log_watcher( self, log_watcher ):
        """Provides a log_watcher object that monitors can use to add/remove log files
        """
        self.__log_watcher = log_watcher

    def __create_docker_logger( self, log ):
        cid = log['cid']
        name = self.containers[cid]
        stream = log['stream']
        stream_name = name + '-' + stream
        last_request = self.__start_time
        if stream_name in self.__checkpoints:
            last_request = self.__checkpoints[stream_name]

        logger = DockerLogger( self.__socket_file, cid, name, stream, log['log_config']['path'], self._config, last_request )
        logger.start()
        return logger

    def __stop_loggers( self, stopping ):
        if stopping:
            for logger in self.docker_loggers:
                if logger.cid in stopping:
                    logger.stop( wait_on_join=True, join_timeout=1 )
                    if self.__log_watcher:
                        self.__log_watcher.remove_log_path( self, logger.log_path )

            self.docker_loggers[:] = [l for l in self.docker_loggers if l.cid not in stopping]
            self.docker_logs[:] = [l for l in self.docker_logs if l['cid'] not in stopping]

    def __start_loggers( self, starting ):
        if starting:
            docker_logs = self.__get_docker_logs( starting )
            for log in docker_logs:
                if self.__log_watcher:
                    log['log_config'] = self.__log_watcher.add_log_config( self, log['log_config'] )
                self.docker_loggers.append( self.__create_docker_logger( log ) )

            self.docker_logs.extend( docker_logs )

    def __load_checkpoints( self ):
        try:
            checkpoints = scalyr_util.read_file_as_json( self.__checkpoint_file )
        except:
            self._logger.info( "No checkpoint file '%s' exists.\n\tAll logs will be read starting from their current end.", self.__checkpoint_file )
            checkpoints = {}

        if checkpoints:
            for name, last_request in checkpoints.iteritems():
                self.__checkpoints[name] = last_request

    def __update_checkpoints( self ):
        """Update the checkpoints for when each docker logger logged a request, and save the checkpoints
        to file.
        """

        for logger in self.docker_loggers:
            last_request = logger.last_request()
            self.__checkpoints[logger.stream_name] = last_request

        # save to disk
        if self.__checkpoints:
            tmp_file = self.__checkpoint_file + '~'
            scalyr_util.atomic_write_dict_as_json_file( self.__checkpoint_file, tmp_file, self.__checkpoints )

    def gather_sample( self ):
        self.__update_checkpoints()

        running_containers = self.__get_running_containers( self.__socket_file )

        #get the containers that have started since the last sample
        starting = {}
        for cid, name in running_containers.iteritems():
            if cid not in self.containers:
                self._logger.info( "Starting logger for container '%s'" % name )
                starting[cid] = name

        #get the containers that have stopped
        stopping = {}
        for cid, name in self.containers.iteritems():
            if cid not in running_containers:
                self._logger.info( "Stopping logger for container '%s'" % name )
                stopping[cid] = name

        #stop the old loggers
        self.__stop_loggers( stopping )

        #update the list of running containers
        #do this before starting new ones, as starting up new ones
        #will access self.containers
        self.containers = running_containers

        #start the new ones
        self.__start_loggers( starting )


    def run( self ):
        self.__load_checkpoints()
        self.containers = self.__get_running_containers( self.__socket_file )
        self.docker_logs = self.__get_docker_logs( self.containers )
        self.docker_loggers = []

        #create and start the DockerLoggers
        for log in self.docker_logs:
            if self.__log_watcher:
                log['log_config'] = self.__log_watcher.add_log_config( self, log['log_config'] )
            self.docker_loggers.append( self.__create_docker_logger( log ) )

        self._logger.info( "Initialization complete.  Starting docker monitor for Scalyr" )
        ScalyrMonitor.run( self )

    def stop(self, wait_on_join=True, join_timeout=5):
        #stop the main server
        ScalyrMonitor.stop( self, wait_on_join=wait_on_join, join_timeout=join_timeout )

        #stop the DockerLoggers
        for logger in self.docker_loggers:
            if self.__log_watcher:
                self.__log_watcher.remove_log_path( self, logger.log_path )
            logger.stop( wait_on_join, join_timeout )
            self._logger.info( "Stopping %s - %s" % (logger.name, logger.stream) )

        self.__update_checkpoints()

