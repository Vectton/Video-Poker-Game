import math
import tkinter as tk

from card import Card, Suit
from exceptions import GameError
from poker import HandType, Phase, VideoPoker

# ------------------------------------------------------------------
# Paleta
# ------------------------------------------------------------------
GREEN_TABLE = '#316b52'
GREEN_FRAME = "#285844"
GREEN_BTN = '#2da16a'
RED_BTN = '#f54237'
GREY_FILLET = '#2b3638'
GREY_FRAME = '#172224'
GREY_BORDER = '#0d181a'
BLUE_BTN = '#0189f4'
BLUE_FRAME = '#021059'
YELLOW_BTN = '#fa9003'
YELLOW_FRAME = '#4f4015'
YELLOW_FILLET = '#986200'
YELLOW_COIN = '#df9830'
YELLOW_WIN = "#dfd330"
WHITE = '#ffffff'
BLACK = '#000000'
GREY_LIGHT = '#dfe3e6'
GREY_MID_LIGHT = "#8b8b8b"

# ------------------------------------------------------------------
# Tipografia
# ------------------------------------------------------------------
FAMILY_TEXT = 'Courier New'
FAMILY_RULE = 'Segoe UI Symbol'
FAMILY_CARD = 'Impact'

FONT_TITLE = (FAMILY_TEXT, 30, 'bold')
FONT_HEADER = (FAMILY_TEXT, 18, 'bold')
FONT_ROW = (FAMILY_TEXT, 11, 'bold')
FONT_SMALL = (FAMILY_TEXT, 9, 'bold')
FONT_HOLD = (FAMILY_TEXT, 15, 'bold')
FONT_BUTTON = (FAMILY_TEXT, 34, 'bold')
FONT_STATUS = (FAMILY_TEXT, 16, 'bold')
FONT_SCORE = (FAMILY_TEXT, 26, 'bold')
FONT_CHIP = (FAMILY_TEXT, 10, 'bold')
FONT_CARD = (FAMILY_CARD, 102)
FONT_BACK = (FAMILY_CARD, 44)
FONT_COIN = (FAMILY_CARD, 20)
FONT_RULE = (FAMILY_RULE, 14)
FONT_RADIUS = (FAMILY_RULE, 14, 'bold')
FONT_RULE_VALUE = (FAMILY_CARD, 16)

ARC_STEPS = 8


# ------------------------------------------------------------------
# Tabela de pontuação
# ------------------------------------------------------------------
PAYTABLE = (
    (HandType.ROYAL_FLUSH, 'ROYAL FLUSH'),
    (HandType.STRAIGHT_FLUSH, 'STRAIGHT FLUSH'),
    (HandType.FOUR_OF_A_KIND, 'QUADRA'),
    (HandType.FULL_HOUSE, 'FULL HOUSE'),
    (HandType.FLUSH, 'FLUSH'),
    (HandType.STRAIGHT, 'SEQUÊNCIA'),
    (HandType.THREE_OF_A_KIND, 'TRINCA'),
    (HandType.TWO_PAIR, 'DOIS PARES'),
    (HandType.JACKS_OR_BETTER, 'JACKS OR BETTER'),
)

HAND_NAMES = {hand: name for hand, name in PAYTABLE}

# ------------------------------------------------------------------
# Formas
# ------------------------------------------------------------------
#----------------- bordas arrendodadas -------------------
def rounded_rect_points(x0: float, y0: float, x1: float, y1: float,
                        radius: float, steps: int = ARC_STEPS) -> list:
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

# ------------ Para as copas e ouros -------------
def is_red_card(card: Card) -> bool:
    if not card.is_face_up:
        return False
    return card.suit in (Suit.HEARTS, Suit.DIAMONDS)


