def compare(idct1, idct2):
    odct = {}
    for key, value in idct1.items():
        if key in idct2:
            odct[key] = (idct1[key], idct2[key])
    for key, value in idct2.items():
        if key in idct1 and key not in odct:
            odct[key] = (idct1[key], idct2[key])
    return odct
