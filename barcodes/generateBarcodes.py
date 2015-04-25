"""
Generate barcode images with various encodings

units are in pixels/points, 1 inch = 72 points
"""
#========================================================
# Imports
#========================================================

from dxfwrite import DXFEngine as dxf
from spaceEncoder import generateLookupTable, encodeToSpacing, spacesToBinary
# sorry you have to manually get a WORKING python smaz port
# the package from 'pip install smaz' is buggy
from smaz import compress # compress(string)
from reedsolo import RSCodec # RSCodec(numSydromes).encode(int[])

#========================================================
# Constants
#========================================================

INCH = 72
PADDING = [2,1,1,1,2]
START_BAND = [1,1,1,1,1,1,1,1]
STOP_BAND =  [1,1,1,1,1,1,1,1]
DATA_LEN = 14
P = 18491 # 11 * 41 * 41
Q = 18551 # 13 * 1427
MAX_DATA_NOTCHES = 13
MIN_DATA_NOTCHES = 10
ENCODING_TABLE = generateLookupTable(PADDING, DATA_LEN, P, Q,
    maxDataNotches=MAX_DATA_NOTCHES, minDataNotches=MIN_DATA_NOTCHES)
ENCODING_TABLE_FILENAME = 'space_encoding.txt'

#========================================================
# Hamming Codes
#========================================================

class Encoding(object):
    def __init__(s, code):
        s.code = code

    def __str__(s):
        strCode = "".join(map(lambda x: str(x), s.code))
        strEncode = "".join(map(lambda x: str(x), s.encode))
        return "Encoding(" + strCode + " -> " + strEncode + ")"

#========================================================
# Barcode drawer
#========================================================

class BarcodeDrawer(object):

    OUTFILE = 'drawings/'

    # Encoding: 0 = 2 unit, 1 = 1 unit
    TWO_WIDTH = 2
    ONE_WIDTH = 1

    LINE_THICKNESS = 0.00001 # lasercutter monitors do this so...

    def __init__(s, code, width=200, height=None, unitWidth=None, barWidth=None,
        notchWidth=2, startBand=[1,1], stopBand=[1,1], includeText=False, margin=None):

        if margin == None:
            margin = width

        s.digits = startBand + code + stopBand

        # Bar width by defualt assumed to be full width
        if barWidth == None:
            barWidth = width
        s.barWidth = barWidth

        s.size = (width, height)
        s.notchWidth = notchWidth
        s.includeText = includeText
        s.startBand = startBand
        s.stopBand = stopBand
        s.code = code
        s.margin = margin

        # Notch unit width
        unitLen = sum(map(lambda x: s.TWO_WIDTH if x==2 else s.ONE_WIDTH, s.digits))
        if unitWidth == None:
            # Sub one notchWidth for first notch, add 2 unit len for buffer
            codeWidth = (height - notchWidth)/(unitLen + 2)
            unitWidth = codeWidth - notchWidth
        s.unitWidth = unitWidth

        # Check valid lengths
        s.barcodeLen = (unitWidth + notchWidth) * unitLen + notchWidth
        # if s.barcodeLen > height:
        #     raise ValueError('Too many digits to fit window')

    def draw(s,outfile):

        # Create image
        drawing = dxf.drawing(s.OUTFILE + outfile)
        drawing.add_layer('VECTOR', color=1)
        drawing.add_layer('ENGRAVE', color=3)

        # Draw text
        if s.includeText:
            text = ''
            text += ''.join(map(str,s.startBand))
            text += '-'
            text += ''.join(map(str,s.code))
            text += '-'
            text += ''.join(map(str,s.stopBand))
            drawing.add(dxf.text(text, height=s.unitWidth))

        # Initial offset
        xOffset = 0
        yOffset = 0

        # Draw notches
        for d in s.digits:
            newOffset = s.drawBar(drawing,d,xOffset,yOffset)
            yOffset = newOffset[1]

        # Draw final notch
        s.drawNotch(drawing, xOffset, yOffset)
        yOffset += s.notchWidth

        s.drawBorder(drawing, xOffset, yOffset)

        drawing.save()

    def drawBar(s, drawing, digit, xOffset, yOffset):
        """ Draw bar and return lower right corner """

        (x0,y0,x1,y1) = s.drawNotch(drawing, xOffset, yOffset)

        # Draw end notch
        x0 = xOffset

        # Notch distance apart encodes digit
        if digit == 2:
            # take into account of notch width
            y0 = y1 + s.TWO_WIDTH*s.unitWidth + s.notchWidth
        elif digit == 1:
            y0 = y1 + s.ONE_WIDTH*s.unitWidth

        return (x0,y0)

    def drawNotch(s, drawing, xOffset, yOffset):
        # Draw start notch
        x0 = xOffset
        y0 = yOffset
        x1 = x0 + s.barWidth
        y1 = y0 + s.notchWidth
        polyline = dxf.polyline(points=[(x0,y0), (x1,y0), (x1,y1), (x0,y1)],
            layer='ENGRAVE', thickness=s.LINE_THICKNESS)
        polyline.close()
        drawing.add(polyline)

        return (x0,y0,x1,y1)

    def drawBorder(s, drawing, xOffset, yOffset):
        x0 = xOffset
        y0 = -s.margin
        x1 = x0 + s.barWidth
        y1 = yOffset + s.margin
        polyline = dxf.polyline(points=[(x0,y0), (x1,y0), (x1,y1), (x0,y1)],
            layer='VECTOR', thickness=s.LINE_THICKNESS, color=256)
        polyline.close()
        drawing.add(polyline)

