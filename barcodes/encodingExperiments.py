"""
Experiments in notch space encodings
"""

def generateAllBinaryCodes(n):
    def generateBinaryCode(code, m):
        if m == 0:
            return [code]
        else:
            return generateBinaryCode(code + [0], m-1) + generateBinaryCode(code + [1], m-1)
    return generateBinaryCode([], n)

def filterPattern(codes, pattern, hasGuard = False):

    def notContainsPattern(code):
        begin = 0
        end = len(code) - len(pattern) + 1
        if hasGuard:
            begin += 1
            end -= 1
        for i in xrange(begin, end):
            if code[i:i+len(pattern)] == pattern:
                return False
        return True

    return filter(notContainsPattern, codes)

def generateCodes(n, boundaryPattern, maxNotches=-1):
    # boundaryPattern = [0, 1, 1, 0]

    codes = generateAllBinaryCodes(n)
    codes = filterPattern(codes, [0, 0])
    codes = [boundaryPattern + code + boundaryPattern for code in codes]
    codes = filterPattern(codes, boundaryPattern, hasGuard=True)

    if maxNotches > 0:
        codes = [code for code in codes if sum(code) < maxNotches]

    return codes

def codeToString(code):
    def bitToString(b):
        if b == 0:
            return ' '
        else:
            return '|'
    return ''.join(map(bitToString, code))

# all_codes = generateCodes(13, [1, 0, 1, 1, 1, 0, 1])

# print len(all_codes)
# for code in all_codes:
#     print codeToString(code)

def compareCodings(minCardinality, maxLength, minCodeLength, maxCodeLength, minPatternLength, maxPatternLength):
    for codeLength in xrange(minCodeLength, maxCodeLength+1):
        for patternLength in xrange(minPatternLength, maxPatternLength+1):
            patterns = generateAllBinaryCodes(patternLength)
            patterns = filterPattern(patterns, [0, 0])
            patterns = [[1] + p + [1] for p in patterns if p == p[::-1]]

            for pattern in patterns:
                numCodes = len(generateCodes(codeLength, pattern))
                if numCodes >= minCardinality and codeLength + len(pattern) <= maxLength:
                    # print str(codeLength + len(pattern)) + ': ' + str(numCodes)
                    print str(codeLength) + ' ' + str(codeLength + len(pattern)) + ' ' + str(len([x for x in pattern if x == 1]) - 1) + ' ' + codeToString(pattern) + ': ' + str(numCodes)

# compareCodings(256, 21, 12, 13, 5, 7)

# this one ===>>> 12 21 6 ||| | |||: 281

notchPat = [1,1,1,0,1,0,1,1,1]
notchCodes = generateCodes(12, notchPat, maxNotches=2*sum(notchPat) + 11)
i = 0
# for code in notchCodes:
#     c = code[len(notchPat)-1:len(code)-len(notchPat)+1]
#     c = code
#     print "{0:3}: {1:22}".format(str(i), codeToString(c))
#     i += 1

def generate(pattern, length, maxNotches=-1):
    def containsPattern(code):
        return code[len(code)-len(pattern):] == pattern
    def g(code):
        if maxNotches > 0 and len(code) > maxNotches:
            return []
        if sum(code) > length - sum(pattern):
            return []
        if len(code) > len(pattern) and containsPattern(code):
            return []
        if sum(code) == length - sum(pattern):
            return h(code)
        return g(code + [2]) +  g(code + [1])
    def h(code):
        for space in pattern:
            if containsPattern(code):
                return []
            code += [space]
        return [code]

    return g(pattern)

def spacesToString(code):
    def spaceToString(b):
        if b == 2:
            return ' |'
        else:
            return '|'
    return '|' + ''.join(map(spaceToString, code))

print '========================================='

pat = [1,1,2,2,1,1]
spaceCodes = generate(pat, 1 + 2 * sum(pat) + 12, maxNotches=len(pat)+11)
# i = 0
# for code in spaceCodes:
#     print "{0:3}: {1:22}".format(str(i), spacesToString(code))
#     i += 1

i = 0
for code in zip(notchCodes, spaceCodes):
    # print "{0:3} {1:22}".format(str(i), codeToString(code[0]))
    # print "{0:3} {1:22}".format(str(i), spacesToString(code[1]))
    if codeToString(code[0]) != spacesToString(code[1]):
        print "{0:3} {1:22}".format(str(i), codeToString(code[0]))
        print "{0:3} {1:22}".format(str(i), spacesToString(code[1]))

    i += 1

