"""
Create slides for a slideshow

TODO: would be nice if it did not give eog focus.
"""
import os

from PIL import Image, ImageDraw, ImageFont

FONT = '/usr/share/fonts/TTF/Vera.ttf'
FONTSIZE = 36
WIDTH = 1024
HEIGHT = 768

class SlideShow:

    def __init__(self):

        self.pos = 0
        self.cache = 'show'
        self.font = ImageFont.truetype(FONT, FONTSIZE)

    def interpret(self, msg):
        """ Load input """
        slides = msg.get('slides', [])
        self.cache = msg.get('folder')
        self.gallery = msg.get('gallery', '..')

        with open(self.cache + '/slides.txt', 'w') as logfile:
            for ix, item in enumerate(slides):
                image = self.prepare_image(item)
                filename = self.cache_image(item, image)

                text = item.get('caption', '')

                # do not write text for heading images
                if item.get('heading'):
                    text = ''
                    
                if text:
                    with open(filename + '.txt', 'w') as caption:
                        caption.write(text)
                print('%s,%d' % (filename, item.get('time', 0)), file=logfile)

    def prepare_image(self, slide):

        image = slide.get('image')
        caption = slide.get('caption')

        if caption is None:
            # use image name, without the suffic
            caption = os.path.splitext(image)[0]

            # convert _ to ' '
            caption = caption.replace('_', ' ')

            # save the caption
            slide['caption'] = caption
 
        # create image
        image_file = self.create_image(image, caption)

        return image_file

    def create_image(self, image_file, caption):
        """ Create an image with a caption """
        suffix = 'png'
        if image_file:
            img = Image.open(os.path.join(self.gallery, image_file))
            width, height = img.size
            ratio = width/WIDTH
            img = img.resize((int(width // ratio),
                              int(height // ratio)),
                             Image.ANTIALIAS)
        else:
            img = Image.new('RGB', (WIDTH, HEIGHT), 'black')
            image = self.add_caption(img, caption)
            
        image = img

        return image


    def cache_image(self, item, image):

        
        
        #name = "%s/slide%d.png" % (self.cache, ix)

        caption = item.get('image')
        if caption is None:
            caption = item.get('caption').split('\n')[0]
            
        caption = caption.split('/')[-1]
        caption = caption.replace(' ', '_')
        
        name = "%s/%s.png" % (self.cache, caption)
        
        with open(name, 'w') as slide:
            image.save(name)

        return name


    def add_caption(self, image, caption, colour=None):
        """ Add a caption to the image """

        if colour is None:
            colour = "white"
    
        width, height = image.size
        draw = ImageDraw.Draw(image)

        draw.font = self.font

        draw.font = self.font
        draw.text((width // 10, height//20), caption,
                  fill=colour)

        return image


        



    
