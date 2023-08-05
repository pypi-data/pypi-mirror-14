
import runpy

import wayround_org.http.server
import wayround_org.wsgi.server


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

          runmode: (one of two values)
            file - load module from filesystem
            module - load module using python import mechanism

          file_or_module_name - depending on runmode value,
              full path to file to load as python module,
              or full python module path to import

          callable_name - name of callable in this file which
              returns WSGI callable
        """
        runmode = config_params['runmode']
        file_or_module_name = config_params['file_or_module_name']
        callable_name = config_params['callable_name']

        self.wsgi_callable = None

        if runmode == 'file':
            res1 = runpy.run_path(file_or_module_name)
            res2 = res1[callable_name]
            self.wsgi_callable = res2()
        elif runmode == 'module':
            res1 = importlib.import_module(file_or_module_name)
            res2 = getattr(res1, callable_name)
            self.wsgi_callable = res2()
        else:
            raise Exception(
                "wsgi module config: invalid runmode parameter value"
                )

        if not callable(self.wsgi_callable):
            raise Exception(
                "wsgi module config: value returned by "
                "`{}':`{}' - isn't callable".format(
                    file_or_module_name,
                    callable_name
                    )
                )

        self.wsgi_server = wayround_org.wsgi.server.WSGIServer(
            self.wsgi_callable
            )

        self.http_server = wayround_org.http.server.HTTPServer(
            self.wsgi_server.callable_for_http_server
            )

        return

    def start(self):
        return

    def stop(self):
        return

    def wait(self):
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

        self.http_server.callable_for_socket_server(
            transaction_id,
            serv,
            serv_stop_event,
            sock,
            addr,
            header_already_parsed=(request_line_parsed, header_fields),
            header_already_readen=(header_bytes, line_terminator)
            )

        return
