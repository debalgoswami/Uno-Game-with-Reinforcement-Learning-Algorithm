from Uno_Game import UnoGame
from SARSA import SARSAAgent
from Q_Learning import QLearningAgent
from Monte_Carlo import MonteCarloRL
import random

if __name__ == "__main__":
    num_players = 3
    uno_game = UnoGame(num_players)

    # Create instances of the agents for each player
    q_learning_agent = QLearningAgent(num_players)
    sarsa_agent = SARSAAgent(num_players)
    monte_carlo_agent = MonteCarloRL(num_players)

    player_wins = [0, 0, 0]

    for episode in range(1, 10001):
        uno_game.__init__(num_players)
        uno_game.deal_initial_cards()
        first_card = uno_game.start_card()
        uno_game.discard_pile.append(first_card)
        uno_game.current_color, uno_game.current_value = uno_game.get_card_info(first_card)

        run_time = True

        while run_time:
            current_player = uno_game.players[uno_game.current_player]

            if uno_game.discard_pile:
                top_card = uno_game.discard_pile[-1]

            # Determine which agent to use based on the current player
            if uno_game.current_player == 0:
                selected_card = q_learning_agent.choose_action(uno_game, top_card)
            elif uno_game.current_player == 1:
                selected_card = sarsa_agent.choose_action(uno_game, top_card)
            else:
                selected_card = monte_carlo_agent.choose_action(uno_game, top_card)

            if selected_card:
                uno_game.play(selected_card)
            elif uno_game.deck:
                current_player.hand.append(uno_game.deck.pop(random.randint(0, len(uno_game.deck) - 1)))
            else:
                uno_game.discard_pile.pop(0)
                uno_game.deck = uno_game.discard_pile

            if len(current_player.hand) == 0:
                print("Episode", episode)
                player_wins[uno_game.current_player] += 1
                run_time = False

    print("Wins after 5000 episodes:")
    print("Player 1 (Q-learning):", player_wins[0])
    print("Player 2 (SARSA):", player_wins[1])
    print("Player 3 (Monte Carlo):", player_wins[2])