from enum import Enum, auto

class Suit(Enum):
    CLUBS = auto()
    DIAMONDS = auto()
    HEARTS = auto()
    SPADES = auto()

    def __str__(self):
        return self.name.capitalize()

class Value(Enum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

    def __str__(self):
        if self == Value.ACE:
            return "A"
        elif self.value <= 10:
            return str(self.value)
        elif self == Value.JACK:
            return "J"
        elif self == Value.QUEEN:
            return "Q"
        elif self == Value.KING:
            return "K"
        return str(self.value)

class Role(Enum):
    SHERIFF = auto()
    DEPUTY = auto()
    OUTLAW = auto()
    RENEGADE = auto()
