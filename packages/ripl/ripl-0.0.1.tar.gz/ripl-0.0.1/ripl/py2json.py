"""
Take a python object and turn it into json.

World's simplest interpreter.
"""

import json

class Py2Json:

    def interpret(self, msg):

        return json.dumps(msg, indent=4)

x = Py2Json()

interpret = x.interpret
