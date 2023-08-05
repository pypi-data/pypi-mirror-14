
import importlib
import logging

"""

module structure description:
    wayround_org_webserver application module must have 2 strict things:
        1. class named 'WebServerModule', which has following
           parameters:
            1. reference to webserver instance;
            2. reference to socket pool
            3. reference to application pool
            4. dict with parameters passed from configuration file
        2. WebServerModule class instances must have callable methods:
            1. 'callable_for_webserver' which must have following parameters:
                # first part of parameters
                #     parameters passed by SocketServer
                transaction_id,
                serv,
                serv_stop_event,
                sock,
                addr,

                # second part of parameters
                #     WebServer socket and application instances
                ws_socket_inst,
                ws_application_inst,

                # third part of parameters
                #     header parsing result (as WebServer reads and parses
                #     header manually to retrive Host parameter)
                header_bytes,
                line_terminator,
                request_line_parsed,
                header_fields
            2. 'start' - called on application start() called
            3. 'stop' - called on application stop() called
            4. 'wait' - called on application wait() called
"""


class Application:
    """

    this class (or it's instances) is not intended for direct initialization.

    it's created, used and destroyed by ApplicationPool class instance
    """

    def __init__(
            self,
            application_data_dict,
            web_server_inst,
            application_pool_inst,
            socket_pool_inst
            ):
        self.name = application_data_dict['name']
        self.domain = application_data_dict['domain']
        self.module = application_data_dict['module']
        self.module_parameters = {}
        if 'module_parameters' in application_data_dict:
            self.module_parameters = application_data_dict['module_parameters']

        self.module_inst = None

        self._web_server_inst = web_server_inst
        self._application_pool_inst = application_pool_inst
        self._socket_pool_inst = socket_pool_inst

        self._load_module(web_server_inst)

        return

    def _load_module(self, web_server_inst):
        """
        result: True - Ok, False - Error
        """

        ret = True

        module = None

        module_name = 'wayround_org.webserver.modules.{}'.format(self.module)

        try:
            module = importlib.import_module(module_name)
        except:
            logging.exception(
                "Error loading module `{}'".format(module_name)
                )
            ret = False

        if ret:

            if not hasattr(module, 'WebServerAppModule'):
                logging.exception(
                    "module `{}' has no WebServerAppModule member".format(
                        module_name
                        )
                    )
                ret = False

        if ret:
            self.module_inst = module.WebServerAppModule(
                web_server_inst,
                self._socket_pool_inst,
                self._application_pool_inst,
                self.module_parameters
                )

        return ret

    def start(self):
        if self.module_inst:
            self.module_inst.start()
        return

    def stop(self):
        if self.module_inst:
            self.module_inst.stop()
        return

    def wait(self):
        if self.module_inst:
            self.module_inst.wait()
        return


class Pool:

    def __init__(self, cfg, web_server_inst, socket_pool_inst):
        self._application_pool = {}
        for i in cfg['applications']:
            d = Application(i, web_server_inst, self, socket_pool_inst)
            self._application_pool[d.name] = d
        return

    def start(self):
        for i in self._application_pool.values():
            i.start()
        return

    def stop(self):
        for i in self._application_pool.values():
            i.stop()
        return

    def wait(self):
        for i in self._application_pool.values():
            i.wait()
        return

    def get_by_name(self, name):
        return self._application_pool.get(name, None)

    def find_by_domain(self, domain):

        ret = []

        for i in list(self._application_pool.values()):
            if i.domain == domain:
                ret.append(i)

        return ret
