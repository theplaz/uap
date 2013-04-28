def fontscompare(a, b):
    
    if a is None:
        a = ''
    if b is None:
        b = ''
    
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
        
    print a
    print b
    
    #remove if in both lists
    for font in a:
        if font in b:
             a.remove(font)
             b.remove(font)
             
    #if '' is included, remove it
    if '' in a:
        a.remove('')
    if '' in b:
        b.remove('')
             
    #a are the ones removed
    #b are the ones added
    print a
    print b
    print len(a)
    print len(b)
    return [len(a),len(b)]