from itertools import count
import random
from re import I
from tkinter import X
Option=['father','green','aeroplane','break','cartoon']
Option2=['angry','brain','child','equal','horse']
def game(x):
    count=0
    count1=0
    for e in range(1):
      for i in x:
           print('Arrange the letters to form a valid word ----->')
           print(''.join(random.sample(i,len(i))))
           a=input("")
           if a==i:
                print()
                print('Correct')
                count+=1
           else:
                print()
                print('wrong')
                count1+=1
    print('Net Score is',count-count1)

print('************ Woard Puzzle Game ************')
game(Option)
a=input('You Want to play Again----(yes/no)')
if a=='yes':
    game(Option2)
else:
    print("Thank you 🙂🙂")














