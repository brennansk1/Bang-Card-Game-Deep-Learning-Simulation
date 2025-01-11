from enums import Suit, Value

class Card:
    """
    Represents a playing card in Bang!: has suit, value, and a 'name' for the effect.
    E.g., suit=Hearts, value=3, name="Bang!"
    """
    def __init__(self, suit: Suit, value: Value, name: str):
        self.suit = suit
        self.value = value
        self.name = name

    def __repr__(self):
        return f"{self.name}({self.suit.name}, {self.value.name})"
