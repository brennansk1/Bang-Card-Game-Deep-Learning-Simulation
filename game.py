import random

class BangGame:
    def __init__(self, players, max_turns=1000, verbose=True):
        if not isinstance(players, list):
            raise TypeError("Expected a list of players for BangGame initialization.")
        self.players = players
        self.deck = self.create_deck()
        self.discard_pile = []
        self.turn = 0
        self.cards_per_turn = 2
        self.current_player = 0
        self.max_turns = max_turns
        self.verbose = verbose  # Verbose flag for print control

    def create_deck(self):
        """Create a deck with all possible Bang! cards."""
        return (
            ['Bang!'] * 15 +
            ['Miss'] * 6 +
            ['Beer'] * 8 +
            ['Panic!'] * 4 +
            ['Cat Balou'] * 4 +
            ['Gatling'] * 2 +
            ['Indians!'] * 2 +
            ['Duel'] * 3 +
            ['General Store'] * 2 +
            ['Saloon'] * 1 +
            ['Wells Fargo'] * 1 +
            ['Stagecoach'] * 1 +
            ['Dynamite'] * 2 +
            ['Jail'] * 3 +
            ['Barrel'] * 2
        )

    def shuffle_deck(self):
        """Shuffle the deck."""
        random.shuffle(self.deck)

    def deal_cards(self, cards_per_player=2):
        """Deal initial cards to all players."""
        for player in self.players:
            for _ in range(cards_per_player):
                if self.deck:
                    card = self.deck.pop()
                    player.hand.append(card)

    def replenish_deck(self):
        """Replenish the deck by shuffling the discard pile if the deck is empty."""
        if not self.deck and self.discard_pile:
            self.deck = self.discard_pile[:]
            self.discard_pile = []
            self.shuffle_deck()

    def start_game(self):
        """Start the game with initial setup."""
        self.shuffle_deck()
        self.deal_cards()

    def next_turn(self):
        """Advance to the next turn."""
        while True:
            self.turn += 1
            self.current_player = self.turn % len(self.players)
            if not self.players[self.current_player].eliminated:
                self.draw_cards_for_turn(self.players[self.current_player])
                return self.current_player

    def draw_cards_for_turn(self, player):
        """Draw cards for the current player at the start of their turn."""
        for _ in range(self.cards_per_turn):
            if not self.deck:
                self.replenish_deck()
            if self.deck:
                card = self.deck.pop()
                player.hand.append(card)

    def step(self, action):
        """
        Takes an action in the game and advances the game state.
        """
        # Ensure action tuple has three elements
        if len(action) == 2:
            player_id, card = action
            target_id = None  # Assign None if no target is provided
        elif len(action) == 3:
            player_id, card, target_id = action
        else:
            raise ValueError(f"Invalid action format: {action}")

        # Convert player_id to integer (if it's a string)
        try:
            player_id = int(player_id)
        except ValueError:
            raise TypeError(f"Invalid player_id '{player_id}'. Expected an integer.")

        player = self.players[player_id]

        # Log the current player's hand
        print(f"Turn {self.turn_counter}: Player {player_id} Hand: {player['hand']}")

        # Ensure the card is in the player's hand
        if card not in player['hand']:
            print(f"Error: Player {player_id} tried to play '{card}', which is not in their hand!")
            return -1, None, False  # Invalid action

        # Process the action based on the card type
        if card == 'Bang!':
            if target_id is not None:
                self._bang_action(player, target_id)
            else:
                print(f"Error: 'Bang!' card requires a target but none was provided by Player {player_id}.")
                return -1, None, False
        elif card == 'Miss':
            self._miss_action(player, target_id)
        elif card == 'Beer':
            self._beer_action(player)
        elif card == 'Duel':
            if target_id is not None:
                self._duel_action(player, target_id)
            else:
                print(f"Error: 'Duel' card requires a target but none was provided by Player {player_id}.")
                return -1, None, False
        elif card == 'Indians!':
            self._indians_action(player)
        elif card == 'Panic!':
            if target_id is not None:
                self._panic_action(player, target_id)
            else:
                print(f"Error: 'Panic!' card requires a target but none was provided by Player {player_id}.")
                return -1, None, False
        elif card == 'Cat Balou':
            if target_id is not None:
                self._cat_balou_action(player, target_id)
            else:
                print(f"Error: 'Cat Balou' card requires a target but none was provided by Player {player_id}.")
                return -1, None, False
        elif card == 'Jail':
            if target_id is not None:
                self._jail_action(player, target_id)
            else:
                print(f"Error: 'Jail' card requires a target but none was provided by Player {player_id}.")
                return -1, None, False
        elif card == 'Dynamite':
            self._dynamite_action(player)
        elif card == 'Stagecoach':
            self._stagecoach_action(player)
        elif card == 'Wells Fargo':
            self._wells_fargo_action(player)
        elif card == 'General Store':
            self._general_store_action(player)
        elif card == 'Barrel':
            self._barrel_action(player)
        else:
            print(f"Error: Unknown card '{card}' played by Player {player_id}.")
            return -1, None, False  # Invalid action

        # Remove the card from the player's hand after it is played
        player['hand'].remove(card)

        # Log the updated hand after playing
        print(f"After Turn {self.turn_counter}: Player {player_id} Hand: {player['hand']}")

        # Advance turn
        self.turn_counter += 1
        done = self._check_game_over()

        return 1, self._get_game_state(), done

    def check_game_over(self):
        """Determine if the game has ended."""
        active_players = [p for p in self.players if not p.eliminated]
        if len(active_players) <= 1:
            return True
        if self.turn >= self.max_turns:
            return True
        if not self.deck and not self.discard_pile and all(not p.hand for p in self.players):
            return True
        return False

    def get_state(self, player_id):
        """Return the current state of the game for a specific player."""
        player = self.players[player_id]
        return {
            "PlayerID": player.player_id,
            "Role": player.role,
            "Health": player.health,
            "Hand": player.hand,
            "DiscardPile": len(self.discard_pile),
            "DeckSize": len(self.deck),
            "Players": [
                {
                    "PlayerID": p.player_id,
                    "Health": p.health,
                    "Eliminated": p.eliminated,
                    "Role": p.role if p.role == "Sheriff" else "Unknown",
                }
                for p in self.players
            ],
        }

    # Card logic methods go here
    def _bang_action(self, player, target_id):
        """Handle the 'Bang!' action."""
        target = self.players[target_id]
        if not target.eliminated:
            if "Miss" in target.hand:
                target.use_card("Miss", self)
                if self.verbose:
                    print(f"Player {target_id} negated 'Bang!' with 'Miss'.")
                return
            target.take_damage(1)
            if self.verbose:
                print(f"Player {player.player_id} hit Player {target_id} with 'Bang!'.")
            if target.health <= 0:
                target.eliminate()

    def _miss_action(self, player):
        """Handle the 'Miss' action."""
        if self.verbose:
            print(f"Player {player.player_id} played 'Miss'. No effect.")
        # 'Miss' is used as a counter; this method is mainly a placeholder.

    def _beer_action(self, player):
        """Heal 1 health if health is below max."""
        if player.health < 4:  # Assume max health is 4
            player.heal(1)
            if self.verbose:
                print(f"Player {player.player_id} healed with 'Beer'.")

    def _panic_action(self, player, target_id):
        """Steal a card from the target player."""
        target = self.players[target_id]
        if not target.eliminated and target.hand:
            stolen_card = random.choice(target.hand)
            target.hand.remove(stolen_card)
            player.hand.append(stolen_card)
            if self.verbose:
                print(f"Player {player.player_id} used 'Panic!' to steal {stolen_card} from Player {target_id}.")

    def _cat_balou_action(self, player, target_id):
        """Discard a card from the target player."""
        target = self.players[target_id]
        if not target.eliminated and target.hand:
            discarded_card = random.choice(target.hand)
            target.hand.remove(discarded_card)
            self.discard_pile.append(discarded_card)
            if self.verbose:
                print(f"Player {player.player_id} used 'Cat Balou' to discard {discarded_card} from Player {target_id}.")

    def _gatling_action(self, player):
        """Deal 1 damage to all other players."""
        for target in self.players:
            if target != player and not target.eliminated:
                target.take_damage(1)
                if self.verbose:
                    print(f"Player {player.player_id} hit Player {target.player_id} with 'Gatling'.")
                if target.health <= 0:
                    target.eliminate()

    def _indians_action(self, player):
        """Force all other players to discard a 'Bang!' card or take 1 damage."""
        for target in self.players:
            if target != player and not target.eliminated:
                if "Bang!" in target.hand:
                    target.use_card("Bang!", self)
                    if self.verbose:
                        print(f"Player {target.player_id} negated 'Indians!' with 'Bang!'.")
                else:
                    target.take_damage(1)
                    if self.verbose:
                        print(f"Player {target.player_id} took 1 damage from 'Indians!'.")
                    if target.health <= 0:
                        target.eliminate()

    def _duel_action(self, player, target_id):
        """Start a duel between the player and the target."""
        target = self.players[target_id]
        if not target.eliminated:
            while True:
                if "Bang!" in target.hand:
                    target.use_card("Bang!", self)
                    if self.verbose:
                        print(f"Player {target.player_id} responded with 'Bang!' in the duel.")
                else:
                    target.take_damage(1)
                    if self.verbose:
                        print(f"Player {target.player_id} lost the duel and took 1 damage.")
                    if target.health <= 0:
                        target.eliminate()
                    break

                if "Bang!" in player.hand:
                    player.use_card("Bang!", self)
                    if self.verbose:
                        print(f"Player {player.player_id} continued the duel with 'Bang!'.")
                else:
                    player.take_damage(1)
                    if self.verbose:
                        print(f"Player {player.player_id} lost the duel and took 1 damage.")
                    if player.health <= 0:
                        player.eliminate()
                    break

    def _general_store_action(self, player):
        """Reveal cards and allow players to pick them."""
        revealed_cards = []
        for _ in range(len(self.players)):
            if self.deck:
                revealed_cards.append(self.deck.pop())
            else:
                self.replenish_deck()
        if self.verbose:
            print(f"General Store revealed: {revealed_cards}")

        for p in self.players:
            if revealed_cards:
                chosen_card = random.choice(revealed_cards)
                p.hand.append(chosen_card)
                revealed_cards.remove(chosen_card)
                if self.verbose:
                    print(f"Player {p.player_id} took {chosen_card} from General Store.")

    def _saloon_action(self):
        """Heal all players by 1 health."""
        for player in self.players:
            if not player.eliminated and player.health < 4:
                player.heal(1)
                if self.verbose:
                    print(f"Player {player.player_id} healed by 'Saloon'.")

    def _wells_fargo_action(self, player):
        """Draw 3 cards."""
        for _ in range(3):
            if not self.deck:
                self.replenish_deck()
            if self.deck:
                card = self.deck.pop()
                player.hand.append(card)
                if self.verbose:
                    print(f"Player {player.player_id} drew {card} with 'Wells Fargo'.")

    def _stagecoach_action(self, player):
        """Draw 2 cards."""
        for _ in range(2):
            if not self.deck:
                self.replenish_deck()
            if self.deck:
                card = self.deck.pop()
                player.hand.append(card)
                if self.verbose:
                    print(f"Player {player.player_id} drew {card} with 'Stagecoach'.")

    def _dynamite_action(self, player):
        """Handle the 'Dynamite' action."""
        player.dynamite = True  # Custom flag for tracking dynamite possession
        if self.verbose:
            print(f"Player {player.player_id} placed 'Dynamite'.")

    def _jail_action(self, player, target_id):
        """Place a player in jail."""
        target = self.players[target_id]
        target.in_jail = True
        if self.verbose:
            print(f"Player {target_id} is now in 'Jail'.")

    def _barrel_action(self, player):
        """Allow the player to draw to negate a 'Bang!'."""
        player.barrel = True
        if self.verbose:
            print(f"Player {player.player_id} played 'Barrel'.")
