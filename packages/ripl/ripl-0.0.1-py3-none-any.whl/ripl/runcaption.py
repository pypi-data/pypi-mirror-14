"""  Run whatever I'm doing at the time

Stuff in here probably belongs elsewhere.
"""

# run script from galleries folder

# fixme, make it md2py 
import md2py
import json2py
import caption
import show
import sys
import os

infile = os.path.expanduser('~/devel/blog/stories/talk.rst')

folder = '.'
if sys.argv[1:]:
    folder = sys.argv[1]
    
if sys.argv[2:]:
    infile = sys.argv[2]

mj = md2py

msg = open(infile)

if infile.endswith('json'):
    mj = json2py
    msg = open(infile).read()

slides = mj.interpret(msg)

print(slides[:5])

ss = caption.SlideShow()
ss.interpret(dict(slides=slides, folder=folder))


