
import pwd
import grp
import threading
import os
import copy
import ssl
import time
import select

import wayround_org.utils.socket


def demote_subprocess(gid, uid):
    def _demote():
        if gid:
            os.setregid(gid, gid)
        if uid:
            os.setreuid(uid, uid)
        return
    return _demote


def reformat_gid_uid(gid, uid):

    if gid:

        if isinstance(gid, str):
            if gid.isnumeric():
                gid = int(gid)
            else:
                gid = grp.getgrnam(gid)[2]

    if uid:

        if isinstance(uid, str):
            if uid.isnumeric():
                uid = int(uid)
            else:
                uid = pwd.getpwnam(uid)[2]

    return gid, uid

# proxify_socket_threads_count = 0


def proxify_socket_threads(one, another, name, stop_event):

    # global proxify_socket_threads_count

    # proxify_socket_threads_count += 1

    th1 = threading.Thread(
        target=proxify_socket,
        args=(one, another, '{} ->'.format(name), stop_event)
        )

    th2 = threading.Thread(
        target=proxify_socket,
        args=(another, one, '{} <-'.format(name), stop_event)
        )

    th1.start()
    th2.start()

    th1.join()
    th2.join()

    # proxify_socket_threads_count -= 1

    # print("proxify_socket_threads_count: {}".format(proxify_socket_threads_count))

    return


def proxify_socket(one, another, name, stop_event):
    data = None
    while True:
        # print('proxify_socket 1')

        if stop_event.is_set():
            break

        data = wayround_org.utils.socket.nb_recv(one, 4096, stop_event)

        # print("proxify_socket recv (name: {}): {}".format(name, data))

        if stop_event.is_set():
            break

        if data is None:
            break

        if len(data) == 0:
            break

        wayround_org.utils.socket.nb_sendall(another, data, stop_event)

    stop_event.set()

    return


def host_value_hendeling_routine(
        header_fields,
        host_mode,
        con_address,
        con_port,
        custom_host_value
        ):

    header_fields = copy.deepcopy(header_fields)

    if host_mode == 'pass':
        pass

    elif host_mode == 'use_addr_port':

        header_fields = remove_host_fields(header_fields)

        header_fields.insert(
            0,
            (b'Host',
                bytes(
                    '{}:{}'.format(
                        con_address,
                        con_port
                        ),
                    'utf-8'
                    )
             )
            )

    elif host_mode == 'custom':

        header_fields = remove_host_fields(header_fields)

        header_fields.insert(0, (b'Host', bytes(custom_host_value, 'utf-8')))

    else:
        raise Exception("programming error")

    return header_fields


def remove_host_fields(header_fields):
    header_fields = copy.deepcopy(header_fields)

    for i in range(len(header_fields) - 1, -1, -1):
        if header_fields[i][0] == b'Host':
            del header_fields[i]

    return header_fields
