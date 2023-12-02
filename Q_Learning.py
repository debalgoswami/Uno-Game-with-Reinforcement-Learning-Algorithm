from Uno_Game import UnoGame
import random

class QLearningAgent:
    def __init__(self, num_players, num_episodes=20000, discount_factor=0.9, exploration_prob=0.2, learning_rate=0.1):
        self.num_players = num_players
        self.num_episodes = num_episodes
        self.discount_factor = discount_factor
        self.exploration_prob = exploration_prob
        self.learning_rate = learning_rate
        self.q_values = {}

    def choose_action(self, uno_game, top_card):
        current_player = uno_game.players[uno_game.current_player]
        valid_moves = [card for card in current_player.hand if uno_game.is_valid_move(current_player, card, top_card)]

        if valid_moves and random.random() < self.exploration_prob:
            # Exploration
            return random.choice(valid_moves)
        elif valid_moves:
            # Exploitation
            return max(valid_moves, key=lambda card: self.q_values.get((uno_game.current_player, card), 0))
        else:
            return None

    def get_reward(self, uno_game, initial_state, top_card):
        current_player = uno_game.players[uno_game.current_player]

        if len(current_player.hand) == 0:
            return 1.0

        if not uno_game.is_valid_move(current_player, initial_state['current_value'], top_card):
            return -0.5

        return 0.1

    def update_q_values(self, state, action, reward, next_state):
        current_player = state['current_player']

        valid_actions = [a for a in next_state['players_hands'][next_state['current_player']] if
                        self.q_values.get((next_state['current_player'], a)) is not None]

        if not valid_actions:
            best_next_q = 0
        else:
            best_next_q = max(self.q_values.get((next_state['current_player'], a), 0) for a in valid_actions)

        current_q = self.q_values.get((current_player, action), 0)
        new_q = current_q + self.learning_rate * (
                reward + self.discount_factor * best_next_q - current_q)
        self.q_values[(current_player, action)] = new_q

    def q_learning(self, uno_game):
        player_1 = 0
        player_2 = 0
        for episode in range(1, self.num_episodes + 1):
            uno_game.__init__(self.num_players)
            uno_game.deal_initial_cards()
            first_card = uno_game.start_card()
            uno_game.discard_pile.append(first_card)
            uno_game.current_color, uno_game.current_value = uno_game.get_card_info(first_card)

            state = uno_game.get_current_state()
            run_time = True

            while run_time:
                current_player = uno_game.players[uno_game.current_player]
                if uno_game.discard_pile:
                    top_card = uno_game.discard_pile[-1]

                if uno_game.current_player == 0:
                    action = self.choose_action(uno_game, top_card)
                else:
                    valid_moves = [card for card in current_player.hand if
                                   uno_game.is_valid_move(current_player, card, top_card)]
                    
                    if valid_moves :
                        action = random.choice(valid_moves) if valid_moves else None
                    else :
                        action = None

                if action is None:
                    if uno_game.deck:
                        current_player.hand.append(uno_game.deck.pop(random.randint(0, len(uno_game.deck) - 1)))
                    else :
                        uno_game.discard_pile.pop(0)
                        uno_game.deck = uno_game.discard_pile

                initial_state = state.copy()

                if action != None:
                    uno_game.play(action)
                    next_state = uno_game.get_current_state()

                if uno_game.current_player == 0:
                    reward = self.get_reward(uno_game, initial_state, top_card)
                    self.update_q_values(initial_state, action, reward, next_state)

                if len(current_player.hand) == 0:
                    print("Episode", episode)
                    if uno_game.current_player == 0:
                        player_1 += 1
                    else:
                        player_2 += 1
                    run_time = False

        print("Q Learning")
        print("Player 1", player_1, "Player 2", player_2)

# Run Q-learning
num_players = 2
uno_game = UnoGame(num_players)
q_learning_agent = QLearningAgent(num_players)
q_learning_agent.q_learning(uno_game)