#========================================================
# Parse options
#========================================================



if __name__ == '__main__':

    data = [
        ('bruh', 'bruh', 2),
        ('hello_world', 'hello world', 3),
        ('hello_tom', 'say hi to tom sullivan for us', 3),
        ('github_url', 'http://github.com/sbarton272/acousticbarcodes-app', 4),
        ('batman', "what did batman say to robin before getting in the car?\n\n\n\nget in the car", 4),
        ('farmer', "What did the farmer say when he lost his tractor?\n\n\n\n\n\n\nI'm going to kill myself.", 4),
        ('long_message', """\
If you had to scratch multiple times in order to see this message, congratulations for your persistence!
If you got this on your first try, congratulations to us for making this robust!\
""", 8)
    ]
    width = INCH / 2
    margin = INCH * 1.5
    unit = 0.5
    notchWidth = 0.5

    for (name, string, nsym) in data:
        print 'Making barcode for:', name
        print 'Raw length:', len(string)
        # compress and transform into int list
        code = compress(string)
        code = [ord(c) for c in code]
        print 'Compressed length:', len(code)
        print 'Compression ratio:', str(100 - int(100.0 * len(code) / len(string))) + '%'
        # add syndromes and transform into int list
        print 'Number of syndromes:', nsym
        code = RSCodec(nsym).encode(code)
        code = list(code)
        print 'Total length:', len(code)
        # turn into space encoding
        code = encodeToSpacing(code, ENCODING_TABLE, PADDING)
        print 'Physical length in unit lengths/pixels/points:', sum(code) + 2 * margin
        print 'Physical length in inches:', 1.0 * sum(code)/INCH + 2 * margin / INCH
        print 'Number of notches:', len(code) + 1

        print 'Drawing...'
        filename = name + '-len' + str(sum(code)) + '-nsym' + str(nsym) + '.dxf'
        drawer = BarcodeDrawer(code, width=width, unitWidth=unit, notchWidth=notchWidth,
            includeText=False, startBand=START_BAND, stopBand=STOP_BAND, margin=margin)
        drawer.draw(filename)
        print 'Finished drawing!\n'

    #save the encoding table
    with open(ENCODING_TABLE_FILENAME,'w') as f:
        f.write('\n'.join([str(spacesToBinary(space)) for space in ENCODING_TABLE]))

