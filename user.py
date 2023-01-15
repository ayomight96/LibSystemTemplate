# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 11:19:16 2023

@author: ayotunde
"""
from DatabaseConnection import DatabaseConnection
from libaryData import Book
from account import Account


class User:
    def __init__(
            self,
            fullName,
            school,
            account=None):
        self.fullName = fullName
        self.school = school
        self.account = account

    def __rpr__(self):
        return f"""{self.fullName} {self.school},
{self.account}
"""


class Student(User):
    bookLimit = 3
    totalBooksAdded = 0

    def __init__(
            self,
            fullName,
            school,
            department,
            account=None):
        super().__init__(fullName, school, account)
        self.department = department
        if account['booksBorrowed'] is not None:
            booksBorrowed = account['booksBorrowed'].split(',')
            self.totalBooksAdded = len(booksBorrowed)

    def menu(self):
        print(f"""Welcome to your Dashboard {self.fullName}
Menu
1. Option 1 ~Profile
2. Option 2 ~Pay Fine
3. Option 3 ~Add Book
3. Option 4 ~Reserve Book
q. Return

""")
        while True:
            c = input("\nSelect Option (1-3|q): ")
            choice = {"1": self.profile,
                      "2": self.payFine,
                      "3": self.addBook,
                      "4": self.reserveBook,
                      "q": "q"}.get(c, "invalid")
            if choice == "q":
                print('Bye..')
                break
            elif choice != "invalid":
                choice()
            else:
                print("Try again...")

    def profile(self):
        print(f"""PROFILE:\n
