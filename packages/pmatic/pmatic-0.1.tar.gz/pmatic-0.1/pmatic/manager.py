#!/usr/bin/env python
# encoding: utf-8
#
# pmatic - A simple API to to the Homematic CCU2
# Copyright (C) 2016 Lars Michelsen <lm@larsmichelsen.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""Implements the main components of the pmatic manager"""

# Add Python 3.x behaviour to 2.7
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

try:
    from builtins import object # pylint:disable=redefined-builtin
except ImportError:
    pass

try:
    # Python 2.x
    import __builtin__ as builtins
except ImportError:
    # Python 3+
    import builtins

import os
import cgi
import sys
import time
import json
import socket
import signal
import inspect
import traceback
import threading
import contextlib
import subprocess
from wsgiref.handlers import SimpleHandler
import wsgiref.simple_server
from hashlib import sha256
from grp import getgrnam
from pwd import getpwnam

try:
    from Cookie import SimpleCookie
except ImportError:
    from http.cookies import SimpleCookie

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import pmatic
import pmatic.utils as utils
from pmatic.exceptions import PMUserError, SignalReceived

# Set while a script is executed with the "/run" page
g_runner = None

class Config(utils.LogMixin):
    config_path = "/etc/config/addons/pmatic/etc"
    script_path = "/etc/config/addons/pmatic/scripts"
    static_path = "/etc/config/addons/pmatic/manager_static"

    ccu_enabled     = True
    ccu_address     = None
    ccu_credentials = None

    log_level = None
    log_file  = "/var/log/pmatic-manager.log"

    event_history_length = 1000

    pushover_api_token = None
    pushover_user_token = None

    @classmethod
    def load(cls):
        try:
            try:
                config = json.load(open(cls._config_path()))
            except IOError as e:
                # a non existing file is allowed.
                if e.errno == 2:
                    config = {}
                else:
                    raise
        except Exception:
            cls.cls_logger().error("Failed to load the config. Terminating.", exc_info=True)
            sys.exit(1)

        for key, val in config.items():
            setattr(cls, key, val)


    @classmethod
    def save(cls):
        config = {}

        for key, val in cls.__dict__.items():
            if key[0] != "_" and key not in [ "config_path", "script_path",
                                              "static_path", "log_file" ] \
               and not inspect.isroutine(val):
                config[key] = val

        json_config = json.dumps(config)
        open(cls._config_path(), "w").write(json_config + "\n")


    @classmethod
    def _config_path(cls):
        return cls.config_path + "/manager.config"



# FIXME This handling is only for testing purposes and will be cleaned up soon
#if not utils.is_ccu():
#    Config.script_path = "/tmp/pmatic-scripts"
#    Config.static_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) \
#                         + "/manager_static"
#    Config.config_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) \
#                         + "/etc"
#    Config.ccu_address = "http://192.168.1.26"
#    Config.ccu_credentials = ("Admin", "EPIC-SECRET-PW")



class Html(object):
    html_escape_table = {
        "&": "&amp;",
        '"': "&quot;",
        "'": "&apos;",
        ">": "&gt;",
        "<": "&lt;",
    }

    def __init__(self):
        super(Html, self).__init__()
        self._form_vars = []


    def page_header(self):
        self.write('<!DOCTYPE HTML>\n'
                   '<html><head>\n')
        self.write("<meta http-equiv=\"Content-Type\" "
                   "content=\"text/html; charset=utf-8\">\n")
        self.write("<meta http-equiv=\"X-UA-Compatible\" "
                   "content=\"IE=edge\">\n")
        self.write("<link rel=\"stylesheet\" href=\"css/font-awesome.min.css\">\n")
        self.write("<link rel=\"stylesheet\" href=\"css/pmatic.css\">\n")
        self.write("<link rel=\"shortcut icon\" href=\"favicon.ico\" type=\"image/ico\">\n")
        self.write('<title>%s</title>\n' % self.escape(self.title()))
        self.write('</head>\n')
        self.write("<body>\n")


    def page_footer(self):
        self.write("</body>")
        self.write("</html>")


    def navigation(self):
        self.write("<ul id=\"navigation\">\n")
        self.write("<li><a href=\"/\"><i class=\"fa fa-code\"></i>Scripts</a></li>\n")
        self.write("<li><a href=\"/run\"><i class=\"fa fa-flash\"></i>Execute Scripts</a></li>\n")
        self.write("<li><a href=\"/schedule\"><i class=\"fa fa-tasks\"></i>Schedule</a></li>\n")
        self.write("<li><a href=\"/event_log\"><i class=\"fa fa-list\"></i>Event Log</a></li>\n")
        self.write("<li><a href=\"/config\"><i class=\"fa fa-gear\"></i>Configuration</a></li>\n")
        self.write("<li class=\"right\"><a href=\"https://larsmichelsen.github.io/pmatic/\" "
                   "target=\"_blank\">pmatic %s</a></li>\n" % self.escape(pmatic.__version__))
        self.write("<li class=\"right\"><a href=\"/state\"><i class=\"fa fa-heart\"></i>"
                   "State</a></li>\n")
        self.write("</ul>\n")


    def is_action(self):
        return bool(self._vars.getvalue("action"))


    def begin_form(self, multipart=None):
        self._form_vars = []
        enctype = " enctype=\"multipart/form-data\"" if multipart else ""
        target_url = self.url or "/"
        self.write("<form method=\"post\" action=\"%s\" %s>\n" %
                            (self.escape(target_url), enctype))


    def end_form(self):
        self.write("</form>\n")


    def add_missing_vars(self):
        """Adds the vars which have been used to call this page but are yet missing in the
        current form as hidden vars to the form."""
        for key in self._vars.keys():
            if key not in self._form_vars:
                self.hidden(key, self._vars[key].value)


    def file_upload(self, name, accept="text/*"):
        self._form_vars.append(name)
        self.write("<input name=\"%s\" type=\"file\" accept=\"%s\">" %
                        (self.escape(name), self.escape(accept)))


    def hidden(self, name, value):
        self._form_vars.append(name)
        self.write("<input type=\"hidden\" name=\"%s\" value=\"%s\">\n" %
            (self.escape(name), self.escape(value)))


    def password(self, name):
        self._form_vars.append(name)
        self.write("<input type=\"password\" name=\"%s\">\n" % self.escape(name))


    def submit(self, label, value="1", name="action"):
        self._form_vars.append(name)
        self.write("<button type=\"submit\" name=\"%s\" "
                   "value=\"%s\">%s</button>\n" %
                    (self.escape(name), self.escape(value), self.escape(label)))


    def input(self, name, deflt=None, cls=None):
        self._form_vars.append(name)
        value = deflt if deflt is not None else ""
        css = (" class=\"%s\"" % self.escape(cls)) if cls else ""
        self.write("<input type=\"text\" name=\"%s\" value=\"%s\"%s>\n" %
                                    (self.escape(name), self.escape(value), css))


    def checkbox(self, name, deflt=False):
        self._form_vars.append(name)
        checked = " checked" if deflt else ""
        self.write("<input type=\"checkbox\" name=\"%s\"%s>\n" %
                                        (self.escape(name), self.escape(checked)))


    def is_checked(self, name):
        return self._vars.getvalue(name) is not None


    def select(self, name, choices, deflt=None, onchange=None):
        self._form_vars.append(name)
        onchange = " onchange=\"%s\"" % self.escape(onchange) if onchange else ""
        self.write("<select name=\"%s\"%s>\n" % (self.escape(name), onchange))
        self.write("<option value=\"\"></option>\n")
        for choice in choices:
            if deflt == choice[0]:
                selected = " selected"
            else:
                selected = ""
            self.write("<option value=\"%s\"%s>%s</option>\n" %
                    (self.escape(choice[0]), selected, self.escape(choice[1])))
        self.write("</select>\n")


    def icon(self, icon_name, title, cls=None):
        css = " " + cls if cls else ""
        self.write("<i class=\"fa fa-%s%s\" title=\"%s\"></i>" %
                 (self.escape(icon_name), self.escape(css), self.escape(title)))


    def icon_button(self, icon_name, url, title):
        self.write("<a class=\"icon_button\" href=\"%s\">" % self.escape(url))
        self.icon(icon_name, title)
        self.write("</a>")


    def button(self, icon_name, label, url):
        self.write("<a class=\"button\" href=\"%s\">" % self.escape(url))
        if icon_name is not None:
            self.icon(icon_name, "")
        self.write(self.escape(label))
        self.write("</a>\n")


    def error(self, text):
        self.message(text, "error", "bomb")


    def success(self, text):
        self.message(text, "success", "check-circle-o")


    def info(self, text):
        self.message(text, "info", "info-circle")


    def message(self, text, cls, icon):
        self.write("<div class=\"message %s\"><i class=\"fa fa-2x fa-%s\"></i> "
                   "%s</div>\n" % (self.escape(cls), self.escape(icon), text))


    def confirm(self, text):
        confirm = self._vars.getvalue("_confirm")

        if not confirm:
            self.begin_form()
            self.message(text, "confirm", "question-circle")
            self.submit("Yes", "yes", name="_confirm")
            self.button(None, "No", "javascript:window.history.back()")
            self.add_missing_vars()
            self.end_form()
            return False
        elif confirm == "yes":
            return True


    def h2(self, title):
        self.write("<h2>%s</h2>\n" % self.escape(title))


    def h3(self, title):
        self.write("<h3>%s</h3>\n" % self.escape(title))


    # FIXME: Escaping - Needs to be escaped here or at all callers
    def p(self, content):
        self.write("<p>%s</p>\n" % content)


    def js_file(self, url):
        self.write("<script type=\"text/javascript\" src=\"%s\"></script>\n" %
                                                        self.escape(url))


    def js(self, script):
        self.write("<script type=\"text/javascript\">%s</script>\n" %
                                                        self.escape(script))


    def redirect(self, delay, url):
        self.js("setTimeout(\"location.href = '%s';\", %d);" % (url, delay*1000))


    def escape(self, text):
        """Escape text for embedding into HTML code."""
        if not utils.is_string(text):
            text = "%s" % text
        return "".join(self.html_escape_table.get(c, c) for c in text)


    def write_text(self, text):
        self.write(self.escape(text))


