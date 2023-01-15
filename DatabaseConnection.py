import sqlite3
import os


class DatabaseConnection:
    def __init__(self) -> any:
        if os.path.exists('/Users/mac/Documents/PYTHON FOLDER/LibSystemTemplate/LibSystemTemplate/LibrarySystem.db') != True:
            connection = self.openConnection()
            cursor = connection.cursor()
            cursor.execute(
                """create table Account(
                        id text,
                        fullName text,
                        userName text,
                        password text,
                        userType text,
                        school text,
                        department text,
                        booksBorrowed text,
                        booksReserved text,
                        booksReturned text,
                        booksLost text,
                        fine integer
                        )""")
            cursor.execute(
                """create table Book(
                        id integer,
                        title text,
                        authors text,
                        averageRating real,
                        isbn integer,
                        isbn13 integer,
                        languageCode text,
                        numberOfPages integer,
                        ratingsCount integer,
                        textReviewsCount integer,
                        publicationDate text,
                        publisher text
                        )""")
            cursor.execute(
                """create table BorrowedBooks(
                    id integer
                    )""")
            cursor.execute(
                """create table ReturnedBooks(
                    id integer
                    )""")
            cursor.execute(
                """create table ReservedBooks(
                    id integer
                    )""")
            connection.commit()
            self.connection.close
            print('Database and Tables Succesfully created')

    # Opens connection to the Database
    @classmethod
    def openConnection(self):
        connection = sqlite3.connect("LibrarySystem.db")
        self.connection = connection
        return connection

    # Closes connection to the Database
    @classmethod
    def closeConnection(self):
        self.connection.close()

    # inserts data into tables
    # takes tableName:str and data:dict as Parameters returns None
    @staticmethod
    def insert(tableName: str, data: dict):
        connection = DatabaseConnection.openConnection()
        cursor = connection.cursor()
        for key in data:
            if key == 'id':
                uniqueId = key
                cursor.execute(
                    "insert into " + tableName + " (" + key + ")values (?)", (data[key],))
                connection.commit()
            else:
                DatabaseConnection.update(tableName, data[uniqueId], data)
        DatabaseConnection.closeConnection()

    # Updates data in tables
    # takes tableName:str, uniqueId:any and data:dict as Parameters returns None
    @staticmethod
    def update(tableName: str, uniqueId: any, data: dict):
        connection = DatabaseConnection.openConnection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT * FROM " + tableName + " WHERE id = :id", {"id": uniqueId})
        rowData = cursor.fetchall()
        if len(rowData) != 0:
            for key in data:
                if key != 'id':
                    cursor.execute(
                        "UPDATE " + tableName + " SET " + key + "=?" + " WHERE id =?", (data[key], uniqueId))
                    connection.commit()
        else:
            raise Exception("Invalid SearchParameters")
        DatabaseConnection.connection.close()

    # Deletes data in tables
    # takes tableName:str and searchParameters:dict as Parameters returns None
    @staticmethod
    def delete(tableName: str, searchParameters: dict) -> bool:
        connection = DatabaseConnection.openConnection()
        cursor = connection.cursor()
        dictCount = len(searchParameters)
        if dictCount > 3:
            raise Exception("Invalid SearchParameters")
        counter = 1
        queryString = ""
        queryVariables = []
        for key in searchParameters:
            queryString += key + " = ?"
            queryVariables.append(searchParameters[key])
            if counter < dictCount:
                queryString += " AND "
                counter += 1
        fullQueryString = "DELETE FROM " + tableName + " WHERE " + queryString
        match dictCount:
            case 1:
                cursor.execute(fullQueryString,
                               (queryVariables[0],))
            case 2:
                cursor.execute(fullQueryString,
                               (queryVariables[0], queryVariables[1]))
            case 3:
                cursor.execute(
                    fullQueryString, (queryVariables[0], queryVariables[1], queryVariables[2]))
        connection.commit()
        DatabaseConnection.connection.close()

    # Retrieves all data in tables
    @staticmethod
    def retrieveAll(tableName: str):
        data = []
        counter = 0
        connection = DatabaseConnection.openConnection()
        cursor = connection.cursor()
        for row in cursor.execute("select * from " + tableName):
            data.append(row)
            counter += 1
        DatabaseConnection.closeConnection()
        return data

    # Retrieves all data in tables that meet specific criteria
    @staticmethod
    def retrieve(tableName: str, searchParameter: any, searchParameterValue=None):
        connection = DatabaseConnection.openConnection()
        cursor = connection.cursor()
        if type(searchParameter) is dict:
            dictCount = len(searchParameter)
            if dictCount < 2 or dictCount > 4:
                raise Exception("Invalid SearchParameters")
            counter = 1
            queryString = ""
            queryVariables = []
            for key in searchParameter:
                queryString += key + " = :" + key
                queryVariables.append(searchParameter[key])
                if counter < dictCount:
                    queryString += " AND "
                    counter += 1
            fullQueryString = "SELECT * FROM " + tableName + " WHERE " + queryString
            match dictCount:
                case 2:
                    cursor.execute(fullQueryString,
                                   (queryVariables[0], queryVariables[1]))
                    data = cursor.fetchall()
                    if len(data) != 0:
                        return data
                    else:
                        return False
                case 3:
                    cursor.execute(
                        fullQueryString, (queryVariables[0], queryVariables[1], queryVariables[2]))
                    data = cursor.fetchall()
                    if len(data) != 0:
                        return data
                    else:
                        return False
                case 4:
                    cursor.execute(
                        fullQueryString, (queryVariables[0], queryVariables[1], queryVariables[2], queryVariables[3]))
                    data = cursor.fetchall()
                    if len(data) != 0:
                        return data
                    else:
                        return False
        else:
            cursor.execute(
                "SELECT * FROM " + tableName + " WHERE " + searchParameter + " = ?", (searchParameterValue,))
            data = cursor.fetchall()
            if len(data) != 0:
                return data
            else:
                return False
        DatabaseConnection.closeConnection()

    # Retrieves all data in tables that meet specific criteria
    @staticmethod
    def retrieveByTextSearch(tableName: str, searchParameterKey, searchParameterValue):
        connection = DatabaseConnection.openConnection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT * FROM " + tableName + " WHERE " + searchParameterKey + " LIKE ?", ('%' + searchParameterValue + '%',))
        data = cursor.fetchall()
        DatabaseConnection.closeConnection()
        if len(data) != 0:
            return data
        else:
            return False
