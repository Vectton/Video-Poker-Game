import os
from poker import VideoPoker, HandType, Phase

class PokerTerminal:
    HAND_NAMES = {
        HandType.ROYAL_FLUSH: "Royal Flush",
        HandType.STRAIGHT_FLUSH: "Straight Flush",
        HandType.FOUR_OF_A_KIND: "Quadra",
        HandType.FULL_HOUSE: "Full House",
        HandType.FLUSH: "Flush",
        HandType.STRAIGHT: "Sequência",
        HandType.THREE_OF_A_KIND: "Trinca",
        HandType.TWO_PAIR: "Dois Pares",
        HandType.JACKS_OR_BETTER: "Par de Valetes ou Melhor",
        HandType.NOTHING: "Nenhuma Mão"
    }

    def __init__(self, poker: VideoPoker):
        self.jogo = poker
        self.rounds = 0

    def print_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("========== Tabela de Pontuação ===========")
        print("| ROYAL FLUSH        |               250 |")
        print("| STRAIGHT FLUSH     |                50 |")
        print("| FOUR OF A KIND     |                25 |")
        print("| FULL HOUSE         |                 9 |")
        print("| FLUSH              |                 6 |")
        print("| STRAIGHT           |                 4 |")
        print("| THREE OF A KIND    |                 3 |")
        print("| TWO PAIR           |                 2 |")
        print("| JACKS OR BETTER    |                 1 |")
        print("| NOTHING            |                 0 |")

        print("\n============== Video Poker ===============")
        
        print(f"Ganhos: {self.jogo.current_points} | Saldo: {self.jogo.points} | Rodadas: {self.rounds}")
        print("------------------------------------------")
        
        if self.jogo.cards:
            print("   " + "   ".join(str(c) for c in self.jogo.cards) + "\n")
            print("    " + "   ".join(f"{i}" for i in range(1, len(self.jogo.cards) + 1)) + "\n")
        else:
            print("\n         [ Aguardando Distribuição ]\n")
        
        if self.jogo.cards:
            try:
                mão_atual = self.jogo.hand_type()
            except TypeError:
                mão_atual = self.jogo.hand_type
                
            print(f"🏆 MÃO: {self.HAND_NAMES.get(mão_atual, 'NOTHING')}")
        print("------------------------------------------")

    def jogar(self):
        while True:
            self.print_screen()
            
            if self.jogo.phase == Phase.READY:
                input("READY: Pressione [ENTER] para dar as cartas...")
                self.jogo.deal()
                
            elif self.jogo.phase == Phase.HOLDING:
                while True:
                    txt = input("HOLDING: Escolha quais MANTER (ex: 1 3 4) ou [ENTER] para trocar todas: ")
                    
                    if not txt.strip():
                        held = []
                        break
                    
                    try:
                        posições = [int(x) for x in txt.split()]
                        
                        if any(p < 1 or p > 5 for p in posições):
                            print("Posição inválida! Escolha números apenas de 1 a 5.")
                            continue
                            
                        held = [p - 1 for p in posições]
                        break
                    except ValueError:
                        print("Entrada inválida! Digite apenas números separados por espaço.")
                
                self.jogo.draw(held)
                self.rounds += 1

if __name__ == "__main__":
    try:
        motor_poker = VideoPoker()
        interface = PokerTerminal(motor_poker)
        interface.jogar()
    except KeyboardInterrupt:
        print("\nAté a próxima!")