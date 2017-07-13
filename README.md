# Page-Scheduling(Management)
Simulate six types of page managemnet such as LRU, FIFO.
## What is it ?
In this project, I'm going to demostrate the six different page management methods.
### Six methods down below:
- First In First Out
- Least Recently Usage
- Additional Reference Bits
- Second chance Page
- Least Frequently Used Page Replacement
- Most Frequently Used Page Replacement
## Example
### Input1.txt
```
3
123412512345
```
The integer on the very top-left is the method of scheduling we are going to do.
- The first integer at the top left cornor means the number of the page frames.
- The second digit string means the sequence of the incoming pages, from left to right.
### Output1.txt
```
----------------------------FIFO----------------------------
1       1              F
2       21             F
3       321            F
4       432            F
1       143            F
2       214            F
5       521            F
1       521            
2       521            
3       352            F
4       435            F
5       435            
Page Fault = 9  Page Replaces = 6  Page Frames = 3

----------------------------LRU-----------------------------
1       1              F
2       21             F
3       321            F
4       432            F
1       143            F
2       214            F
5       521            F
1       152            
2       215            
3       321            F
4       432            F
5       543            F
Page Fault = 10  Page Replaces = 7  Page Frames = 3

-----------------Additional Reference Bits------------------
1       1              F
2       12             F
3       123            F
4       423            F
1       413            F
2       412            F
5       512            F
1       512            
2       512            
3       312            F
4       342            F
5       345            F
Page Fault = 10  Page Replaces = 7  Page Frames = 3

---------------------Second chance Page---------------------
1       1              F
2       21             F
3       321            F
4       432            F
1       143            F
2       214            F
5       521            F
1       521            
2       521            
3       352            F
4       435            F
5       435            
Page Fault = 9  Page Replaces = 6  Page Frames = 3

-----------Least Frequently Used Page Replacement-----------
1       1              F
2       21             F
3       321            F
4       432            F
1       143            F
2       214            F
5       521            F
1       152            
2       215            
3       321            F
4       421            F
5       521            F
Page Fault = 10  Page Replaces = 7  Page Frames = 3

-----------Most Frequently Used Page Replacement------------
1       1              F
2       21             F
3       321            F
4       432            F
1       143            F
2       214            F
5       521            F
1       152            
2       215            
3       325            F
4       435            F
5       543            
Page Fault = 9  Page Replaces = 6  Page Frames = 3
```
- Attribute on the left represents the page number.
- Attribute in the middle represents the pages in the memory.(No particular order)
- Attribute on the right represents that if the page gets page fault.
- The total count of page fault, page replacement, page frames are on the last row.
