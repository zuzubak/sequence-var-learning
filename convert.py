import index
conv='./conv.csv'

def c(filepath,bird_number):
    l=index.get_data_list(conv)
    print(l)
    strings_list=index.get_data_list(filepath)
    converted_strings=[]
    for string in strings_list:
        converted_string=''
        for char in string:
            new_char='['+char+']'
            for sublist in l:
                if sublist[bird_number]==char:
                    new_char=sublist[0]
            converted_string=converted_string+new_char
        converted_strings.append(converted_string)
    return converted_strings