from utils.logger import logger


class DoCliBaseError(Exception):
    def __init__(self, data: str = None):
        self.data = data
        logger.error(self.__str__())

    def __str__(self):
        return f"Error: {self.__class__.__name__}{(' : %s' % self.data) if self.data is not None else ''}"


class DoCliUserExist(DoCliBaseError):
    pass


class DoCliPermissionError(DoCliBaseError):
    pass


class DoCliLoginError(DoCliBaseError):
    pass


class DoCliShopIdError(DoCliBaseError):
    pass


class DoCliError(DoCliBaseError):
    pass


class DoCliCookiesError(DoCliBaseError):
    pass
