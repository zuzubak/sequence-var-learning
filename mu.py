import random
def play(n):
    string='i'
    rnd=random.random()
    for i in range(n):
        for j in range(100):
            while string != 'u':
                string='i'
                if 0.75<rnd<1 and len(string)<10:
                    string=string+string
                    print(string)
                if 0<rnd<0.25:
                    if 'uu' in string:
                        string.replace('uu','')
                    print(string)
                if 0.25<rnd<0.5:
                    if string[-1]=='i':
                        string=string+'u'
                    print(string)
                if 0.5<rnd<0.75:
                    if 'iii' in string:
                        string.replace('iii','u')
                    print(string)
    print(string)