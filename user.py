

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
