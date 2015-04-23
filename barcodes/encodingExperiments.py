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

def generateCodes(n, boundaryPattern, maxNotches=-1, minNotches=0, allowPalindromes=True):
    # boundaryPattern = [0, 1, 1, 0]

    codes = generateAllBinaryCodes(n)
    codes = filterPattern(codes, [0, 0])
    codes = [boundaryPattern + code + boundaryPattern for code in codes]
    codes = filterPattern(codes, boundaryPattern, hasGuard=True)
    codes = [code for code in codes if code != code[::-1]]

    codes = [code for code in codes if sum(code) >= minNotches]
    if maxNotches > 0:
        codes = [code for code in codes if sum(code) <= maxNotches]

    if not allowPalindromes:
        codes = [code for code in codes if code != code[::-1]]

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

def compareCodings(minCardinality, maxLength, minCodeLength, maxCodeLength, minPatternLength, maxPatternLength,
    minNotches=0, maxNotches=-1, allowPalindromes=True):
    for codeLength in xrange(minCodeLength, maxCodeLength+1):
        for patternLength in xrange(minPatternLength, maxPatternLength+1):
            patterns = generateAllBinaryCodes(patternLength)
            patterns = filterPattern(patterns, [0, 0])
            patterns = [[1] + p + [1] for p in patterns if p == p[::-1]]
            # patterns = [[1] + p + [1] for p in patterns]

            for pattern in patterns:
                numCodes = len(generateCodes(codeLength, pattern, minNotches=minNotches, maxNotches=maxNotches, allowPalindromes=allowPalindromes))
                if numCodes >= minCardinality and codeLength + len(pattern) <= maxLength:
                    # print str(codeLength + len(pattern)) + ': ' + str(numCodes)
                    # print str(codeLength) + ' ' + str(codeLength + len(pattern)) + ' ' + str(len([x for x in pattern if x == 1]) - 1) + ' ' + codeToString(pattern) + ': ' + str(numCodes)
                    print '{0:2} {1:2} {2:2} {3:3} {4:10}'.format(str(codeLength), str(codeLength + len(pattern)), str(len([x for x in pattern if x == 1]) - 1), str(numCodes), codeToString(pattern))

# compareCodings(256, 22, 12, 14, 5, 7,
#     minNotches=21,
#     # maxNotches=25,
#     allowPalindromes=False
#     )

# this one ===>>> 12 21 6 ||| | |||: 281

notchPat = [1,1,1,0,1,0,1,1,1]
notchCodes = generateCodes(12, notchPat, maxNotches=2*sum(notchPat) + 11)
i = 0
# for code in notchCodes:
#     c = code[len(notchPat)-1:len(code)-len(notchPat)+1]
#     c = code
#     print "{0:3}: {1:22}".format(str(i), codeToString(c))
#     i += 1

def generate(pattern, length, minNotches=0, maxNotches=-1, excludePalindromes=False):
    def isPalindrome(code):
        return excludePalindromes and code == code[::-1]
        # return False
    def containsPattern(code):
        return code[len(code)-len(pattern):] == pattern
    def g(code):
        if sum(code) > length - sum(pattern):
            return []
        if len(code) > len(pattern) and containsPattern(code):
            return []
        if maxNotches > 0 and len(code) > maxNotches - len(pattern):
            return []
        if sum(code) == length - sum(pattern) and not isPalindrome(code[len(pattern):]):
            return h(code)
        return g(code + [2]) +  g(code + [1])
    def h(code):
        if len(code) < minNotches - len(pattern):
            return []
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

# pat = [1,1,2,2,1,1]
pat = [2,1,1,1,2]
codeLen = 14
minCodeNotches = 10
maxCodeNotches = 13
spaceCodes = generate(pat, 1 + 2 * sum(pat) + codeLen,
    excludePalindromes=True,
    minNotches=2*len(pat)+minCodeNotches,
    maxNotches=2*len(pat)+maxCodeNotches
    )
print len(spaceCodes)
# import collections
# counter = collections.Counter(map(len, spaceCodes))
# print counter
# print counter[18] + counter[20] + counter[22] + counter[24]
# print counter[19] + counter[21] + counter[23] + counter[17]
# i = 0
# for code in sorted(spaceCodes, key=lambda code: len(code)):
#     print "{0:3}: {1:22} {2:3}".format(str(i), spacesToString(code[len(pat):-len(pat)]), len(code))
#     i += 1

# i = 0
# for code in zip(notchCodes, spaceCodes):
#     print "{0:3} {1:22}".format(str(i), codeToString(code[0]))
#     print "{0:3} {1:22}".format(str(i), spacesToString(code[1]))
#     # if codeToString(code[0]) != spacesToString(code[1]):
#     #     print "{0:3} {1:22}".format(str(i), codeToString(code[0]))
#     #     print "{0:3} {1:22}".format(str(i), spacesToString(code[1]))

#     i += 1

