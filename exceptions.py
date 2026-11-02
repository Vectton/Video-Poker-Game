class GameError(Exception):
    pass
class EmptyStockError(GameError):
    pass
class InvalidActionError(GameError):
    pass
class InvalidPositionError(InvalidActionError):
    pass
class CardNotInHandError(GameError):
    pass

