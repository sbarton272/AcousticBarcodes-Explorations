"""
Generate barcode images with various encodings

TODO
- Include text at bottom
- DXF instead
"""
#========================================================
# Imports
#========================================================

from PIL import Image, ImageDraw

#========================================================
# Constants
#========================================================

START_BAND = [1,1]
STOP_BAND = [0,1]

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
    ZERO_WIDTH = 2
    ONE_WIDTH = 1

    def __init__(s, code, width=200, height=500, unitWidth=None, barWidth=None,
        notchWidth=2, startBand=[1,1], stopBand=[0,1], includeText=False):
        
        s.digits = startBand + code + stopBand

        # Bar width by defualt assumed to be full width
        if barWidth == None:
            barWidth = width
        s.barWidth = barWidth

        s.size = (width, height)
        s.notchWidth = notchWidth

        # Notch unit width
        unitLen = sum(map(lambda x: s.ZERO_WIDTH if x==0 else s.ONE_WIDTH, s.digits))
        if unitWidth == None:
            # Sub one notchWidth for first notch
            codeWidth = (height - notchWidth)/unitLen
            unitWidth = codeWidth - notchWidth
        s.unitWidth = unitWidth

        # Check valid lengths
        s.barcodeLen = (s.unitWidth + s.notchWidth) * unitLen
        if s.barcodeLen > height:
            raise ValueError('Too many digits to fit window')

        # Create image
        s.im = Image.new('RGBA', s.size, (255,255,255,0))
        s.drawIm = ImageDraw.Draw(s.im)

    def draw(s,outfile,preview=False):

        xOffset = (s.size[0] - s.barWidth) / 2
        yOffset = (s.size[1] - s.barcodeLen) / 2

        for d in s.digits:
            out = s.drawBar(d,xOffset,yOffset)
            yOffset = out[1]

        if preview:
            s.im.show()

        s.im.save(s.OUTFILE + outfile)


    def drawBar(s, digit, xOffset, yOffset):
        """ Draw bar and return lower right corner """
        
        # Draw start notch
        x0 = xOffset
        y0 = yOffset
        x1 = x0 + s.barWidth
        y1 = y0
        s.drawIm.line((x0,y0,x1,y1), fill=(0,0,0,0), width=s.notchWidth)

        # Draw end notch
        x0 = xOffset

        # Notch distance apart encodes digit
        if digit == 0:
            y0 = y1 + s.ZERO_WIDTH*s.unitWidth + s.notchWidth
        elif digit == 1:
            y0 = y1 + s.ONE_WIDTH*s.unitWidth + s.notchWidth
        else:
            # Only encode binary
            return (x0,y0)

        x1 = x0 + s.barWidth
        y1 = y0
        s.drawIm.line((x0,y0,x1,y1), fill=(0,0,0,0), width=s.notchWidth)

        return (x0,y0)

#========================================================
# Parse options
#========================================================

if __name__ == '__main__':
    
    drawer = BarcodeDrawer([1,0,1], 150, 500, 30, 150, 10)
    drawer.draw('1101.png',True)

