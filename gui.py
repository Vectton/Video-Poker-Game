'''Interface gráfica do Video Poker — tkinter puro.

A GUI só desenha o estado que o modelo expõe e repassa os cliques:
não avalia mãos, não sorteia cartas e não calcula pontuação.
'''

import math
import random
import tkinter as tk
from enum import Enum


# ------------------------------------------------------------------
# Paleta
# ------------------------------------------------------------------
GREEN_TABLE = '#3f6e17'
RED_BTN = '#f54237'
GREY_FILLET = '#2b3638'
GREY_FRAME = '#172123'
BLUE_BTN = '#0189f4'
YELLOW_BTN = '#fa9003'
WHITE = '#ffffff'
BLACK = '#000000'
GREY_LIGHT = '#dfe3e6'

# ------------------------------------------------------------------
# Tipografia
# ------------------------------------------------------------------
FAMILY_TEXT = 'Courier New'
FAMILY_CARD = 'Segoe UI Symbol'

FONT_TITLE = (FAMILY_TEXT, 30, 'bold')
FONT_HEADER = (FAMILY_TEXT, 14, 'bold')
FONT_ROW = (FAMILY_TEXT, 10, 'bold')
FONT_SMALL = (FAMILY_TEXT, 9, 'bold')
FONT_HOLD = (FAMILY_TEXT, 10, 'bold')
FONT_BUTTON = (FAMILY_TEXT, 17, 'bold')
FONT_STATUS = (FAMILY_TEXT, 10, 'bold')
FONT_SCORE = (FAMILY_TEXT, 26, 'bold')
FONT_CARD = (FAMILY_CARD, 92)
FONT_BACK = (FAMILY_CARD, 91)

ARC_STEPS = 8


# ------------------------------------------------------------------
# Modelo temporário (stub) — trocar pelos módulos reais do jogo
# ------------------------------------------------------------------
class Phase(Enum):
    READY = 'ready'
    HOLDING = 'holding'


class HandType(Enum):
    NOTHING = 0
    JACKS_OR_BETTER = 1
    TWO_PAIRS = 2
    THREE_OF_A_KIND = 3
    STRAIGHT = 4
    FLUSH = 6
    FULL_HOUSE = 9
    FOUR_OF_A_KIND = 25
    STRAIGHT_FLUSH = 50
    ROYAL_FLUSH = 250


PAYTABLE = (
    (HandType.ROYAL_FLUSH, 'ROYAL FLUSH'),
    (HandType.STRAIGHT_FLUSH, 'STRAIGHT FLUSH'),
    (HandType.FOUR_OF_A_KIND, 'QUADRA'),
    (HandType.FULL_HOUSE, 'FULL HOUSE'),
    (HandType.FLUSH, 'FLUSH'),
    (HandType.STRAIGHT, 'SEQUENCIA'),
    (HandType.THREE_OF_A_KIND, 'TRINCA'),
    (HandType.TWO_PAIRS, 'DOIS PARES'),
    (HandType.JACKS_OR_BETTER, 'JACKS OR BETTER'),
)

HAND_NAMES = {hand: name for hand, name in PAYTABLE}

SUIT_BASES = (0x1F0A0, 0x1F0B0, 0x1F0C0, 0x1F0D0)
DECK = tuple(
    chr(base + offset)
    for base in SUIT_BASES
    for offset in range(1, 0x0F)
    if offset != 0x0C  # o cavaleiro não faz parte do baralho
)


class StubCard:
    '''Carta temporária: a GUI só consome o glifo devolvido por __str__.'''

    __slots__ = ('_symbol',)

    def __init__(self, symbol: str) -> None:
        self._symbol = symbol

    def __str__(self) -> str:
        return self._symbol


class VideoPoker:
    '''Modelo provisório: mantém o estado que a interface precisa mostrar.'''

    HAND_SIZE = 5
    # Q♥ J♥ 8♣ 7♦ K♥ — a mesma mão do rascunho, para abrir idêntico
    INITIAL_HAND = ('\U0001F0BD', '\U0001F0BB', '\U0001F0D8', '\U0001F0C7', '\U0001F0BE')

    def __init__(self) -> None:
        self.phase = Phase.READY
        self.points = 305
        self.current_points = 0
        self.cards = tuple(StubCard(symbol) for symbol in self.INITIAL_HAND)

    def deal(self) -> None:
        if self.phase is not Phase.READY:
            raise ValueError('deal() só é permitido na fase READY')
        self.phase = Phase.HOLDING
        self.current_points = 0
        self.cards = tuple(StubCard(symbol) for symbol in random.sample(DECK, self.HAND_SIZE))

    def draw(self, held) -> None:
        if self.phase is not Phase.HOLDING:
            raise ValueError('draw() só é permitido na fase HOLDING')
        held = set(held)
        self.cards = tuple(
            card if index in held else StubCard(random.choice(DECK))
            for index, card in enumerate(self.cards)
        )
        self.phase = Phase.READY
        # A avaliação de verdade é do modelo; aqui só refletimos o fictício
        self.current_points = self.hand_type().value
        self.points += self.current_points

    def hand_type(self) -> HandType:
        # Troque por outro membro para ver o destaque da tabela funcionando
        return HandType.NOTHING


