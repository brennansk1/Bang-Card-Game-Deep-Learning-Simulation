# run_training.py

import random
import numpy as np
import time
from datetime import datetime
from tqdm import tqdm  # for progress bar
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque

from bang_game import BangGame  # assumes bang_game.py has roles = [Sheriff, Renegade, Outlaw, Outlaw, Deputy]


class DQNAgent:
    def __init__(
        self,
        state_size,
        action_size,
        lr=0.001,
        gamma=0.99,
        epsilon=1.0,
        epsilon_min=0.01,
        epsilon_decay=0.995,
        memory_size=2000,
    ):
        self.state_size = state_size
        self.action_size = action_size
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay

        self.memory = deque(maxlen=memory_size)

        self.model = nn.Sequential(
            nn.Linear(self.state_size, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, self.action_size)
        )
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)
        self.criterion = nn.MSELoss()

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state, valid_actions=None):
        # Epsilon-greedy
        if np.random.rand() < self.epsilon:
            if valid_actions:
                return random.choice(valid_actions)
            else:
                return random.randrange(self.action_size)
        else:
            with torch.no_grad():
                state_tensor = torch.tensor(state, dtype=torch.float32).unsqueeze(0)
                q_values = self.model(state_tensor).numpy().squeeze()
            if valid_actions:
                masked = np.full_like(q_values, -np.inf)
                for a in valid_actions:
                    masked[a] = q_values[a]
                return int(np.argmax(masked))
            else:
                return int(np.argmax(q_values))

    def replay(self, batch_size=32):
        if len(self.memory) < batch_size:
            return

        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                next_tensor = torch.tensor(next_state, dtype=torch.float32).unsqueeze(0)
                future_q = self.model(next_tensor).detach().max(dim=1)[0].item()
                target += self.gamma * future_q

            state_tensor = torch.tensor(state, dtype=torch.float32).unsqueeze(0)
            current_q_values = self.model(state_tensor).detach().numpy().squeeze()

            current_q_values[action] = target
            target_arr = np.array(current_q_values, dtype=np.float32)
            target_tensor = torch.from_numpy(target_arr).unsqueeze(0)

            self.optimizer.zero_grad()
            output = self.model(state_tensor)
            loss = self.criterion(output, target_tensor)
            loss.backward()
            self.optimizer.step()

        # Decay epsilon
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay


def build_state_dict(game):
    """
    Minimal function to gather the game state for encoding.
    """
    st = {
        "turn": game.turn_count,
        "current_player": game.current_player_idx,
        "players": [],
        "deck_size": len(game.deck.cards),
        "discard_size": len(game.deck.discard_pile)
    }
    for p in game.players:
        st_p = {
            "health": p.health,
            "hand_size": len(p.hand),
            "eliminated": p.eliminated
        }
        st["players"].append(st_p)
    return st

def encode_state(game_state):
    """
    Convert that dictionary into a numeric vector.
    """
    turn = game_state["turn"]
    cp = game_state["current_player"]
    deck_s = game_state["deck_size"]
    disc_s = game_state["discard_size"]

    arr = [turn, cp, deck_s, disc_s]
    for pinfo in game_state["players"]:
        arr += [pinfo["health"], int(pinfo["eliminated"]), pinfo["hand_size"]]
    return np.array(arr, dtype=np.float32)

def train_bang_agents(num_episodes=20, turn_cap=100):
    """
    We ensure each game has exactly 5 players with roles:
        1 Sheriff, 1 Renegade, 2 Outlaws, 1 Deputy
    By referencing a bang_game.py that has that distribution.
    We add a progress bar for time estimate using tqdm.
    """
    # We'll create a dummy game to measure state_size
    dummy_game = BangGame(verbose=False, game_number=0)
    dummy_state = build_state_dict(dummy_game)
    dummy_vec = encode_state(dummy_state)
    state_size = len(dummy_vec)
    action_size = 11  # 0 => pass, 1..10 => cards in hand

    agent = DQNAgent(
        state_size=state_size,
        action_size=action_size,
        lr=0.001,
        gamma=0.99,
        epsilon=1.0,
        epsilon_min=0.01,
        epsilon_decay=0.995,
        memory_size=5000,
    )

    outcomes = {
        "Renegade": 0,
        "Outlaws": 0,
        "Sheriff/Deputies": 0,
        "Other": 0
    }

    # We'll do a progress bar for the episodes
    import time
    from tqdm import tqdm

    start_time = time.time()

    for episode in tqdm(range(num_episodes), desc="Training Progress", unit="episode"):
        game = BangGame(verbose=False, game_number=episode+1)
        # This game presumably has roles = [Sheriff, Renegade, Outlaw, Outlaw, Deputy]
        # guaranteed by bang_game.py

        # We'll do a naive approach: let run_game finish
        while True:
            if game.turn_count > turn_cap:
                print(f"Episode {episode+1} => turn cap exceeded => ignoring outcome.")
                break

            current_p = game.players[game.current_player_idx]
            if current_p.eliminated:
                game._next_player()
                if game._check_end_game():
                    break
                continue

            outcome = game.run_game()
            break

        outcome = game._print_winner()
        print(f"Episode {episode+1} ended after {game.turn_count} turns => {outcome}")

        if "Renegade" in outcome:
            outcomes["Renegade"] += 1
        elif "Outlaws" in outcome:
            outcomes["Outlaws"] += 1
        elif "Sheriff and Deputies" in outcome:
            outcomes["Sheriff/Deputies"] += 1
        else:
            outcomes["Other"] += 1

        # Here you might do agent training in detail (step-by-step),
        # or sample from memory replay, etc. We'll keep it minimal here.

    end_time = time.time()
    total_time = end_time - start_time
    print(f"Training took {total_time:.2f} seconds total.")

    return outcomes

if __name__ == "__main__":
    results = train_bang_agents(num_episodes=5)
    print("Final outcomes:")
    print("Renegade:", results["Renegade"])
    print("Outlaws:", results["Outlaws"])
    print("Sheriff/Deputies:", results["Sheriff/Deputies"])
    print("Other:", results["Other"])
