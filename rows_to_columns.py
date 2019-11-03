def rtc(matrix):
    out_dict = {}
    for i in range(len(matrix[0])):
        out_dict[i] = []
    for row in matrix:
        i = 0
        for item in row:
            out_dict[i].append(item)
            i += 1
    return out_dict
