"""
Generate barcode images with various encodings

TODO
- Include text at bottom
- DXF instead
"""
#========================================================
# Imports
#========================================================

from dxfwrite import DXFEngine as dxf

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

    def __init__(s, code, width=200, height=None, unitWidth=None, barWidth=None,
        notchWidth=2, startBand=[1,1], stopBand=[0,1], includeText=False):
        
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

        # Notch unit width
        unitLen = sum(map(lambda x: s.ZERO_WIDTH if x==0 else s.ONE_WIDTH, s.digits))
        if unitWidth == None:
            # Sub one notchWidth for first notch, add 2 unit len for buffer
            codeWidth = (height - notchWidth)/(unitLen + 2) 
            unitWidth = codeWidth - notchWidth
        s.unitWidth = unitWidth

        # Check valid lengths
        s.barcodeLen = (unitWidth + notchWidth) * unitLen + notchWidth
        if s.barcodeLen > height:
            raise ValueError('Too many digits to fit window')

    def draw(s,outfile):

        # Create image
        drawing = dxf.drawing(s.OUTFILE + outfile)
        drawing.add_layer('layer', color=1)

        # Draw text
        if s.includeText:
            text = ''
            text += ''.join(map(str,s.startBand))
            text += '-'
            text += ''.join(map(str,s.code))
            text += '-'
            text += ''.join(map(str,s.stopBand))
            drawing.add(dxf.text(text, height=s.unitWidth/3))

        # Initial offset
        xOffset = (s.size[0] - s.barWidth) / 2
        yOffset = (s.size[1] - s.barcodeLen) / 2

        # Draw notches
        for d in s.digits:
            newOffset = s.drawBar(drawing,d,xOffset,yOffset)
            yOffset = newOffset[1]

        # Draw final notch
        s.drawNotch(drawing, xOffset, yOffset)

        drawing.save()

    def drawBar(s, drawing, digit, xOffset, yOffset):
        """ Draw bar and return lower right corner """
        
        (x0,y0,x1,y1) = s.drawNotch(drawing, xOffset, yOffset)

        # Draw end notch
        x0 = xOffset

        # Notch distance apart encodes digit
        if digit == 0:
            y0 = y1 + s.ZERO_WIDTH*s.unitWidth
        elif digit == 1:
            y0 = y1 + s.ONE_WIDTH*s.unitWidth

        return (x0,y0)

    def drawNotch(s, drawing, xOffset, yOffset):
        # Draw start notch
        x0 = xOffset
        y0 = yOffset
        x1 = x0 + s.barWidth
        y1 = y0 + s.notchWidth
        drawing.add(dxf.polyline(points=[(x0,y0), (x1,y0), (x1,y1), (x0,y1), (x0,y0)]))
        return (x0,y0,x1,y1)

#========================================================
# Parse options
#========================================================

if __name__ == '__main__':
    
    codes = [[1,1,1],[0,0,0],[0,1,0],[1,0,1]]
    width = 15
    height = 20
    unit = 1
    notchWidth = [.3,.5]

    for code in codes:
        codeStr = ''.join(map(str,code))

        for n in notchWidth:
            filename = 'code' + codeStr + '-notch' + str(n) + '-len' + str(unit) + '.dxf'
            drawer = BarcodeDrawer(code, width=width, height=height, unitWidth=unit, notchWidth=n,
                includeText=True)
            drawer.draw(filename)

