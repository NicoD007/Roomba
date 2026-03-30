class User:
    def __init__(self, username: str, email: str, password: str) -> None:
        self._username = username
        self._password = password
        self._email = email
        self._userId: int = 0

    def getUsername(self) -> str:
        return self._username

    def setEmail(self, email: str) -> None:
        self._email = email 

    def start(self) -> None:
        pass