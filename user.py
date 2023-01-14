# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 11:19:16 2023

@author: ayotunde
"""

class User :
    def __init__(self,f,s,a=None):
        self.f = f
        self.s = s
        self.account = a
    def __rpr__(self):
        return f"""{self.f} {self.s}, 
{self.a}
"""

class Student(User): 
    b_limit = 3
    def __init__(self,f,s,dept,acc=None):
        super().__init__(f,s,acc)
        self.d = dept

    def menu(self):
        print(f"""menu for Student
1. Option 1
2. Option 2
3. Option 3 ~Add book
4. Option 4 ~User record
q. Return

""")
        while True:
            c = input("\nSelect Option (1-4|q): ")
            choice = {"1" :self.f_opt1,
                  "2" :self.f_opt2,
                  "3" :self.f_opt3,
                  "4" :self.f_opt4,
                  "q" :"q"}.get(c,"invalid")        
            if choice == "q":
                print('Bye..')
                break
            elif choice != "invalid":
                choice()
            else:
                print("Try again...")

    def f_opt1(self):
        print("option-1")
    def f_opt2(self):
        print("option-2")
    def f_opt3(self):
        print("option-3~")
        # check if the book is availble
        self.account.l_books_borrowed.append(439682584)
        # update file
    def f_opt4(self):
        # print current status
        print(self)
    def f_ex(self):
        return
    def __repr__(self):
        return f"{self.f}\n {self.account}"
    
class Staff:
    pass

class Libarian:
    pass