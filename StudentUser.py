from DatabaseConnection import DatabaseConnection
from Account import Account
from Book import Book
from User import User
from Fine import Fine


class StudentUser(User):
    bookLimit = 3
    totalBooksAdded = 0
    totalReservedBooks = 0
    totalReturnedBooks = 0

    def __init__(
            self,
            fullName,
            school,
            department,
            account=None
    ):
        super().__init__(fullName, school, account)
        self.department = department
        if account['borrowedBooks'] is not None:
            borrowedBooks = account['borrowedBooks'].split(',')
            self.totalBooksAdded = len(borrowedBooks)
        if account['reservedBooks'] is not None:
            reservedBooks = account['reservedBooks'].split(',')
            self.totalReservedBooks = len(reservedBooks)
        if account['returnedBooks'] is not None:
            returnedBooks = account['returnedBooks'].split(',')
            self.totalReturnedBooks = len(returnedBooks)

    def menu(self):
        print(f"""Welcome to your Dashboard {self.fullName}
Menu
1. Option 1 ~Profile
2. Option 2 ~Pay Fine
3. Option 3 ~Add Book
4. Option 4 ~Reserve Book
5. Option 5 ~View Borrowed Books
6. Option 6 ~Return Book
7. Option 7 ~View Returned Book
7. Option 8 ~View Reserved Book
q. Return

""")
        while True:
            c = input("\nSelect Option (1-5|q): ")
            choice = {"1": self.profile,
                      "2": self.payFine,
                      "3": self.addBook,
                      "4": self.reserveBook,
                      "5": self.viewBorrowedBooks,
                      "6": self.returnBook,
                      "7": self.viewReturnedBooks,
                      "8": self.viewReservedBooks,
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
User Name: {self.account['userName']}\n
User Type: {self.account['userType']}\n
Books Borrowed: {self.totalBooksAdded}\n
Books Reserved: {self.totalReservedBooks}\n
Books Returned: {self.totalReturnedBooks}\n
Books Lost: {self.account['lostBooks']}\n
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
            data = DatabaseConnection.retrieve(
                'Fine',
                'id',
                self.account['id']
            )
            if data != False:
                count = 1
                totalFineData = []
                for fine in data:
                    fineData = (Fine.fineDataFromDatabase(fine))
                    totalFineData.append(fineData)
                    print(f"""
                    Fine Payment Menu:

                    {count}. Fine for {fineData['bookTitle']} - ({fineData['fine']})
                    """
                          )
                    count += 1
                    print('q. Return')
                while True:
                    c = input(
                        f"\nSelect the fine you would like to pay (1-{count}|q): ")
                    if c == '':
                        print('you have made an invalid entry')
                        self.payFine()
                    elif c == "q":
                        self.menu()
                    elif c == str(1):
                        payment = input(
                            "Enter amount you would like to pay (please enter a number): ")
                        if payment == '':
                            print('You have entered an invalid amount')
                            self.payFine()
                        else:
                            payment = int(payment)
                            amountLeftToBePaid = fineData[0]['fine'] - payment
                            if amountLeftToBePaid > 0:
                                print(
                                    f'Payment was succesful, you have {amountLeftToBePaid} left to be paid')
                                self.account['fine'] = self.account['fine'] - payment
                                DatabaseConnection.update(
                                    'Account',
                                    self.account['id'],
                                    {
                                        'fine': self.account['fine']
                                    }
                                )
                                DatabaseConnection.update(
                                    'Fine',
                                    fineData[0]['bookId'],
                                    {
                                        'fine': amountLeftToBePaid,
                                        'fineStatus': 'partly paid'
                                    }
                                )
                            elif amountLeftToBePaid == 0:
                                print(
                                    'Payment was succesful, you have no fine left to be paid')
                                self.account['fine'] = self.account['fine'] - payment
                                DatabaseConnection.update(
                                    'Account',
                                    self.account['id'],
                                    {
                                        'fine': self.account['fine']
                                    }
                                )
                                DatabaseConnection.update(
                                    'Fine',
                                    fineData[0]['bookId'],
                                    {
                                        'fineStatus': 'paid'
                                    }
                                )
                            elif amountLeftToBePaid < 0:
                                print(
                                    'Transaction unsuccesful, you have overpaid, kindly retry.')
                                self.payFine()
                    elif c == str(2):
                        payment = input(
                            "Enter amount you would like to pay (please enter a number): ")
                        if payment == '':
                            print('You have entered an invalid amount')
                            self.payFine()
                        else:
                            payment = int(payment)
                            amountLeftToBePaid = fineData[1]['fine'] - payment
                            if amountLeftToBePaid > 0:
                                print(
                                    f'Payment was succesful, you have {amountLeftToBePaid} left to be paid')
                                self.account['fine'] = self.account['fine'] - payment
                                DatabaseConnection.update(
                                    'Account',
                                    self.account['id'],
                                    {
                                        'fine': self.account['fine']
                                    }
                                )
                                DatabaseConnection.update(
                                    'Fine',
                                    fineData[1]['bookId'],
                                    {
                                        'fine': amountLeftToBePaid,
                                        'fineStatus': 'partly paid'
                                    }
                                )
                            elif amountLeftToBePaid == 0:
                                print(
                                    'Payment was succesful, you have no fine left to be paid')
                                self.account['fine'] = self.account['fine'] - payment
                                DatabaseConnection.update(
                                    'Account',
                                    self.account['id'],
                                    {
                                        'fine': self.account['fine']
                                    }
                                )
                                DatabaseConnection.update(
                                    'Fine',
                                    fineData[1]['bookId'],
                                    {
                                        'fineStatus': 'paid'
                                    }
                                )
                            elif amountLeftToBePaid < 0:
                                print(
                                    'Transaction unsuccesful, you have overpaid, kindly retry.')
                                self.payFine()
                    elif c == str(3):
                        payment = input(
                            "Enter amount you would like to pay (please enter a number): ")
                        if payment == '':
                            print('You have entered an invalid amount')
                            self.payFine()
                        else:
                            payment = int(payment)
                            amountLeftToBePaid = fineData[2]['fine'] - payment
                            if amountLeftToBePaid > 0:
                                print(
                                    f'Payment was succesful, you have {amountLeftToBePaid} left to be paid')
                                self.account['fine'] = self.account['fine'] - payment
                                DatabaseConnection.update(
                                    'Account',
                                    self.account['id'],
                                    {
                                        'fine': self.account['fine']
                                    }
                                )
                                DatabaseConnection.update(
                                    'Fine',
                                    fineData[2]['bookId'],
                                    {
                                        'fine': amountLeftToBePaid,
                                        'fineStatus': 'partly paid'
                                    }
                                )
                            elif amountLeftToBePaid == 0:
                                print(
                                    'Payment was succesful, you have no fine left to be paid')
                                self.account['fine'] = self.account['fine'] - payment
                                DatabaseConnection.update(
                                    'Account',
                                    self.account['id'],
                                    {
                                        'fine': self.account['fine']
                                    }
                                )
                                DatabaseConnection.update(
                                    'Fine',
                                    fineData[2]['bookId'],
                                    {
                                        'fineStatus': 'paid'
                                    }
                                )
                            elif amountLeftToBePaid < 0:
                                print(
                                    'Transaction unsuccesful, you have overpaid, kindly retry.')
                                self.payFine()
                    else:
                        print('you have made an invalid entry')
                        self.payFine()
            else:
                print('You currently have no borrowed Books')
                self.menu()
            DatabaseConnection.update(
                'Fine',

            )

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
                                            'borrowedBooks': str(bookToBeAdded['id'])
                                        }
                                    )
                                    self.enterBorrowedIntoDatabase(
                                        bookToBeAdded['id'],
                                        bookToBeAdded['title'],
                                        self.account['id'],
                                    )
                                    self.updateAccount()
                                    self.totalBooksAdded += 1
                                    print(
                                        f"You have succesfully borrowed the book: {bookToBeAdded['title']}")
                                    self.menu()
                            else:
                                borrowedBooks = self.account['borrowedBooks'].split(
                                    ',')
                                num = 0
                                for item in borrowedBooks:
                                    borrowedBooks[num] = int(item)
                                    num += 1
                                if bookToBeAdded['id'] not in borrowedBooks:
                                    if self.verifyIfBookHasBeenBorrowed(bookToBeAdded['id']):
                                        print(
                                            "This book has been borrowed by another User")
                                        self.menu()
                                    else:
                                        DatabaseConnection.update(
                                            'Account',
                                            self.account['id'],
                                            {
                                                'borrowedBooks': self.account['borrowedBooks'] + ',' + str(bookToBeAdded['id'])
                                            }
                                        )
                                        self.enterBorrowedIntoDatabase(
                                            bookToBeAdded['id'],
                                            bookToBeAdded['title'],
                                            self.account['id'],
                                        )
                                        self.updateAccount()
                                        self.totalBooksAdded += 1
                                        print(
                                            f"You have succesfully borrowed the book: {bookToBeAdded['title']}")
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
                        if self.totalReservedBooks == 0:
                            if self.verifyIfBookHasBeenBorrowed(bookToBeAdded['id']):
                                print("This book has been reserved by another User")
                                self.menu()
                            else:
                                DatabaseConnection.update(
                                    'Account',
                                    self.account['id'],
                                    {
                                        'reservedBooks': str(bookToBeAdded['id'])
                                    }
                                )
                                self.enterReservedIntoDatabase(
                                    bookToBeAdded['id'],
                                    bookToBeAdded['title'],
                                    self.account['id'],
                                )
                                self.updateAccount()
                                self.totalReservedBooks += 1
                                self.menu()
                        else:
                            reservedBooks = self.account['reservedBooks'].split(
                                ',')
                            num = 0
                            for item in reservedBooks:
                                reservedBooks[num] = int(item)
                                num += 1
                            if bookToBeAdded['id'] not in reservedBooks:
                                if self.verifyIfBookHasBeenBorrowed(bookToBeAdded['id']):
                                    print(
                                        "This book has been reserved by another User")
                                    self.menu()
                                else:
                                    DatabaseConnection.update(
                                        'Account',
                                        self.account['id'],
                                        {
                                            'reservedBooks': self.account['reservedBooks'] + ',' + str(bookToBeAdded['id'])
                                        }
                                    )
                                    self.enterReservedIntoDatabase(
                                        bookToBeAdded['id'],
                                        bookToBeAdded['title'],
                                        self.account['id'],
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

    def viewBorrowedBooks(self):
        if self.totalBooksAdded != 0:
            borrowedBooks = self.account['borrowedBooks'].split(',')
            count = 1
            for book in borrowedBooks:
                bookData = Book.bookDataFromDatabase(
                    DatabaseConnection.retrieve(
                        'Book',
                        'id',
                        int(book[0])
                    )
                )
                print(f"""
                Book {count}:
                     Title: {bookData['title']}
                     Authors: {bookData['authors']}
                     Average Rating: {bookData['averageRating']}
                     ISBN: {bookData['isbn']}
                     Language Code: {bookData['languageCode']}
                     Number of Pages: {bookData['numberOfPages']}
                     Ratings Count: {bookData['ratingsCount']}
                     Text Reviews Count: {bookData['textReviewsCount']}
                     Publication Date: {bookData['publicationDate']}
                     Publisher: {bookData['publisher']}
                """
                      )
                count += 1
            self.menu()
        else:
            print('You currently have no borrowed Books')
            self.menu()

    def viewReservedBooks(self):
        if self.totalReservedBooks != 0:
            reservedBooks = self.account['reservedBooks'].split(',')
            count = 1
            for book in reservedBooks:
                bookData = Book.bookDataFromDatabase(
                    DatabaseConnection.retrieve(
                        'Book',
                        'id',
                        int(book[0])
                    )
                )
                print(f"""
                Book {count}:
                     Title: {bookData['title']}
                     Authors: {bookData['authors']}
                     Average Rating: {bookData['averageRating']}
                     ISBN: {bookData['isbn']}
                     Language Code: {bookData['languageCode']}
                     Number of Pages: {bookData['numberOfPages']}
                     Ratings Count: {bookData['ratingsCount']}
                     Text Reviews Count: {bookData['textReviewsCount']}
                     Publication Date: {bookData['publicationDate']}
                     Publisher: {bookData['publisher']}
                """
                      )
                count += 1
            self.menu()
        else:
            print('You currently have no reserved Books')
            self.menu()

    def viewReturnedBooks(self):
        if self.totalReturnedBooks != 0:
            returnedBooks = self.account['returnedBooks'].split(',')
            count = 1
            for book in returnedBooks:
                bookData = Book.bookDataFromDatabase(
                    DatabaseConnection.retrieve(
                        'Book',
                        'id',
                        int(book[0])
                    )
                )
                print(f"""
                Book {count}:
                     Title: {bookData['title']}
                     Authors: {bookData['authors']}
                     Average Rating: {bookData['averageRating']}
                     ISBN: {bookData['isbn']}
                     Language Code: {bookData['languageCode']}
                     Number of Pages: {bookData['numberOfPages']}
                     Ratings Count: {bookData['ratingsCount']}
                     Text Reviews Count: {bookData['textReviewsCount']}
                     Publication Date: {bookData['publicationDate']}
                     Publisher: {bookData['publisher']}
                """
                      )
                count += 1
            self.menu()
        else:
            print('You currently have no Returned Books')
            self.menu()

    def returnBook(self):
        if self.totalBooksAdded != 0:
            borrowedBooks = self.account['borrowedBooks'].split(',')
            count = 1
            totalBookData = []
            print("Books Borrowed Menu:\n ")
            for book in borrowedBooks:
                bookData = (Book.bookDataFromDatabase(
                    DatabaseConnection.retrieve(
                        'Book',
                        'id',
                        int(book[0])
                    )
                ))
                totalBookData.append(bookData)
                print(f"""
                 {count}. Title: {bookData['title']}
                """
                      )
                count += 1
            print(f"""                 q. Return
            """)
            while True:
                c = input(
                    f"\nSelect the book you would like to return (1-{count-1}|q): ")
                if c == '':
                    print('you have made an invalid entry')
                    self.returnBook()
                elif c == "q":
                    self.menu()
                elif c == str(1):
                    bookId = borrowedBooks[0]
                    DatabaseConnection.insert(
                        'ReturnedBook',
                        {
                            'id': int(bookId),
                            'bookTitle': totalBookData[0]['title'],
                            'returnerId': self.account['id']
                        }
                    )
                    DatabaseConnection.delete(
                        'BorrowedBook',
                        {
                            'id': int(bookId),
                            'borrowerId': self.account['id']
                        }
                    )
                    del borrowedBooks[0]
                    if len(borrowedBooks) != 0:
                        borrowedBooksString = ','.join(borrowedBooks)
                    else:
                        borrowedBooksString = None
                    if self.totalReturnedBooks != 0:
                        returnedBooksString = self.account['returnedBooks']  + ',' + bookId
                    else:
                        returnedBooksString = bookId
                    DatabaseConnection.update(
                        'Account',
                        self.account['id'],
                        {
                            'borrowedBooks': borrowedBooksString,
                            'returnedBooks': returnedBooksString,
                        }
                    )
                    self.account['returnedBooks'] = returnedBooksString
                    self.account['borrowedBooks'] = borrowedBooksString
                    self.totalReturnedBooks += 1
                    self.totalBooksAdded -= 1
                    print("Book succesfully returned")
                    self.menu()
                elif c == str(2):
                    bookId = borrowedBooks[1]
                    DatabaseConnection.insert(
                        'ReturnedBook',
                        {
                            'id': int(borrowedBooks[1]),
                            'bookTitle': totalBookData[1]['title'],
                            'returnerId': self.account['id']
                        }
                    )
                    DatabaseConnection.delete(
                        'BorrowedBook',
                        {
                            'id': int(bookId),
                            'borrowerId': self.account['id']
                        }
                    )
                    del borrowedBooks[1]
                    borrowedBooksString = ','.join(borrowedBooks) 
                    if self.totalReturnedBooks != 0:
                        returnedBooksString = self.account['returnedBooks']  + ',' + bookId
                    else:
                        returnedBooksString = bookId
                    DatabaseConnection.update(
                        'Account',
                        self.account['id'],
                        {
                            'borrowedBooks': borrowedBooksString,
                            'returnedBooks': returnedBooksString,
                        }
                    )
                    self.account['returnedBooks'] = returnedBooksString
                    self.account['borrowedBooks'] = borrowedBooksString
                    self.totalReturnedBooks += 1
                    self.totalBooksAdded -= 1
                    print("Book succesfully returned")
                    self.menu()
                elif c == str(3):
                    bookId = borrowedBooks[2]
                    DatabaseConnection.insert(
                        'ReturnedBook',
                        {
                            'id': int(bookId),
                            'bookTitle': totalBookData[2]['title'],
                            'returnerId': self.account['id']
                        }
                    )
                    DatabaseConnection.delete(
                        'BorrowedBook',
                        {
                            'id': int(bookId),
                            'borrowerId': self.account['id']
                        }
                    )
                    del borrowedBooks[2]
                    borrowedBooksString = ','.join(borrowedBooks)
                    if len(self.totalReturnedBooks) != 0:
                        returnedBooks = self.account['borrowedBooks'].split(
                            ',')
                        returnedBooksString = ','.join(returnedBooks) + ',' + bookId
                    else:
                        returnedBooksString = bookId
                    DatabaseConnection.update(
                        'Account',
                        self.account['id'],
                        {
                            'borrowedBooks': borrowedBooksString,
                            'returnedBooks': returnedBooksString ,
                        }
                    )
                    self.account['returnedBooks'] = returnedBooksString
                    self.account['borrowedBooks'] = borrowedBooksString
                    self.totalReturnedBooks += 1
                    self.totalBooksAdded -= 1
                    print("Book succesfully returned")
                    self.menu()
                else:
                    print('you have made an invalid entry')
                    self.returnBook()
        else:
            print('You currently have no Returned Books')
            self.menu()

    def bookDoesNotExist(self):
        print(
            'This book does not exist in our database, kindly check the title and try again.')
        self.addBook()

    def verifyIfBookHasBeenBorrowed(self, id):
        if self.verifyIfBookHasBeenReserved(id):
            return True
        else:
            data = DatabaseConnection.retrieve('BorrowedBook',
                                               'id',
                                               id
                                               )
            if data != False:
                return True
            else:
                return False

    def verifyIfBookHasBeenReserved(self, id):
        data = DatabaseConnection.retrieve('ReservedBook',
                                           'id',
                                           id
                                           )
        if data != False:
            return True
        else:
            return False

    def enterReservedIntoDatabase(self, bookId, bookTitle, userId):
        DatabaseConnection.insert(
            'ReservedBook',
            {
                'id': bookId,
                'bookTitle': bookTitle,
                'reserverId': userId
            }
        )

    def enterBorrowedIntoDatabase(self, bookId, bookTitle, userId):
        DatabaseConnection.insert(
            'BorrowedBook',
            {
                'id': bookId,
                'bookTitle': bookTitle,
                'borrowerId': userId
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
