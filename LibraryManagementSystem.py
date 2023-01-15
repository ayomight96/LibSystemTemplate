# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 11:14:49 2023

@author: ayotunde
"""
from LibraryData import LibraryData
from Account import Account
from StudentUser import StudentUser
from DatabaseConnection import DatabaseConnection


class LibraryManagementSystem:
    def __init__(self):
        LibraryData.loadBooks()
        LibraryManagementSystem.landing()

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
            userData = LibraryManagementSystem.authenticate(userName, password)
            if userData != False:
                accountData = Account.accountDataFromDatabase(userData)
                student = StudentUser(
                    accountData['fullName'],
                    accountData['school'],
                    accountData['department'],
                    accountData
                )
                student.menu()
            else:
                print("Login failure..")
                LibraryManagementSystem.landing()

    @staticmethod
    def landing():
        print(f"""\n\nWelcome to the Library Management System Landing Page
1. Option 1 ~Sign Up
2. Option 2 ~Log In
q. Return\n

""")
        while True:
            c = input("\nSelect Option (1-2|q): ")
            choice = {"1": LibraryManagementSystem.signUp,
                      "2": LibraryManagementSystem.login,
                      "q": "q\n"}.get(c, "invalid")
            if choice == "q":
                print('Bye..\n')
                break
            elif choice != "invalid\n":
                choice()
            else:
                print("Try again...\n")

    @staticmethod
    def signUp():
        while True:
            userTypeInput = input(
                "Enter 1 if you are a Staff and 2 if you are a Student: ")
            if userTypeInput == '':
                print("You have made an invalid entry, please try again.")
                LibraryManagementSystem.signUp()
            else:
                userTypeInput = int(userTypeInput)
                if userTypeInput == 1:
                    userType = 'Staff'
                elif userTypeInput == 2:
                    userType = 'Student'
                else:
                    print("You have made an invalid entry, please try again.\n")
                    LibraryManagementSystem.signUp()
            userName = input("Enter User Name: ")
            fullName = input("Enter Full Name: ")
            school = input("Enter School: ")
            department = input("Enter Department: ")
            password = input("Enter password: ")
            confirmPassword = input("Confirm password: ")
            if LibraryManagementSystem.verifyUserDetails(
                userName,
                fullName,
                password,
                confirmPassword,
                school,
                department
            ) and LibraryManagementSystem.isUserNotDuplicated(
                userName,
                fullName,
                password
            ):
                print("You have succesfully signed up, you can now login\n")
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
                LibraryManagementSystem.landing()
            else:
                print("Sign up failure..")
                LibraryManagementSystem.landing()


s = LibraryManagementSystem()
