
import time
import threading
import grp
import pwd
import os
import ssl

import wayround_org.utils.osutils
import wayround_org.utils.socket

import wayround_org.http.message

import wayround_org.webserver.config
import wayround_org.webserver.socket
import wayround_org.webserver.application


class Server:

    def __init__(
            self,
            config_filepath
            ):

        self._config_filepath = config_filepath

        self.socket_pool = None
        self.application_pool = None

        self.gid = None
        self.uid = None

        return

    def start(self):

        cfg = wayround_org.webserver.config.read_from_fs(self._config_filepath)

        self.socket_pool = wayround_org.webserver.socket.Pool(
            cfg,
            self.callable_target_for_socket_pool,
            cls_to_use=wayround_org.webserver.socket.Socket
            )
        self.application_pool = wayround_org.webserver.application.Pool(
            cfg,
            self,
            self.socket_pool
            )

        self.socket_pool.connect_applications(self.application_pool)

        self.application_pool.start()
        self.socket_pool.start()

        self.gid = None
        self.uid = None

        try:
            self.gid = cfg['general']['gid']
        except KeyError:
            pass

        try:
            self.uid = cfg['general']['uid']
        except KeyError:
            pass

        self.gid, self.uid = wayround_org.utils.osutils.convert_gid_uid(
            self.gid, self.uid
            )

        if self.gid is not None:
            os.setregid(self.gid, self.gid)

        if self.uid is not None:
            os.setreuid(self.uid, self.uid)

        return

    def stop(self):
        self.socket_pool.stop()
        self.application_pool.stop()
        return

    def wait(self):
        return

    def wait_for_shutdown(self):
        print("Press CTRL+C to shutdown")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("CTRL+C pressed - shutting down.. please wait..")
        self.stop()
        self.wait()
        return

    def callable_target_for_socket_pool(
            self,
            transaction_id,
            serv,
            serv_stop_event,
            sock,
            addr,
            ws_socket_inst
            ):

        sock.setblocking(False)

        if isinstance(sock, ssl.SSLSocket):
            wayround_org.utils.socket.nb_handshake(
                sock,
                stop_event=serv_stop_event
                )

        error = False
        ws_application_inst = None

        (header_bytes, line_terminator,
            request_line_parsed, header_fields,
            error) = wayround_org.http.message.read_and_parse_header(sock)

        if error:
            print("Some error on read_and_parse_header()")

        if error:
            # in case of error socket must be closed anyway
            sock.close()

        if not error:

            host_field_value = None

            if ws_socket_inst.default_application_name is not None:
                ddn = self.application_pool.get_by_name(
                    ws_socket_inst.default_application_name
                    )

                if ddn is not None:
                    host_field_value = ddn.domain
                else:
                    raise Exception(
                        "configure: socket has default application name, "
                        "but it's not found int application pool"
                        )

            host_field_value_client_provided = False

            for i in header_fields:
                if i[0].lower() == 'host':
                    host_field_value = i[1]
                    host_field_value_client_provided = True
                    break

            if host_field_value is None:
                self.error_socket_shutdown(
                    sock,
                    wayround_org.http.message.HTTPResponse(
                        500,
                        None,
                        "Internal Server Error: "
                        "not configured default and "
                        "not Host request field provided"
                        )
                    )
                error = True

        if not error:
            if host_field_value is not None:
                if not host_field_value in ws_socket_inst.domains:
                    self.error_socket_shutdown(
                        sock,
                        wayround_org.http.message.HTTPResponse(
                            500,
                            None,
                            "Internal Server Error: "
                            "requested Host not served by this socket"
                            )
                        )
                    error = True

        if not error:
            ws_application_inst = ws_socket_inst.domains[host_field_value]

            # creating new thread here to free all unneeded resources used by
            # callable_target_for_socket_pool()

            t = threading.Thread(
                name='callable_target_for_socket_pool child',
                target=ws_application_inst.module_inst.callable_for_webserver,
                args=(
                    transaction_id,
                    serv,
                    serv_stop_event,
                    sock,
                    addr,

                    ws_socket_inst,
                    ws_application_inst,

                    header_bytes,
                    line_terminator,
                    request_line_parsed,
                    header_fields
                    )
                )
            t.start()

        return

    def error_socket_shutdown(self, sock, http_response):
        http_response.send_into_socket(sock)
        sock.shutdown(socket.SHUT_WR)
        sock.close()
        return