# ------------------------------------------------------------------
# Componentes
# ------------------------------------------------------------------
# ---------------- Canvas das molduras ----------------
class RoundedBox(tk.Canvas):
    def __init__(self, master: tk.Widget, width: int, height: int, radius: int = 8,
                 fill: str = WHITE, outline: str = GREY_FILLET, thickness: int = 2,
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
        self.tag_lower('moldura')

        for text, x, y, font, colour, anchor in self._texts.values():
            self.create_text(x, y, text=text, font=font, fill=colour,
                             anchor=anchor, tags='texto')

# --------- Ficha de Poker -------------------
class PokerChip(tk.Canvas):
    def __init__(self, master: tk.Widget, size: int = 24, label: str = '',
                 bg: str = GREY_LIGHT) -> None:
        super().__init__(master, width=size, height=size, bg=bg,
                         highlightthickness=0, bd=0)
        self.size = size
        self.label = label
        self.draw()

    def draw(self) -> None:
        self.delete('all')
        size = self.size
        self.create_oval(1, 1, size - 1, size - 1,
                         fill=GREY_LIGHT, outline=GREY_FRAME, width=2)

        if not self.label and size >= 22:
            radius = size * 0.41
            x = self.size / 2
            y = self.size / 2
            
            for angle in range(0, 360, 45):
                a = math.radians(angle)
                x1, y1 = x + math.cos(a) * radius * 0.72, y + math.sin(a) * radius * 0.72
                x2, y2 = x + math.cos(a) * radius, y + math.sin(a) * radius
                self.create_line(x1, y1, x2, y2, fill=GREY_MID_LIGHT, width=5)

        inner = size * (0.22 if self.label else 0.34)
        self.create_oval(inner, inner, size - inner, size - inner,
                         fill=GREY_MID_LIGHT, outline=GREY_MID_LIGHT)

        if self.label:
            self.create_oval(1, 1, size - 1, size - 1,
                             fill=YELLOW_COIN, outline=YELLOW_FILLET, width=3)
            self.create_text(size / 2, size / 2, text=self.label,
                             fill=GREY_FRAME, font=FONT_COIN)


# ------------------------------------------------------------------
# Interface
# ------------------------------------------------------------------
class PokerApp(tk.Tk):
    PAD = 16
    LEFT_W = 352
    RIGHT_W = 640
    CONTENT_H = 672
    RULE_W = 340
    PANEL_H = 344
    ROW_H = 36
    ROW_W = 316
    SCORE_H = 136
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
        y = max((self.winfo_screenheight() - self.winfo_height()) // 33, 0)
        self.geometry(f'+{x}+{y}')

# -------------- Painel esquerdo ------------------
    def _build_left_panel(self) -> None:
        self.left = tk.Frame(self, bg=GREY_FILLET, width=self.LEFT_W,
                             height=self.CONTENT_H)
        self.left.pack(side='left', padx=(0, 0), pady=(0,0))
        self.left.pack_propagate(False)

        self._build_paytable()
        self._build_score()
        self._build_stats()

    def _build_paytable(self) -> None:
        header = RoundedBox(self.left, width=self.RULE_W, height=40, radius=10,
                            fill=BLUE_FRAME, outline=GREY_BORDER, parent_bg=GREY_FILLET)
        header.pack(pady=(12, 8))
        header.set_text('title', 'REGRAS', self.RULE_W / 2, 20,
                        font=FONT_TITLE, colour=GREY_LIGHT, anchor='center')

        panel = RoundedBox(self.left, width=self.RULE_W, height=self.PANEL_H,
                           radius=14, fill=GREY_FRAME, outline=GREY_FILLET,
                           thickness=2, parent_bg=GREY_FILLET)
        panel.pack()
        panel.draw_rounded(4, 4, self.RULE_W - 4, self.PANEL_H - 4, 12,
                           '', GREY_BORDER, 3)

        top = (self.PANEL_H - len(PAYTABLE) * self.ROW_H) / 2
        self.rules_panel = panel
        self.rule_rows = []

        for index, (hand, label) in enumerate(PAYTABLE):
            row_top = top + index * self.ROW_H

            row = tk.Canvas(panel, width=self.ROW_W, height=self.ROW_H - 4,
                            bg=GREY_FILLET, highlightthickness=0, bd=0)
            row.place(x=12, y=row_top + 2)

            middle = (self.ROW_H - 4) / 2
            name = row.create_text(6, middle, text=label, anchor='w',
                                   font=FONT_RULE, fill=WHITE)
            chip = PokerChip(row, size=30, bg=YELLOW_FRAME)
            chip.place(x=194, y=middle - 15)
            value = row.create_text(246, middle, text=str(hand.value), anchor='center',
                                    font=FONT_RULE_VALUE, fill=WHITE)

            if index < len(PAYTABLE) - 1:
                panel.create_line(20, row_top + self.ROW_H, self.RULE_W - 20,
                                  row_top + self.ROW_H, fill=GREY_FILLET, width=3,
                                  tags='deco')

            self.rule_rows.append({'hand': hand, 'row': row, 'name': name,
                                   'value': value, 'chip': chip})

    def _build_score(self) -> None:
        header = RoundedBox(self.left, width=self.RULE_W, height=36, radius=10,
                            fill=YELLOW_FILLET, outline=GREY_BORDER, parent_bg=GREY_FILLET)
        header.pack(pady=(12, 6))
        header.set_text('title', 'SCORE', self.RULE_W / 2, 18,
                        font=FONT_TITLE, colour=GREY_LIGHT, anchor='center')

        box = RoundedBox(self.left, width=self.RULE_W, height=self.SCORE_H, radius=12,
                         fill=YELLOW_FRAME, outline=GREY_BORDER, parent_bg=GREY_FILLET)
        box.pack()

        self.ponto_chip = PokerChip(box, size=96, label='PONTOS', bg=YELLOW_FRAME)
        self.ponto_chip.place(x=12, y=22)
        self.ponto_chip = PokerChip(box, size=56, label='PONTOS', bg=YELLOW_COIN)
        self.ponto_chip.place(x=32, y=42)

        box.draw_rounded(120, 12, 326, 128, 10, GREY_FRAME, GREY_BORDER, 2)
        box.set_text('caption', 'PONTUAÇÃO', 172, 28, font=FONT_HEADER,
                     colour=WHITE, anchor='w')
        box.set_text('total', '0', 186, 64, font=FONT_SCORE,
                     colour=WHITE, anchor='w')
        box.set_text('money', 'TOTAL $$$', 173, 104, font=FONT_HEADER,
                     colour=WHITE, anchor='w')

        self.score_chip = PokerChip(box, size=44, bg=GREY_FRAME)
        self.score_chip.place(x=134, y=42)
        self.score_box = box

    def _build_stats(self) -> None:
        cells = tk.Frame(self.left, bg=GREY_FILLET)
        cells.pack(pady=(10, 0))
        for column in range(3):
            cells.grid_columnconfigure(column, weight=1)

        self.options_box = self._stat_cell(cells, 0, 'NÃO PARE', YELLOW_BTN, WHITE, None)
        self.wins_box = self._stat_cell(cells, 1, 'VITÓRIAS', GREY_FRAME, WHITE, '0')
        self.rounds_box = self._stat_cell(cells, 2, 'ROUND', GREY_FRAME, WHITE, '0')

    def _stat_cell(self, parent: tk.Widget, column: int, caption: str, fill: str,
                   caption_colour: str, value) -> RoundedBox:
        box = RoundedBox(parent, width=108, height=56, radius=10, fill=fill,
                         outline=GREY_FILLET, parent_bg=GREY_FILLET)
        box.grid(row=0, column=column, padx=4)

        if value is None:
            box.set_text('caption', caption, 54, 28, font=FONT_RULE,
                         colour=caption_colour, anchor='center')
            return box

        box.set_text('caption', caption, 54, 15, font=FONT_RULE,
                     colour=caption_colour, anchor='center')
        box.draw_rounded(12, 26, 96, 48, 7, GREY_FILLET, GREY_FILLET, 1)
        box.set_text('value', value, 54, 37, font=FONT_RULE,
                     colour=WHITE, anchor='center')
        return box

# ---------- painel direito ----------------
    def _build_right_panel(self) -> None:
        self.right = tk.Frame(self, bg=GREEN_TABLE, width=self.RIGHT_W,
                              height=self.CONTENT_H)
        self.right.pack(side='left', padx=self.PAD, pady=0)
        self.right.pack_propagate(False)

        self._build_title()
        self._build_result_box()
        self._build_actions()
        self._build_cards()
        self._build_status()

    def _build_title(self) -> None:
        row = tk.Frame(self.right, bg=GREEN_TABLE)
        row.pack(fill='x', pady=(26, 0))
        row.grid_columnconfigure(0, weight=1)
        row.grid_columnconfigure(2, weight=1)

        tk.Frame(row, bg=WHITE, height=2).grid(row=0, column=0, sticky='ew', padx=(0, 16))
        tk.Label(row, text='VIDEO♕POKER', bg=GREEN_TABLE, fg=WHITE,
                 font=FONT_TITLE).grid(row=0, column=1)
        tk.Frame(row, bg=WHITE, height=2).grid(row=0, column=2, sticky='ew', padx=(16, 0))

    def _build_result_box(self) -> None:
        self.result_box = RoundedBox(self.right, width=460, height=96, radius=14,
                                     fill=RED_BTN, outline=GREY_BORDER, thickness=2,
                                     parent_bg=GREEN_TABLE)
        self.result_box.place_forget()

    def _build_cards(self) -> None:
        holder = RoundedBox(self.right, width=577, height=210, radius=18,
                            fill=GREEN_FRAME, outline=GREEN_FRAME, parent_bg=GREEN_TABLE)
        holder.pack(side='bottom', pady=(0, 10))

        inner = tk.Frame(holder, bg=GREEN_FRAME)
        inner.place(relx=0.5, rely=0.5, anchor='center')

        self.card_boxes = []
        self.hold_labels = []

        for index in range(self.poker.HAND_SIZE):
            slot = tk.Frame(inner, bg=GREEN_FRAME, width=self.CARD_W+4, height=180)
            slot.pack_propagate(False) 
            slot.pack(side='left', padx=7)

            hold = RoundedBox(slot, width=65, height=32, radius=9, 
                              fill=RED_BTN, outline=RED_BTN, parent_bg=GREEN_FRAME)
            hold.set_text('label', 'HELD', 32, 17, font=FONT_HOLD, colour=WHITE, anchor='center')
            
            box = RoundedBox(slot, width=self.CARD_W, height=self.CARD_H, radius=9,
                             fill=WHITE, outline=GREY_LIGHT, parent_bg=GREEN_FRAME,
                             command=lambda i=index: self.toggle_hold(i))

            box.place(x=0, y=46)

            self.hold_labels.append(hold)
            self.card_boxes.append(box)

    def _build_status(self) -> None:
        self.status = tk.Label(self.right, text='Pressione DEAL para dar as cartas',
                               bg=GREEN_TABLE, fg=WHITE, font=FONT_STATUS)
        self.status.pack(side='bottom', pady=(0, 10))

    def _build_actions(self) -> None:
        row = tk.Frame(self.right, bg=GREEN_TABLE)
        row.pack(side='bottom', pady=(0, 20))

        self.action_btn = RoundedBox(row, width=480, height=90, radius=18,
                                     fill=GREEN_FRAME, outline=GREEN_FRAME,
                                     parent_bg=GREEN_TABLE, command=self.action)
        
        self.action_btn.draw_rounded(148, 10, 326, 78, 10, GREEN_BTN, WHITE, 2)
        self.action_btn.pack(side='left')
        self.action_btn.set_text('label', 'DEAL', 235, 43, font=FONT_BUTTON,
                                 colour=WHITE, anchor='center')

        deck = RoundedBox(row, width=78, height=118, radius=9,
                          fill=WHITE, outline=GREY_LIGHT, parent_bg=GREEN_TABLE)
        deck.pack(side='left', padx=(26, 0))
        
        deck.set_text('back', chr(int(Card.BACK_UNICODE, 16)), 39, 35,
                      font=(FAMILY_CARD, 86), colour=RED_BTN, anchor='center')

# ----------- Atualizações de Exibição --------------
    def update_view(self) -> None:
        self._render_cards()
        self._render_paytable()
        self._render_score()
        self._render_action()
        self._render_stats()
        self._render_result_box()

    def _render_cards(self) -> None:
        cards = self.poker.cards
        is_result_phase = (self.poker.phase is Phase.READY and self.last_hand is not None)
        winning_indices = self.poker.winning_cards_indices() if is_result_phase else set()

        for index in range(self.poker.HAND_SIZE):
            card = cards[index] if index < len(cards) else None
            held = index in self.held
            box = self.card_boxes[index]

            if card is None:
                box.set_fill(WHITE) 
                box.set_text('back', chr(int(Card.BACK_UNICODE, 16)), 47, 45,
                             font=(FAMILY_CARD, 102), colour=RED_BTN, anchor='center')
            elif is_result_phase:
                if self.last_hand is not HandType.NOTHING:
                    box.set_fill(YELLOW_WIN if index in winning_indices else GREY_LIGHT)
                else:
                    box.set_fill(GREY_LIGHT)
                box.set_text('back', ' ', 47, 45,
                             font=FONT_CARD, colour=WHITE, anchor='center')
            else:
                box.set_fill(GREY_LIGHT if held else WHITE)
                box.set_text('back', ' ', 47, 45,
                             font=FONT_CARD, colour=WHITE, anchor='center')

            box.set_text('face', str(card) if card else '',
                         47, 45,
                         font=FONT_CARD,
                         colour=RED_BTN if card and is_red_card(card) else BLACK,
                         anchor='center')
            
            if held:
                self.hold_labels[index].place(x=16, y=0)
                box.place(x=0, y=34)
            else:
                self.hold_labels[index].place_forget()
                box.place(x=0, y=46)

    def _render_result_box(self) -> None:
        if self.poker.phase is Phase.READY and self.last_hand is not None:
            if self.last_hand is HandType.NOTHING:
                self.result_box.set_fill(RED_BTN)
                self.result_box.set_text('title', 'NENHUMA COMBINAÇÃO', 230, 34,
                                         font=FONT_SCORE, colour=WHITE, anchor='center')
                self.result_box.set_text('subtitle', 'TENTE NOVAMENTE', 230, 68,
                                         font=FONT_HEADER, colour=WHITE, anchor='center')
            else:
                name = HAND_NAMES.get(self.last_hand, '')
                self.result_box.set_fill(BLUE_BTN)
                self.result_box.set_text('title', name, 230, 34,
                                         font=FONT_SCORE, colour=WHITE, anchor='center')
                self.result_box.set_text('subtitle', f'+{self.poker.current_points} PONTOS', 230, 68,
                                         font=(FAMILY_CARD, 22), colour=YELLOW_WIN, anchor='center')
            self.result_box.place(x=90, y=140)
        else:
            self.result_box.place_forget()

    def _render_paytable(self) -> None:
        for entry in self.rule_rows:
            active = entry['hand'] is self.last_hand
            background = GREY_LIGHT if active else GREY_FRAME
            ink = GREY_FRAME if active else GREY_LIGHT

            entry['row'].configure(bg=background)
            entry['row'].itemconfigure(entry['name'], fill=ink)
            entry['row'].itemconfigure(entry['value'], fill=ink)
            entry['chip'].configure(bg=background)

    def _render_score(self) -> None:
        self.score_box.set_text('total', str(self.poker.points), 226, 64,
                                font=FONT_SCORE, colour=RED_BTN, anchor='w')

    def _render_action(self) -> None:
        ready = self.poker.phase is Phase.READY
        self.action_btn.draw_rounded(148, 10, 326, 78, 10, (GREEN_BTN if ready else RED_BTN), WHITE, 2)
        self.action_btn.set_text('label', 'DEAL' if ready else 'DRAW', 235, 43,
                                 font=FONT_BUTTON, colour=WHITE, anchor='center')

    def _render_stats(self) -> None:
        self.wins_box.set_text('value', str(self.wins), 54, 37,
                               font=FONT_RULE_VALUE, colour=YELLOW_BTN, anchor='center')
        self.rounds_box.set_text('value', str(self.rounds), 54, 37,
                                 font=FONT_RULE_VALUE, colour=YELLOW_BTN, anchor='center')

# ------------ Ações Ativadas ------------------
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
                hand = self.poker.draw(self.held)
                self.held.clear()
                self.last_hand = hand
                if hand is not HandType.NOTHING:
                    self.wins += 1
                self.status.configure(text='')
        except GameError as error:
            self.status.configure(text=str(error) or 'Ação inválida nesta fase')

        self.update_view()


def main() -> None:
    app = PokerApp(VideoPoker())
    app.mainloop()

if __name__ == '__main__':
    main()
