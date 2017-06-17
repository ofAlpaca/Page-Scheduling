'''
	Operating System - Page Scheduling v1.1
	- PageScheduling.py
    -> Method.py

	Created by ShauShian, Chiang on 2017/06/17.
	Copyright @ 2017 ShauShian, Chiang. All rights reserved.
'''

import queue

class FCFO:
    def __init__(self, _frame, _page_list):
        self.frame_size = _frame
        self.mem = []
        self.list = queue.Queue(len(_page_list))
        for p in _page_list:
            self.list.put(p)
        self.fault = 0
        self.replace = 0
        self.print_buf = '{:-^60}\n'.format('FIFO')

    def is_page_fault(self, _p):
        return not _p in self.mem
        
    def page_fault_confirm(self, _p): # When page fault happened.
        self.fault += 1

        if len(self.mem) == self.frame_size:
            self.mem.remove(self.mem[0]) # Dequeue the first page to mem.
            self.replace += 1

        self.mem.append(_p) # Enqueue the new page to mem.

    def start(self):
        fault = False
        while self.list.qsize() > 0:
            next_page = self.list.get()

            self.print_buf += '{:<8}'.format(next_page) # Add the next page to the print buffer.

            if self.is_page_fault(next_page): # Next page is not in the memory.
                self.page_fault_confirm(next_page) # Only page fault or replacement as well.
                fault = True # Raise the page fault flag up.

            str = ''
            for i in reversed(self.mem):
                str += i
            self.print_buf += '{:<15}'.format(str)
            if fault:
                self.print_buf += 'F'
                fault = False
            self.print_buf += '\n'
        self.print_buf += 'Page Fault = {0}  Page Replaces = {1}  Page Frames = {2}\n\n'.format(self.fault, self.replace, self.frame_size)

    def print_status(self):
        print(self.print_buf)
        return self.print_buf
            
#--------------------------------------------------------------------------------

class LRU:
    def __init__(self, _frame, _page_list):
        self.frame_size = _frame
        self.mem = {}
        self.time = 0
        self.list = queue.Queue(len(_page_list))
        for p in _page_list:
            self.list.put(p)
        self.fault = 0
        self.replace = 0
        self.print_buf = '{:-^60}\n'.format('LRU')

    def is_page_fault(self, _p):
        return not _p in self.mem

    def page_fault_confirm(self, _p):
        self.fault += 1
        minpage = ''
        mintime = -1

        if len(self.mem) == self.frame_size: # It is full in mem.
            for page, timestamp in self.mem.items(): # Find the least recently using page.
                if mintime == -1 or timestamp < mintime:
                    minpage = page
                    mintime = timestamp
            del self.mem[minpage] # Remove the LRU page.
            self.replace += 1

        self.mem[_p] = self.time # Append the new page key and time stamp into mem.

    def start(self):
        fault = False
        while self.list.qsize() > 0:
            next_page = self.list.get()
            self.print_buf += '{:<8}'.format(next_page) # Add the next page to the print buffer.

            if self.is_page_fault(next_page): # Page is not in mem.
                self.page_fault_confirm(next_page)
                fault = True
            else: # If the page exist, updating the timestamp.
                self.mem[next_page] = self.time

            str = ''
            for i in sorted(self.mem.items(), key = lambda x : x[1])[::-1]:
                str += i[0]
            self.print_buf += '{:<15}'.format(str)
            if fault:
                self.print_buf += 'F'
                fault = False
            self.print_buf += '\n'

            self.time += 1 # Move to next clock.
        self.print_buf += 'Page Fault = {0}  Page Replaces = {1}  Page Frames = {2}\n\n'.format(self.fault, self.replace, self.frame_size)

    def print_status(self):
        print(self.print_buf)
        return self.print_buf

#--------------------------------------------------------------------------------

class RefBit:
    def __init__(self):
        self.page = ''
        self.shift_register = '00000000'

    def shift_right(self, _bit):
        self.shift_register = _bit + self.shift_register[0:7]

    def bin2dec(self):
        dec = 0
        n = 7
        for b in self.shift_register :
           dec += int(b) * (2**n)
           n -= 1
        return dec
        

