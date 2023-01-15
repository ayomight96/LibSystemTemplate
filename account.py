# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 11:19:56 2023

@author: ayotunde
"""

import uuid


class Account:
    def __init__(
        self,
        userName,
        fullName,
        password,
        userType,
        school,
        department,
        booksBorrowed=None,
        booksReserved=None,
        booksReturned=None,
        booksLost=None,
        fine=0
    ):
        self.userName = userName
        self.password = password
        self.fullName = fullName
        self.userType = userType
        self.school = school
        self.department = department
        self.id = uuid.uuid4()
        self.booksBorrowed = booksBorrowed
        self.booksReserved = booksReserved
        self.booksReturned = booksReturned
        self.booksLost = booksLost
        self.fine = fine

    def data(self):
        return {
            'id': str(self.id),
            'fullName': self.fullName,
            'userName': self.userName,
            'password': self.password,
            'userType': self.userType,
            'school': self.school,
            'department': self.department,
            'booksBorrowed': self.booksBorrowed,
            'booksReserved': self.booksReserved,
            'booksReturned': self.booksReturned,
            'booksLost': self.booksLost,
            'fine': self.fine
        }

    @staticmethod
    def accountDataFromDatabase(data):
        return {
            'id': data[0][0],
            'fullName': data[0][1],
            'userName': data[0][2],
            'password': data[0][3],
            'userType': data[0][4],
            'school': data[0][5],
            'department': data[0][6],
            'booksBorrowed': data[0][7],
            'booksReserved': data[0][8],
            'booksReturned': data[0][9],
            'booksLost': data[0][10],
            'fine': data[0][11],
        }
