# game_engine.py

import random

CARD_COUNTS = {
    "Guard": (1, 5),
    "Priest": (2, 2),
    "Baron": (3, 2),
    "Handmaid": (4, 2),
    "Prince": (5, 2),
    "King": (6, 1),
    "Countess": (7, 1),
    "Princess": (8, 1),
}

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.protected = False
        self.out = False
        self.discards = []

class LoveLetterGameEngine:
    def __init__(self, player_names):
        self.players = [Player(n) for n in player_names]
        self.deck = []
        self.hidden = None
        self.discard_pile = []
        self.current_index = 0
        self.has_drawn = False
        self.scores = {p.name: 0 for p in self.players}
        self.log = []

    def start_round(self):
        self.deck = []
        for name, (value, count) in CARD_COUNTS.items():
            self.deck += [(name, value)] * count
        random.shuffle(self.deck)
        self.hidden = self.deck.pop()
        for p in self.players:
            p.hand = [self.deck.pop()]
            p.out = False
            p.protected = False
            p.discards = []
        self.current_index = 0
        self.has_drawn = False
        self.log = []

    def get_game_state(self, for_player=None):
        state = {
            "players": [
                {
                    "name": p.name,
                    "hand_count": len(p.hand) if for_player != p.name else [c[0] for c in p.hand],
                    "protected": p.protected,
                    "out": p.out,
                    "discards": p.discards,
                }
                for p in self.players
            ],
            "deck_count": len(self.deck),
            "discard_pile": self.discard_pile,
            "log": self.log[-10:],  # last 10 entries
            "current_player": self.players[self.current_index].name,
        }
        return state

    # Placeholder for play_card logic
    def play_card(self, player_name, card_index, target_name=None, guess=None):
        player = next(p for p in self.players if p.name == player_name)
        card = player.hand.pop(card_index)
        self.discard_pile.append((player.name, card[0]))
        self.log.append(f"{player.name} played {card[0]}")
        # TODO: implement Guard, Baron, Prince, etc.
        self.next_turn()
        return self.get_game_state()

    def next_turn(self):
        alive = [p for p in self.players if not p.out]
        if len(alive) <= 1:
            return  # round over
        self.current_index = (self.current_index + 1) % len(self.players)
