
import logging
import select
import socket
import threading
import time
import gc
import copy
import os
import subprocess

import wayround_org.http.message

import wayround_org.webserver.module_miscs


class WebServerAppModule:

    def __init__(
            self,
            ws_inst,
            socket_pool,
            domain_pool,
            config_params
            ):
        """
        parameters:

          address - domain name or IP
          port    - port number
        """
        self.remote_address = config_params['address']
        self.remote_port = config_params['port']

        self.host_mode = 'pass'
        if 'host_mode' in config_params:
            self.host_mode = config_params['host_mode']

        if not self.host_mode in ['pass', 'use_addr_port', 'custom']:
            raise ValueError(
                "invalid `host_mode' in `{}' app config"
                )

        self.host_value = None
        if 'host_value' in config_params:
            self.host_value = config_params['host_value']

        # print("before on_start")

        self.on_start = None
        if 'on_start' in config_params:
            _t = config_params['on_start']

            self.on_start = {
                'gid': _t.get('gid', None),
                'uid': _t.get('uid', None),
                'cmd': _t.get('cmd', None),
                'args': _t.get('args', None),
                'cwd': _t.get('cwd', None)
                }

            # print("on_start set to: {}".format(self.on_start))

        self._proc = None

        self.gid = None
        self.uid = None

        return

    def start(self):
        if self.on_start is not None:

            # checking uid and gid

            try:
                self.gid = self.on_start['gid']
            except KeyError:
                pass

            try:
                self.uid = self.on_start['uid']
            except KeyError:
                pass

            self.gid, self.uid = \
                wayround_org.webserver.module_miscs.reformat_gid_uid(
                    self.gid,
                    self.uid
                    )

            # starting process

            cmd = []

            cmd += [self.on_start['cmd']]

            if self.on_start['args']:
                cmd += self.on_start['args']

            # print("starting: {}".format(' '.join(cmd)))

            self._httpd_process = subprocess.Popen(
                cmd,
                cwd=self.on_start['cwd'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=wayround_org.webserver.module_miscs.demote_subprocess(
                    self.gid,
                    self.uid
                    )
                )

        return

    def stop(self):
        if self.on_start is not None:
            if self._proc is not None:
                self._proc.terminate()
        return

    def wait(self):
        if self.on_start is not None:
            self.on_start.wait()
        return

    def callable_for_webserver(
            self,
            transaction_id,
            serv,
            serv_stop_event,
            sock,
            addr,

            ws_socket_inst,
            ws_domain_inst,

            header_bytes,
            line_terminator,
            request_line_parsed,
            header_fields
            ):

        remote_socket = socket.socket()
        remote_socket.setblocking(False)

        while True:
            try:
                remote_socket.connect((self.remote_address, self.remote_port))
            except BlockingIOError:
                pass
            except:
                raise
            else:
                break

        header_fields = \
            wayround_org.webserver.module_miscs.host_value_hendeling_routine(
                header_fields,
                self.host_mode,
                self.remote_address,
                self.remote_port,
                self.host_value
                )

        http_req = wayround_org.http.message.HTTPRequest(
            transaction_id,
            serv,
            serv_stop_event,
            sock,
            addr,
            request_line_parsed,
            header_fields
            )

        http_req2 = wayround_org.http.message.ClientHTTPRequest(
            http_req.method,
            http_req.requesttarget,
            http_req.header_fields,
            ''
            )

        reassembled_header_bytes = http_req2.format_header() + line_terminator

        stop_event = threading.Event()

        wayround_org.utils.socket.nb_sendall(
            remote_socket,
            reassembled_header_bytes,
            stop_event
            )

        wayround_org.webserver.module_miscs.proxify_socket_threads(
            sock,
            remote_socket,
            'some',
            stop_event
            )

        try:
            sock.shutdown(socket.SHUT_WR)
        except:
            logging.exception('s1')

        try:
            remote_socket.shutdown(socket.SHUT_WR)
        except:
            logging.exception('s1')

        try:
            sock.close()
        except:
            logging.exception('c1')

        try:
            remote_socket.close()
        except:
            logging.exception('c2')

        return
