#!/usr/bin/env python
#
# Copyright 2015 Tiago Hillebrandt <tiagohillebrandt@ubuntu.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from bottle import ServerAdapter, route, run, server_names
from socket import gethostname

@route('/welcome/<name>', method='POST')
def welcome_message(name):
    """
    Prints the welcome message.
    """
    print("Welcome aboard, " + name)

class SSLWebServer(ServerAdapter):
    """
    CherryPy web server with SSL support.
    """

    def run(self, handler):
        """
        Runs a CherryPy Server using the SSL certificate.
        """
        from cherrypy import wsgiserver
        from cherrypy.wsgiserver.ssl_pyopenssl import pyOpenSSLAdapter

        server = wsgiserver.CherryPyWSGIServer((self.host, self.port), handler)

        server.ssl_adapter = pyOpenSSLAdapter(
            certificate="cert.crt",
            private_key="private.key",
            certificate_chain="intermediate_cert.crt"
        )

        try:
            server.start()
        except:
            server.stop()

server_names['sslwebserver'] = SSLWebServer

run(host=gethostname(), port=8080, server='sslwebserver')