class FieldStorage(cgi.FieldStorage):
    def getvalue(self, key, default=None):
        value = cgi.FieldStorage.getvalue(self, key.encode("utf-8"), default)
        if value is not None:
            return value.decode("utf-8")
        else:
            return None



class PageHandler(object):
    @classmethod
    def pages(cls):
        pages = {}
        for subclass in cls.__subclasses__():
            if hasattr(subclass, "url"):
                pages[subclass.url] = subclass
        return pages


    @classmethod
    def base_url(self, environ):
        parts = environ['PATH_INFO'][1:].split("/")
        return parts[0]


    @classmethod
    def get(cls, environ):
        pages = cls.pages()
        try:
            page = pages[cls.base_url(environ)]

            if cls.is_password_set() and not cls._is_authenticated(environ):
                return pages["login"]
            else:
                return page
        except KeyError:
            static_file_class = StaticFile.get(environ['PATH_INFO'])
            if not static_file_class:
                return pages["404"]
            else:
                return static_file_class


    @classmethod
    def is_password_set(self):
        return os.path.exists(os.path.join(Config.config_path, "manager.secret"))


    @classmethod
    def _get_auth_cookie_value(self, environ):
        for name, cookie in SimpleCookie(environ.get("HTTP_COOKIE")).items():
            if name == "pmatic_auth":
                return cookie.value


    @classmethod
    def _is_authenticated(self, environ):
        value = self._get_auth_cookie_value(environ)
        if not value or value.count(":") != 1:
            return False

        salt, salted_hash = value.split(":", 1)

        filepath = os.path.join(Config.config_path, "manager.secret")
        secret = open(filepath).read().strip()

        correct_hash = sha256(secret + salt).hexdigest().decode("utf-8")

        return salted_hash == correct_hash


    def __init__(self, manager, environ, start_response):
        super(PageHandler, self).__init__()
        self._manager = manager
        self._env = environ
        self._start_response = start_response

        self._http_headers = [
            (b'Content-type', self._get_content_type().encode("utf-8")),
        ]
        self._page = []

        self._read_environment()


    def _get_content_type(self):
        return b'text/html; charset=UTF-8'


    def _read_environment(self):
        self._read_vars()


    def _set_cookie(self, name, value):
        cookie = SimpleCookie()
        cookie[name.encode("utf-8")] = value.encode("utf-8")
        self._http_headers.append((b"Set-Cookie", cookie[name.encode("utf-8")].OutputString()))


    @property
    def vars(self):
        return self._vars


    def _read_vars(self):
        wsgi_input = self._env["wsgi.input"]
        if not wsgi_input:
            self._vars = cgi.FieldStorage()
            return

        self._vars = FieldStorage(fp=wsgi_input, environ=self._env,
                                  keep_blank_values=1)


    def _send_http_header(self):
        self._start_response(self._http_status(200), self._http_headers)


    def process_page(self):
        self._send_http_header()

        self.page_header()
        self.navigation()
        self.write("<div id=\"content\">\n")

        action_result = None
        if self.is_action():
            try:
                action_result = self.action()
            except PMUserError as e:
                self.error(e)
            except Exception as e:
                self.error("Unhandled exception: %s" % e)
                self.logger.debug("Unhandled exception (action)", exc_info=True)

        # The action code can disable regular rendering of the page,
        # e.g. to only show a confirmation dialog.
        if action_result != False:
            try:
                self.process()
            except PMUserError as e:
                self.error(e)
            except Exception as e:
                self.error("Unhandled exception: %s" % e)
                self.logger.debug("Unhandled exception (process)", exc_info=True)

        self.write("\n</div>")
        self.page_footer()

        return self._page


    def ensure_password_is_set(self):
        if not self.is_password_set():
            raise PMUserError("To be able to access this page you first have to "
                            "<a href=\"/config\">set a password</a> and authenticate "
                            "afterwards.")


    def title(self):
        return "No title specified"


    def action(self):
        self.write_text("Not implemented yet.")


    def process(self):
        self.write_text("Not implemented yet.")


    def write(self, code):
        if utils.is_text(code):
            code = code.encode("utf-8")
        self._page.append(code)


    def _http_status(self, code):
        if code == 200:
            return b'200 OK'
        elif code == 301:
            return b'301 Moved Permanently'
        elif code == 302:
            return b'302 Found'
        elif code == 304:
            return b'304 Not Modified'
        elif code == 404:
            return b'404 Not Found'
        elif code == 500:
            return b'500 Internal Server Error'
        else:
            return str(code)



class StaticFile(PageHandler):
    @classmethod
    def get(self, path_info):
        if ".." in path_info:
            return # don't allow .. in paths to prevent opening of unintended files

        if path_info.startswith("/css/") or path_info.startswith("/fonts/") \
           or path_info.startswith("/scripts/") or path_info.startswith("/js/"):
            file_path = StaticFile.system_path_from_pathinfo(path_info)
            if os.path.exists(file_path):
                return StaticFile


    @classmethod
    def system_path_from_pathinfo(self, path_info):
        if path_info.startswith("/scripts/"):
            return os.path.join(Config.script_path, path_info[9:])
        else:
            return os.path.join(Config.static_path, path_info.lstrip("/"))


    def _get_content_type(self):
        ext = self._env["PATH_INFO"].split(".")[-1]
        if ext == "css":
            return "text/css; charset=UTF-8"
        if ext == "js":
            return "application/x-javascript; charset=UTF-8"
        elif ext == "otf":
            return "application/vnd.ms-opentype"
        elif ext == "eot":
            return "application/vnd.ms-fontobject"
        elif ext == "ttf":
            return "application/x-font-ttf"
        elif ext == "woff":
            return "application/octet-stream"
        elif ext == "woff2":
            return "application/octet-stream"
        else:
            return "text/plain; charset=UTF-8"


    def _check_cached(self, file_path):
        client_cached_age = self._env.get('HTTP_IF_MODIFIED_SINCE', None)
        if not client_cached_age:
            return False

        # Try to parse the If-Modified-Since HTTP header provided by
        # the client to make client cache usage possible.
        try:
            t = time.strptime(client_cached_age, "%a, %d %b %Y %H:%M:%S %Z")
            if t == time.gmtime(os.stat(file_path).st_mtime):
                return True
        except ValueError:
            # strptime raises ValueError when wrong time format is being provided
            return False


    def process_page(self):
        path_info = self._env["PATH_INFO"]
        file_path = StaticFile.system_path_from_pathinfo(self._env["PATH_INFO"])

        is_cached = self._check_cached(file_path)
        if is_cached:
            self._start_response(self._http_status(304), [])
            return []

        mtime = os.stat(file_path).st_mtime
        self._http_headers.append((b"Last-Modified",
                    time.strftime("%a, %d %b %Y %H:%M:%S UTC", time.gmtime(mtime))))

        if path_info.startswith("/scripts"):
            self._http_headers.append((b"Content-Disposition",
                b"attachment; filename=\"%s\"" % os.path.basename(path_info)))

        self._start_response(self._http_status(200), self._http_headers)
        return [ l for l in open(file_path) ]



class AbstractScriptPage(object):
    def _get_scripts(self):
        if not os.path.exists(Config.script_path):
            raise PMUserError("The script directory %s does not exist." %
                                                    Config.script_path)

        for dirpath, _unused_dirnames, filenames in os.walk(Config.script_path):
            if dirpath == Config.script_path:
                relpath = ""
            else:
                relpath = dirpath[len(Config.script_path)+1:]

            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                if os.path.isfile(filepath) and filename[0] != ".":
                    if relpath:
                        yield os.path.join(relpath, filename)
                    else:
                        yield filename



class AbstractScriptProgressPage(Html):
    def __init__(self):
        super(AbstractScriptProgressPage, self).__init__()
        self._runner = None


    def _abort_url(self):
        raise NotImplementedError()


    def _handle_abort(self):
        if not self._is_running():
            raise PMUserError("There is no script running to abort.")

        self._runner.abort()
        self.success("The script has been aborted.")


    def _progress(self):
        self.h2(self.title())
        if not self._is_started():
            self.p("There is no script running.")
            return

        runner = self._runner

        self.write("<table>")
        self.write("<tr><th>Script</th>"
                   "<td>%s</td></tr>" % self.escape(self._runner.script))
        self.write("<tr><th>Started at</th>"
                   "<td>%s</td></tr>" % time.strftime("%Y-%m-%d %H:%M:%S",
                                                      time.localtime(runner.started)))

        self.write("<tr><th>Finished at</th>"
                   "<td>")
        if not self._is_running() and runner.finished is not None:
            self.write_text(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(runner.finished)))
        else:
            self.write_text("-")
        self.write("</td></tr>")

        self.write("<tr><th>Current state</th>"
                   "<td>")
        if self._is_running():
            self.icon("spinner", "The script is running...", cls="fa-pulse")
            self.write_text(" Running... ")
            if runner.abortable:
                self.icon_button("close", self._abort_url(), "Stop this script.")
        elif runner.exit_code is not None:
            if runner.exit_code == 0:
                self.icon("check", "Successfully finished")
            else:
                self.icon("times", "An error occured")
            self.write(" Finished (Exit code: <tt>%d</tt>)" % runner.exit_code)
        else:
            self.icon("times", "Not running")
            self.write_text(" Started but not running - something went wrong.")
        self.write("</td></tr>")

        self.write("<tr><th class=\"toplabel\">Output</th>")
        self.write("<td>")
        output = self.escape(self._output()) or "<i>(no output)</i>"
        self.write("<pre id=\"output\">%s</pre>" % output)
        self.write("</td></tr>")
        self.write("</table>")

        if self._is_running():
            self.js_file("js/update_output.js")


    def _set_runner(self, runner):
        self._runner = runner


    def _is_started(self):
        return self._runner is not None


    def _is_running(self):
        return self._runner and self._runner.is_alive()


    def _exit_code(self):
        return self._runner.exit_code


    def _output(self):
        return "".join(self._runner.output.getvalue())



