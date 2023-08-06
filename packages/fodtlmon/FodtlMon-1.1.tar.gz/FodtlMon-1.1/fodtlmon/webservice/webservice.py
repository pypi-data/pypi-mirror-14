"""
webservice
Copyright (C) 2016 Walid Benghabrit

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
__author__ = 'walid'
from http.server import SimpleHTTPRequestHandler
from http.server import HTTPServer
from urllib.parse import urlparse, parse_qs
from socketserver import ThreadingMixIn, ForkingMixIn
import threading
from fodtlmon.fotl.fotlmon import *


# Threading server
class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass


# Forking server
class ForkingSimpleServer(ForkingMixIn, HTTPServer):
    pass


class Webservice:
    """
    Web service class
    """
    monitors = {}
    server_port = 8000

    def __init__(self):
        pass

    @staticmethod
    def run(server_class=ThreadingSimpleServer):
        server_address = ('', Webservice.server_port)
        httpd = server_class(server_address, Webservice.HTTPRequestHandler)
        print("Server start on port " + str(Webservice.server_port))
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Stopping server...")
        httpd.server_close()

    @staticmethod
    def start(port=8000):
        Webservice.server_port = port
        threading.Thread(target=Webservice.run).start()

        # HTTPRequestHandler
    class HTTPRequestHandler(SimpleHTTPRequestHandler):

        @staticmethod
        def get_arg(args, name, method):
            try:
                if method == "GET":
                    return args[name]
                elif method == "POST":
                    return args[name][0]
                else:
                    return "Method error"
            except:
                return None

        def do_GET(self):
            # print("[GET] " + self.path)
            p = self.path
            k = urlparse(p).query
            args = parse_qs(k)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            path = p.replace(k, "")
            if path[-1] == "?":
                path = path[:-1]
            res = self.handle_req(path, args, "GET")
            self.wfile.write(res.encode("utf-8"))

        def do_POST(self):
            k = urlparse(self.path).query
            var_len = int(self.headers['Content-Length'])
            post_vars = self.rfile.read(var_len).decode('utf-8')
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            if len(post_vars) == 0:
                args = parse_qs(k)
            else:
                args = parse_qs(post_vars, encoding="utf8")

            res = self.handle_req(self.path, args, "POST")
            self.wfile.write(res.encode("utf-8"))

        def handle_req(self, path, args, method):
            # print(args)
            print(path)
            res = "Error"
            method_name = path.replace("/", "_")[1:]
            if hasattr(Webservice.API, method_name):
                res = getattr(Webservice.API, method_name)(args, method)
            return res

    class API:
        """
        Webservice API
        """
        @staticmethod
        def require_args(names, args, method):
            res = {}
            for arg in names:
                tmp = Webservice.HTTPRequestHandler.get_arg(args, arg, method)
                if tmp is None:
                    return "Missing %s" % arg
                else:
                    res[arg] = tmp[0]
            return res

        @staticmethod
        def api_monitor_all(args, method):
            """
                URL : /api/monitor/all
            """
            return str([str(x) for x in Webservice.monitors.keys()])

        @staticmethod
        def api_monitor_register(args, method):
            """
                URL : /api/monitor/register
            """
            args_names = ["mon_name", "formula", "trace"]
            _args = Webservice.API.require_args(args_names, args, method)
            if isinstance(_args, str): return _args
            tr = Trace().parse(_args.get("trace"))
            fl = FodtlParser.parse(_args.get("formula"))
            Webservice.monitors[_args.get("mon_name")] = Fotlmon(fl, tr)
            return "Registered"

        @staticmethod
        def api_monitor_events_push(args, method):
            """
                URL : /api/monitor/events/push
            """
            args_names = ["mon_name", "event"]
            _args = Webservice.API.require_args(args_names, args, method)
            if isinstance(_args, str): return _args
            mon = Webservice.monitors.get(_args.get("mon_name"))
            res = "Monitor not found !"
            if mon is not None:
                e = Event.parse(_args.get("event"))
                if e is not None:
                    mon.push_event(e)
                    res = "Pushed"
                else:
                    return "Bad event format !"
            return res

        @staticmethod
        def api_monitor_run(args, method):
            """
                URL : /api/monitor/run
            """
            args_names = ["mon_name"]
            _args = Webservice.API.require_args(args_names, args, method)
            if isinstance(_args, str): return _args
            mon = Webservice.monitors.get(_args.get("mon_name"))
            res = "Monitor not found !"
            if mon is not None:
                res = mon.monitor(struct_res=True)
                res["result"] = str(res.get("result"))
            return str(res)

        @staticmethod
        def api_monitor_remove(args, method):
            """
                URL : /api/monitor/remove
            """
            args_names = ["mon_name"]
            _args = Webservice.API.require_args(args_names, args, method)
            if isinstance(_args, str): return _args
            mon = Webservice.monitors.get(_args.get("mon_name"))
            res = "Monitor not found !"
            if mon is not None:
                del Webservice.monitors[_args.get("mon_name")]
                res = "Deleted"
            return res