Full Name: {self.account['fullName']}\n
User Name: {self.account['fullName']}\n
User Type: {self.account['fullName']}\n
Books Borrowed: {self.totalBooksAdded}\n
Books Reserved: {self.account['booksReserved']}\n
Books Returned: {self.account['booksReturned']}\n
Books Lost: {self.account['booksLost']}\n
Books Fine: {self.account['fine']}
""")
        self.menu()

    def payFine(self):
        if self.account['fine'] == 0:
            print('You have no pending fine to pay')
            self.menu()
        print(f"Fine yet to be paid: {self.account['fine']}")
        payment = input(
            "Enter amount you would like to pay (please enter a number): ")
        if payment == '':
            print('You have entered an invalid amount')
            self.payFine()
        else:
            payment = int(payment)
            amountLeftToBePaid = self.account['fine'] - payment
            if amountLeftToBePaid > 0:
                print(
                    f'Payment was succesful, you have {amountLeftToBePaid} left to be paid')
                self.account['fine'] = amountLeftToBePaid
                DatabaseConnection.update(
                    'Account',
                    self.account['id'],
                    {
                        'fine': amountLeftToBePaid
                    }
                )
            elif amountLeftToBePaid == 0:
                print('Payment was succesful, you have no fine left to be paid')
                self.account['fine'] = amountLeftToBePaid
                DatabaseConnection.update(
                    'Account',
                    self.account['id'],
                    {
                        'fine': amountLeftToBePaid
                    }
                )
            elif amountLeftToBePaid < 0:
                print('Transaction unsuccesful, you have overpaid, kindly retry.')
                self.payFine()

    def addBook(self):
        if self.totalBooksAdded < self.bookLimit:
            while True:
                book = input(
                    "Enter the title of the book you would like to borrow: ")
                if book == '':
                    self.bookDoesNotExist()
                else:
                    booksData = DatabaseConnection.retrieveByTextSearch(
                        'Book',
                        'title',
                        book
                    )
                    if booksData != False:
                        print('''These are the book titles that match your entry,
                        \nif you see the one you are looking for amongst them kindly
                        \ncopy the full title and enter it below:
                        ''')
                        count = 1
                        for book in booksData:
                            book = Book.bookDataFromDatabase2(book)
                            print(f"{count}. {book['title']}")
                            count += 1
                        bookTitleChoice = input('copy and paste Title here: ')
                        if bookTitleChoice != '':
                            bookToBeAdded = Book.bookDataFromDatabase(
                                DatabaseConnection.retrieve(
                                    'Book',
                                    'title',
                                    bookTitleChoice
                                ))
                            if self.totalBooksAdded == 0:
                                if self.verifyIfBookHasBeenBorrowed(bookToBeAdded['id']):
                                    print(
                                        "This book has been borrowed by another User")
                                    self.menu()
                                else:
                                    DatabaseConnection.update(
                                        'Account',
                                        self.account['id'],
                                        {
                                            'booksBorrowed': str(bookToBeAdded['id'])
                                        }
                                    )
                                    self.enterBorrowedIntoDatabase(
                                        bookToBeAdded['id'])
                                    self.updateAccount()
                                    self.totalBooksAdded += 1
                                    self.menu()
                            else:
                                booksBorrowed = self.account['booksBorrowed'].split(
                                    ',')
                                num = 0
                                for item in booksBorrowed:
                                    booksBorrowed[num] = int(item)
                                    num += 1
                                if bookToBeAdded['id'] not in booksBorrowed:
                                    DatabaseConnection.update(
                                        'Account',
                                        self.account['id'],
                                        {
                                            'booksBorrowed': self.account['booksBorrowed'] + ',' + str(bookToBeAdded['id'])
                                        }
                                    )
                                    self.updateAccount()
                                    self.totalBooksAdded += 1
                                    self.menu()
                                else:
                                    print('This book has been borrowed by you')
                                    self.menu()
                    else:
                        self.bookDoesNotExist()
                        self.menu()
        else:
            print('You can not borrow any more books, you have exceeded your limits')
            self.menu()

    def reserveBook(self):
        while True:
            book = input(
                "Enter the title of the book you would like to reserve: ")
            if book == '':
                self.bookDoesNotExist()
            else:
                booksData = DatabaseConnection.retrieveByTextSearch(
                    'Book',
                    'title',
                    book
                )
                if booksData != False:
                    print('''These are the book titles that match your entry,
                        \nif you see the one you are looking for amongst them kindly
                        \ncopy the full title and enter it below:
                        ''')
                    count = 1
                    for book in booksData:
                        book = Book.bookDataFromDatabase2(book)
                        print(f"{count}. {book['title']}")
                        count += 1
                    bookTitleChoice = input('copy and paste Title here: ')
                    if bookTitleChoice != '':
                        bookToBeAdded = Book.bookDataFromDatabase(
                            DatabaseConnection.retrieve(
                                'Book',
                                'title',
                                bookTitleChoice
                            ))
                        if self.totalBooksAdded == 0:
                            if self.verifyIfBookHasBeenBorrowed(bookToBeAdded['id']):
                                print("This book has been reserved by another User")
                                self.menu()
                            else:
                                DatabaseConnection.update(
                                    'Account',
                                    self.account['id'],
                                    {
                                        'booksBorrowed': str(bookToBeAdded['id'])
                                    }
                                )
                                self.enterReservedIntoDatabase(
                                    bookToBeAdded['id'])
                                self.updateAccount()
                                self.totalBooksAdded += 1
                                self.menu()
                        else:
                            booksBorrowed = self.account['booksBorrowed'].split(
                                ',')
                            num = 0
                            for item in booksBorrowed:
                                booksBorrowed[num] = int(item)
                                num += 1
                            if bookToBeAdded['id'] not in booksBorrowed:
                                DatabaseConnection.update(
                                    'Account',
                                    self.account['id'],
                                    {
                                        'booksBorrowed': self.account['booksBorrowed'] + ',' + str(bookToBeAdded['id'])
                                    }
                                )
                                self.updateAccount()
                                self.totalBooksAdded += 1
                                self.menu()
                            else:
                                print('This book has been borrowed by you')
                                self.menu()
                else:
                    self.bookDoesNotExist()
                    self.menu()

    def bookDoesNotExist(self):
        print(
            'This book does not exist in our database, kindly check the title and try again.')
        self.addBook()

    def verifyIfBookHasBeenBorrowed(self, id):
        if self.verifyIfBookHasBeenReserved(id):
            return True
        else:
            data = DatabaseConnection.retrieve('BorrowedBooks',
                                               'id',
                                               id
                                               )
            if data != False:
                return True
            else:
                return False

    def verifyIfBookHasBeenReserved(self, id):
        data = DatabaseConnection.retrieve('ReservedBooks',
                                           'id',
                                           id
                                           )
        if data != False:
            return True
        else:
            return False

    def enterReservedIntoDatabase(self, id):
        DatabaseConnection.insert(
            'ReservedBooks',
            {
                'id': id
            }
        )

    def enterBorrowedIntoDatabase(self, id):
        DatabaseConnection.insert(
            'BorrowedBooks',
            {
                'id': id
            }
        )

    def updateAccount(self):
        self.account = Account.accountDataFromDatabase(DatabaseConnection.retrieve(
            'Account', {
                'userName': self.account['userName'],
                'password': self.account['password']
            }
        )
        )


class Libarian:
    pass
