"""
Simple slide shower using eog.

TODO: would be nice if it did not give eog focus.
"""
import os
import time
import subprocess

from PIL import Image, ImageDraw

class SlideShow:

    def __init__(self):

        self.slides = []
        self.pos = 0
        self.wait = 0
        self.feh = None

    def interpret(self, msg):
        """ Create a slide show """

        self.captions = msg.get('captions', '.')
        
        for item in msg['slides']:
            self.add(item)

    def add(self, slide):

        self.slides.append(slide)

    def next(self):

        # send feh a signal to move to the next slide
        # 10 is SIGUSR1
        # this is byzantine, must be a better way to send a signal
        # from python
        os.system('kill -s 10 %d' % self.feh.pid)

    def show(self):
        
        #os.system('eog -g -w %s &' % image_file)
        #os.system('feh -F %s &' % image_file)
        slides = ' '.join([x.get('image', '') for x in self.slides])
        cmd = 'feh --scale-down --caption-path %s %s' % (
            self.captions, slides)
        self.feh = subprocess.Popen(cmd.split(' '))

    def set_duration(self, duration):
        """ Calculate how long each slide should show """
        fixed = sum(int(x.get('time', 0)) for x in self.slides)

        nfixed = len([x for x in self.slides if x.get('time', 0) > 0])

        unfixed = len(self.slides) - nfixed

        self.wait = max(1, int(duration / unfixed))

    def run(self):
        """ Run the show """

        self.show()

        if not self.wait:
            return
        
        for image in self.slides:
            wait = image.get('time', 0)
            wait = max(self.wait, wait)
            print('waiting %d seconds %s' % (
                wait, image.get('image', '')))
            yield image
            time.sleep(wait)
            self.next()

        



    
