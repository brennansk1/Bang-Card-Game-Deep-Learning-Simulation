import csv
import os

class GameLogger:
    """
    Logs game events to a CSV file.
    We now append all episodes/games to the same CSV, so data accumulates.

    Columns:
      - GameID
      - Turn
      - PlayerID
      - Role
      - Character
      - Action
      - CardName
      - TargetID
      - HP_Before
      - HP_After
      - DamageDealt
      - CardsInHand_Start
      - CardsInHand_End
      - AggressiveAction
      - GameResult
      - SurvivedTurns
    """

    def __init__(self, filename="bang_log.csv"):
        """
        If the file doesn't exist, we create it and write a header.
        If it does exist, we append new rows (no new header).
        """
        self.filename = filename
        file_exists = os.path.isfile(self.filename)

        if not file_exists:
            # create new file and write header
            with open(self.filename, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "GameID",
                    "Turn",
                    "PlayerID",
                    "Role",
                    "Character",
                    "Action",
                    "CardName",
                    "TargetID",
                    "HP_Before",
                    "HP_After",
                    "DamageDealt",
                    "CardsInHand_Start",
                    "CardsInHand_End",
                    "AggressiveAction",
                    "GameResult",
                    "SurvivedTurns"
                ])
        # If file exists, do nothing: we will just append rows later.

    def log_event(
        self,
        game_id: int,
        turn_in_game: int,
        player_id: int,
        role: str,
        character: str,
        action: str,
        card_name: str = "",
        target_id: int = None,
        hp_before: int = None,
        hp_after: int = None,
        damage_dealt: int = 0,
        cards_in_hand_start: int = None,
        cards_in_hand_end: int = None,
        aggressive_action: int = 0,
        game_result: str = "",
        survived_turns: int = 0
    ):
        """
        Appends a single row to the CSV, not overwriting existing data.
        """
        with open(self.filename, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            row = [
                game_id,
                turn_in_game,
                player_id,
                role,
                character,
                action,
                card_name,
                str(target_id) if target_id is not None else "",
                str(hp_before) if hp_before is not None else "",
                str(hp_after) if hp_after is not None else "",
                str(damage_dealt),
                str(cards_in_hand_start) if cards_in_hand_start is not None else "",
                str(cards_in_hand_end) if cards_in_hand_end is not None else "",
                str(aggressive_action),
                game_result,
                str(survived_turns)
            ]
            writer.writerow(row)
