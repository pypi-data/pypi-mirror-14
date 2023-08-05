"""
Create slides for a slideshow

Each slide is a heading plus a list of rows.

Each row is a list of text strings or image names.

This uses PIL to create an image for each slide.
"""
import os

from PIL import Image, ImageDraw, ImageFont

FONT = '/usr/share/fonts/TTF/Vera.ttf'
FONTSIZE = 36
WIDTH = 1024
HEIGHT = 768

class Slide2png:

    def __init__(self):

        self.pos = 0
        self.padding = 10
        self.cache = 'show'
        self.font = ImageFont.truetype(FONT, FONTSIZE)

    def interpret(self, msg):
        """ Load input """
        slides = msg.get('slides', [])
        self.cache = msg.get('folder', '.')
        self.gallery = msg.get('gallery', '..')

        # in case slides is a generator, turn it into a list
        # since I am going to go through it twice
        slides = [slide for slide in slides]

        # Write slides.txt with list of slides
        with open(self.cache + '/slides.txt', 'w') as logfile:
            for slide in slides:
                heading = slide['heading']['text']
                filename = self.get_image_name(heading)
                
                print('%s,%d' % (filename, slide.get('time', 0)),
                      file=logfile)

        # Now spin through slides again
        for slide in slides:

            image = self.draw_slide(slide)

            heading = slide['heading']['text']
            filename = self.get_image_name(heading)

            self.cache_image(filename, image)

        # fixme -- just return info in slides.txt as list of dicts
        return

    def draw_slide(self, slide):
        """ Return layout information for slide """

        image = Image.new('RGB', (WIDTH, HEIGHT), 'black')
        draw = ImageDraw.Draw(image)
        draw.font = self.font
        
        self.draw_slide_text(draw, slide)

        self.draw_slide_images(draw, slide, image)

        return image

    def draw_slide_text(self, draw, slide):

        heading = slide['heading']
        print(heading['text'])
        rows = slide['rows']

        
        left, top = heading['top'], heading['left']
        
        draw.text((left, top), heading['text'], fill='white')

        for row in rows:
            for item in row['items']:
                top, left = item['top'], item['left']
                
                print('tl', item['top'], item['left'])
                print('wh', item['width'], item['height'])

                print(item.get('text', ''))
                print(item.get('image', ''))

                text = item.get('text')

                if not text:
                    continue

                draw.text((left, top), text, fill='white')

                      
            print()

    def draw_slide_images(self, draw, slide, image):

        heading = slide['heading']
        rows = slide['rows']
        
        left, top = heading['top'], heading['left']
        
        for row in rows:
            for item in row['items']:
                top, left = item['top'], item['left']
                
                print('tl', item['top'], item['left'])
                print('wh', item['width'], item['height'])

                print(item.get('text', ''))
                print(item.get('image', ''))

                text = item.get('text')

                image_file = item.get('image')

                if not image_file: continue

                source = self.find_image(item)
                if source:
                    self.draw_image(image, item, source)
                else:
                    # no image, just use text
                    draw.text((left, top), text, fill='white')
                        
                      
            print()


    def find_image(self, item):
        """ Try and find the image file 

        some magic here would be good.

        FIXME move elsewhere and make so everyone can use.

        interpreter that finds things?
        """
        image_file = item['image']

        guess = os.path.join(self.gallery, image_file)
        if os.path.exists(guess):
            return guess

        return None
        

    def draw_image(self, image, item, source):
        """ Add an image to the image """
        top, left = item['top'], item['left']
        width, height = item['width'], item['height']
        image_file = item['image']
        
        img = Image.open(source)

        iwidth, iheight = img.size

        wratio = width / iwidth
        hratio = height / iheight

        print(width, height, iwidth, iheight)

        ratio = min(wratio, hratio)
        print(wratio, hratio, ratio)

        print('resizing %s %6.4f' % (image_file, ratio))
        
        img = img.resize((int(iwidth * ratio),
                          int(iheight * ratio)),
                         Image.ANTIALIAS)
        

        # get updated image size
        iwidth, iheight = img.size
        
        # Adjust top, left for actual size of image so centre
        # is in the same place as it would have been
        
        top += (height - iheight) // 2
        left += (width - iwidth) // 2
        
        # now paste the image
        print('pasting %s' % image_file)
        print(left, top)
        image.paste(img, (left, top))
        

    def slugify(self, name):
        """ Turn name into a slug suitable for an image file name """
        slug = ''
        last = ''
        for char in name.replace('#', '').lower().strip():
            if not char.isalnum():
                char = '_'

            if last == '_' and char == '_':
                continue

            slug += char
            last = char

        return slug
    
    def cache_image(self, name, image):
        
        
        with open(name, 'w') as slide:
            image.save(name)

        return name


    def get_image_name(self, label):

        return "%s/%s.png" % (self.cache, self.slugify(label))