class ARB: # Additional Reference Bits Page Replacement.
    def __init__(self, _frame, _page_list):
        self.frame_size = _frame
        self.mem = []
        for r in range(0,self.frame_size):
            newRef = RefBit()
            self.mem.append(newRef)

        self.list = queue.Queue(len(_page_list))
        for p in _page_list:
            self.list.put(p)
        self.refbits = ['0'] * self.frame_size
        self.fault = 0
        self.replace = 0
        self.print_buf = '{:-^60}\n'.format('Additional Reference Bits')

    def is_page_fault(self, _p):
        for m in self.mem:
            if m.page == _p:
                return False
        return True

    def is_memory_full(self):
        for m in self.mem:
            if m.page == '':
                return False
        return True

    def index_of_page(self, _p):
        for m in range(0,self.frame_size):
            if self.mem[m].page == _p:
                return m
        return None

    def update_refbits(self):
        for i in range(0, self.frame_size):
            self.mem[i].shift_right( self.refbits[i] )
            self.refbits[i] = '0'

    def page_fault_confirm(self, _p):
        self.fault += 1
        minref = -1
        for empty in range(0, self.frame_size): # Find the page which is empty as initial value.
            if self.mem[empty].page == '':
                minpage_index = empty
                break

        if self.is_memory_full(): # It is full in mem.
            for p in range(0, self.frame_size): # Find the least reference bit page.
                if minref == -1 or self.mem[p].bin2dec() < minref:
                    minpage_index = p
                    minref = self.mem[p].bin2dec()

            self.mem[minpage_index].page = '' # Remove the page.
            self.replace += 1

        self.mem[minpage_index].page = _p # Append the new page.
        self.mem[minpage_index].shift_register = '00000000' # A new page register.

    def start(self):
        fault = False
        while self.list.qsize() > 0:
            next_page = self.list.get()
            self.print_buf += '{:<8}'.format(next_page) # Add the next page to the print buffer.

            if self.is_page_fault(next_page): # Page is not in mem.
                self.page_fault_confirm(next_page) # Do page fault only or page replacement.
                fault = True

            # Updating the refernece bit.
            self.refbits[self.index_of_page(next_page)] = '1' # Find the index of the next page.
            self.update_refbits() # Make reference bit shift into shift register. 

            str = ''
            for i in self.mem:
                str += i.page
            self.print_buf += '{:<15}'.format(str)
            if fault:
                self.print_buf += 'F'
                fault = False
            self.print_buf += '\n'

        self.print_buf += 'Page Fault = {0}  Page Replaces = {1}  Page Frames = {2}\n\n'.format(self.fault, self.replace, self.frame_size)

    def print_status(self):
        print(self.print_buf)
        return self.print_buf

#--------------------------------------------------------------------------------

class ClockPage:
     def __init__(self, _p):
         self.page = _p
         self.refbit = 0

class SCP: # Second Chance Page Replacement.
    def __init__(self, _frame, _pagelist):
        self.frame_size = _frame
        self.mem = []
        self.list = queue.Queue(len(_pagelist))
        for p in _pagelist:
            self.list.put(p)
        self.fault = 0
        self.replace = 0
        self.print_buf = '{:-^60}\n'.format('Second chance Page')

    def is_page_fault(self, _p):
        for i in self.mem:
            if _p == i.page:
                return False
        return True

    def index_of_page(self, _p):
        for i in range(0, self.frame_size):
            if self.mem[i].page == _p:
                return i

    def page_fault_confirm(self, _p):
        self.fault += 1
        newPage = ClockPage(_p)

        if len(self.mem) == self.frame_size: # It is full.
            while self.mem[0].refbit == 1: # Reference bit is 1, change it to 0 and updating the timestap.
               tmp = self.mem.pop(0)
               tmp.refbit = 0 # Give it second chance.
               self.mem.append(tmp) # Add it to the rear.

            self.mem.pop(0) # Remove the front page.
            self.replace += 1

        newPage.refbit = 1 # First time access.
        self.mem.append(newPage) # Add new page to the rear.

    def start(self):
        fault = False
        while self.list.qsize() > 0:
            next_page = self.list.get()
            self.print_buf += '{:<8}'.format(next_page) # Add the next page to the print buffer.

            if self.is_page_fault(next_page): # Is there a page fault.
                self.page_fault_confirm(next_page)
                fault = True
            else: # No page fault.
                self.mem[self.index_of_page(next_page)].refbit = 1 # Being reference, so change refbit to 1.

            str = ''
            for i in self.mem[::-1]:
                str += i.page
            self.print_buf += '{:<15}'.format(str)
            if fault:
                self.print_buf += 'F'
                fault = False
            self.print_buf += '\n'

        self.print_buf += 'Page Fault = {0}  Page Replaces = {1}  Page Frames = {2}\n\n'.format(self.fault, self.replace, self.frame_size)

    def print_status(self):
        print(self.print_buf)
        return self.print_buf

