import random
from enums import Suit, Value
from card import Card

def create_official_deck():
    """
    Return a list of Card objects approximating the official 80-card Bang! base deck.
    """

    official_cards_data = [
        # ---- 25 Bang! ----
        (Suit.SPADES,   Value.TWO,   "Bang!"),
        (Suit.SPADES,   Value.THREE, "Bang!"),
        (Suit.SPADES,   Value.FOUR,  "Bang!"),
        (Suit.SPADES,   Value.FIVE,  "Bang!"),
        (Suit.SPADES,   Value.SIX,   "Bang!"),
        (Suit.SPADES,   Value.SEVEN, "Bang!"),
        (Suit.SPADES,   Value.EIGHT, "Bang!"),
        (Suit.SPADES,   Value.NINE,  "Bang!"),
        (Suit.SPADES,   Value.TEN,   "Bang!"),
        (Suit.SPADES,   Value.JACK,  "Bang!"),
        (Suit.CLUBS,    Value.TWO,   "Bang!"),
        (Suit.CLUBS,    Value.THREE, "Bang!"),
        (Suit.CLUBS,    Value.FOUR,  "Bang!"),
        (Suit.CLUBS,    Value.FIVE,  "Bang!"),
        (Suit.CLUBS,    Value.SIX,   "Bang!"),
        (Suit.CLUBS,    Value.SEVEN, "Bang!"),
        (Suit.CLUBS,    Value.EIGHT, "Bang!"),
        (Suit.CLUBS,    Value.NINE,  "Bang!"),
        (Suit.CLUBS,    Value.TEN,   "Bang!"),
        (Suit.CLUBS,    Value.JACK,  "Bang!"),
        (Suit.CLUBS,    Value.QUEEN, "Bang!"),
        (Suit.CLUBS,    Value.KING,  "Bang!"),
        (Suit.HEARTS,   Value.FIVE,  "Bang!"),
        (Suit.HEARTS,   Value.SIX,   "Bang!"),
        (Suit.HEARTS,   Value.SEVEN, "Bang!"),

        # ---- 12 Missed! ----
        (Suit.SPADES,   Value.ACE,   "Missed!"),
        (Suit.HEARTS,   Value.EIGHT, "Missed!"),
        (Suit.HEARTS,   Value.NINE,  "Missed!"),
        (Suit.HEARTS,   Value.TEN,   "Missed!"),
        (Suit.HEARTS,   Value.JACK,  "Missed!"),
        (Suit.HEARTS,   Value.QUEEN, "Missed!"),
        (Suit.DIAMONDS, Value.TWO,   "Missed!"),
        (Suit.DIAMONDS, Value.THREE, "Missed!"),
        (Suit.DIAMONDS, Value.FOUR,  "Missed!"),
        (Suit.DIAMONDS, Value.FIVE,  "Missed!"),
        (Suit.DIAMONDS, Value.SIX,   "Missed!"),
        (Suit.DIAMONDS, Value.SEVEN, "Missed!"),

        # ---- 6 Beer ----
        (Suit.HEARTS,   Value.TWO,   "Beer"),
        (Suit.HEARTS,   Value.THREE, "Beer"),
        (Suit.HEARTS,   Value.FOUR,  "Beer"),
        (Suit.HEARTS,   Value.ACE,   "Beer"),
        (Suit.DIAMONDS, Value.EIGHT, "Beer"),
        (Suit.DIAMONDS, Value.NINE,  "Beer"),

        # ---- 1 Saloon ----
        (Suit.HEARTS,   Value.KING,  "Saloon"),

        # ---- 2 Stagecoach ----
        (Suit.DIAMONDS, Value.TEN,   "Stagecoach"),
        (Suit.DIAMONDS, Value.JACK,  "Stagecoach"),

        # ---- 1 Wells Fargo ----
        (Suit.HEARTS,   Value.TEN,   "Wells Fargo"),

        # ---- 4 Cat Balou ----
        (Suit.DIAMONDS, Value.QUEEN, "Cat Balou"),
        (Suit.DIAMONDS, Value.KING,  "Cat Balou"),
        (Suit.HEARTS,   Value.QUEEN, "Cat Balou"),
        (Suit.HEARTS,   Value.KING,  "Cat Balou"),

        # ---- 4 Panic! ----
        (Suit.HEARTS,   Value.NINE,  "Panic!"),
        (Suit.HEARTS,   Value.JACK,  "Panic!"),
        (Suit.DIAMONDS, Value.FOUR,  "Panic!"),
        (Suit.DIAMONDS, Value.FIVE,  "Panic!"),

        # ---- 2 General Store ----
        (Suit.CLUBS,    Value.NINE,  "General Store"),
        (Suit.CLUBS,    Value.QUEEN, "General Store"),

        # ---- 2 Indians! ----
        (Suit.DIAMONDS, Value.TEN,   "Indians!"),
        (Suit.DIAMONDS, Value.JACK,  "Indians!"),

        # ---- 3 Duel ----
        (Suit.SPADES,   Value.EIGHT, "Duel"),
        (Suit.SPADES,   Value.NINE,  "Duel"),
        (Suit.SPADES,   Value.TEN,   "Duel"),

        # ---- 1 Gatling ----
        (Suit.HEARTS,   Value.SEVEN, "Gatling"),

        # ---- 3 Jail ----
        (Suit.SPADES,   Value.FOUR,  "Jail"),
        (Suit.SPADES,   Value.FIVE,  "Jail"),
        (Suit.SPADES,   Value.SIX,   "Jail"),

        # ---- 1 Dynamite ----
        (Suit.SPADES,   Value.TWO,   "Dynamite"),

        # ---- 2 Volcanic ----
        (Suit.CLUBS,    Value.FOUR,  "Volcanic"),
        (Suit.CLUBS,    Value.FIVE,  "Volcanic"),

        # ---- 3 Schofield ----
        (Suit.CLUBS,    Value.EIGHT, "Schofield"),
        (Suit.CLUBS,    Value.JACK,  "Schofield"),
        (Suit.DIAMONDS, Value.ACE,   "Schofield"),

        # ---- 1 Remington ----
        (Suit.CLUBS,    Value.SEVEN, "Remington"),

        # ---- 1 Rev. Carbine ----
        (Suit.CLUBS,    Value.TWO,   "Rev. Carbine"),

        # ---- 1 Winchester ----
        (Suit.CLUBS,    Value.THREE, "Winchester"),

        # ---- 2 Mustang ----
        (Suit.HEARTS,   Value.EIGHT, "Mustang"),
        (Suit.HEARTS,   Value.NINE,  "Mustang"),

        # ---- 1 Scope ----
        (Suit.CLUBS,    Value.ACE,   "Scope"),

        # ---- 2 Barrel ----
        (Suit.SPADES,   Value.QUEEN, "Barrel"),
        (Suit.SPADES,   Value.KING,  "Barrel"),
    ]

    cards = []
    for (suit, value, name) in official_cards_data:
        cards.append(Card(suit, value, name))

    return cards

class Deck:
    """
    Manages a draw pile (cards) and a discard pile.
    """

    def __init__(self):
        self.cards = create_official_deck()
        self.discard_pile = []

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        if not self.cards:
            # reshuffle from discard
            if self.discard_pile:
                self.cards = self.discard_pile[:]
                self.discard_pile.clear()
                self.shuffle()
            else:
                return None
        if self.cards:
            return self.cards.pop()
        return None

    def discard(self, card: Card):
        self.discard_pile.append(card)

    def __len__(self):
        return len(self.cards)

    def discard_count(self):
        return len(self.discard_pile)