class PageMain(PageHandler, Html, AbstractScriptPage, utils.LogMixin):
    url = ""

    def title(self):
        return "Manage pmatic Scripts"


    def save_script(self, filename, script):
        if not os.path.exists(Config.script_path):
            os.makedirs(Config.script_path)

        filepath = os.path.join(Config.script_path, filename)
        open(filepath, "w").write(script)
        os.chmod(filepath, 0o755)


    def action(self):
        self.ensure_password_is_set()
        action = self._vars.getvalue("action")
        if action == "upload":
            self._handle_upload()
        elif action == "delete":
            return self._handle_delete()


    def _handle_upload(self):
        if not self._vars.getvalue("script"):
            raise PMUserError("You need to select a script to upload.")

        filename = self._vars["script"].filename
        script = self._vars["script"].file.read()
        first_line = script.split(b"\n", 1)[0]

        if not first_line.startswith(b"#!/usr/bin/python") \
           and not first_line.startswith(b"#!/usr/bin/env python"):
            raise PMUserError("The uploaded file does not seem to be a pmatic script.")

        if len(script) > 1048576:
            raise PMUserError("The uploaded file is too large.")

        self.save_script(filename, script)
        self.success("The script has been uploaded.")


    def _handle_delete(self):
        filename = self._vars.getvalue("script")

        if not self.confirm("Do you really want to delete the script %s?" % filename):
            return False

        if not filename:
            raise PMUserError("You need to provide a script name to delete.")

        if filename not in self._get_scripts():
            raise PMUserError("This script does not exist.")

        filepath = os.path.join(Config.script_path, filename)
        os.unlink(filepath)
        self.success("The script has been deleted.")


    def process(self):
        self.ensure_password_is_set()
        self.upload_form()
        self.scripts()


    def upload_form(self):
        self.h2("Upload Script")
        self.p("You can either upload your scripts using this form or "
               "copy the files on your own, e.g. using SFTP or SCP, directly "
               "to <tt>%s</tt>." % self.escape(Config.script_path))
        self.p("Please note that existing scripts with equal names will be overwritten "
               "without warning.")
        self.write("<div class=\"upload_form\">\n")
        self.begin_form(multipart=True)
        self.file_upload("script")
        self.submit("Upload script", "upload")
        self.end_form()
        self.write("</div>\n")


    def scripts(self):
        self.h2("Scripts")
        self.write("<div class=\"scripts\">\n")
        self.write("<table><tr>\n")
        self.write("<th>Actions</th>"
                   "<th class=\"largest\">Filename</th>"
                   "<th>Last modified</th></tr>\n")
        for filename in self._get_scripts():
            path = os.path.join(Config.script_path, filename)
            last_mod_ts = os.stat(path).st_mtime

            self.write("<tr>")
            self.write("<td>")
            self.icon_button("trash", "?action=delete&script=%s" % filename,
                              "Delete this script")
            self.icon_button("bolt", "/run?script=%s&action=run" % filename,
                              "Execute this script now")
            self.icon_button("download", "/scripts/%s" % filename,
                              "Download this script")
            self.write("</td>")
            self.write("<td>%s</td>" % self.escape(filename))
            self.write("<td>%s</td>" % time.strftime("%Y-%m-%d %H:%M:%S",
                                                     time.localtime(last_mod_ts)))
            self.write("</tr>")
        self.write("</table>\n")
        self.write("</div>\n")



class PageRun(PageHandler, AbstractScriptProgressPage, AbstractScriptPage, utils.LogMixin):
    url = "run"

    def title(self):
        return "Execute pmatic Scripts"


    def _abort_url(self):
        return "/run?action=abort"


    def action(self):
        self.ensure_password_is_set()
        action = self._vars.getvalue("action")
        if action == "run":
            self._handle_run()
        elif action == "abort":
            self._set_runner(g_runner)
            self._handle_abort()


    def _handle_run(self):
        script = self._vars.getvalue("script")
        if not script:
            raise PMUserError("You have to select a script.")

        if script not in self._get_scripts():
            raise PMUserError("You have to select a valid script.")

        if self._is_running():
            raise PMUserError("There is another script running. Wait for it to complete "
                            "or stop it to be able to execute another script.")

        self._execute_script(script)
        self.success("The script has been started.")


    def process(self):
        self.ensure_password_is_set()
        self._start_form()

        self._set_runner(g_runner)
        self._progress()


    def _start_form(self):
        self.h2("Execute Scripts")
        self.p("This page is primarily meant for testing purposes. You can choose "
               "which script you like to execute and then start it. The whole output of "
               "the script is captured and shown in the progress area below. You "
               "can execute only one script at the time. Please note: You are totally "
               "free to execute your scripts on the command line or however you like.")
        self.write("<div class=\"execute_form\">\n")
        self.begin_form()
        self.write_text("Select the script: ")
        self.select("script", sorted([ (s, s) for s in self._get_scripts() ]))
        self.submit("Run script", "run")
        self.end_form()
        self.write("</div>\n")


    def _execute_script(self, script):
        global g_runner
        g_runner = ScriptRunner(self._manager, script)
        g_runner.start()



class PageAjaxUpdateOutput(PageHandler, Html, utils.LogMixin):
    url = "ajax_update_output"

    def _get_content_type(self):
        return b"text/plain; charset=UTF-8"

    def process_page(self):
        output = []

        self._start_response(self._http_status(200), self._http_headers)
        if not g_runner:
            return output

        # Tell js code to continue reloading or not
        if not g_runner.is_alive():
            self.write_text("0")
        else:
            self.write_text("1")

        self.write_text("".join(g_runner.output))

        return self._page



class PageLogin(PageHandler, Html, utils.LogMixin):
    url = "login"

    def title(self):
        return "Log in to pmatic Manager"


    def action(self):
        password = self._vars.getvalue("password")

        if not password:
            raise PMUserError("Invalid password.")

        filepath = os.path.join(Config.config_path, "manager.secret")
        secret = open(filepath).read().strip()

        if secret != sha256(password).hexdigest():
            raise PMUserError("Invalid password.")

        self._login(secret)
        self.success("You have been authenticated. You can now <a href=\"/\">proceed</a>.")
        self.redirect(2, "/")


    def _login(self, secret):
        salt = "%d" % int(time.time())
        salted_hash = sha256(secret + salt).hexdigest()
        cookie_value = salt + ":" + salted_hash
        self._set_cookie("pmatic_auth", cookie_value)


    def process(self):
        self.h2("Login")
        self.p("Welcome to the pmatic Manager. Please provide your manager "
               "password to log in.")
        self.write("<div class=\"login\">\n")
        self.begin_form()
        self.password("password")
        self.submit("Log in", "login")
        self.end_form()
        self.write("</div>\n")



