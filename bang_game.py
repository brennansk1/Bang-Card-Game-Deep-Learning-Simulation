# bang_game.py

import random
from enums import Role, Suit, Value
from deck import Deck
from player import Player
from character_data import CHARACTERS
from distance import effective_distance
from game_logger import GameLogger

class BangGame:
    """
    Ensures each game:
      - Exactly 5 players with roles in seat order:
          0 => Sheriff
          1 => Renegade
          2 => Outlaw
          3 => Outlaw
          4 => Deputy
      - Thoroughly logs CardName, TargetID, HP_Before, HP_After, etc., 
        so missing data is minimized.
      - Each player's final GameResult is logged (Win, Loss, NoOutcome).
    """

    def __init__(self, verbose=False, logger=None, game_number=1):
        self.num_players = 5
        self.verbose = verbose
        self.game_number = game_number

        # If no logger is provided, create a default that APPENDS data to bang_log.csv
        self.logger = logger if logger else GameLogger(filename="bang_log.csv")

        # Hard-code the roles => no duplicates
        # [Sheriff(0), Renegade(1), Outlaw(2), Outlaw(3), Deputy(4)]
        self.roles = [
            Role.SHERIFF,
            Role.RENEGADE,
            Role.OUTLAW,
            Role.OUTLAW,
            Role.DEPUTY
        ]

        # Pick 5 unique characters
        chosen_chars = random.sample(CHARACTERS, 5)
        # random.shuffle(chosen_chars) # if you want seat-based randomization

        self.players = []
        for i in range(5):
            (char_name, base_hp, _) = chosen_chars[i]
            p = Player(
                player_id=i,
                role=self.roles[i],
                character_name=char_name,
                max_health=base_hp
            )
            self.players.append(p)

        self.deck = Deck()
        self.deck.shuffle()

        self.turn_count = 0
        self.current_player_idx = 0

        # track how many total turns each player survived
        self.player_survived_turns = [0]*5

        self._setup_game()

    def _setup_game(self):
        """
        Deal initial cards = player's HP, set flags for Paul Regret, etc.
        """
        for p in self.players:
            for _ in range(p.health):
                c = self.deck.draw()
                if c:
                    p.hand.append(c)

        for p in self.players:
            if p.character_name == "Paul Regret":
                p.mustang += 1
            if p.character_name == "Rose Doolan":
                p.scope += 1
            if p.character_name == "Jourdonnais":
                p.barrel += 1

    def run_game(self):
        """
        Runs the game to completion, ensuring consistent role distribution
        and thorough logging for minimal missing data.
        """
        while True:
            current_player = self.players[self.current_player_idx]
            if current_player.eliminated:
                self._next_player()
                if self._check_end_game():
                    break
                continue

            self.turn_count += 1
            # Everyone alive => survived 1 more turn
            for idx, p in enumerate(self.players):
                if not p.eliminated:
                    self.player_survived_turns[idx]+=1

            # store #cards at start
            cards_in_hand_start = len(current_player.hand)

            # handle dynamite
            if current_player.dynamite:
                self._handle_dynamite(current_player)
                if current_player.eliminated:
                    if self._check_end_game():
                        break
                    self._next_player()
                    continue

            # handle jail
            if current_player.in_jail and current_player.role != Role.SHERIFF:
                self._handle_jail(current_player)
                if current_player.eliminated:
                    if self._check_end_game():
                        break
                    self._next_player()
                    continue
                if getattr(current_player,"skipped_play",False):
                    current_player.skipped_play=False
                    self._discard_phase(current_player, cards_in_hand_start)
                    if self._check_end_game():
                        break
                    self._next_player()
                    continue

            # draw
            self._draw_phase(current_player)

            # play
            self._play_phase(current_player)

            # discard
            self._discard_phase(current_player, cards_in_hand_start)

            if self._check_end_game():
                break
            self._next_player()

        return self._print_winner()

    ###############################
    # DYNAMITE / JAIL
    ###############################
    def _handle_dynamite(self, player):
        c = self._draw_for_draw_check(player)
        if not c:
            return

        hp_before = player.health
        if c.suit==Suit.SPADES and Value.TWO.value <= c.value.value <= Value.NINE.value:
            hp_after = hp_before - 3
            self.logger.log_event(
                game_id=self.game_number,
                turn_in_game=self.turn_count,
                player_id=player.player_id,
                role=player.role.name,
                character=player.character_name,
                action="DynamiteExplode",
                card_name="Dynamite",
                hp_before=hp_before,
                hp_after=hp_after,
                damage_dealt=3
            )
            self._apply_damage(player, 3, None)
            player.dynamite=False
        else:
            # pass left
            player.dynamite=False
            nxt=(player.player_id+1)%5
            while self.players[nxt].eliminated:
                nxt=(nxt+1)%5
            self.players[nxt].dynamite=True
            self.logger.log_event(
                game_id=self.game_number,
                turn_in_game=self.turn_count,
                player_id=player.player_id,
                role=player.role.name,
                character=player.character_name,
                action="DynamitePass",
                card_name="Dynamite",
                target_id=nxt
            )

    def _handle_jail(self, player):
        c=self._draw_for_draw_check(player)
        if not c:
            return
        if c.suit==Suit.HEARTS:
            player.in_jail=False
            self.logger.log_event(
                game_id=self.game_number,
                turn_in_game=self.turn_count,
                player_id=player.player_id,
                role=player.role.name,
                character=player.character_name,
                action="JailEscape",
                card_name="Jail"
            )
        else:
            player.in_jail=False
            player.skipped_play=True
            self.logger.log_event(
                game_id=self.game_number,
                turn_in_game=self.turn_count,
                player_id=player.player_id,
                role=player.role.name,
                character=player.character_name,
                action="JailSkip",
                card_name="Jail"
            )

    #########################
    # DRAW / PLAY / DISCARD
    #########################
    def _draw_phase(self, player):
        for _ in range(2):
            c = self.deck.draw()
            if c:
                player.hand.append(c)
                self.logger.log_event(
                    game_id=self.game_number,
                    turn_in_game=self.turn_count,
                    player_id=player.player_id,
                    role=player.role.name,
                    character=player.character_name,
                    action="Draw",
                    card_name=str(c)
                )

    def _play_phase(self, player):
        if getattr(player,"skipped_play",False):
            return
        player.bang_used_this_turn=0
        local_hand = list(player.hand)
        random.shuffle(local_hand)
        for card in local_hand:
            if card in player.hand:
                self._attempt_play_card(player, card)

    def _attempt_play_card(self, player, card):
        self.logger.log_event(
            game_id=self.game_number,
            turn_in_game=self.turn_count,
            player_id=player.player_id,
            role=player.role.name,
            character=player.character_name,
            action="PlayCard",
            card_name=str(card)
        )
        if card.name=="Bang!":
            if (player.weapon!="Volcanic"
                and player.character_name!="Willy the Kid"
                and player.bang_used_this_turn>=1):
                return
            rng=self._weapon_range(player.weapon)
            candidates=[]
            for t in self.players:
                if t!=player and not t.eliminated:
                    dist=effective_distance(self,player,t)
                    if dist<=rng:
                        candidates.append(t)
            if not candidates:
                return
            target = random.choice(candidates)
            player.hand.remove(card)
            self.deck.discard(card)
            self._play_bang(player, target, card)
            player.bang_used_this_turn+=1
        elif card.name=="Missed!":
            player.hand.remove(card)
            self.deck.discard(card)
        else:
            # discard
            player.hand.remove(card)
            self.deck.discard(card)

    def _play_bang(self, player, target, card):
        hp_before=target.health
        hp_after=hp_before-1
        self.logger.log_event(
            game_id=self.game_number,
            turn_in_game=self.turn_count,
            player_id=player.player_id,
            role=player.role.name,
            character=player.character_name,
            action="Bang",
            card_name=str(card),
            target_id=target.player_id,
            hp_before=hp_before,
            hp_after=hp_after,
            damage_dealt=1,
            aggressive_action=1
        )
        self._apply_damage(target,1,player)

    def _apply_damage(self, target, amount, source):
        hp_before=target.health
        target.take_damage(amount)
        hp_after=target.health
        self.logger.log_event(
            game_id=self.game_number,
            turn_in_game=self.turn_count,
            player_id=(source.player_id if source else -1),
            role=(source.role.name if source else "Env"),
            character=(source.character_name if source else "None"),
            action="Damage",
            target_id=target.player_id,
            hp_before=hp_before,
            hp_after=hp_after,
            damage_dealt=amount,
            aggressive_action=1 if source and source!=target else 0
        )
        if target.eliminated:
            self.logger.log_event(
                game_id=self.game_number,
                turn_in_game=self.turn_count,
                player_id=(source.player_id if source else -1),
                role=(source.role.name if source else "Env"),
                character=(source.character_name if source else "None"),
                action="Eliminate",
                target_id=target.player_id
            )

    def _discard_phase(self, player, cards_in_hand_start):
        if len(player.hand)>player.health:
            excess=len(player.hand)-player.health
            discards=random.sample(player.hand,excess)
            for c in discards:
                player.hand.remove(c)
                self.deck.discard(c)
                self.logger.log_event(
                    game_id=self.game_number,
                    turn_in_game=self.turn_count,
                    player_id=player.player_id,
                    role=player.role.name,
                    character=player.character_name,
                    action="Discard",
                    card_name=str(c)
                )
        cards_in_hand_end = len(player.hand)
        # TurnEnd event => logs the final hand count
        self.logger.log_event(
            game_id=self.game_number,
            turn_in_game=self.turn_count,
            player_id=player.player_id,
            role=player.role.name,
            character=player.character_name,
            action="TurnEnd",
            cards_in_hand_start=cards_in_hand_start,
            cards_in_hand_end=cards_in_hand_end
        )

    ###########################
    # NEXT_PLAYER, ENDGAME
    ###########################
    def _next_player(self):
        nxt=(self.current_player_idx+1)%5
        for _ in range(5):
            if not self.players[nxt].eliminated:
                self.current_player_idx=nxt
                return
            nxt=(nxt+1)%5

    def _check_end_game(self):
        sheriff_alive = any(p.role==Role.SHERIFF and not p.eliminated for p in self.players)
        outlaws_alive = any(p.role==Role.OUTLAW and not p.eliminated for p in self.players)
        renegade_alive = any(p.role==Role.RENEGADE and not p.eliminated for p in self.players)

        if not sheriff_alive:
            alive=[p for p in self.players if not p.eliminated]
            if len(alive)==1 and alive[0].role==Role.RENEGADE:
                return True  # renegade alone => renegade wins
            return True       # else outlaws
        if sheriff_alive and not outlaws_alive and not renegade_alive:
            return True       # sheriff/deputies
        return False

    def _draw_for_draw_check(self, player):
        c=self.deck.draw()
        if c:
            self.deck.discard(c)
        return c

    def _weapon_range(self, w):
        if w=="Volcanic":return 1
        elif w=="Schofield":return 2
        elif w=="Remington":return 3
        elif w=="Rev. Carbine":return 4
        elif w=="Winchester":return 5
        return 1

    def _print_winner(self):
        sheriff_alive=any(p.role==Role.SHERIFF and not p.eliminated for p in self.players)
        outlaws_alive=any(p.role==Role.OUTLAW and not p.eliminated for p in self.players)
        renegade_alive=any(p.role==Role.RENEGADE and not p.eliminated for p in self.players)

        msg=""
        if not sheriff_alive:
            alive=[p for p in self.players if not p.eliminated]
            if len(alive)==1 and alive[0].role==Role.RENEGADE:
                msg="Renegade wins!"
                self._assign_outcomes("RENEGADE")
            else:
                msg="Outlaws win!"
                self._assign_outcomes("OUTLAW")
        else:
            if (not outlaws_alive) and (not renegade_alive):
                msg="Sheriff and Deputies win!"
                self._assign_outcomes("SH_DEPUTY")
            else:
                msg="No final official outcome (possibly ended early)."
                self._assign_outcomes("NONE")
        return msg

    def _assign_outcomes(self, winning_role):
        """
        For each player => logs 'GameOver', ensuring 'GameResult' is NOT missing.
        SurvivedTurns is recorded for each seat.
        """
        for i,p in enumerate(self.players):
            final_res="Loss"
            if not p.eliminated:
                if winning_role=="RENEGADE" and p.role==Role.RENEGADE:
                    final_res="Win"
                elif winning_role=="OUTLAW" and p.role==Role.OUTLAW:
                    final_res="Win"
                elif winning_role=="SH_DEPUTY" and p.role in [Role.SHERIFF,Role.DEPUTY]:
                    final_res="Win"
                elif winning_role=="NONE":
                    final_res="NoOutcome"

            self.logger.log_event(
                game_id=self.game_number,
                turn_in_game=self.turn_count,
                player_id=i,
                role=p.role.name,
                character=p.character_name,
                action="GameOver",
                game_result=final_res,
                survived_turns=self.player_survived_turns[i]
            )
