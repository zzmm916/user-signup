#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re

page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>Signup</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>

</head>
<body>
    <h1>Signup</h1>
"""


page_footer = """
</body>
</html>
"""

#class MainHandler(webapp2.RequestHandler):

form = """
<form method="post">

    <label>
        Username
    </label>
    <input type="text" name="username" value="%(username)s" />%(username_error)s

    <br>
    <label>
        Password
        <input type = "password" name = "password"/>%(pass_error)s
    </label>
    <br>
    <label>
        Verify password
        <input type="password" name="vp"/>%(pass_match_error)s
    </label>
    <br>
    <label>
        Email (optional)
        <input type="text" name="email" value="%(email)s"/>%(email_error)s
    </label>
    <br>
    <input type="submit"/>
</form>
    """

content=page_header + form + page_footer

class MainHandler(webapp2.RequestHandler):

    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    def valid_username(self, s):
        return self.USER_RE.match(s)

    PASS_RE = re.compile(r"^.{3,20}$")
    def valid_password(self, p):
        return self.PASS_RE.match(p)

    EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
    def valid_email(self, email):
        return self.EMAIL_RE.match(email)


    def write_form(self, username_error="", pass_error="", pass_match_error="", email_error="", username="", email=""):
        self.response.out.write(content % {'username_error': username_error, 'pass_error': pass_error,
         'pass_match_error': pass_match_error, 'email_error': email_error, 'username': username, 'email':email})

    def get(self):
        self.write_form()

    #def error(self, usernameerror, passerror,emailerror):
    def post(self):

        name = self.request.get("username")
        pas = self.request.get("password")
        e = self.request.get("email")
        vp= self.request.get("vp")
        username_error=""
        pass_error=""
        pass_match_error=""
        email_error=""
        isError = False

        if not self.valid_username(name):
            username_error='<p class="error">The users username is not valid</p>'
            isError = True
        if not self.valid_password(pas):
            pass_error = '<p class="error">The users password is not valid</p>'
            isError = True
        if   vp!=pas:
            pass_match_error = '<p class="error">The users password and password-confirmation do not match</p>'
            isError = True
        if e != "" and not self.valid_email(e):
            email_error = '<p class="error">The user provides an email, but its not a valid email.</p>'
            isError = True
        if isError:
            self.write_form(username_error, pass_error, pass_match_error, email_error, name, e)
        else:
            self.redirect("/welcome?username="+name)

class Welcome(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")
        welcome= "Welcome, "+ username +"!"
        welcome_msg = '<h1>' + welcome + '</h1>'
        self.response.write(welcome_msg)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', Welcome)
], debug=True)