class PageConfiguration(PageHandler, Html, utils.LogMixin):
    url = "config"

    def title(self):
        return "Configuration of pmatic Manager"


    def action(self):
        action = self._vars.getvalue("action")
        if action == "set_password":
            self._handle_set_password()
        elif action == "save_config":
            self._handle_save_config()


    def _handle_set_password(self):
        password = self._vars.getvalue("password")

        if not password:
            raise PMUserError("You need to provide a password and it must not be empty.")

        if len(password) < 6:
            raise PMUserError("The password must have a minimal length of 6 characters.")

        filepath = os.path.join(Config.config_path, "manager.secret")
        open(filepath, "w").write(sha256(password).hexdigest()+"\n")
        self.success("The password has been set. You will be redirect to the "
                     "<a href=\"/\">login</a>.")
        self.redirect(2, "/")


    # FIXME: Validations!
    def _handle_save_config(self):
        log_level_name = self._vars.getvalue("log_level")
        if not log_level_name:
            Config.log_level = None
        else:
            Config.log_level = log_level_name

        self._save_ccu_config()
        self._save_pushover_config()

        event_history_length = self._vars.getvalue("event_history_length")
        try:
            event_history_length = int(event_history_length)
            if event_history_length < 1:
                raise PMUserError("The minimum event history length is 1.")
            Config.event_history_length = event_history_length

        except ValueError:
            raise PMUserError("Invalid event history length given.")

        Config.save()
        self.success("The configuration has been updated.")


    def _save_ccu_config(self):
        ccu_config_changed = False

        ccu_enabled = self.is_checked("ccu_enabled")
        if ccu_enabled != Config.ccu_enabled:
            ccu_config_changed = True
        Config.ccu_enabled = ccu_enabled

        ccu_address = self._vars.getvalue("ccu_address")
        if not ccu_address:
            ccu_address = None

        if ccu_address != Config.ccu_address:
            ccu_config_changed = True
        Config.ccu_address = ccu_address

        ccu_username = self._vars.getvalue("ccu_username").strip()
        ccu_password = self._vars.getvalue("ccu_password")
        if not ccu_username or not ccu_password:
            if Config.ccu_enabled and not utils.is_ccu():
                raise PMUserError("You need to configure the CCU credentials to be able to "
                                  "communicate with your CCU.")
            ccu_credentials = None
        else:
            ccu_credentials = ccu_username, ccu_password

        if ccu_credentials != Config.ccu_credentials:
            ccu_config_changed = True
        Config.ccu_credentials = ccu_credentials

        if ccu_config_changed:
            self.logger.info("Reinitializing CCU connection (config changed)")
            self._manager.init_ccu()


    def _save_pushover_config(self):
        pushover_api_token = self._vars.getvalue("pushover_api_token")
        if not pushover_api_token:
            Config.pushover_api_token = None
        else:
            Config.pushover_api_token = pushover_api_token

        pushover_user_token = self._vars.getvalue("pushover_user_token")
        if not pushover_user_token:
            Config.pushover_user_token = None
        else:
            Config.pushover_user_token = pushover_user_token


    def process(self):
        self.password_form()
        self.config_form()


    def password_form(self):
        self.h2("Set Manager Password")
        self.p("To make the pmatic manager fully functional, you need to "
               "configure a password for accessing the manager first. Only after "
               "setting a password functions like uploading files are enabled.")
        self.write("<div class=\"password_form\">\n")
        self.begin_form()
        self.write("<table>")
        self.write("<tr><th>Password</th>")
        self.write("<td>")
        self.password("password")
        self.write("</td></tr>")
        self.write("</table>")
        self.submit("Set password", "set_password")
        self.end_form()
        self.write("</div>\n")


    def config_form(self):
        self.h2("Configuration")
        self.write("<div class=\"config_form\">\n")
        self.begin_form()
        self.write("<table>")

        self.write("<tr><th>Log Level"
                   "<p>Log entries having the configured log level (or a worse one) are logged to"
                   " the file <tt>%s</tt> by default.</p>"
                   "</th>" % Config.log_file)
        self.write("<td>")
        self.select("log_level", [ (l, l) for l in pmatic.log_level_names ], Config.log_level)
        self.write("</td>")
        self.write("</tr>")

        self.write("<tr><th>Event Log Entries"
                   "<p>Number of event log entries to keep. Once you the pmatic manager received "
                   "more events from the CCU, the older ones will be dropped.</p>"
                   "</th>")
        self.write("<td>")
        self.input("event_history_length", str(Config.event_history_length))
        self.write("</td>")
        self.write("</tr>")

        self.write("</table>")

        self.h3("Connect to remote CCU")
        self.p("You can start the pmatic Manager on another device than the CCU. In this case you "
               "have to configure the address and credentials to log into the CCU. If you start "
               "the pmatic Manager on your CCU, you can leave these options empty.")

        self.write("<table>")
        self.write("<tr><th>Connect with CCU</th>")
        self.write("<td>")
        self.checkbox("ccu_enabled", Config.ccu_enabled)
        self.write("</td>")
        self.write("</tr>")
        self.write("<tr><th>Address</th>")
        self.write("<td>")
        self.input("ccu_address", Config.ccu_address)
        self.write("</td>")
        self.write("</tr>")
        self.write("<tr><th>Username</th>")
        self.write("<td>")
        self.input("ccu_username", Config.ccu_credentials[0]
                                    if Config.ccu_credentials else "")
        self.write("</td>")
        self.write("</tr>")
        self.write("<tr><th>Password</th>")
        self.write("<td>")
        self.password("ccu_password")
        self.write("</td>")
        self.write("</tr>")
        self.write("</table>")

        self.h3("Pushover Notifications")
        self.p("If you like to use pushover notifications, you need to configure your "
               "credentials here in order to make them work.")
        self.write("<table>")
        self.write("<tr><th>API Token</th>")
        self.write("<td>")
        self.input("pushover_api_token", Config.pushover_api_token)
        self.write("</td>")
        self.write("</tr>")
        self.write("<tr><th>User/Group Token</th>")
        self.write("<td>")
        self.input("pushover_user_token", Config.pushover_user_token)
        self.write("</td>")
        self.write("</tr>")
        self.write("</table>")
        self.submit("Save configuration", "save_config")
        self.end_form()
        self.write("</div>\n")



class PageEventLog(PageHandler, Html, utils.LogMixin):
    url = "event_log"

    def title(self):
        return "Events received from the CCU"


    def process(self):
        self.h2("Events received from the CCU")
        self.p("This page shows the last %d events received from the CCU. These are events "
               "which you can register your pmatic scripts on to be called once such an event "
               "is received." % Config.event_history_length)

        if not Config.ccu_enabled:
            self.info("The connection with the CCU is disabled. In this mode the manager "
                      "can not receive any event from the CCU. To be able to receive "
                      "events, you need to configure the CCU address, credentials and "
                      "enable the CCU connection.")
            return

        if not self._manager.event_manager.initialized:
            self.info("The event processing has not been initialized yet. Please come back "
                      "in one or two minutes.")
            return

        self.p("Received <i>%d</i> events in total since the pmatic manager has been started." %
                                                    self._manager.event_history.num_events_total)

        self.write("<table>")
        self.write("<tr><th>Time</th><th>Device</th><th>Channel</th><th>Parameter</th>"
                   "<th>Event-Type</th><th>Value</th>")
        self.write("</tr>")
        for event in reversed(self._manager.event_history.events):
            #"time"           : updated_param.last_updated,
            #"time_changed"   : updated_param.last_changed,
            #"param"          : updated_param,
            #"value"          : updated_param.value,
            #"formated_value" : "%s" % updated_param,
            param = event["param"]

            if event["time"] == event["time_changed"]:
                ty = "changed"
            else:
                ty = "updated"

            self.write("<tr>")
            self.write("<td>%s</td>" % time.strftime("%Y-%m-%d %H:%M:%S",
                                                     time.localtime(event["time"])))
            self.write("<td>%s (%s)</td>" % (self.escape(param.channel.device.name),
                                             self.escape(param.channel.device.address)))
            self.write("<td>%s</td>" % self.escape(param.channel.name))
            self.write("<td>%s</td>" % self.escape(param.name))
            self.write("<td>%s</td>" % self.escape(ty))
            self.write("<td>%s (Raw value: %s)</td>" %
                 (self.escape(event["formated_value"]), self.escape(event["value"])))
            self.write("</tr>")
        self.write("</table>")



class PageSchedule(PageHandler, Html, utils.LogMixin):
    url = "schedule"

    def title(self):
        return "Schedule your pmatic Scripts"


    def action(self):
        self.ensure_password_is_set()
        action = self._vars.getvalue("action")
        if action == "delete":
            return self._handle_delete()
        elif action == "start":
            return self._handle_start()


    def _handle_delete(self):
        schedule_id = self._vars.getvalue("schedule_id")
        if not schedule_id:
            raise PMUserError("You need to provide a schedule to delete.")
        schedule_id = int(schedule_id)

        if not self._manager.scheduler.exists(schedule_id):
            raise PMUserError("This schedule does not exist.")

        if not self.confirm("Do you really want to delete this schedule?"):
            return False

        self._manager.scheduler.remove(schedule_id)
        self._manager.scheduler.save()
        self.success("The schedule has been deleted.")


    def _handle_start(self):
        schedule_id = self._vars.getvalue("schedule_id")
        if not schedule_id:
            raise PMUserError("You need to provide a schedule to start.")
        schedule_id = int(schedule_id)

        if not self._manager.scheduler.exists(schedule_id):
            raise PMUserError("This schedule does not exist.")

        schedule = self._manager.scheduler.get(schedule_id)
        schedule.execute()

        self.success("The schedule has been started.")


    def process(self):
        self.h2("Schedule your pmatic Scripts")
        self.p("This page shows you all currently existing script schedules. A schedule controls "
               "in which situations a script is being executed.")

        self.button("tasks", "Add schedule", "/add_schedule")
        self.write("<br>")
        self.write("<br>")

        self.write("<table>")
        self.write("<tr><th>Actions</th><th>Name</th><th>On/Off</th><th>Conditions</th>"
                   "<th>Script</th><th>Last triggered</th><th>Currently running</th>")
        self.write("</tr>")
        for schedule in self._manager.scheduler.schedules:
            self.write("<tr>")
            self.write("<td>")
            self.icon_button("edit", "/edit_schedule?schedule_id=%d" % schedule.id,
                              "Edit this schedule")
            self.icon_button("trash", "?action=delete&schedule_id=%d" % schedule.id,
                              "Delete this schedule")

            if schedule.last_triggered:
                self.icon_button("file-text-o",
                        "/schedule_result?schedule_id=%d" % schedule.id,
                        "Show the last schedule run result")

            if not schedule.is_running:
                self.icon_button("bolt", "?action=start&schedule_id=%d" % schedule.id,
                                 "Manually trigger this schedule now")

            self.write("</td>")
            self.write("<td>%s</td>" % self.escape(schedule.name))

            self.write("<td>")
            if schedule.disabled:
                self.icon("close", "The schedule is currently disabled.")
            else:
                self.icon("check", "The schedule is currently enabled.")
            self.write("</td>")

            self.write("<td>")
            for condition in schedule.conditions:
                self.write(condition.display()+"<br>")
            self.write("</td>")
            self.write("<td>%s</td>" % self.escape(schedule.script))
            last_triggered = schedule.last_triggered
            if last_triggered:
                last_triggered = time.strftime("%Y-%m-%d %H:%M:%S",
                                               time.localtime(last_triggered))
            else:
                last_triggered = "<i>Not triggered yet.</i>"
            self.write("<td>%s</td>" % last_triggered)
            self.write("<td>%s</td>" % ("running" if schedule.is_running else "not running"))
            self.write("</tr>")
        self.write("</table>")



