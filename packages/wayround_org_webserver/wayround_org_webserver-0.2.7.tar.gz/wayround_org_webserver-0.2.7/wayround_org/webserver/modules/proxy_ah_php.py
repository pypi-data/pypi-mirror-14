
import subprocess
import socket
import threading
import select
import logging
import io
import os
import time
import tempfile
import gc

import wayround_org.utils.path

import wayround_org.webserver.module_miscs


class WebServerAppModule:

    def __init__(
            self,
            ws_inst,
            socket_pool,
            domain_pool,
            config_params
            ):

        # print("proxy_apache_httpd_php module init")

        self.remote_address = config_params['address']
        self.remote_port = config_params['port']
        self.host_value = None
        if 'host_value' in config_params:
            self.host_value = config_params['host_value']

        self.httpd_command = config_params['httpd_command']
        self.document_root = config_params['document_root']

        self.access_log = config_params['access_log']
        self.error_log = config_params['error_log']

        os.makedirs(os.path.dirname(self.access_log), exist_ok=True)
        os.makedirs(os.path.dirname(self.error_log), exist_ok=True)

        # self.uwsgi_cwd = config_params['uwsgi_cwd']
        #self.uwsgi_user = config_params['uwsgi_user']
        #self.uwsgi_group = config_params['uwsgi_group']

        self._httpd_process = None

        self.gid = config_params.get('gid', 0)
        self.uid = config_params.get('uid', 0)

        self.host_mode = config_params.get('host_mode', 'pass')

        #self._one_thread_lock = threading.Lock()

        self.tmp_ini_dir = tempfile.TemporaryDirectory()
        self.tmp_ini_dir_file_name = wayround_org.utils.path.join(
            self.tmp_ini_dir.name,
            'httpd.conf'
            )

        self.pidfile = wayround_org.utils.path.join(
            self.tmp_ini_dir.name,
            'pidfile'
            )

        return

    def render_config(self):
        ret = r"""\

LoadModule authn_file_module modules/mod_authn_file.so
#LoadModule authn_dbm_module modules/mod_authn_dbm.so
#LoadModule authn_anon_module modules/mod_authn_anon.so
#LoadModule authn_dbd_module modules/mod_authn_dbd.so
#LoadModule authn_socache_module modules/mod_authn_socache.so
LoadModule authn_core_module modules/mod_authn_core.so
LoadModule authz_host_module modules/mod_authz_host.so
LoadModule authz_groupfile_module modules/mod_authz_groupfile.so
LoadModule authz_user_module modules/mod_authz_user.so
#LoadModule authz_dbm_module modules/mod_authz_dbm.so
#LoadModule authz_owner_module modules/mod_authz_owner.so
#LoadModule authz_dbd_module modules/mod_authz_dbd.so
LoadModule authz_core_module modules/mod_authz_core.so
LoadModule access_compat_module modules/mod_access_compat.so
LoadModule auth_basic_module modules/mod_auth_basic.so
#LoadModule auth_form_module modules/mod_auth_form.so
#LoadModule auth_digest_module modules/mod_auth_digest.so
#LoadModule allowmethods_module modules/mod_allowmethods.so
#LoadModule file_cache_module modules/mod_file_cache.so
#LoadModule cache_module modules/mod_cache.so
#LoadModule cache_disk_module modules/mod_cache_disk.so
#LoadModule cache_socache_module modules/mod_cache_socache.so
#LoadModule socache_shmcb_module modules/mod_socache_shmcb.so
#LoadModule socache_dbm_module modules/mod_socache_dbm.so
#LoadModule socache_memcache_module modules/mod_socache_memcache.so
#LoadModule watchdog_module modules/mod_watchdog.so
#LoadModule macro_module modules/mod_macro.so
#LoadModule dbd_module modules/mod_dbd.so
#LoadModule dumpio_module modules/mod_dumpio.so
#LoadModule echo_module modules/mod_echo.so
#LoadModule buffer_module modules/mod_buffer.so
#LoadModule data_module modules/mod_data.so
#LoadModule ratelimit_module modules/mod_ratelimit.so
LoadModule reqtimeout_module modules/mod_reqtimeout.so
#LoadModule ext_filter_module modules/mod_ext_filter.so
#LoadModule request_module modules/mod_request.so
#LoadModule include_module modules/mod_include.so
LoadModule filter_module modules/mod_filter.so
#LoadModule reflector_module modules/mod_reflector.so
#LoadModule substitute_module modules/mod_substitute.so
#LoadModule sed_module modules/mod_sed.so
#LoadModule charset_lite_module modules/mod_charset_lite.so
#LoadModule deflate_module modules/mod_deflate.so
#LoadModule xml2enc_module modules/mod_xml2enc.so
#LoadModule proxy_html_module modules/mod_proxy_html.so
LoadModule mime_module modules/mod_mime.so
LoadModule log_config_module modules/mod_log_config.so
#LoadModule log_debug_module modules/mod_log_debug.so
#LoadModule log_forensic_module modules/mod_log_forensic.so
#LoadModule logio_module modules/mod_logio.so
LoadModule env_module modules/mod_env.so
#LoadModule mime_magic_module modules/mod_mime_magic.so
#LoadModule expires_module modules/mod_expires.so
LoadModule headers_module modules/mod_headers.so
#LoadModule usertrack_module modules/mod_usertrack.so
#LoadModule unique_id_module modules/mod_unique_id.so
LoadModule setenvif_module modules/mod_setenvif.so
LoadModule version_module modules/mod_version.so
#LoadModule remoteip_module modules/mod_remoteip.so
LoadModule proxy_module modules/mod_proxy.so
LoadModule proxy_connect_module modules/mod_proxy_connect.so
LoadModule proxy_ftp_module modules/mod_proxy_ftp.so
LoadModule proxy_http_module modules/mod_proxy_http.so
LoadModule proxy_fcgi_module modules/mod_proxy_fcgi.so
LoadModule proxy_scgi_module modules/mod_proxy_scgi.so
#LoadModule proxy_fdpass_module modules/mod_proxy_fdpass.so
LoadModule proxy_wstunnel_module modules/mod_proxy_wstunnel.so
LoadModule proxy_ajp_module modules/mod_proxy_ajp.so
LoadModule proxy_balancer_module modules/mod_proxy_balancer.so
LoadModule proxy_express_module modules/mod_proxy_express.so
#LoadModule session_module modules/mod_session.so
#LoadModule session_cookie_module modules/mod_session_cookie.so
#LoadModule session_dbd_module modules/mod_session_dbd.so
LoadModule slotmem_shm_module modules/mod_slotmem_shm.so
#LoadModule slotmem_plain_module modules/mod_slotmem_plain.so
#LoadModule ssl_module modules/mod_ssl.so
#LoadModule dialup_module modules/mod_dialup.so
LoadModule lbmethod_byrequests_module modules/mod_lbmethod_byrequests.so
LoadModule lbmethod_bytraffic_module modules/mod_lbmethod_bytraffic.so
LoadModule lbmethod_bybusyness_module modules/mod_lbmethod_bybusyness.so
LoadModule lbmethod_heartbeat_module modules/mod_lbmethod_heartbeat.so
LoadModule unixd_module modules/mod_unixd.so
#LoadModule heartbeat_module modules/mod_heartbeat.so
#LoadModule heartmonitor_module modules/mod_heartmonitor.so
#LoadModule dav_module modules/mod_dav.so
LoadModule status_module modules/mod_status.so
LoadModule autoindex_module modules/mod_autoindex.so
#LoadModule asis_module modules/mod_asis.so
#LoadModule info_module modules/mod_info.so
<IfModule !mpm_prefork_module>
    #LoadModule cgid_module modules/mod_cgid.so
</IfModule>
<IfModule mpm_prefork_module>
    #LoadModule cgi_module modules/mod_cgi.so
</IfModule>
#LoadModule dav_fs_module modules/mod_dav_fs.so
#LoadModule dav_lock_module modules/mod_dav_lock.so
#LoadModule vhost_alias_module modules/mod_vhost_alias.so
#LoadModule negotiation_module modules/mod_negotiation.so
LoadModule dir_module modules/mod_dir.so
#LoadModule actions_module modules/mod_actions.so
#LoadModule speling_module modules/mod_speling.so
#LoadModule userdir_module modules/mod_userdir.so
LoadModule alias_module modules/mod_alias.so
#LoadModule rewrite_module modules/mod_rewrite.so

LoadModule php5_module modules/libphp5.so

ServerRoot "/multihost/x86_64-pc-linux-gnu"
Listen {address}:{port}

#<IfModule unixd_module>
#User daemon
#Group daemon
#</IfModule>

<Directory />
    AllowOverride none
    Require all denied
</Directory>

DocumentRoot "{document_root}"

<Directory "{document_root}">
    # Options Indexes FollowSymLinks

    AllowOverride None

    Require all granted
</Directory>

<IfModule dir_module>
    DirectoryIndex index.php
</IfModule>

<IfModule log_config_module>
    LogFormat "%h %l %u %t \"%r\" %>s %b \"%{{Referer}}i\" \"%{{User-Agent}}i\"" combined
    LogFormat "%h %l %u %t \"%r\" %>s %b" common

    <IfModule logio_module>
      # You need to enable mod_logio.c to use %I and %O
      LogFormat "%h %l %u %t \"%r\" %>s %b \"%{{Referer}}i\" \"%{{User-Agent}}i\" %I %O" combinedio
    </IfModule>

    CustomLog "{access_log}" common
</IfModule>

ErrorLog "{error_log}"

<IfModule mime_module>
    TypesConfig /etc/mime.types

    AddType application/x-compress .Z
    AddType application/x-gzip .gz .tgz
</IfModule>

<FilesMatch \.php$>
    SetHandler application/x-httpd-php
</FilesMatch>

<FilesMatch "\.ph(p[2-6]?|tml)$">
    SetHandler application/x-httpd-php
</FilesMatch>

PidFile "{pidfile}"

""".format(
            address=self.remote_address,
            port=self.remote_port,
            document_root=self.document_root,
            pidfile=self.pidfile,
            error_log=self.error_log,
            access_log=self.access_log
            )

        return ret

    def start(self):

        tmp_ini_dir_file = open(self.tmp_ini_dir_file_name, 'w')
        tmp_ini_dir_file.write(self.render_config())
        tmp_ini_dir_file.close()

        self.gid, self.uid = \
            wayround_org.webserver.module_miscs.reformat_gid_uid(
                self.gid,
                self.uid
                )

        p = subprocess.Popen(
            ['chown',
             '-R',
             '{}:{}'.format(self.gid, self.uid),
             self.tmp_ini_dir.name
             ]
            )

        p.wait()

        cmd = [self.httpd_command] + [
            '-f', self.tmp_ini_dir_file_name,
            '-k', 'start'
            ]
        self._httpd_process = subprocess.Popen(
            cmd,
            cwd=self.document_root,
            stdin=subprocess.PIPE,
            preexec_fn=wayround_org.webserver.module_miscs.demote_subprocess(
                self.gid,
                self.uid
                )
            )
        return

    def stop(self):
        if self._httpd_process is not None:
            cmd = [self.httpd_command] + [
                '-f', self.tmp_ini_dir_file_name,
                '-k', 'stop'
                ]
            httpd_process = subprocess.Popen(
                cmd,
                cwd=self.document_root,
                stdin=subprocess.PIPE
                )
            httpd_process.wait()
            # self._httpd_process.terminate()
            # self._httpd_process.wait()
        return

    def wait(self):
        if self._httpd_process is not None:
            self._httpd_process.wait()
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
                remote_socket.connect(
                    (self.remote_address, self.remote_port)
                    )
            except BlockingIOError:
                pass
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

        # gc.collect()

        return
