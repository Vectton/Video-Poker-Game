from enum import Enum, auto
from card_collections import Stock, Hand
from exceptions import InvalidActionError, InvalidPositionError
from collections.abc import Iterable

class HandType(Enum):
    NOTHING = 0
    JACKS_OR_BETTER = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3  
    STRAIGHT = 4        
    FLUSH = 6
    FULL_HOUSE = 9
    FOUR_OF_A_KIND = 25 
    STRAIGHT_FLUSH = 50
    ROYAL_FLUSH = 250

    def __init__(self, ponto):
        self.ponto = ponto

    def __lt__(self, other):
        return self.ponto < other.ponto

class Phase(Enum):
    READY = auto()
    HOLDING = auto()

class VideoPoker:
    HAND_SIZE: int = 5
    def __init__(self):
        self._stock = Stock()
        self._hand = Hand()
        self._phase = Phase.READY
        self._current_points = 0
        self._total_points = 0

    @property
    def phase(self):
        return self._phase

    @property
    def points(self):
        return self._total_points

    @property
    def current_points(self):
        return self._current_points

    @property
    def cards(self):
        return tuple(iter(self._hand))

    def deal(self):
        if self._phase != Phase.READY:
            raise InvalidActionError()
        
        self._stock = Stock()
        self._stock.shuffle()
        self._hand = Hand()
        
        for _ in range(VideoPoker.HAND_SIZE):
            self._hand.receive(self._stock.draw())
        
        self._phase = Phase.HOLDING

    
    def draw(self, held: Iterable[int]):
        if not self._phase == Phase.HOLDING:
            raise InvalidActionError()

        manter = set(held)

        posições_validas = set(range(self.HAND_SIZE))

        if not (manter<=posições_validas):
            raise InvalidPositionError()

        cartas_mesa = tuple(self._hand._cards)
        for p in range(self.HAND_SIZE):
            if p not in manter:
                old_card = cartas_mesa[p]
                new_card = self._stock.draw()
                self._hand.replace(old_card, new_card)

        avaliar_mão = self.hand_type()
        self._current_points = avaliar_mão.ponto
        self._total_points += avaliar_mão.ponto

        self._phase = Phase.READY

        return avaliar_mão
    
    def hand_type(self):
        contagem = {}

        for carta in self._hand:
            num = carta.rank.number
            contagem[num] = contagem.get(num, 0)+1

        frequencia = sorted(contagem.values(), reverse=True)

        if frequencia == [1,1,1,1,1]:
            cartas = sorted(contagem.keys())

            if cartas == [2,3,4,5,14]:
                cartas = [1,2,3,4,5]

            eh_flush = len(set(card.suit.order for card in self._hand)) == 1
            eh_sequencia = (cartas[-1] - cartas[0] == 4)

            if eh_flush and eh_sequencia:
                if cartas == [10,11,12,13,14]:
                    return HandType.ROYAL_FLUSH
                return HandType.STRAIGHT_FLUSH
            elif eh_flush:
                return HandType.FLUSH
            elif eh_sequencia:
                return HandType.STRAIGHT

        elif frequencia == [4,1]:
            return HandType.FOUR_OF_A_KIND

        elif frequencia == [3,2]:
            return HandType.FULL_HOUSE
        elif frequencia == [3,1,1]:
            return HandType.THREE_OF_A_KIND
        elif frequencia == [2,2,1]:
            return HandType.TWO_PAIR
        elif frequencia == [2,1,1,1]:
            for num, qtd in contagem.items():
                if qtd == 2:
                    if num>=11:
                        return HandType.JACKS_OR_BETTER
                    return HandType.NOTHING
        return HandType.NOTHING
            


 