class PageEditSchedule(PageHandler, AbstractScriptPage, Html, utils.LogMixin):
    url = "edit_schedule"

    def _get_mode(self):
        return "edit"


    def _get_schedule(self):
        schedule_id = self._vars.getvalue("schedule_id")
        if schedule_id is None:
            raise PMUserError("You need to provide a <tt>schedule_id</tt>.")
        schedule_id = int(schedule_id)

        if not self._manager.scheduler.exists(schedule_id):
            raise PMUserError("The schedule you are trying to edit does not exist.")

        return self._manager.scheduler.get(schedule_id)


    def _get_condition_types(self):
        types = []
        for subclass in Condition.types():
            types.append((subclass.type_name, subclass.type_title))
        return types


    def _set_submitted_vars(self, schedule, submit):
        if self._vars.getvalue("submitted") == "1":
            # submitted for reload or saving!

            schedule.name = self._vars.getvalue("name")
            if submit and not schedule.name:
                raise PMUserError("You have to provide a name.")

            schedule.keep_running = self.is_checked("keep_running")
            schedule.run_inline   = self.is_checked("run_inline")
            schedule.disabled     = self.is_checked("disabled")

            script = self._vars.getvalue("script")
            if script and script not in self._get_scripts():
                raise PMUserError("The given script does not exist.")
            if submit and not script:
                raise PMUserError("You have to select a script.")
            schedule.script = script

            num_conditions = int(self._vars.getvalue("num_conditions"))
            schedule.clear_conditions()
            has_error = False
            for condition_id in range(num_conditions):
                condition_type = self._vars.getvalue("cond_%d_type" % condition_id)
                if condition_type:
                    cls = Condition.get(condition_type)
                    if not cls:
                        raise PMUserError("Invalid condition type \"%s\" given." % condition_type)

                    condition = cls(self._manager)
                    try:
                        condition.set_submitted_vars(self, "cond_%d_" % condition_id)
                    except PMUserError as e:
                        if submit:
                            self.error(e)
                        has_error = True

                    schedule.add_condition(condition)

            if submit and has_error:
                raise PMUserError("An error occured, please correct this.")


    def action(self):
        schedule = self._get_schedule()
        self._set_submitted_vars(schedule, submit=True)
        schedule.save()
        self.success("The schedule has been saved. Opening the schedule list now.")
        self.redirect(2, "/schedule")


    def title(self):
        return "Edit Script Schedule"


    def process(self):
        self.h2(self.title())

        mode = self._get_mode()
        schedule = self._get_schedule()
        self._set_submitted_vars(schedule, submit=False)

        self.begin_form()
        if mode == "edit":
            self.hidden("schedule_id", str(schedule.id))
        self.hidden("submitted", "1")
        self.write("<table>")
        self.write("<tr><th>Name</th><td>")
        self.input("name", schedule.name)
        self.write("</td></tr>")

        self.write("<tr><th>Keep running"
                   "<p>Keep the script running and restart it automatically after it has been "
                   "started once. <i>Note:</i> If the script is respawning too often, it's "
                   "restarts will be delayed.</p></th><td>")
        self.checkbox("keep_running", schedule.keep_running)
        self.write("</td></tr>")

        self.write("<tr><th>Disabled"
                   "<p>You can use this option to disable future executions of this "
                   "schedule till you re-enable it.</p></th><td>")
        self.checkbox("disabled", schedule.disabled)
        self.write("</td></tr>")

        self.write("<tr><th>Run inline"
                   "<p>Execute the script inline the manager process with access to the managers "
                   "CCU object. Use this if your scripts need access to CCU provided information "
                   "like devices, channels or values. If you uncheck this, your script will be "
                   "started as separate process.<br>You can use your regular, unmodified pmatic "
                   "scripts with this. If you create a CCU() object in your code, it will not "
                   "create a new object but use the pmatic managers object which is already "
                   "initialized then.</p></th><td>")
        self.checkbox("run_inline", schedule.run_inline)
        self.write("</td></tr>")

        self.write("<tr><th>Script to execute</th><td>")
        self.select("script", sorted([ (s, s) for s in self._get_scripts() ]), schedule.script)
        self.write("</td></tr>")
        self.write("</table>")

        self.h3("Conditions")
        self.p("Here you need to specify at least one condition for the script to be started. "
               "If you create multiple conditions, each of the conditions issues the script on "
               "it's own.")
        self.write("<table>")
        self.write("<tr>")
        self.write("<th>Type</th>")
        self.write("<th>Parameters</th>")
        self.write("</tr>")

        self.hidden("num_conditions", str(len(schedule.conditions)+1))
        for condition_id, condition in enumerate(schedule.conditions + [Condition(self._manager)]):
            varprefix = "cond_%d_" % condition_id
            self.write("<tr>")
            self.write("<td>")
            self.write("Execute script ")
            self.select(varprefix+"type", self._get_condition_types(),
                        deflt=condition.type_name,
                        onchange="this.form.submit()")
            self.write("</td>")

            self.write("<td>")
            condition.input_parameters(self, varprefix)
            self.write("</td>")
            self.write("</tr>")

        self.write("</table>")
        self.submit("Save", "save")
        self.end_form()



class PageAddSchedule(PageEditSchedule, PageHandler):
    url = "add_schedule"

    def _get_mode(self):
        return "new"


    def _get_schedule(self):
        return Schedule(self._manager)


    def title(self):
        return "Add Script Schedule"



class PageScheduleResult(PageHandler, AbstractScriptProgressPage, utils.LogMixin):
    url = "schedule_result"

    def title(self):
        return "Scheduled Script Result"


    def _get_schedule(self):
        schedule_id = self._vars.getvalue("schedule_id")
        if schedule_id is None:
            raise PMUserError("You need to provide a <tt>schedule_id</tt>.")
        schedule_id = int(schedule_id)

        if not self._manager.scheduler.exists(schedule_id):
            raise PMUserError("The schedule you are trying to edit does not exist.")

        return self._manager.scheduler.get(schedule_id)


    def _abort_url(self):
        schedule_id = int(self._vars.getvalue("schedule_id"))
        return "/schedule_result?schedule_id=%d&action=abort" % schedule_id


    def action(self):
        self.ensure_password_is_set()
        action = self._vars.getvalue("action")
        if action == "abort":
            schedule = self._get_schedule()
            self._set_runner(schedule.runner)

            self._handle_abort()


    def process(self):
        self.ensure_password_is_set()

        schedule = self._get_schedule()
        self._set_runner(schedule.runner)

        self._progress()



class PageState(PageHandler, Html, utils.LogMixin):
    url = "state"

    def title(self):
        return "pmatic Manager State"

    def process(self):
        self.h2(self.title())

        self.p("This page shows you some details about the overall state of the pmatic Manager.")

        self.h3("General")

        self.write("<table class=\"info\">")
        vmsize, vmrss = self._current_memory_usage()
        self.write("<tr><th>Memory Usage (Virtual)</th>")
        self.write("<td>%0.2f MB</td></tr>" % (vmsize/1024.0/1024.0))
        self.write("<tr><th>Memory Usage (Resident)</th>")
        self.write("<td>%0.2f MB</td></tr>" % (vmrss/1024.0/1024.0))
        self.write("</table>")

        self.h3("CCU Connection")

        self.write("<table class=\"info\">")
        self.write("<tr><th>Current State</th>")
        if not Config.ccu_enabled:
            cls  = "state1"
            text = "Disabled (by command line or configuration)"
        elif self._manager.ccu.api.initialized:
            cls  = "state0"
            text = "Initialized"
        else:
            cls  = "state2"
            text = "Not initialized (%s)" % (self._manager.ccu.api.fail_reason or "No error")
        self.write("<td class=\"%s\">%s" % (cls, text))
        self.write("</td></tr>")

        devices = self._manager.ccu.devices
        self.write("<tr><th>Number of Devices</th>")
        self.write("<td>%s</td></tr>" % len(devices))

        num_channels = sum([ len(device.channels) for device in devices ])
        self.write("<tr><th>Number of Channels</th>")
        self.write("<td>%s</td></tr>" % num_channels)

        self.write("</table>")

        self.h3("CCU Event Processing")

        self.write("<table class=\"info\">")
        self.write("<tr><th>Current State</th>")
        if not Config.ccu_enabled:
            cls  = "state0"
            text = "Disabled (because CCU connection is disabled)"
        elif self._manager.event_manager.initialized:
            cls  = "state0"
            text = "Initialized"
        else:
            cls  = "state2"
            text = "Not initialized (%s)" % (self._manager.event_manager.fail_reason or "No error")
        self.write("<td class=\"%s\">%s" % (cls, text))
        self.write("</td></tr>")

        self.write("<tr><th>Number of Events</th>")
        self.write("<td>%s</td></tr>" % self._manager.event_history.num_events_total)

        self.write("<tr><th>Time of Last Event</th>")
        self.write("<td>%s</td></tr>" % time.strftime("%Y-%m-%d %H:%M:%S",
                               time.localtime(self._manager.event_history.last_event_time)))

        self.write("</table>")

        # FIXME: Care about too larget logfiles
        #self.h2("pmatic Manager Logfile")
        #self.write("<pre id=\"logfile\">")
        #for line in open(Config.log_file):
        #    self.write_text(line.decode("utf-8"))
        #self.write("</pre>")
        #self.js("document.getElementById(\"logfile\").scrollTop = "
        #        "document.getElementById(\"logfile\").scrollHeight;")

    def _current_memory_usage(self):
        """Returns the current vm and resizent usage in bytes"""
        vmsize, vmrss = 0, 0
        for line in open('/proc/self/status'):
            if line.startswith("VmSize:"):
                vmsize = int(line.split()[1])*1024
            elif line.startswith("VmRSS"):
                vmrss = int(line.split()[1])*1024

        return vmsize, vmrss



