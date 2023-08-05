"""
This one is going to read markdown.

For now, I am trying to read a talk outline and turn it into something
that will create a slideshow.

"""

import os

class Mark2Py:

    def __init__(self):

        pass

    def interpret(self, infile):
        """ Process a file of rest and return list of dicts """

        data = []

        for record in self.generate_records(infile):
            data.append(record)

        return data

    def hash_count(self, line):
        """ Count hashes at start of line

        Sad but true..
        """
        count = 0
        for c in line:
            if c != '#':
                break
            count += 1

        return count

    def generate_lines(self, infile):
        """ Split file into lines

        return dict with line=input, depth=n
        """
        pound = '#'
        
        for line in infile:

            heading = 0

            if line.startswith(pound):
                heading = self.hash_count(line)

            yield dict(line=line, heading=heading)


    def generate_records(self, infile):
        """ Process a file of rest and yield dictionaries """

        state = 0
        record = {}

        for item in self.generate_lines(infile):

            line = item['line']
            heading = item['heading']
            
            # any Markdown heading is just a caption, no image
            if heading:
                print(line)
                record['heading'] = True
                record['caption'] = line[1:].strip()

                state = 'caption'
                continue

            if not line[0].isspace():
                # at a potential image
                if state == 'caption':
                    yield record
                    record = {}
                    state = 0

            if state == 'caption':
                record['caption'] += '\n' + line[:-1]
                continue

            fields = line.split(',')

            # nothing there, carry on
            if not fields: continue

            image = fields[0].strip()

            if not image: continue

            record['image'] = image

            try:
                time = float(fields[1])
            except:
                time = 0

            record['time'] = time

            try:
                caption = fields[2].strip()
            except:
                caption = None

            if caption:
                record['caption'] = caption

            # yield it if we have anything
            if record:
                yield record
                record = {}


                


x = Mark2Py()

interpret = x.interpret
            

