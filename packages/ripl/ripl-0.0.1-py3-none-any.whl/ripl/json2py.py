"""
Take a json string and turn it into python.

Result should be a list of dictionaries or a dictionary of lists or
whatever, per the json input.

World's simplest interpreter.
"""

import json

class Json2Py:

    def interpret(self, msg):

        return json.loads(msg)

    
x = Json2Py()

interpret = x.interpret
