def fontscompare(a, b):
    
    if a is None or b is None:
        return [None, None]
    
    #cut this text
    a = a.replace('(via Flash)', '')
    b = b.replace('(via Flash)', '')
    
    #tokenize
    a = a.split(', ')
    b = b.split(', ')
    
    #remove spaces
    for font in a:
        font = font.strip()
    for font in b:
        font = font.strip()
    
    #remove if in both lists
    for font in a:
        if font in b:
             a.remove(font)
             b.remove(font)
             
    #a are the ones removed
    #b are the ones added
    print a
    print b
    print len(a)
    print len(b)
    return [len(a),len(b)]