from enum import Enum
from functools import total_ordering

@total_ordering
class Rank(Enum):
    TWO = (2, '2')
    THREE = (3, '3')
    FOUR =  (4, '4')
    FIVE = (5, '5')
    SIX = (6,'6')
    SEVEN = (7,'7')
    EIGHT = (8,'8')
    NINE = (9,'9')
    TEN = (10, '10')
    JACK = (11, 'J')
    QUEEN = (12, 'Q')
    KING = (13, 'K')
    ACE = (14, 'A')

    def __init__(self, number: int, label: str):
        self.number = number 
        self.label = label

    def __lt__(self, other):
        if not isinstance(other, Rank):
            return NotImplemented
        return self.number<other.number

@total_ordering
class Suit(Enum):
    CLUBS = (1, '♣', 0x1F0D0)
    DIAMONDS = (2,'♦', 0x1F0C0)
    HEARTS = (3,'♥', 0x1F0B0)
    SPADES = (4, '♠', 0x1F0A0)

    def __init__(self, order, symbol, unicode_base):
        self.order = order
        self.symbol = symbol
        self.unicode_base = unicode_base

    def __lt__(self, other):
        if not isinstance(other, Suit):
            return NotImplemented
        return self.order < other.order

@total_ordering
class Card:
    BACK_UNICODE = '1F0A0'

    def __init__(self, rank: Rank, suit: Suit, face_up: bool = True):
        self._rank = rank
        self._suit = suit
        self._is_face_up = face_up

    @property
    def rank(self):
        return self._rank

    @property
    def suit(self):
        return self._suit

    @property
    def is_face_up(self):
        return self._is_face_up

    def flip(self):
        self._is_face_up = not self._is_face_up  

    def __eq__(self, other):
        if not isinstance(other, Card):
            return NotImplemented
        return self._rank.number == other.rank.number and self._suit.order == other.suit.order

    def __lt__(self, other):
        if isinstance(other, Card):
            if self._rank.number == other.rank.number:
                return self._suit.order < other.suit.order
            return self._rank.number < other.rank.number

    def __hash__(self):
        return hash((self._rank, self._suit))
        
    def __str__(self):
        if self._is_face_up == False:
            return chr(int(Card.BACK_UNICODE, 16))

        if self._rank == Rank.ACE:
            offset = 1
        elif self._rank == Rank.QUEEN:
            offset = 13
        elif self._rank == Rank.KING:
            offset = 14
        else:
            offset = self._rank.number

        return chr(self._suit.unicode_base + offset)
        
    def __repr__(self) -> str:
        if not self._is_face_up:
            return f"Card({chr(int(self.BACK_UNICODE, 16))})"

        return f"Card({self._rank.label}{self._suit.symbol})"


def teste():
    carta_1 = Card(Rank.ACE, Suit.CLUBS)
    carta_2 = Card(Rank.TWO, Suit.DIAMONDS)

    print(carta_1==carta_2) #False
    print(carta_1<carta_2) #False
    print(carta_1>carta_2) #True
    print(carta_1>=carta_2) #True
    print(carta_1<=carta_2) #False

    carta_3 = Card(Rank.FIVE, Suit.HEARTS)
    carta_4 = Card(Rank.SEVEN, Suit.SPADES)

    print(carta_2>carta_3) #False

    print(f"Rank: {carta_3.rank}, Suit: {carta_3.suit}")
    print(f"Rank: {carta_4.rank}, Suit: {carta_4.suit}")

    carta_5 = Card(Rank.QUEEN, Suit.CLUBS)
    carta_6 = Card(Rank.KING, Suit.DIAMONDS)
    carta_7 = Card(Rank.JACK, Suit.SPADES)
    print(carta_1<carta_5) #False

    print(f"{carta_1}, {carta_2}, {carta_3}, {carta_4}, {carta_5}, {carta_6}, {carta_7}")
    for b in Suit:
        print(f"{b}")