class Page404(PageHandler, Html, utils.LogMixin):
    url = "404"


    def _send_http_header(self):
        self._start_response(self._http_status(404), self._http_headers)


    def title(self):
        return "404 - Page not Found"


    def process(self):
        self.p("The requested page could not be found.")



@contextlib.contextmanager
def catch_stdout_and_stderr(out=None):
    old_out, old_err = sys.stdout, sys.stderr

    if out is None:
        out = StringIO()

    sys.stdout = out
    sys.stderr = out

    yield out

    sys.stdout, sys.stderr = old_out, old_err



class ScriptRunner(threading.Thread, utils.LogMixin):
    def __init__(self, manager, script, run_inline=False, keep_running=False):
        threading.Thread.__init__(self)
        self.daemon = True

        self._manager     = manager

        self.script       = script
        self.run_inline   = run_inline

        self.keep_running = keep_running
        self.restarted    = None

        self.output     = StringIO()
        self.exit_code  = None
        self.started    = time.time()
        self.finished   = None

        self._p = None


    def run(self):
        while True:
            try:
                self.logger.info("Starting script (%s): %s",
                        "inline" if self.run_inline else "external", self.script)
                script_path = os.path.join(Config.script_path, self.script)

                if self.run_inline:
                    exit_code = self._run_inline(script_path)
                else:
                    exit_code = self._run_external(script_path)

                self.exit_code = exit_code
                self.finished  = time.time()

                self.logger.info("Finished (Exit-Code: %d).", self.exit_code)
            except Exception:
                self.logger.error("Failed to execute %s", self.script, exc_info=True)
                self.logger.debug(traceback.format_exc())

            # Either execute the script once or handle the keep_running option.
            # when the script is restarting too fast, delay it for some time.
            if not self.keep_running:
                break

            elif self.restarted != None and time.time() - self.restarted < 5:
                delay = 30 - (time.time() - self.restarted)
                self.logger.info("Last restart is less than 5 seconds ago, delaying restart for "
                                 "%d seconds (\"Keep running\" is enabled)." % delay)
                time.sleep(delay)
                self.restarted = time.time()

            else:
                self.logger.info("Restarting the script (\"Keep running\" is enabled)")
                self.restarted = time.time()


    def _run_external(self, script_path):
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"

        self._p = subprocess.Popen(["/usr/bin/env", "python", "-u", script_path], shell=False,
                                   cwd="/", env=env, stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)

        while True:
            nextline = self._p.stdout.readline().decode("utf-8")
            if nextline == "" and self._p.poll() is not None:
                break
            self.output.write(nextline)
        exit_code = self._p.poll()

        return exit_code


    def _run_inline(self, script_path):
        exit_code = 0
        try:
            # Make the ccu object available globally so that the __new__ method
            # of the CCU class can use and return this instead of creating a new
            # CCU object within the pmatic scripts.
            builtins.manager_ccu = self._manager.ccu

            # Catch stdout and stderr of the executed python script and write
            # it to the same StringIO() object.
            with catch_stdout_and_stderr(self.output):
                script_globals = {}
                # would use execfile() but it's not available in Python 3.x
                exec(compile(open(script_path, "rb").read(),
                             script_path, 'exec'), script_globals)
        except SystemExit as e:
            exit_code = e.code
        except Exception as e:
            self.logger.debug("Exception in inline script %s", script_path, exc_info=True)
            self.output.write("%s" % e)
            exit_code = 1

        return exit_code


    @property
    def abortable(self):
        return not self.run_inline


    def abort(self):
        if self.abortable:
            self._abort_external()


    # FIXME: Set self.exit_code, self.output and self.finished()?
    def _abort_external(self):
        if not self._p:
            return

        self._p.terminate()
        # And wait for the termination (at least shortly)
        timer = 10
        while timer > 0 and self._p.poll() is None:
            timer -= 1
            time.sleep(0.1)



class PMServerHandler(wsgiref.simple_server.ServerHandler, utils.LogMixin):
    server_software = 'pmatic-manager'

    # Hook into ServerHandler to be able to catch exceptions about disconnected clients
    def _server_handler_write(self, data):
        try:
            SimpleHandler.write(self, data)
        except socket.error as e:
            # Client disconnected while answering it's request.
            if e.errno != 32:
                raise


    def log_exception(self, exc_info):
        self.logger.error("Unhandled exception", exc_info=True)



# Found no elegant way to patch it. Sorry.
wsgiref.simple_server._ServerHandler = wsgiref.simple_server.ServerHandler
wsgiref.simple_server.ServerHandler = PMServerHandler


