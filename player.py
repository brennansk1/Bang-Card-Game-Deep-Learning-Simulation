from enums import Role
from card import Card

class Player:
    """
    A single Bang! player, storing:
      - role (Sheriff, Deputy, Outlaw, Renegade)
      - character name
      - health, max_health
      - a hand of Card objects
      - whether eliminated
      - equipment flags, etc.
    """

    def __init__(self, player_id: int, role: Role, character_name: str, max_health: int):
        self.player_id = player_id
        self.role = role
        self.character_name = character_name
        self.max_health = max_health

        # If Sheriff, +1 HP
        if role == Role.SHERIFF:
            self.max_health += 1

        self.health = self.max_health
        self.hand = []
        self.eliminated = False

        # Equipment
        self.weapon = None
        self.mustang = 0
        self.scope = 0
        self.barrel = 0

        self.in_jail = False
        self.dynamite = False

        # Track usage of Bang this turn if not Volcanic/Willy
        self.bang_used_this_turn = 0

    def __repr__(self):
        return (f"Player[{self.player_id}] {self.character_name} "
                f"({self.role.name}), HP:{self.health}/{self.max_health}")

    def take_damage(self, amount=1):
        self.health -= amount
        if self.health <= 0:
            self.eliminate()

    def eliminate(self):
        self.health = 0
        self.eliminated = True
        self.hand.clear()

    def heal(self, amount=1):
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health
