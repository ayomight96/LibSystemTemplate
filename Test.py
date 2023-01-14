import json

class LibaryData:
    books = {}
    def __init__(self):
        pass
        
    @classmethod  
    def loadBooks(cls):
        with open('book2.json') as bookCollection:
            books= json.load(bookCollection)
            for book in books:
                cls.books["isbn"]= Book(book["title"],book["authors"])
     
    #  xxxxxxxxxxxx           
     
        
     
        
     


class  Book:
    def __init__(
        self,
        title,
        author,
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
        self.title = title
        self.author = author
        self.averageRating = averageRating
        self.isbn = isbn
        self.isbn13 = isbn13
        self.languageCode = languageCode
        self.numberOfPages = numberOfPages
        self.ratingsCount = ratingsCount
        self.textReviewsCount = textReviewsCount
        self.publicationDate = publicationDate
        self.publisher = publisher
    
    def __repr__(self) -> str:
        pass