# ------------------------------------------------------------------
# Geometria
# ------------------------------------------------------------------
def rounded_rect_points(x0: float, y0: float, x1: float, y1: float,
                        radius: float, steps: int = ARC_STEPS) -> list:
    '''Contorno de um retângulo de cantos arredondados, pronto para create_polygon.

    Quatro arcos de 90° amostrados no sentido que fecha o polígono, porque o
    eixo y do canvas cresce para baixo.
    '''
    radius = max(0.0, min(radius, (x1 - x0) / 2, (y1 - y0) / 2))
    corners = (
        (x1 - radius, y0 + radius, 270),
        (x1 - radius, y1 - radius, 0),
        (x0 + radius, y1 - radius, 90),
        (x0 + radius, y0 + radius, 180),
    )
    points = []
    for cx, cy, start in corners:
        for step in range(steps + 1):
            angle = math.radians(start + 90 * step / steps)
            points.append(cx + radius * math.cos(angle))
            points.append(cy + radius * math.sin(angle))
    return points


def is_red_suit(symbol: str) -> bool:
    '''Copas e ouros são vermelhos; o naipe vem codificado no próprio glifo.'''
    if not symbol:
        return False
    return (ord(symbol[0]) & 0xF0) in (0xB0, 0xC0)


# ------------------------------------------------------------------
# Componentes
# ------------------------------------------------------------------
class RoundedBox(tk.Canvas):
    '''Canvas que se desenha como um retângulo de cantos arredondados.'''

    def __init__(self, master: tk.Widget, width: int, height: int, radius: int = 10,
                 fill: str = WHITE, outline: str = GREY_FRAME, thickness: int = 2,
                 parent_bg: str = GREEN_TABLE, command=None) -> None:
        super().__init__(master, width=width, height=height, bg=parent_bg,
                         highlightthickness=0, bd=0)
        self.radius = radius
        self.fill = fill
        self.outline = outline
        self.thickness = thickness
        self._texts = {}

        self.bind('<Configure>', lambda _event: self.redraw())
        if command is not None:
            self.bind('<Button-1>', lambda _event: command())

        self.redraw()

    def set_fill(self, colour: str) -> None:
        if colour != self.fill:
            self.fill = colour
            self.redraw()

    def set_text(self, tag: str, text: str, x: float, y: float, font=FONT_ROW,
                 colour: str = WHITE, anchor: str = 'w') -> None:
        self._texts[tag] = (text, x, y, font, colour, anchor)
        self.redraw()

    def draw_rounded(self, x0: float, y0: float, x1: float, y1: float, radius: float,
                     fill: str, outline: str, thickness: int = 2) -> None:
        '''Desenha uma forma arredondada decorativa que sobrevive aos redraws.'''
        self.create_polygon(rounded_rect_points(x0, y0, x1, y1, radius),
                            fill=fill, outline=outline, width=thickness, tags='deco')

    def redraw(self) -> None:
        self.delete('moldura')
        self.delete('texto')

        width = self.winfo_width()
        height = self.winfo_height()
        if width <= 1:
            width = self.winfo_reqwidth()
        if height <= 1:
            height = self.winfo_reqheight()

        inset = self.thickness / 2
        self.create_polygon(
            rounded_rect_points(inset, inset, width - inset, height - inset, self.radius),
            fill=self.fill, outline=self.outline, width=self.thickness, tags='moldura',
            joinstyle='round',
        )
        # A moldura é o pano de fundo: fica sempre atrás das decorações
        self.tag_lower('moldura')

        for text, x, y, font, colour, anchor in self._texts.values():
            self.create_text(x, y, text=text, font=font, fill=colour,
                             anchor=anchor, tags='texto')


