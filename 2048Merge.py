"""
#http://www.codeskulptor.org/#user41_GvqDPV2v37_4.py

Merge function for 2048 game.
"""

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    
    shifted = []
    result = []
    skip_next = False
    
    # shift all non-zero values to left
    for num in line:
        if num != 0:
            shifted.append(num)
    while len(shifted) < len(line):
        shifted.append(0)
    print (shifted)
    
    # merge adjacent equal values from left to right
    for num in range(0,len(shifted) - 1):
        if skip_next:
            skip_next = False
        else:
            if shifted[num] == shifted[num + 1]:
                result.append(shifted[num] * 2)
                skip_next = True
            else:
                result.append(shifted[num])
    
    if shifted[-1] != 0 and skip_next == False:
        result.append(shifted[-1])
    
    while len(result) < len(line):
        result.append(0)
        
    return result
                      
