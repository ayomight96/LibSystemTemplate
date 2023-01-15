from DatabaseConnection import DatabaseConnection
import json
from Book import Book

class LibraryData:
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
