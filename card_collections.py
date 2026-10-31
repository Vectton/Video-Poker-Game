from abc import ABC, abstractmethod
from collections.abc import Iterable
from  exceptions import EmptyStockError, CardNotInHandError
from card import Card, Suit, Rank
import random

class CardColletion(ABC):
    def __init__(self, cards: Iterable[Card] = ()):
        self._cards: list[Card] = list(cards)

    def __len__(self):
        return len(self._cards)

    @abstractmethod
    def __iter__(self):
        ...

class Stock(CardColletion):
    def __init__(self):
        super().__init__()

        for suit in Suit:
            for rank in Rank:
                self._cards.append(Card(rank, suit))
        
    def shuffle(self):
        random.shuffle(self._cards)

    def draw(self):
        if not self._cards:
            raise EmptyStockError("Não há cartas no Baralho!")
        topo = self._cards.pop()
        return topo

    def __iter__(self):
        return iter(reversed(self._cards))

class Hand(CardColletion):
    def __init__(self):
        super().__init__()

    def receive(self,card: Card):
        self._cards.append(card)

    def discard(self, card: Card):
        index = self._index_card(card)
        return self._cards.pop(index)
    
    def replace(self, old: Card, new: Card):
        indice = self._index_card(old)
        self._cards[indice] = new
        return old
    def __iter__(self):
        return iter(self._cards)

    def _index_card(self, card):
        try:
            return self._cards.index(card)
        except ValueError:
            raise CardNotInHandError("A carta não está na mão!") from None

def teste():
    baralho = Stock()
    mão = Hand()

    for a in range(5):
        print(f"{baralho._cards[a]}", end=" ")
    print(f"\nCartas total: {len(baralho)}") #52


    baralho.shuffle()
    for a in range(5):
        print(f"{baralho._cards[a]}", end=" ")
        mão.receive(baralho.draw())
    print("\nprimeiras cartas pós shuffle")
    for b in range(5):
        print(baralho._cards[b], end=" ")

    print(f"\nCartas na mão: {len(mão)}")
    for a in range(len(mão)):
        print(mão._cards[a], end=" ")
    print(f"\nCartas no Baralho: {len(baralho)}")

    print(f"Lista de Cartas na mão: {list(mão)}")

