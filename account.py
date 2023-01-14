# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 11:19:56 2023

@author: ayotunde
"""

class Account:
    def __init__(self,a_id, password, f_name,l_books_borrowed=[],l_books_reserved=[],
                 history_return=None,l_lost_Books = None, acc_fine=None):
        self.a_id=a_id
        self.password = password
        self.f_name = f_name
        self.l_books_borrowed=l_books_borrowed
        self.l_books_reserved=l_books_reserved
        self.history_return = history_return
        self.l_lost_Books = l_lost_Books
        self.acc_fine = acc_fine
    
    @classmethod
    def load_account(cls, a_id):
        with open("accounts.json") as fd:
            acc = json.load(fd)
            return Account(acc[a_id]["id"],
                           acc[a_id]["password"], 
                           acc[a_id]["f_name"], 
                           acc[a_id]["l_books_borrowed"], 
                           acc[a_id]["l_books_reserved"],
                           acc[a_id]["l_return_books"],
                           acc[a_id]['l_lost_books'],
                           acc[a_id]["acc_fine"]
                            )
        
    def cal_fine(self):
        pass
    def __repr__(self):
        return f"""{'*'*20}
id: {self.a_id}
books_borrowed: {self.l_books_borrowed}
    """