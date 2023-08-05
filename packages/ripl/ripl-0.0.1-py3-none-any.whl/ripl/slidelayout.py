"""
Add layout information to slides

Each slide is a heading plus a list of rows.

Each row is a list of text strings or image names.

This uses PIL to measure the size of text so it can
figure out where to lay everything out.

Input is a list of dictionaries.

Each dictionary describes a single slide.
"""
import os

from PIL import Image, ImageDraw, ImageFont

FONT = '/usr/share/fonts/TTF/Vera.ttf'
FONTSIZE = 36
WIDTH = 1024
HEIGHT = 768

class SlideLayout:

    def __init__(self):

        self.pos = 0
        self.padding = 10
        self.cache = 'show'
        self.font = ImageFont.truetype(FONT, FONTSIZE)

    def interpret(self, msg):
        """ Load input """
        slides = msg.get('slides', [])

        result = []
        for slide in slides:
            image = self.layout(slide)

            result.append(image)

        return result

    def layout(self, slide):
        """ Return layout information for slide """

        image = Image.new('RGB', (WIDTH, HEIGHT), 'black')
        draw = ImageDraw.Draw(image)
        draw.font = self.font
        
        self.vertical_layout(draw, slide)
        
        self.horizontal_layout(draw, slide)

        return slide


    def vertical_layout(self, draw, slide):
        """ Augment slide with vertical layout info """
        padding = self.padding
        heading = slide['heading']

        width, height = draw.textsize(heading['text'])
        top = padding
        left = padding

        # Calculate size and location of heading
        heading.update(dict(
            width = width,
            height = height,
            top = self.padding,
            left = self.padding))

        top += height + padding

        # count how many rows just text and how many have image
        rows = slide['rows']
        text_rows = 0
        image_rows = 0

        # calculate size of all text objects
        total_height = top
        for row in rows:

            row_height = 0

            images = 0
            for item in row['items']:
                if item.get('image'):
                    images += 1

                text = item.get('text')
                
                if text is None: continue
                    
                width, height = draw.textsize(text)

                item.update(dict(
                    width = width,
                    height = height))

                row_height = max(row_height, height)
                

            if images:
                image_rows += 1
                row['images'] = images
            else:
                row['height'] = row_height
                text_rows += 1

            total_height += row_height + padding
                
        # Calculate average height for image rows
        if image_rows:
            
            available = HEIGHT - total_height

            image_height = available // image_rows

            image_text_offset = image_height // 2

        # now spin through rows again setting top
        # (and height for images)
        for row in rows:
            text_top = top
            
            images = row.get('images', 0)
            if images:
                text_top += image_text_offset

            for item in row['items']:
                if item.get('text') is not None:
                    item['top'] = text_top
                else:
                    # image
                    item['top'] = top
                    item['height'] = image_height
                    row['height'] = image_height

            
            top += row.get('height', 0) + padding

        return

    def horizontal_layout(self, draw, slide):
        """ Augment slide with horizontal layout info """
        padding = self.padding
        heading = slide['heading']

        top = padding
        left = padding

        top += heading['height'] + padding

        rows = slide['rows']

        for row in rows:

            images = row.get('images', 0)

            items = row['items']
            
            used_width = sum(x.get('width', 0) for x in items)

            available_width = WIDTH - (
                used_width + ((1 + len(items)) * padding))

            if images:
                image_width = available_width // images

            # OK, now set left for all items and image_width for images
            left = padding
            for item in row['items']:

                if item.get('image'):
                    item['width'] = image_width

                item['left'] = left    

                left += item['width'] + padding

        return



