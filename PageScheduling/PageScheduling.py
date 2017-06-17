'''
	Operating System - Page Scheduling v1.1
	-> PageScheduling.py
    - Method.py

	Created by ShauShian, Chiang on 2017/06/17.
	Copyright @ 2017 ShauShian, Chiang. All rights reserved.
'''

from Method import *

def main():
    pageframe = 0
    page_ls = []
    n = input('Enter the input filename:')

    with open(n) as file:
        pageframe = int(file.readline())
        page_ls = list(file.read())
        page_ls.pop() # Remove the '\n'.

    buffer = '' # A buffer to wait for writing.
    f = FCFO(pageframe, page_ls)
    l = LRU(pageframe, page_ls)
    a = ARB(pageframe, page_ls)
    s = SCP(pageframe, page_ls)
    u = LFU(pageframe, page_ls)
    m = MLFU(pageframe, page_ls)
    
    f.start()
    buffer += f.print_status()

    l.start()
    buffer += l.print_status()

    a.start()
    buffer += a.print_status()

    s.start()
    buffer += s.print_status()

    u.start()
    buffer += u.print_status()

    m.start()
    buffer += m.print_status()

    num = [ x for x in n if x in '0123456789' ]
    
    with open('output' + num[0] + '.txt', 'w') as writeF:
        writeF.write(buffer)

if __name__ == '__main__':
    main()
