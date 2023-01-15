# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 11:14:49 2023

@author: ayotunde
"""
from libaryData import LibaryData
from account import Account
from user import Student
from DatabaseConnection import DatabaseConnection


class LibManSystem:
    def __init__(self):
        LibaryData.loadBooks()
        LibManSystem.landing()

    @staticmethod
    def authenticate(userName, password):
        userData = DatabaseConnection.retrieve('Account', {
            'userName': userName,
            'password': password
        }
        )
        if userData != False:
            return userData
        else:
            return False

    @staticmethod
    def verifyUserDetails(
            userName,
            fullName,
            password,
            confirmPassword,
            school,
            department):
        if userName and fullName and password and confirmPassword and school and department != "" and password == confirmPassword:
            return True
        return False

    @staticmethod
    def isUserNotDuplicated(userName, fullName, password):
        userData = DatabaseConnection.retrieve('Account', {
            'userName': userName,
            'fullName': fullName,
            'password': password
        }
        )
        if userData is not False:
            return False
        else:
            return True

    @staticmethod
    def login():
        while True:
            userName = input("input User Name: ")
            password = input("input password: ")
            userData = LibManSystem.authenticate(userName, password)
            if userData != False:
                accountData = Account.accountDataFromDatabase(userData)
                student = Student(
                    accountData['fullName'],
                    accountData['school'],
                    accountData['department'],
                    accountData
                )
                student.menu()
                print("back to login")
            else:
                print("Login failure..")
                LibManSystem.login()

    @staticmethod
    def landing():
        print(f"""Welcome to the Library Management System Landing Page
1. Option 1 ~Sign Up
2. Option 2 ~Log In
q. Return

""")
        while True:
            c = input("\nSelect Option (1-2|q): ")
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
            userTypeInput = input(
                "Enter 1 if you are a Staff and 2 if you are a Student: ")
            if userTypeInput == '':
                print("You have made an invalid entry, please try again.")
                LibManSystem.signUp()
            else:
                userTypeInput = int(userTypeInput)
                if userTypeInput == 1:
                    userType = 'Staff'
                elif userTypeInput == 2:
                    userType = 'Student'
                else:
                    print("You have made an invalid entry, please try again.")
                    LibManSystem.signUp()
            userName = input("Enter User Name: ")
            fullName = input("Enter Full Name: ")
            school = input("Enter School: ")
            department = input("Enter Department: ")
            password = input("Enter password: ")
            confirmPassword = input("Confirm password: ")
            if LibManSystem.verifyUserDetails(
                userName,
                fullName,
                password,
                confirmPassword,
                school,
                department
            ) and LibManSystem.isUserNotDuplicated(
                userName,
                fullName,
                password
            ):
                print("You have succesfully signed up, you can now login")
                account = Account(
                    userName,
                    fullName,
                    password,
                    userType, 
                    school,
                    department
                )
                DatabaseConnection.insert(
                    'Account',
                    account.data()
                )
                LibManSystem.landing()
            else:
                print("Sign up failure..")
                LibManSystem.landing()


s = LibManSystem()
