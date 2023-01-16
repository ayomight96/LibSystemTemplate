class Fine:
    def __init__(
        self,
        id,
        bookId,
        fine,
        fineStatus
    ):
        self.id = id
        self.bookId = bookId
        self.fine = fine
        self.fineStatus = fineStatus

    def data(self):
        return {
            'id': self.id,
            'bookId': self.bookId,
            'fine': self.fine,
            'fineStatus': self.fineStatus,
        }

    @staticmethod
    def fineDataFromDatabase(data):
        return {
            'id': data[0][0],
            'bookId': data[0][1],
            'fine': data[0][2],
            'fineStatus': data[0][3],
        }
