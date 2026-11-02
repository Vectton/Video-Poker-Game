# 🃏 Video Poker — Jacks or Better

Projeto prático desenvolvido em Python aplicando os pilares de Orientação a Objetos (encapsulamento, herança, classes abstratas, enumerações, sobrecarga de operadores e tratamento de exceções).

---

## 👥 Equipe e Docente

* **Integrantes:**
  * HEVERTON JOSE COSTA OLIVEIRA
  * GABRIEL MORAES DE OLIVEIRA
  * DAVI GABRIEL BATISTA MACIEL
  * HENRIQUE TAVARES POLLI
  * ARTHUR SILVA SANTOS
* **Professor(a):**
  * EFREN LOPES DE SOUZA
* **Disciplina:** Programação Orientada a Objetos (POO)

---

## 🚀 Como Inicializar o Jogo

O projeto foi construído utilizando apenas módulos da biblioteca padrão do Python. Não é necessário instalar nenhuma dependência externa!

### Opção 1: Clonar o repositório (Git)

Abra o terminal (ou Prompt de Comando / PowerShell) e execute:

```
git clone https://github.com/Vectton/Video-Poker-Game.git
cd Video-Poker-Game

```

### Opção 2: Baixar os arquivos completos (ZIP)

Caso não queira ou não tenha o Git instalado:

1. Acesse a página principal do repositório no GitHub: `https://github.com/Vectton/Video-Poker-Game`.

2. Clique no botão verde **Code**.

3. Selecione a opção **Download ZIP**.

4. Extraia o arquivo `.zip` no seu computador e navegue até a pasta extraída usando o terminal ou prompt de comando.

### 🎮 Caso A: Jogar pela Interface Gráfica (GUI)

Para abrir o jogo com a interface visual interativa (feita em Tkinter):

```
python poker_gui.py

```

* **Como jogar na GUI:**

  1. Clique em **DEAL** para receber as cartas.

  2. Clique nas cartas que deseja manter (o botão vermelho **HELD** aparecerá sobre as selecionadas).

  3. Clique em **DRAW** para trocar as cartas restantes e conferir a combinação e os pontos obtidos.

### 💻 Caso B: Jogar pelo Terminal (CLI)

Para uma experiência direta no terminal de comando:

```
python poker_terminal.py

```

* **Como jogar no Terminal:**

  1. Pressione `[ENTER]` para dar as cartas (`deal`).

  2. Digite as posições das cartas que deseja manter separadas por espaço (exemplo: `1 3 4`) ou apenas aperte `[ENTER]` para trocar todas.

  3. O terminal avaliará a mão final e exibirá a pontuação acumulada.

## 📂 Estrutura do Projeto

```
├── card.py              # Classes Card, Rank e Suit (regras e representação Unicode)
├── card_collections.py  # Coleção abstrata CardCollection, Baralho (Stock) e Mão (Hand)
├── exceptions.py        # Hierarquia de exceções personalizadas (GameError)
├── poker.py             # Modelo principal (VideoPoker, Phase e HandType)
├── poker_gui.py         # Interface Gráfica com Tkinter
└── poker_terminal.py    # Interface via Terminal (Prompt)

```