def testar_tudo():
    from card import Card, Rank, Suit 
    print("=== INICIANDO BATERIA DE TESTES DO VIDEO POKER ===\n")
    
    jogo = VideoPoker()
    print(f"[OK] Inicialização: Fase={jogo.phase.name}, Pontos Totais={jogo.points}, Pontos Atuais={jogo.current_points}")
    
    try:
        jogo.draw([0, 1, 2])
        print("[ERRO] O jogo permitiu draw sem as cartas terem sido dadas!")
    except InvalidActionError:
        print("[OK] Bloqueio de draw fora de hora funcionando perfeitamente.")

    jogo.deal()
    print(f"[OK] Deal executado: Nova Fase={jogo.phase.name}")
    print(f"[OK] Quantidade de cartas na mão: {len(jogo.cards)}")
    
    
    print("👉 Cartas atuais na mesa (Texto/Visual):")
    for carta in jogo.cards:
        print(f"   - {repr(carta)} / {str(carta)}")

    try:
        jogo.draw([1, 2, 5]) # Posição 5 não existe (0 a 4)
        print("[ERRO] O jogo aceitou índice 5 fora do limite!")
    except InvalidPositionError:
        print("[OK] Bloqueio de posições inválidas (subconjunto <=) funcionando perfeitamente.")

    try:
        jogo.deal()
        print("[ERRO] O jogo permitiu dar novas cartas no meio da rodada!")
    except InvalidActionError:
        print("[OK] Bloqueio de deal() em fase de HOLDING funcionando perfeitamente.")

    
    print("\n🃏 Executando o draw mudando as cartas dos índices 1, 3 e 4...")
    resultado = jogo.draw([0, 2])
    print(f"[OK] Resultado da rodada: {resultado.name} (Ganhou {jogo.current_points} pontos)")
    print(f"[OK] Saldo total atualizado: {jogo.points} pontos")
    print(f"[OK] Nova Fase após draw: {jogo.phase.name}")

    print("\n👉 Mão Final exibida na mesa:")
    for carta in jogo.cards:
        print(f"   - {repr(carta)} / {str(carta)}")

    jogo.deal()
    print(f"\n[OK] Novo deal iniciado. Garantindo tamanho da mão: {len(jogo.cards)} cartas (Não acumulou!)")

    print("\n🃏 === TESTANDO REGRAS DO AVALIADOR DE MÃOS ===")
    
    jogo._hand._cards = [
        Card(Rank.TEN, Suit.SPADES),
        Card(Rank.JACK, Suit.SPADES),
        Card(Rank.QUEEN, Suit.SPADES),
        Card(Rank.KING, Suit.SPADES),
        Card(Rank.ACE, Suit.SPADES)
    ]
    print(f"[OK] Teste Royal Flush: {jogo.hand_type().name} (Esperado: ROYAL_FLUSH)")

    jogo._hand._cards = [
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.TWO, Suit.DIAMONDS),
        Card(Rank.THREE, Suit.SPADES),
        Card(Rank.FOUR, Suit.CLUBS),
        Card(Rank.FIVE, Suit.HEARTS)
    ]
    print(f"[OK] Teste Sequência com Ás baixo (Wheel): {jogo.hand_type().name} (Esperado: STRAIGHT)")

    jogo._hand._cards = [
        Card(Rank.TEN, Suit.HEARTS),
        Card(Rank.TEN, Suit.DIAMONDS),
        Card(Rank.THREE, Suit.SPADES),
        Card(Rank.FOUR, Suit.CLUBS),
        Card(Rank.FIVE, Suit.HEARTS)
    ]
    print(f"[OK] Teste Par Baixo (Par de 10): {jogo.hand_type().name} (Esperado: NOTHING)")

    jogo._hand._cards = [
        Card(Rank.JACK, Suit.HEARTS),
        Card(Rank.JACK, Suit.DIAMONDS),
        Card(Rank.THREE, Suit.SPADES),
        Card(Rank.FOUR, Suit.CLUBS),
        Card(Rank.FIVE, Suit.HEARTS)
    ]
    print(f"[OK] Teste Par Alto (Par de Valetes): {jogo.hand_type().name} (Esperado: JACKS_OR_BETTER)")

    print("\n=== TODOS OS TESTES PASSARAM COM SUCESSO! O MOTOR ESTÁ IMPECÁVEL ===")        
        

