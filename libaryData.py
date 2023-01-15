#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 19:11:18 2022

@author: Stish
"""

# class LibManSystem:
#     def __init__(self):
#         LibaryData.loadBooks()
#         LibManSystem.login()
#     @staticmethod
#     def authenticate(uid,password):
#         if uid == "Stish" and password=="abc":
#             return True
#         return False
#     @staticmethod
#     def login():

#         while True:
#             print("Welcome...")

#             uid = input("User id: ")
#             password = input("input password: ")
#             if LibManSystem.authenticate(uid,password):
#                 print("All good")
#                 a = Account.load_account("student888")
#                 u = Student(a.f_name,"Sarna",'CEBE',a)
#                 u.menu()
#                 print("back to login")
#             else:
#                 print("Login failure..")
import re
from DatabaseConnection import DatabaseConnection
import json


class LibaryData:
    def __init__(self):
        pass

    @classmethod
    def loadBooks(cls):
        DatabaseConnection()
        with open('book2.json') as fd:
            books = json.load(fd)
            for b in books:
                book = Book(
                    b['bookID'],
                    b['title'],
                    b['authors'],
                    b['average_rating'],
                    b['isbn'],
                    b['isbn13'],
                    b['language_code'],
                    b['num_pages'],
                    b['ratings_count'],
                    b['text_reviews_count'],
                    b['publication_date'],
                    b['publisher'],
                )
                bookData = DatabaseConnection.retrieve(
                    'Book',
                    {
                        'id': book.data()['id'],
                        'title': book.data()['title'],
                        'authors': book.data()['authors'],
                    }
                )
                if bookData == False:
                    DatabaseConnection.insert(
                        'Book',
                        book.data()
                    )


class User:
    def __init__(self, f, s, a=None):
        self.f = f
        self.s = s
        self.account = a

    def __rpr__(self):
        return f"""{self.f} {self.s}, 
{self.a}
"""


class Student(User):
    bookLimit = 3

    def __init__(self, f, s, dept, acc=None):
        super().__init__(f, s, acc)
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
            choice = {"1": self.f_opt1,
                      "2": self.f_opt2,
                      "3": self.f_opt3,
                      "4": self.f_opt4,
                      "q": "q"}.get(c, "invalid")
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

# class Account:
#     def __init__(self,a_id, password, f_name,l_books_borrowed=[],l_books_reserved=[],
#                  history_return=None,l_lost_Books = None, acc_fine=None):
#         self.a_id=a_id
#         self.password = password
#         self.f_name = f_name
#         self.l_books_borrowed=l_books_borrowed
#         self.l_books_reserved=l_books_reserved
#         self.history_return = history_return
#         self.l_lost_Books = l_lost_Books
#         self.acc_fine = acc_fine

#     @classmethod
#     def load_account(cls, a_id):
#         with open("accounts.json") as fd:
#             acc = json.load(fd)
#             return Account(acc[a_id]["id"],
#                            acc[a_id]["password"],
#                            acc[a_id]["f_name"],
#                            acc[a_id]["l_books_borrowed"],
#                            acc[a_id]["l_books_reserved"],
#                            acc[a_id]["l_return_books"],
#                            acc[a_id]['l_lost_books'],
#                            acc[a_id]["acc_fine"]
#                             )

#     def cal_fine(self):
#         pass
#     def __repr__(self):
#         return f"""{'*'*20}
# id: {self.a_id}
# books_borrowed: {self.l_books_borrowed}
#     """


class Book:
    def __init__(
        self,
        id,
        title,
        authors,
        averageRating,
        isbn,
        isbn13,
        languageCode,
        numberOfPages,
        ratingsCount,
        textReviewsCount,
        publicationDate,
        publisher
    ):
        self.id = id
        self.title = title
        self.authors = authors
        self.averageRating = averageRating
        self.isbn = isbn
        self.isbn13 = isbn13
        self.languageCode = languageCode
        self.numberOfPages = numberOfPages
        self.ratingsCount = ratingsCount
        self.textReviewsCount = textReviewsCount
        self.publicationDate = publicationDate
        self.publisher = publisher

    def data(self):
        return {
            'id': self.id,
            'title': self.title,
            'authors': self.authors,
            'averageRating': self.averageRating,
            'isbn': self.isbn,
            'isbn13': self.isbn13,
            'languageCode': self.languageCode,
            'numberOfPages': self.numberOfPages,
            'ratingsCount': self.ratingsCount,
            'textReviewsCount': self.textReviewsCount,
            'publicationDate': self.publicationDate,
            'publisher': self.publisher
        }

    @staticmethod
    def bookDataFromDatabase(data):
        return {
            'id': data[0][0],
            'title': data[0][1],
            'author': data[0][2],
            'averageRating': data[0][3],
            'isbn': data[0][4],
            'languageCode': data[0][5],
            'numberOfPages': data[0][6],
            'ratingsCount': data[0][7],
            'textReviewsCount': data[0][8],
            'publicationDate': data[0][9],
            'publisher': data[0][10],
        }

    @staticmethod
    def bookDataFromDatabase2(data):
        return {
            'id': data[0],
            'title': data[1],
            'author': data[2],
            'averageRating': data[3],
            'isbn': data[4],
            'languageCode': data[5],
            'numberOfPages': data[6],
            'ratingsCount': data[7],
            'textReviewsCount': data[8],
            'publicationDate': data[9],
            'publisher': data[10],
        }
