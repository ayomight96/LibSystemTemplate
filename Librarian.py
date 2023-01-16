from DatabaseConnection import DatabaseConnection
from Account import Account
from Book import Book


class Librarian:

    @staticmethod
    def menu():
        print(f"""Welcome to the Admin Dashboard
Menu
1. Option 1 ~Books in the Library System
3. Option 2 ~View Borrowed Books
3. Option 3 ~View Reserved Books
4. Option 4 ~View Returned Books
q. Return

""")
        while True:
            c = input("\nSelect Option (1-5|q): ")
            choice = {"1": Librarian.booksInTheLibrarySystem,
                      "2": Librarian.viewBorrowedBooks,
                      "3": Librarian.viewReservedBooks,
                      "4": Librarian.viewReturnedBooks,
                      "q": "q"}.get(c, "invalid")
            if choice == "q":
                print('Bye..')
                break

            elif choice != "invalid":
                choice()
            else:
                print("Try again...")

    @staticmethod
    def bookStatistics():
        print(f"""Book Statistics:\n
Total Number of Books in the Library System: {len(Librarian.booksInTheLibrarySystem)}\n
Total Number of Borrowed Books: {len(Librarian.borrowedBooks)}\n
Total Number of Reserved Books: {len(Librarian.reservedBooks)}\n
Total Number of Returned Books: {len(Librarian.returnedBooks)}\n
""")
        Librarian.menu()

    @staticmethod
    def booksInTheLibrarySystem():
        books = DatabaseConnection.retrieveAll('Book')
        if books != False:
            count = 1
            for book in books:
                bookData = Book.bookDataFromDatabase(book)
                print(f"""
                Book {count}:
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
            Librarian.menu()
        else:
            print('You currently have no borrowed Books')
            Librarian.menu()

    @staticmethod
    def viewBorrowedBooks():
        borrowedBooks = DatabaseConnection.retrieveAll('BorrowedBook')
        if borrowedBooks != False:
            count = 1
            for book in borrowedBooks:
                borrowerData = Account.accountDataFromDatabase(DatabaseConnection.retrieve(
                    'Account',
                    'id',
                    book[0]
                )
                )
                print(f"""
                Book {count}:
                     Book Title: {book[1]}
                     Borrower Name: {borrowerData['fullName']}
                """
                      )
                count += 1
            Librarian.menu()
        else:
            print('You currently have no borrowed Books')
            Librarian.menu()

    @staticmethod
    def viewReservedBooks():
        reservedBooks = DatabaseConnection.retrieveAll('ReservedBook')
        if reservedBooks != False:
            count = 1
            for book in reservedBooks:
                borrowerData = Account.accountDataFromDatabase(DatabaseConnection.retrieve(
                    'Account',
                    'id',
                    book[0]
                )
                )
                print(f"""
                Book {count}:
                     Book Title: {book[1]}
                     Borrower Name: {borrowerData['fullName']}
                """
                      )
                count += 1
            Librarian.menu()
        else:
            print('You currently have no reserved Books')
            Librarian.menu()

    @staticmethod
    def viewReturnedBooks():
        returnedBooks = DatabaseConnection.retrieveAll('ReturnedBook')
        if returnedBooks != False:
            count = 1
            for book in returnedBooks:
                borrowerData = Account.accountDataFromDatabase(DatabaseConnection.retrieve(
                    'Account',
                    'id',
                    book[0]
                )
                )
                print(f"""
                Book {count}:
                     Book Title: {book[1]}
                     Borrower Name: {borrowerData['fullName']}
                """
                      )
                count += 1
            Librarian.menu()
        else:
            print('You currently have no returned Books')
            Librarian.menu()
