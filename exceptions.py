class GamerError(Exception):
    pass
class EmptyStockError(GamerError):
    pass
class InvalidActionError(GamerError):
    pass
class InvalidPositionError(InvalidActionError):
    pass
class CardNotInHandError(GamerError):
    pass

