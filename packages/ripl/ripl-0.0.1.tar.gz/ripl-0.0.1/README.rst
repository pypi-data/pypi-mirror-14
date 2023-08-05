==============================
 Really Incredibly Point Less
==============================

RIPL == Really Incredibly Point Less

or

RIPL == Read Interpret Print Loop

This started life as some simple utilities to help me write a
presentation.

The idea was to write something in restructured text and have some
code to read the text, interpret it and turn it into a bunch of slides
for a presentation.

In the end I went with markdown, but only a subset of markdown is
really supported.

For each slide, you can specify a heading and then some lines of text
for the slide.

You can also specify an image to display, or images.


Installation / Usage
====================

To install use pip:

    $ pip install ripl


Or clone the repo:

    $ git clone https://github.com/swfiua/ripl.git
    $ python setup.py install


Interpretters
=============

So far it is just a bunch of python modules which I call
interpretters.

Each module has a class with an interpret method.

py2json and json2py
-------------------

The built-in *json* module does all the work here.   These just turn
json into python dictionaries and lists and vice-versa.

md2slides.py
------------

This reads the markdown and turns it into a list of slides.  Each
slide is just a python dictionary full of information about the
slides.

slide2png.py
------------

This takes the output from md2slides (or anything in a similar format)
and creates a folder full of slides.

As well as a bunch of image files, slide2png.py outputs a file with
the list of slides in the slideshow.

layout
++++++

I would like to strip the layout code in slide2png into a separate
interpretter.

This would just augment the incoming information with layout data.

create_images
+++++++++++++

The code that actually creates the images could then work with the
layout code.


show
----

This actually displays the slideshow.

It has an option to say how many minutes the slideshow should be and
will automatically advance the slides for you, pechakucha style.

run*.py
-------

Various scripts to run everything.

TODO
====

rest2py and py2rest

mark2rest and rest2mark

rest2json and json2rest

py2json and json2py.  these are done coutesy of import json.

Chaining converstions and examining information loss.

Get sphinx and readthedocs working here.

python-snowballstemmer looks interesting, seems to be finding stems of
words and also to be multi-lingual.


