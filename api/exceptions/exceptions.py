
class AppException(Exception):
    def __init__(self, type):
        self.__type = type

    def get_type(self):
        return self.__type


class ProfileAlreadyExists(AppException):
    def __init__(self, guid: str, full_name: str, scientometric_database: str):
        super().__init__("profile.already_exists")
        self.message = "profile ({}, {}, {}) already exists".format(guid, full_name, scientometric_database)


class ProfileNotFound(AppException):
    def __init__(self, guid: str, scientometric_database: str):
        super().__init__("profile.not_found")
        self.message = "profile ({}, {}) not found".format(guid, scientometric_database)
