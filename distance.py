# distance.py

def seat_distance(players, from_idx, to_idx):
    """
    Basic seat distance ignoring eliminated players:
    - We gather only the indices of not-eliminated players in order (clockwise).
    - Then we find the positions of from_idx and to_idx in that 'alive' list
      to calculate the minimal seat hops in a circular manner.
    """
    if from_idx == to_idx:
        return 0

    alive_indices = [i for i, p in enumerate(players) if not p.eliminated]
    from_pos = alive_indices.index(from_idx)
    to_pos = alive_indices.index(to_idx)
    clockwise = (to_pos - from_pos) % len(alive_indices)
    counterclockwise = (from_pos - to_pos) % len(alive_indices)
    return min(clockwise, counterclockwise)

def effective_distance(game, from_player, to_player):
    """
    Final distance = seat distance
                     + to_player.mustang 
                     - from_player.scope
    If distance < 1 => set distance=1.
    (We ignore who has a weapon here, since that affects range, not distance.)
    """
    base = seat_distance(game.players, from_player.player_id, to_player.player_id)
    dist = base + to_player.mustang - from_player.scope
    if dist < 1:
        dist = 1
    return dist
