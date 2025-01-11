# main.py

from run_training import train_bang_agents

def main():
    # Call the training function, which returns a dictionary of outcomes.
    results = train_bang_agents(num_episodes=1000)

    # Now 'results' is guaranteed to be a dictionary, not None.
    print("Training complete!")
    print("Renegade wins:", results["Renegade"])
    print("Outlaws win:", results["Outlaws"])
    print("Sheriff/Deputies win:", results["Sheriff/Deputies"])
    print("Other outcomes:", results["Other"])

if __name__ == "__main__":
    main()