class Manager(wsgiref.simple_server.WSGIServer, utils.LogMixin):
    def __init__(self, address):
        wsgiref.simple_server.WSGIServer.__init__(
            self, address, RequestHandler)
        self.set_app(self._request_handler)

        self.ccu           = None
        self.event_manager = EventManager(self)

        self.event_history = EventHistory()
        self.scheduler = Scheduler(self)
        self.scheduler.start()


    # FIXME: When running the manager from remote:
    # - Handle pmatic.exceptions.PMConnectionError correctly
    #   The connection should be retried later and all depending
    #   code needs to be able to deal with an unconnected manager.
    # - Handle pmatic.exceptions.PMException:
    #       [session_login] JSONRPCError: too many sessions (501)
    def init_ccu(self):
        """This method initializes the manager global CCU object. It is called during startup
        of the manager, but also when the CCU related configuration changed to apply the changes.
        """
        if self.ccu:
            self.ccu.close()
            self.ccu = None

        if Config.ccu_enabled:
            self.logger.info("Initializing connection with CCU...")
            self.ccu = pmatic.CCU(address=Config.ccu_address,
                                  credentials=Config.ccu_credentials)
        else:
            self.logger.info("Connection with CCU is disabled")

        self._register_for_ccu_events()


    def _register_for_ccu_events(self):
        if self.event_manager.is_alive():
            self.event_manager.stop()
        self.event_manager = None

        if not Config.ccu_enabled:
            return

        self.event_manager = EventManager(self)
        self.logger.info("Registering for CCU events...")
        self.event_manager.start()


    def _request_handler(self, environ, start_response):
        # handler_class may be any subclass of PageHandler
        handler_class = PageHandler.get(environ)
        page = handler_class(self, environ, start_response)
        return page.process_page()


    def process_request(self, request, client_address):
        try:
            super(Manager, self).process_request(request, client_address)
        except socket.error as e:
            if e.errno == 32:
                self.logger.debug("%s: Client disconnected while answering it's request.",
                                                client_address, exc_info=True)
            else:
                raise


    def daemonize(self, user=0, group=0):
        # do the UNIX double-fork magic, see Stevens' "Advanced
        # Programming in the UNIX Environment" for details (ISBN 0201563177)
        try:
            pid = os.fork()
            if pid > 0:
                # exit first parent
                sys.exit(0)
        except OSError as e:
            sys.stderr.write("Fork failed (#1): %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        # decouple from parent environment
        # chdir -> don't prevent unmounting...
        os.chdir("/")

        # Create new process group with the process as leader
        os.setsid()

        # Set user/group depending on params
        if group:
            os.setregid(getgrnam(group)[2], getgrnam(group)[2])
        if user:
            os.setreuid(getpwnam(user)[2], getpwnam(user)[2])

        # do second fork
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError as e:
            sys.stderr.write("Fork failed (#2): %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        sys.stdout.flush()
        sys.stderr.flush()

        si = os.open("/dev/null", os.O_RDONLY)
        so = os.open("/dev/null", os.O_WRONLY)
        os.dup2(si, 0)
        os.dup2(so, 1)
        os.dup2(so, 2)
        os.close(si)
        os.close(so)

        self.logger.debug("Daemonized with PID %d.", os.getpid())


    def register_signal_handlers(self):
        signal.signal(signal.SIGINT,  self.signal_handler)
        signal.signal(signal.SIGQUIT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)


    def signal_handler(self, signum, _unused_stack_frame):
        raise SignalReceived(signum)



class RequestHandler(wsgiref.simple_server.WSGIRequestHandler, utils.LogMixin):
    def log_message(self, fmt, *args):
        self.logger.debug("%s %s", self.client_address[0], fmt%args)



class EventManager(threading.Thread, utils.LogMixin):
    """Manages the CCU event handling for the the Manager()."""
    def __init__(self, manager):
        threading.Thread.__init__(self)
        self._manager         = manager
        self.daemon           = True
        self._initialized     = False
        self._fail_exc        = None
        self._terminate       = False


    def run(self):
        while not self._terminate:
            if not self.initialized:
                self._fail_exc = None
                try:
                    self._do_register_for_ccu_events()
                except Exception as e:
                    self._fail_exc = e
                    self.logger.error("Error in EventManager (%s). Restarting in 10 seconds.", e)
                    self.logger.debug("Exception:", exc_info=True)
                    time.sleep(10)
            else:
                # FIXME: Replace this polling by some trigger mechanism
                time.sleep(1)


    def _do_register_for_ccu_events(self):
        self._manager.ccu.events.init()
        self.logger.debug("events initialized")
        self._manager.ccu.events.on_value_updated(self._on_value_updated)
        self.logger.info("Event processing initialized.")
        self._initialized = True


    def _on_value_updated(self, updated_param):
        self._manager.event_history.add_event({
            "time"           : updated_param.last_updated,
            "time_changed"   : updated_param.last_changed,
            "param"          : updated_param,
            "value"          : updated_param.value,
            "formated_value" : "%s" % updated_param,
        })


    @property
    def initialized(self):
        return self._initialized


    @property
    def fail_reason(self):
        return self._fail_exc


    def stop(self):
        self._terminate = True
        self.join()



class EventHistory(object):
    def __init__(self):
        self._events = []
        self._num_events_total = 0
        self._last_event_time = None


    def add_event(self, event_dict):
        self._last_event_time = time.time()
        self._num_events_total += 1
        self._events.append(event_dict)
        if len(self._events) > Config.event_history_length:
            self._events.pop(0)


    @property
    def events(self):
        return self._events


    @property
    def num_events_total(self):
        return self._num_events_total


    @property
    def last_event_time(self):
        return self._last_event_time



class Scheduler(threading.Thread, utils.LogMixin):
    def __init__(self, manager):
        threading.Thread.__init__(self)
        self.daemon = True

        self._manager = manager
        self._schedules = []

        self._on_startup_executed = False
        self._on_ccu_init_executed = False

        self.load()


    def run(self):
        self.logger.debug("Starting Scheduler")
        while True:
            try:
                if not self._on_startup_executed:
                    # Run on startup scripts
                    for schedule in self._schedules_with_condition_type(ConditionOnStartup):
                        self.execute(schedule)
                    self._on_startup_executed = True

                if not self._on_ccu_init_executed and self._manager.event_manager.initialized:
                    # Run on ccu init scripts
                    for schedule in self._schedules_with_condition_type(ConditionOnCCUInitialized):
                        self.execute(schedule)
                    self._on_ccu_init_executed = True

                self._execute_timed_schedules()
            except Exception:
                self.logger.error("Exception in Scheduler", exc_info=True)

            # FIXME: Optimization: Don't wake up every second. Sleep till next scheduled event.
            time.sleep(1)

        self.logger.debug("Stopped Scheduler")


    def _execute_timed_schedules(self):
        """Checks all configured timed schedules whether or not the next occurance has been
        reached. Then, if reached, the schedule is executed and the next occurance is calculated.
        """
        for schedule in self.enabled_schedules:
            for condition in schedule.conditions:
                if isinstance(condition, ConditionOnTime):
                    if condition.next_time <= time.time():
                        this_time = condition.next_time
                        condition.calculate_next_time()
                        self.logger.debug("Timed condition matched: %d. Next will be: %d.",
                                                            this_time, condition.next_time)
                        self.execute(schedule)
                    #else:
                    #    self.logger.debug("Timed condition is not due yet (%d <= %d)",
                    #                                    condition.next_time, time.time())


    def _schedules_with_condition_type(self, cls):
        for schedule in self.enabled_schedules:
            matched = False
            for condition in schedule.conditions:
                if isinstance(condition, cls):
                    matched = True
                    break

            if matched:
                yield schedule


    def execute(self, schedule):
        """Executes a script schedule. This is normally issued by the Scheduler itself when it
        detected that a condition of a schedule matched.

        Each of the executed scripts are started in a separate ScriptRunner object which is
        managing the executed script, collecting it's output and restarts the script when it
        it is configured to be kept running and terminates.

        The script runner is connected with the *schedule* object so that the Scheduler knows
        that the schedule is currently being executed and should not be started a second time
        in parallel.
        """
        self.logger.info("[%s] Executing script..." % schedule.name)
        if schedule.is_running:
            self.logger.info("[%s] Conditions matched, but script was already running.",
                                                                            schedule.name)
            return

        schedule.execute()


    @property
    def enabled_schedules(self):
        """Return all non disabled schedules."""
        for schedule in self._schedules:
            if not schedule.disabled:
                yield schedule


    @property
    def schedules(self):
        return self._schedules


    def exists(self, schedule_id):
        return schedule_id < len(self._schedules)


    def get(self, schedule_id):
        return self._schedules[schedule_id]


    def add(self, schedule):
        if schedule.id is None:
            num = len(self._schedules)
            schedule.id = num
            self._schedules.append(schedule)
        else:
            self._schedules[schedule.id] = schedule


    def remove(self, schedule_id):
        """Removes the schedule with the given *schedule_id* from the Scheduler. Tolerates non
        existing schedule ids.

        When a schedule is currently running, it is being terminated (if possible)."""
        try:
            schedule = self._schedules.pop(schedule_id)

            if schedule.is_running:
                schedule.runner.abort()
        except IndexError:
            pass


    def load(self):
        try:
            try:
                fh = open(Config.config_path + "/manager.schedules")
                schedule_config = json.load(fh)
            except IOError as e:
                # a non existing file is allowed.
                if e.errno == 2:
                    schedule_config = []
                else:
                    raise

            for schedule_cfg in schedule_config:
                schedule = Schedule(self._manager)
                schedule.from_config(schedule_cfg)
                self.add(schedule)

        except Exception:
            self.logger.error("Failed to load schedules. Terminating.", exc_info=True)
            sys.exit(1)


    def save(self):
        schedule_config = []
        for schedule in self._schedules:
            schedule_config.append(schedule.to_config())

        json_config = json.dumps(schedule_config)
        open(Config.config_path + "/manager.schedules", "w").write(json_config + "\n")



class Schedule(object):
    def __init__(self, manager):
        self._manager     = manager

        self.id           = None
        self.name         = ""
        self.disabled     = False
        self.keep_running = False
        self.run_inline   = True
        self.script       = ""
        self.conditions   = []

        self.last_triggered = None
        self._runner        = None


    @property
    def is_running(self):
        return self._runner and self._runner.is_alive()


    def execute(self):
        self.last_triggered = time.time()
        # FIXME: Recycle old runner?
        self._runner = ScriptRunner(self._manager, self.script,
                                    self.run_inline, self.keep_running)
        self._runner.start()


    @property
    def runner(self):
        return self._runner


    def add_condition(self, condition):
        num = len(self.conditions)
        condition.id = num
        self.conditions.append(condition)


    def clear_conditions(self):
        self.conditions = []


    def from_config(self, cfg):
        for key, val in cfg.items():
            if key != "conditions":
                setattr(self, key, val)
            else:
                for condition_cfg in val:
                    cls = Condition.get(condition_cfg["type_name"])
                    if not cls:
                        raise PMUserError("Failed to load condition type: %s" %
                                                        condition_cfg["type_name"])
                    condition = cls(self._manager)
                    condition.from_config(condition_cfg)
                    self.add_condition(condition)


    def to_config(self):
        return {
            "name"         : self.name,
            "disabled"     : self.disabled,
            "keep_running" : self.keep_running,
            "run_inline"   : self.run_inline,
            "script"       : self.script,
            "conditions"   : [ c.to_config() for c in self.conditions ],
        }


    def save(self):
        self._manager.scheduler.add(self)
        self._manager.scheduler.save()



class Condition(object):
    type_name = ""
    type_title = ""

    @classmethod
    def types(cls):
        return cls.__subclasses__()

    @classmethod
    def get(cls, type_name):
        for subclass in cls.__subclasses__():
            if subclass.type_name == type_name:
                return subclass
        return None


    def __init__(self, manager):
        self._manager = manager


    def from_config(self, cfg):
        for key, val in cfg.items():
            setattr(self, key, val)


    def to_config(self):
        return {
            "type_name": self.type_name,
        }


    def display(self):
        return self.type_title


    def input_parameters(self, page, varprefix):
        pass


    def set_submitted_vars(self, page, varprefix):
        pass



class ConditionOnStartup(Condition):
    type_name = "on_startup"
    type_title = "on manager startup"

    def input_parameters(self, page, varprefix):
        page.write("<i>This condition has no parameters.</i>")



class ConditionOnCCUInitialized(Condition):
    type_name = "on_ccu_initialized"
    type_title = "on connection with CCU initialized"

    def input_parameters(self, page, varprefix):
        page.write("<i>This condition has no parameters.</i>")



class ConditionOnDeviceEvent(Condition):
    type_name = "on_device_event"
    type_title = "on device event"

    _event_types = [
        ("updated", "Value updated"),
        ("changed", "Value changed"),
    ]

    def __init__(self, manager):
        super(ConditionOnDeviceEvent, self).__init__(manager)
        self.device     = None
        self.channel    = None
        self.param      = None
        self.event_type = None


    def from_config(self, cfg):
        self.device = self._manager.ccu.devices.query(
                                device_address=cfg["device_address"]).get(cfg["device_address"])
        if not self.device:
            return

        try:
            self.channel = self.device.channel_by_address(cfg["channel_address"])
        except KeyError:
            return

        self.param = self.channel.values.get(cfg["param_id"])
        if not self.param:
            return

        self.event_type = cfg["event_type"]


    def to_config(self):
        cfg = super(ConditionOnDeviceEvent, self).to_config()
        cfg.update({
            "device_address"  : self.device.address,
            "channel_address" : self.channel.address,
            "param_id"        : self.param.id,
            "event_type"      : self.event_type,
        })
        return cfg


    def display(self):
        txt = super(ConditionOnDeviceEvent, self).display()
        txt += ": %s, %s, %s, %s" % (self.device.name, self.channel.name,
                                     self.param.name, dict(self._event_types)[self.event_type])
        return txt


    def _device_choices(self):
        for device in self._manager.ccu.devices:
            yield device.address, "%s (%s)" % (device.name, device.address)


    def _channel_choices(self):
        if not self.device:
            return

        for channel in self.device.channels:
            yield channel.address, "%s (%s)" % (channel.name, channel.address)


    def _param_choices(self):
        if not self.channel:
            return

        for param_id, param in self.channel.values.items():
            yield param_id, "%s (%s)" % (param.name, param_id)


    def input_parameters(self, page, varprefix):
        page.write("Device: ")
        page.select(varprefix+"device_address",
                    sorted(self._device_choices(), key=lambda x: x[1]),
                    self.device and self.device.address, onchange="this.form.submit()")
        page.write("Channel: ")
        page.select(varprefix+"channel_address",
                    sorted(self._channel_choices(), key=lambda x: x[1]),
                    self.channel and self.channel.address, onchange="this.form.submit()")
        page.write("Parameter: ")
        page.select(varprefix+"param_id",
                    sorted(self._param_choices(), key=lambda x: x[1]),
                    self.param and self.param.id, onchange="this.form.submit()")
        page.write("Type: ")
        page.select(varprefix+"event_type", self._event_types, self.event_type)


    def set_submitted_vars(self, page, varprefix):
        device_address = page.vars.getvalue(varprefix+"device_address")
        if device_address:
            self.device = self._manager.ccu.devices.query(
                                device_address=device_address).get(device_address)
            if not self.device:
                raise PMUserError("Unable to find the given device.")
        else:
            return

        channel_address = page.vars.getvalue(varprefix+"channel_address")
        if channel_address:
            try:
                self.channel = self.device.channel_by_address(channel_address)
            except KeyError:
                raise PMUserError("Unable to find the given channel.")
        else:
            return

        param_id = page.vars.getvalue(varprefix+"param_id")
        if param_id:
            self.param = self.channel.values.get(param_id)
            if not self.param:
                raise PMUserError("Unable to find the given channel.")
        else:
            return

        event_type = page.vars.getvalue(varprefix+"event_type")
        if event_type:
            if event_type not in dict(self._event_types):
                raise PMUserError("Invalid event type given.")
            self.event_type = event_type



class ConditionOnTime(Condition):
    type_name = "on_time"
    type_title = "based on time"

    _interval_choices = [
        ("daily",   "Daily"),
        ("weekly",  "Weekly"),
        ("monthly", "Monthly"),
    ]

    def __init__(self, manager):
        super(ConditionOnTime, self).__init__(manager)
        self.interval_type = None
        self.day_of_week   = 1
        self.day_of_month  = 1
        self.time_of_day   = (13, 00)

        self._next_time = None


    @property
    def next_time(self):
        if self._next_time is None:
            self.calculate_next_time()
        return self._next_time


    def calculate_next_time(self):
        """From now, calculate the next unix timestamp matching this condition."""

        # Initialize vars to be used as indices for timeparts
        year, month, mday, hour, minute, second, wday = range(7)

        now = time.time()

        # Construct list of time parts for today, using the configured time
        ref_parts = list(time.localtime(now))
        ref_parts[hour]   = self.time_of_day[0]
        ref_parts[minute] = self.time_of_day[1]
        ref_parts[second] = 0

        if self.interval_type == "daily":
            # When todays time is less than the configured time of day, the next
            # occurance is today at the given time. Otherwise it is tomorrow.
            ref_ts = time.mktime(tuple(ref_parts))
            if now >= ref_ts:
                ref_ts += 24 * 60 * 60 # tomorrow

        elif self.interval_type == "weekly":
            # When current weekday is less than the configured weekday, the next
            # occurance is in this week, otherwise it is next week.
            ref_ts = time.mktime(tuple(ref_parts))
            days_difference = (self.day_of_week-1) - ref_parts[wday]
            ref_ts += days_difference * 24 * 60 * 60
            if now >= ref_ts:
                ref_ts += 7 * 24 * 60 * 60 # next week

        elif self.interval_type == "monthly":
            # When current day of month is less than the configured day, the next
            # occurance is in this month, otherwise it is next month.
            ref_parts[mday] = self.day_of_month
            ref_ts = time.mktime(tuple(ref_parts))
            if now >= ref_ts:
                # next month
                if ref_parts[month] == 12:
                    ref_parts[month] = 1
                    ref_parts[year] += 1
                else:
                    ref_parts[month] += 1
                ref_ts = time.mktime(tuple(ref_parts))
        else:
            raise NotImplementedError()

        # Fix eventual timezone changes
        ref_parts = list(time.localtime(ref_ts))
        ref_parts[hour]   = self.time_of_day[0]
        ref_parts[minute] = self.time_of_day[1]
        ref_parts[second] = 0
        ref_ts = time.mktime(tuple(ref_parts))

        self._next_time = ref_ts


    def display(self):
        txt = super(ConditionOnTime, self).display()
        txt += ": %s" % self.interval_type
        if self.interval_type == "weekly":
            txt += " on day %d of week" % self.day_of_week
        elif self.interval_type == "monthly":
            txt += " on day %d of month" % self.day_of_month

        txt += ", at %02d:%02d o'clock" % self.time_of_day

        return txt


    def from_config(self, cfg):
        super(ConditionOnTime, self).from_config(cfg)
        self.time_of_day = tuple(self.time_of_day)


    def to_config(self):
        cfg = super(ConditionOnTime, self).to_config()
        cfg.update({
            "interval_type" : self.interval_type,
            "time_of_day"   : self.time_of_day,
        })

        if self.interval_type == "weekly":
            cfg["day_of_week"] = self.day_of_week
        elif self.interval_type == "monthly":
            cfg["day_of_month"] = self.day_of_month

        return cfg


    def input_parameters(self, page, varprefix):
        page.write("<table><tr><td>")
        page.write("Interval: ")
        page.write("</td><td>")
        page.select(varprefix+"interval_type", self._interval_choices,
                    self.interval_type, onchange="this.form.submit()")

        if self.interval_type == "weekly":
            page.write("Day of week: ")
            page.input(varprefix+"day_of_week", "%d" % self.day_of_week, cls="day_of_week")

        elif self.interval_type == "monthly":
            page.write("Day of month: ")
            page.input(varprefix+"day_of_month", "%d" % self.day_of_month, cls="day_of_month")
        page.write("</td></tr>")

        page.write("<tr><td>")
        page.write("Time (24h format): ")
        page.write("</td><td>")
        page.input(varprefix+"time_of_day", "%02d:%02d" % self.time_of_day, cls="time_of_day")
        page.write("</td></tr>")
        page.write("</table>")


    def set_submitted_vars(self, page, varprefix):
        interval_type = page.vars.getvalue(varprefix+"interval_type")

        if page.is_action() and not interval_type:
            raise PMUserError("You need to configure an interval.")

        if interval_type:
            if interval_type not in dict(self._interval_choices):
                raise PMUserError("Invalid interval given.")
            self.interval_type = interval_type

        self._set_time_of_day(page, varprefix)

        if self.interval_type == "weekly":
            self._set_weekly_vars(page, varprefix)
        elif self.interval_type == "monthly":
            self._set_monthly_vars(page, varprefix)


    def _set_time_of_day(self, page, varprefix):
        time_of_day = page.vars.getvalue(varprefix+"time_of_day")
        if not time_of_day:
            raise PMUserError("You need to provide a time.")

        time_parts = time_of_day.split(":")
        if len(time_parts) != 2:
            raise PMUserError("The time has to be given in <tt>HH:MM</tt> format.")

        try:
            time_parts = tuple(map(int, time_parts))
        except ValueError:
            raise PMUserError("The time has to be given in <tt>HH:MM</tt> format.")

        hours, minutes = time_parts

        if hours < 0 or hours > 23:
            raise PMUserError("The hours need to be between 00 and 23.")

        if minutes < 0 or minutes > 59:
            raise PMUserError("The minutes need to be between 00 and 59.")

        self.time_of_day = time_parts


    def _set_weekly_vars(self, page, varprefix):
        day_of_week = page.vars.getvalue(varprefix+"day_of_week")

        if page.is_action() and not day_of_week:
            raise PMUserError("You need to configure the day of the week.")

        if day_of_week:
            try:
                day_of_week = int(day_of_week)
            except ValueError:
                raise PMUserError("Invalid day of week given.")

            if day_of_week < 1 or day_of_week > 7:
                raise PMUserError("Invalid day of week given. It needs to be given as number "
                                  "between 1 and 7.")

            self.day_of_week = day_of_week


    def _set_monthly_vars(self, page, varprefix):
        day_of_month = page.vars.getvalue(varprefix+"day_of_month")

        if page.is_action() and not day_of_month:
            raise PMUserError("You need to configure the day of the month.")

        if day_of_month:
            try:
                day_of_month = int(day_of_month)
            except ValueError:
                raise PMUserError("Invalid day of month given.")

            if day_of_month < 1 or day_of_month > 31:
                raise PMUserError("Invalid day of month given. It needs to be given as number "
                                  "between 1 and 31.")

            self.day_of_month = day_of_month
