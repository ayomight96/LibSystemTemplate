# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 11:14:49 2023

@author: ayotunde
"""
from libaryData import LibaryData
from account import Account
from user import Student


class LibManSystem:
    def __init__(self):
        LibaryData.loadBooks()
        LibManSystem.login()

    @staticmethod
    def authenticate(uid, password):
        if uid == "Stish" and password == "abc":
            return True
        return False

    @staticmethod
    def verifyUserDetails(userName, fullName, password, confirmPassword):
        if userName and fullName and password and confirmPassword != "" and password == confirmPassword:
            return True
        return False

    @staticmethod
    def login():

        while True:
            print("Welcome...")

            uid = input("User id: ")
            password = input("input password: ")
            if LibManSystem.authenticate(uid, password):
                print("All good")
                a = Account.load_account("student888")
                u = Student(a.f_name, "Sarna", 'CEBE', a)
                u.menu()
                print("back to login")
            else:
                print("Login failure..")

    @staticmethod
    def landing():
        print(f"""Welcome to the Library Management System Landing Page
1. Option 1 ~Sign Up
2. Option 2 ~Sign In
q. Return

""")
        while True:
            print("Welcome...")

            c = input("\nSelect Option (1-4|q): ")
            choice = {"1": LibManSystem.signUp,
                      "2": LibManSystem.login,
                      "q": "q"}.get(c, "invalid")
            if choice == "q":
                print('Bye..')
                break
            elif choice != "invalid":
                choice()
            else:
                print("Try again...")

    @staticmethod
    def signUp():
        while True:
            userName = input("Enter User Name : ")
            fullName = input("Enter Full Name: ")
            password = input("Enter password: ")
            confirmPassword = input("Confirm password: ")
            if LibManSystem.verifyUserDetails(
                userName,
                fullName,
                password,
                confirmPassword
            ):
                print("All good")
                a = Account.load_account("student888")
                u = Student(a.f_name, "Sarna", 'CEBE', a)
                u.menu()
                print("back to login")
            else:
                print("Login failure..")


s = LibManSystem()
