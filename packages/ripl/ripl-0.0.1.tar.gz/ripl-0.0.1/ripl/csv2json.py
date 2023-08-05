"""
This one is going to read csv.

For now, I am trying to read a talk outline and turn it into something
that will create a slideshow.

"""

import os
import sys
import csv
import pandas

import getopt


class Csv2Json

    def __init__(self):
        
        pass

    def interpret(self, infile):
        """ Process a file of rest and return json """

        # need row headings
        data = pandas.read_csv(infile)

        # FIXME find the right foo
        return json.dumps(data.foo())
            
                


if __name__ == '__main__':

    csv2json = Csv2Json()

    return csv2json.interpret(sys.stdin.read())

