from DatabaseConnection import DatabaseConnection
from Account import Account
from Book import Book
from User import User


class StudentUser(User):
    bookLimit = 3
    totalBooksAdded = 0

    def __init__(
            self,
            fullName,
            school,
            department,
            account=None
    ):
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
4. Option 4 ~Reserve Book
5. Option 5 ~View Borrowed Books
q. Return

""")
        while True:
            c = input("\nSelect Option (1-4|q): ")
            choice = {"1": self.profile,
                      "2": self.payFine,
                      "3": self.addBook,
                      "4": self.reserveBook,
                      "5": self.viewBorrowedBook,
                      "q": "q"}.get(c, "invalid")
            if choice == "q":
                print('Bye..')
                return False

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
                                        bookToBeAdded['id'],
                                        self.account['id'],
                                    )
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
                                    if self.verifyIfBookHasBeenBorrowed(bookToBeAdded['id']):
                                        print(
                                            "This book has been borrowed by another User")
                                        self.menu()
                                    else:
                                        DatabaseConnection.update(
                                            'Account',
                                            self.account['id'],
                                            {
                                                'booksBorrowed': self.account['booksBorrowed'] + ',' + str(bookToBeAdded['id'])
                                            }
                                        )
                                        self.enterBorrowedIntoDatabase(
                                            bookToBeAdded['id'],
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
                                    bookToBeAdded['id'],
                                    self.account['id'],
                                )
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
                                if self.verifyIfBookHasBeenBorrowed(bookToBeAdded['id']):
                                    print(
                                        "This book has been reserved by another User")
                                    self.menu()
                                else:
                                    DatabaseConnection.update(
                                        'Account',
                                        self.account['id'],
                                        {
                                            'booksBorrowed': self.account['booksBorrowed'] + ',' + str(bookToBeAdded['id'])
                                        }
                                    )
                                    self.enterReservedIntoDatabase(
                                        bookToBeAdded['id'],
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

    def viewBorrowedBook(self):
        booksBorrowed = self.account['booksBorrowed'].split(',')
        if len(booksBorrowed) != 0:
            count = 1
            for book in booksBorrowed:
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

    def enterReservedIntoDatabase(self, bookId, userId):
        DatabaseConnection.insert(
            'ReservedBook',
            {
                'id': bookId,
                'reserverId': userId
            }
        )

    def enterBorrowedIntoDatabase(self, bookId, userId):
        DatabaseConnection.insert(
            'BorrowedBook',
            {
                'id': bookId,
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
