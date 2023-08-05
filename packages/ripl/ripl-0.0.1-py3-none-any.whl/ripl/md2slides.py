"""
This one is going to read markdown.

For now, I am trying to read a talk outline and turn it into something
that will create a slideshow.

This interpretter just turns markdown into a list of dictionaries.

The idea is then to feed this information into something like
caption.py which will create slides
"""

import os

class Mark2Slide:

    def __init__(self):

        pass

    def hash_count(self, line, pound=None):
        """ Count hashes (or other run of chars) at start of line

        >>> x = Mark2Slide()
        >>> x.hash_count('### hello')
        3

        >>> x = Mark2Slide()
        >>> x.hash_count(' hello', ' ')
        1

        """
        if pound is None:
            pound = '#'
            
        count = 0
        for c in line:
            if c != pound:
                break
            count += 1

        return count

    def generate_lines(self, infile):
        """ Split file into lines

        return dict with line=input, depth=n
        """
        pound = '#'
        
        for line in infile:

            heading = self.hash_count(line)

            indent = self.hash_count(line, pound=' ')

            yield dict(line=line.strip(),
                       heading=heading,
                       indent=indent)


    def generate_slides(self, infile):
        """ Process a file of rest and yield dictionaries """

        state = 0

        # each slide is a dict
        slide = {}

        last_heading = 0

        for item in self.generate_lines(infile):

            line = item['line']
            heading = item['heading']
            indent = item['indent']

            # Any heading is the heading for a new slide
            if heading:

                if slide and last_heading <= 1:
                    yield slide

                last_heading = heading
                    
                rows = []
                slide = dict(
                    heading = dict(text=line),
                    rows = rows)

                continue

            # Any block with more than one hash is a comment
            if last_heading > 1:
                continue

            if indent == 0 and line:
                # at a potential image
                rows.append(self.build_row(line))

            else:
                # Just add the line of text
                items = [dict(text=(' ' * indent) + line)]
                rows.append(dict(items=items))

        if slide:
            yield slide

    interpret = generate_slides
    

    def build_row(self, line):
        """ Line describes an image or images to show

        Returns a dict with a list of dicts of image names or text items

        Examples:

        # A single image to display
        >>> x.build_row('foo.png')
        [{'image': 'foo.png'}]

        # Two images with text in between:
        >>> x.build_row('foo.png or bar.jpg')
        [{'image': 'foo.png'}, {'text': 'or'}, {'image': 'bar.png'}]

        """

        items = []
        row = dict(items=items)
        fields = line.split(' ')

        image_exts = ['.png', '.jpg']

        # nothing there, carry on
        if not fields: return row

        for field in fields:

            ext = os.path.splitext(field)[-1]

            if ext.lower() in image_exts:
                items.append(
                    dict(image=field))

            else:
                items.append(
                    dict(text=field))

        return row


x = Mark2Slide()

interpret = x.interpret

if __name__ == '__main__':

    import sys
    m2s = Mark2Slide()

    slides = m2s.interpret(sys.stdin)

    for slide in slides:
        print(slide['heading'])

        rows = slide['rows']
        for row in rows:
            print(row)
