
import uuid


class Account:
    def __init__(
        self,
        userName,
        fullName,
        password,
        userType,
        school,
        department,
        borrowedBooks=None,
        reservedBooks=None,
        returnedBooks=None,
        lostBooks=None,
        fine=0
    ):
        self.userName = userName
        self.password = password
        self.fullName = fullName
        self.userType = userType
        self.school = school
        self.department = department
        self.id = uuid.uuid4()
        self.borrowedBooks = borrowedBooks
        self.reservedBooks = reservedBooks
        self.returnedBooks = returnedBooks
        self.lostBooks = lostBooks
        self.fine = fine

    def data(self):
        return {
            'id': str(self.id),
            'fullName': self.fullName,
            'userName': self.userName,
            'password': self.password,
            'userType': self.userType,
            'school': self.school,
            'department': self.department,
            'borrowedBooks': self.borrowedBooks,
            'reservedBooks': self.reservedBooks,
            'returnedBooks': self.returnedBooks,
            'lostBooks': self.lostBooks,
            'fine': self.fine
        }

    @staticmethod
    def accountDataFromDatabase(data):
        return {
            'id': data[0][0],
            'fullName': data[0][1],
            'userName': data[0][2],
            'password': data[0][3],
            'userType': data[0][4],
            'school': data[0][5],
            'department': data[0][6],
            'borrowedBooks': data[0][7],
            'reservedBooks': data[0][8],
            'returnedBooks': data[0][9],
            'lostBooks': data[0][10],
            'fine': data[0][11],
        }
