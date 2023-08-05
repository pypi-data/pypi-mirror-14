"""  Run whatever I'm doing at the time

Stuff in here probably belongs elsewhere.
"""

# run script from galleries folder
import sys
import time

# fixme, make it md2py 
import md2py
import json2py
import show

import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-t', '--time',
                    default=0, type=int,
                    help='time for slideshow in minutes')
parser.add_argument('-f', '--folder',
                    default='.',
                    help="folder of slides")
parser.add_argument('-s', '--slides',
                    default='slides.txt',
                    help='list of slides to show')
parser.add_argument('-w', '--wait',
                    default=0, type=int,
                    help='time to wait for slideshow')


args = parser.parse_args()

folder = args.folder
infile = args.slides
wait = args.wait


msg = open(infile)

mj = md2py

if infile.endswith('json'):
    mj = json2py
    msg = open(infile).read()

slides = mj.interpret(msg)

print("Number of slides:", len(slides))

print()
print(slides[0]['image'])
print()

ss = show.SlideShow()

ss.interpret(dict(slides=slides, captions=folder))

if args.time:
    ss.set_duration(args.time * 60)

time.sleep(wait)

for item in ss.run():
    # not sure what to do here
    pass
