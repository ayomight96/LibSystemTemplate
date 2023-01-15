class Book:
    def __init__(
        self,
        id,
        title,
        authors,
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
        self.id = id
        self.title = title
        self.authors = authors
        self.averageRating = averageRating
        self.isbn = isbn
        self.isbn13 = isbn13
        self.languageCode = languageCode
        self.numberOfPages = numberOfPages
        self.ratingsCount = ratingsCount
        self.textReviewsCount = textReviewsCount
        self.publicationDate = publicationDate
        self.publisher = publisher

    def data(self):
        return {
            'id': self.id,
            'title': self.title,
            'authors': self.authors,
            'averageRating': self.averageRating,
            'isbn': self.isbn,
            'isbn13': self.isbn13,
            'languageCode': self.languageCode,
            'numberOfPages': self.numberOfPages,
            'ratingsCount': self.ratingsCount,
            'textReviewsCount': self.textReviewsCount,
            'publicationDate': self.publicationDate,
            'publisher': self.publisher
        }

    @staticmethod
    def bookDataFromDatabase(data):
        return {
            'id': data[0][0],
            'title': data[0][1],
            'authors': data[0][2],
            'averageRating': data[0][3],
            'isbn': data[0][4],
            'isbn13': data[0][5],
            'languageCode': data[0][6],
            'numberOfPages': data[0][7],
            'ratingsCount': data[0][8],
            'textReviewsCount': data[0][9],
            'publicationDate': data[0][10],
            'publisher': data[0][11],
        }

    @staticmethod
    def bookDataFromDatabase2(data):
        return {
            'id': data[0],
            'title': data[1],
            'authors': data[2],
            'averageRating': data[3],
            'isbn': data[4],
            'languageCode': data[5],
            'numberOfPages': data[6],
            'ratingsCount': data[7],
            'textReviewsCount': data[8],
            'publicationDate': data[9],
            'publisher': data[10],
        }