class PokerChip(tk.Canvas):
    '''Ficha circular usada ao lado de cada prêmio e no placar.'''

    def __init__(self, master: tk.Widget, size: int = 20, fill: str = YELLOW_BTN,
                 edge: str = GREY_FRAME, parent_bg: str = GREEN_TABLE) -> None:
        super().__init__(master, width=size, height=size, bg=parent_bg,
                         highlightthickness=0, bd=0)
        rim = size * 0.06
        self.create_oval(rim, rim, size - rim, size - rim,
                         fill=fill, outline=edge, width=2)
        self.create_oval(size * 0.22, size * 0.22, size * 0.78, size * 0.78,
                         outline=WHITE, width=2, dash=(2, 2))
        self.create_oval(size * 0.41, size * 0.41, size * 0.59, size * 0.59,
                         fill=edge, outline='')


# ------------------------------------------------------------------
# Aplicação
# ------------------------------------------------------------------
class PokerApp(tk.Tk):
    '''Janela principal.'''

    PAD = 16
    LEFT_W = 372
    RIGHT_W = 640
    CONTENT_H = 628
    RULE_W = 340
    RULE_H = 30
    CARD_W = 94
    CARD_H = 130

    def __init__(self, poker: VideoPoker) -> None:
        super().__init__()
        self.poker = poker
        self.held = set()
        self.rounds = 0
        self.wins = 0
        self.last_hand = None

        self.title('Video Poker')
        self.configure(bg=GREEN_TABLE)
        self.resizable(False, False)

        self._build_left_panel()
        self._build_right_panel()
        self.update_view()
        self._center_window()

    def _center_window(self) -> None:
        self.update_idletasks()
        x = max((self.winfo_screenwidth() - self.winfo_width()) // 2, 0)
        y = max((self.winfo_screenheight() - self.winfo_height()) // 3, 0)
        self.geometry(f'+{x}+{y}')

    # ---------------- painel esquerdo: 12 RoundedBox ----------------
    def _build_left_panel(self) -> None:
        self.left = tk.Frame(self, bg=GREEN_TABLE, width=self.LEFT_W,
                             height=self.CONTENT_H, highlightthickness=2,
                             highlightbackground=GREY_FRAME, bd=0)
        self.left.pack(side='left', padx=(self.PAD, 0), pady=self.PAD)
        self.left.pack_propagate(False)

        self._build_paytable()   # 1 cabeçalho + 9 linhas = 10
        self._build_score()      # 1 cabeçalho + 1 placar    =  2
        self._build_stats()

    def _build_paytable(self) -> None:
        header = RoundedBox(self.left, width=self.RULE_W, height=40, radius=10,
                            fill=GREY_FRAME, outline=GREY_FILLET, parent_bg=GREEN_TABLE)
        header.pack(pady=(12, 10))
        header.set_text('title', 'REGRAS', self.RULE_W / 2, 20,
                        font=FONT_HEADER, colour=WHITE, anchor='center')

        self.rows = {}
        self.row_chips = {}

        for hand, label in PAYTABLE:
            row = RoundedBox(self.left, width=self.RULE_W, height=self.RULE_H, radius=7,
                             fill=GREY_FILLET, outline=GREY_FRAME, parent_bg=GREEN_TABLE)
            row.pack(pady=1)
            row.set_text('name', label, 14, self.RULE_H / 2,
                         font=FONT_ROW, colour=WHITE, anchor='w')
            row.set_text('value', str(hand.value), self.RULE_W - 14, self.RULE_H / 2,
                         font=FONT_ROW, colour=YELLOW_BTN, anchor='e')

            chip = PokerChip(row, size=18, parent_bg=GREY_FILLET)
            chip.place(x=self.RULE_W - 56, y=(self.RULE_H - 18) / 2)

            self.rows[hand] = row
            self.row_chips[hand] = chip

    def _build_score(self) -> None:
        header = RoundedBox(self.left, width=self.RULE_W, height=34, radius=10,
                            fill=GREY_FRAME, outline=GREY_FILLET, parent_bg=GREEN_TABLE)
        header.pack(pady=(16, 8))
        header.set_text('title', 'SCORE', self.RULE_W / 2, 17,
                        font=FONT_HEADER, colour=WHITE, anchor='center')

        box = RoundedBox(self.left, width=self.RULE_W, height=120, radius=10,
                         fill=GREY_FRAME, outline=GREY_FILLET, parent_bg=GREEN_TABLE)
        box.pack()

        # Círculo "PONTOS" e moldura interna: itens decorativos do próprio canvas
        box.create_oval(18, 18, 102, 102, fill=WHITE, outline=GREY_FRAME,
                        width=2, tags='deco')
        box.create_text(60, 60, text='PONTOS', font=FONT_SMALL,
                        fill=GREY_FRAME, tags='deco')
        box.draw_rounded(112, 14, 326, 106, 8, WHITE, GREY_FRAME, 2)

        box.set_text('caption', 'PONTUAÇÃO', 124, 30, font=FONT_SMALL,
                     colour=GREY_FRAME, anchor='w')
        box.set_text('total', '0', 164, 66, font=FONT_SCORE,
                     colour=GREY_FRAME, anchor='w')
        box.set_text('money', 'TOTAL $$$', 124, 94, font=FONT_SMALL,
                     colour=YELLOW_BTN, anchor='w')

        self.score_chip = PokerChip(box, size=26, parent_bg=WHITE)
        self.score_chip.place(x=126, y=46)
        self.score_box = box

    def _build_stats(self) -> None:
        cells = tk.Frame(self.left, bg=GREEN_TABLE)
        cells.pack(pady=(14, 0))

        tk.Label(cells, text='', bg=GREEN_TABLE, font=FONT_SMALL).grid(row=0, column=0)
        tk.Label(cells, text='VITÓRIAS', bg=GREEN_TABLE, fg=WHITE,
                 font=FONT_SMALL).grid(row=0, column=1)
        tk.Label(cells, text='ROUND', bg=GREEN_TABLE, fg=WHITE,
                 font=FONT_SMALL).grid(row=0, column=2)

        def cell(column: int, text: str) -> tk.Label:
            label = tk.Label(cells, text=text, bg=GREY_FILLET, fg=WHITE,
                             font=FONT_SMALL, width=13, height=2, bd=1, relief='solid')
            label.grid(row=1, column=column, padx=4)
            return label

        self.options_label = cell(0, 'OPÇÕES')
        self.wins_label = cell(1, '0')
        self.rounds_label = cell(2, '0')

    # ---------------- painel direito: 6 RoundedBox ----------------
    def _build_right_panel(self) -> None:
        self.right = tk.Frame(self, bg=GREEN_TABLE, width=self.RIGHT_W,
                              height=self.CONTENT_H)
        self.right.pack(side='left', padx=self.PAD, pady=self.PAD)
        self.right.pack_propagate(False)

        self._build_title()
        self._build_actions()
        self._build_status()
        self._build_cards()

    def _build_title(self) -> None:
        row = tk.Frame(self.right, bg=GREEN_TABLE)
        row.pack(fill='x', pady=(26, 0))
        row.grid_columnconfigure(0, weight=1)
        row.grid_columnconfigure(2, weight=1)

        tk.Frame(row, bg=WHITE, height=2).grid(row=0, column=0, sticky='ew', padx=(0, 16))
        tk.Label(row, text='VIDEO POKER', bg=GREEN_TABLE, fg=WHITE,
                 font=FONT_TITLE).grid(row=0, column=1)
        tk.Frame(row, bg=WHITE, height=2).grid(row=0, column=2, sticky='ew', padx=(16, 0))

    def _build_cards(self) -> None:
        holder = tk.Frame(self.right, bg=GREEN_TABLE)
        holder.pack(side='bottom', pady=(0, 10))

        self.card_boxes = []
        self.hold_labels = []

        for index in range(self.poker.HAND_SIZE):
            slot = tk.Frame(holder, bg=GREEN_TABLE)
            slot.pack(side='left', padx=7)

            hold = tk.Label(slot, text='HELD', bg=GREEN_TABLE, fg=GREEN_TABLE,
                            font=FONT_HOLD)
            hold.pack(pady=(0, 4))

            box = RoundedBox(slot, width=self.CARD_W, height=self.CARD_H, radius=9,
                             fill=WHITE, outline=GREY_FRAME, parent_bg=GREEN_TABLE,
                             command=lambda i=index: self.toggle_hold(i))
            box.pack()

            self.card_boxes.append(box)
            self.hold_labels.append(hold)

    def _build_status(self) -> None:
        self.status = tk.Label(self.right, text='', bg=GREEN_TABLE, fg=WHITE,
                               font=FONT_STATUS)
        self.status.pack(side='bottom', pady=(0, 14))

    def _build_actions(self) -> None:
        row = tk.Frame(self.right, bg=GREEN_TABLE)
        row.pack(side='bottom', pady=(0, 20))

        self.action_btn = RoundedBox(row, width=430, height=70, radius=18,
                                     fill=BLUE_BTN, outline=GREY_FRAME,
                                     parent_bg=GREEN_TABLE, command=self.action)
        self.action_btn.pack(side='left')
        self.action_btn.set_text('label', 'DEAL', 215, 35, font=FONT_BUTTON,
                                 colour=WHITE, anchor='center')

        deck_holder = tk.Frame(row, bg=GREEN_TABLE)
        deck_holder.pack(side='left', padx=(26, 0))
        deck = tk.Frame(deck_holder, bg=GREY_FRAME, width=78, height=118,
                        highlightthickness=2, highlightbackground=GREY_FILLET, bd=0)
        deck.pack_propagate(False)
        deck.pack()
        tk.Label(deck, text='\U0001F0A0', bg=GREY_FRAME, fg=BLUE_BTN,
                 font=FONT_BACK).pack(expand=True)

    # ---------------- modelo -> tela ----------------
    def update_view(self) -> None:
        self._render_cards()
        self._render_paytable()
        self._render_score()
        self._render_action()
        self._render_stats()

    def _render_cards(self) -> None:
        for index in range(self.poker.HAND_SIZE):
            if index < len(self.poker.cards):
                symbol = str(self.poker.cards[index])
            else:
                symbol = ''

            held = index in self.held
            box = self.card_boxes[index]
            box.set_fill(GREY_LIGHT if held else WHITE)
            box.set_text('face', symbol, self.CARD_W / 2, self.CARD_H / 2,
                         font=FONT_CARD,
                         colour=RED_BTN if is_red_suit(symbol) else BLACK,
                         anchor='center')
            self.hold_labels[index].configure(fg=YELLOW_BTN if held else GREEN_TABLE)

    def _render_paytable(self) -> None:
        for hand, (label, row) in self._paytable_entries().items():
            active = hand is self.last_hand
            row.set_fill(YELLOW_BTN if active else GREY_FILLET)
            self.row_chips[hand].configure(bg=YELLOW_BTN if active else GREY_FILLET)
            row.set_text('name', label, 14, self.RULE_H / 2, font=FONT_ROW,
                         colour=GREY_FRAME if active else WHITE, anchor='w')
            row.set_text('value', str(hand.value), self.RULE_W - 14, self.RULE_H / 2,
                         font=FONT_ROW,
                         colour=GREY_FRAME if active else YELLOW_BTN, anchor='e')

    def _paytable_entries(self) -> dict:
        if not hasattr(self, '_entries'):
            self._entries = {hand: (label, self.rows[hand]) for hand, label in PAYTABLE}
        return self._entries

    def _render_score(self) -> None:
        self.score_box.set_text('total', str(self.poker.points), 164, 66,
                                font=FONT_SCORE, colour=GREY_FRAME, anchor='w')

    def _render_action(self) -> None:
        ready = self.poker.phase is Phase.READY
        self.action_btn.set_fill(BLUE_BTN if ready else RED_BTN)
        self.action_btn.set_text('label', 'DEAL' if ready else 'DRAW', 215, 35,
                                 font=FONT_BUTTON, colour=WHITE, anchor='center')

    def _render_stats(self) -> None:
        self.wins_label.configure(text=str(self.wins))
        self.rounds_label.configure(text=str(self.rounds))

    # ---------------- eventos ----------------
    def toggle_hold(self, index: int) -> None:
        if self.poker.phase is not Phase.HOLDING:
            self.status.configure(text='Dê as cartas primeiro')
            return

        if index in self.held:
            self.held.discard(index)
        else:
            self.held.add(index)
        self.update_view()

    def action(self) -> None:
        try:
            if self.poker.phase is Phase.READY:
                self.poker.deal()
                self.held.clear()
                self.last_hand = None
                self.rounds += 1
                self.status.configure(text='Clique nas cartas que quer manter')
            else:
                self.poker.draw(self.held)
                self.held.clear()
                self.last_hand = self.poker.hand_type()
                if self.last_hand is not HandType.NOTHING:
                    self.wins += 1
                self.status.configure(text=self._result_text())
        except ValueError as error:
            # O stub lança ValueError; o modelo real vai lançar GameError
            self.status.configure(text=str(error))

        self.update_view()

    def _result_text(self) -> str:
        if self.last_hand is None or self.last_hand is HandType.NOTHING:
            return 'Nenhuma combinação'
        name = HAND_NAMES.get(self.last_hand, '')
        return f'{name}  +{self.poker.current_points} pontos'


def main() -> None:
    app = PokerApp(VideoPoker())
    app.mainloop()


if __name__ == '__main__':
    main()