#--------------------------------------------------------------------------------

class CounterPage:
     def __init__(self, _p):
         self.page = _p
         self.counter = 0

class LFU: # Least Frequently Used Page Replacement.
    def __init__(self, _frame, _pagelist):
        self.frame_size = _frame
        self.mem = []
        self.list = queue.Queue(len(_pagelist))
        for p in _pagelist:
            self.list.put(p)
        self.fault = 0
        self.replace = 0
        self.print_buf = '{:-^60}\n'.format('Least Frequently Used Page Replacement')

    def is_page_fault(self, _p):
        for i in self.mem:
            if _p == i.page:
                return False
        return True

    def index_of_page(self, _p):
        for i in range(0, self.frame_size):
            if self.mem[i].page == _p:
                return i

    def find_min_page(self):
        min_counter = 0
        min_index = -1
        for i in range(0, self.frame_size):
            if min_index == -1 or min_counter > self.mem[i].counter:
                min_counter = self.mem[i].counter
                min_index  = i

        return min_index


    def page_fault_confirm(self, _p):
        self.fault += 1
        newPage = CounterPage(_p)

        if len(self.mem) == self.frame_size: # It is full.
            index = self.find_min_page()
            self.mem.pop(index) # Remove the min counter page.
            self.replace += 1

        self.mem.append(newPage) # Add new page to the rear.

    def start(self):
        fault = False
        while self.list.qsize() > 0:
            next_page = self.list.get()
            self.print_buf += '{:<8}'.format(next_page) # Add the next page to the print buffer.

            if self.is_page_fault(next_page): # Is there a page fault.
                self.page_fault_confirm(next_page)
                fault = True
            else: # No page fault.
                tmp = self.mem.pop(self.index_of_page(next_page))
                tmp.counter += 1 # Being reference, so add 1 to counter.
                self.mem.append(tmp) # After adding, move it to rear.

            str = ''
            for i in self.mem[::-1]:
                str += i.page
            self.print_buf += '{:<15}'.format(str)
            if fault:
                self.print_buf += 'F'
                fault = False
            self.print_buf += '\n'

        self.print_buf += 'Page Fault = {0}  Page Replaces = {1}  Page Frames = {2}\n\n'.format(self.fault, self.replace, self.frame_size)

    def print_status(self):
        print(self.print_buf)
        return self.print_buf

#--------------------------------------------------------------------------------

class MLFU: # Most Frequently Used Page Replacement.
    def __init__(self, _frame, _pagelist):
        self.frame_size = _frame
        self.mem = []
        self.list = queue.Queue(len(_pagelist))
        for p in _pagelist:
            self.list.put(p)
        self.fault = 0
        self.replace = 0
        self.print_buf = '{:-^60}\n'.format('Most Frequently Used Page Replacement')

    def is_page_fault(self, _p):
        for i in self.mem:
            if _p == i.page:
                return False
        return True

    def index_of_page(self, _p):
        for i in range(0, self.frame_size):
            if self.mem[i].page == _p:
                return i

    def find_max_page(self):
        max_counter = 0
        max_index = -1
        for i in range(0, self.frame_size):
            if max_index == -1 or max_counter < self.mem[i].counter:
                max_counter = self.mem[i].counter
                max_index  = i

        return max_index


    def page_fault_confirm(self, _p):
        self.fault += 1
        newPage = CounterPage(_p)

        if len(self.mem) == self.frame_size: # It is full.
            index = self.find_max_page()
            self.mem.pop(index) # Remove the min counter page.
            self.replace += 1

        self.mem.append(newPage) # Add new page to the rear.

    def start(self):
        fault = False
        while self.list.qsize() > 0:
            next_page = self.list.get()
            self.print_buf += '{:<8}'.format(next_page) # Add the next page to the print buffer.

            if self.is_page_fault(next_page): # Is there a page fault.
                self.page_fault_confirm(next_page)
                fault = True
            else: # No page fault.
                tmp = self.mem.pop(self.index_of_page(next_page))
                tmp.counter += 1 # Being reference, so add 1 to counter.
                self.mem.append(tmp) # After adding, move it to rear.

            str = ''
            for i in self.mem[::-1]:
                str += i.page
            self.print_buf += '{:<15}'.format(str)
            if fault:
                self.print_buf += 'F'
                fault = False
            self.print_buf += '\n'

        self.print_buf += 'Page Fault = {0}  Page Replaces = {1}  Page Frames = {2}\n\n'.format(self.fault, self.replace, self.frame_size)

    def print_status(self):
        print(self.print_buf)
        return self.print_buf