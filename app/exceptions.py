class WalletNotFoundError(Exception):
    pass


class InvalidAmountError(Exception):
    pass


class InsufficientBalanceError(Exception):
    pass

class UserNotFoundError(Exception):
    pass

class UnauthorizedWalletAccessError(Exception):
    pass