#!/usr/bin/env python
# Copyright (c) 2013 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""
Example web server providing single factor U2F enrollment and authentication.
It is intended to be run standalone in a single process, and stores user data
in memory only, with no permanent storage.

Enrollment will overwrite existing users.
If username is omitted, a default value of "user" will be used.

Any error will be returned as a stacktrace with a 400 response code.

Note that this is intended for test/demo purposes, not production use!

This example requires webob to be installed.
"""

from u2flib_server.jsapi import DeviceRegistration
from u2flib_server.u2f import (start_register, complete_register,
                               start_authenticate, verify_authenticate)
from webob.dec import wsgify
from webob import exc
import logging as log
import json
import traceback
import argparse


def get_origin(environ):
    if environ.get('HTTP_HOST'):
        host = environ['HTTP_HOST']
    else:
        host = environ['SERVER_NAME']
        if environ['wsgi.url_scheme'] == 'https':
            if environ['SERVER_PORT'] != '443':
                host += ':' + environ['SERVER_PORT']
        else:
            if environ['SERVER_PORT'] != '80':
                host += ':' + environ['SERVER_PORT']

    return '%s://%s' % (environ['wsgi.url_scheme'], host)


class U2FServer(object):

    """
    Very basic server providing a REST API to enroll one or more U2F device with
    a user, and to perform authentication with the enrolled devices.
    Only one challenge is valid at a time.

    Four calls are provided: enroll, bind, sign and verify. Each of these
    expects a username parameter, and bind and verify expect a
    second parameter, data, containing the JSON formatted data which is output
    by the U2F browser API upon calling the ENROLL or SIGN commands.
    """

    def __init__(self):
        self.users = {}

    @wsgify
    def __call__(self, request):
        self.facet = get_origin(request.environ)
        self.app_id = self.facet

        page = request.path_info_pop()

        if not page:
            return json.dumps([self.facet])

        try:
            username = request.params.get('username', 'user')
            data = request.params.get('data', None)

            if page == 'enroll':
                return self.enroll(username)
            elif page == 'bind':
                return self.bind(username, data)
            elif page == 'sign':
                return self.sign(username)
            elif page == 'verify':
                return self.verify(username, data)
            else:
                raise exc.HTTPNotFound()
        except Exception:
            log.exception("Exception in call to '%s'", page)
            return exc.HTTPBadRequest(comment=traceback.format_exc())

    def enroll(self, username):
        if username not in self.users:
            self.users[username] = {}

        user = self.users[username]
        devices = [DeviceRegistration.wrap(device)
                   for device in user.get('_u2f_devices_', [])]
        enroll = start_register(self.app_id, devices)
        user['_u2f_enroll_'] = enroll.json
        return enroll.json

    def bind(self, username, data):
        user = self.users[username]
        binding, cert = complete_register(user.pop('_u2f_enroll_'), data,
                                          [self.facet])
        devices = [DeviceRegistration.wrap(device)
                   for device in user.get('_u2f_devices_', [])]
        devices.append(binding)
        user['_u2f_devices_'] = [d.json for d in devices]

        log.info("U2F device enrolled. Username: %s", username)
        log.debug("Attestation certificate:\n%s", cert.as_text())

        return json.dumps(True)

    def sign(self, username):
        user = self.users[username]
        devices = [DeviceRegistration.wrap(device)
                   for device in user.get('_u2f_devices_', [])]
        challenge = start_authenticate(devices)
        user['_u2f_challenge_'] = challenge.json
        return challenge.json

    def verify(self, username, data):
        user = self.users[username]
        devices = [DeviceRegistration.wrap(device)
                   for device in user.get('_u2f_devices_', [])]

        challenge = user.pop('_u2f_challenge_')
        c, t = verify_authenticate(devices, challenge, data, [self.facet])
        return json.dumps({
            'touch': t,
            'counter': c
        })

application = U2FServer()

if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    parser = argparse.ArgumentParser(
        description='U2F test server',
        add_help=True,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('-i', '--interface', nargs='?', default='localhost',
                        help='network interface to bind to')
    parser.add_argument('-p', '--port', nargs='?', type=int, default=8081,
                        help='TCP port to bind to')

    args = parser.parse_args()

    log.basicConfig(level=log.DEBUG, format='%(asctime)s %(message)s',
                    datefmt='[%d/%b/%Y %H:%M:%S]')
    log.info("Starting server on http://%s:%d", args.interface, args.port)
    httpd = make_server(args.interface, args.port, application)
    httpd.serve_forever()
