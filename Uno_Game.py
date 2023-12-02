import random

def limit_duplicates(lst):
        count_dict = {}
        result = []

        for item in lst:
            if item in count_dict:
                count_dict[item] += 1
                if count_dict[item] <= 2:
                    result.append(item)
            else:
                count_dict[item] = 1
                result.append(item)

        return result

class UnoGame:
    def __init__(self, num_players):
        self.num_players = num_players
        self.players = [Player() for _ in range(num_players)]
        self.deck = self.create_deck()
        self.current_player = 0
        self.discard_pile = []
        self.current_color = None
        self.current_value = None
        self.direction = 1  # 1 for clockwise, -1 for counterclockwise | Can change during game based on reverse card

    def regenerate_deck(self):
        if (self.deck == 0) :
            self.deck = self.create_deck()

    def create_deck(self):
        colors = ['Red', 'Green', 'Blue', 'Yellow']
        values = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'Skip', 'Reverse', 'Draw Two']
        wild_cards = ['Wild', 'Wild Draw Four']
        deck = [f"{color} {value}" for color in colors for value in values]
        deck = limit_duplicates(deck) # Because the game has two of each card
        deck.extend(wild_cards * 4)  # Four of each wild card
        deck.extend(deck*5)
        random.shuffle(deck)
        return deck

    def deal_initial_cards(self):
        for player in self.players:
            if self.deck:
                player.hand = [self.deck.pop() for _ in range(7)]
                if (player.hand == None) : continue
            else:
                self.regenerate_deck()

    def start_card(self) :
        colors = ['Red', 'Green', 'Blue', 'Yellow']
        values = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        color_first = random.choice(colors)
        value_first = random.choice(values)
        return f"{color_first} {value_first}"

    def play(self, card):
        if (card == None) : return 
        
        player = self.players[self.current_player]

        player.hand.remove(card)
        self.discard_pile.append(card)
        color, value = self.get_card_info(card)

        if value is not None:
            if value == 'Reverse':
                self.direction *= -1
                if len(player.hand) == 0 : return

            if value == 'Skip':
                if len(player.hand) == 0 : return
                self.current_player = (self.current_player + self.direction) % self.num_players
            
            if 'Draw Two' in value:
                if len(player.hand) == 0 : return
                next_player = self.players[(self.current_player + self.direction) % self.num_players]
                for _ in range(2):
                    if self.deck :
                        next_player.hand.append(self.deck.pop())
                    else :
                        self.regenerate_deck()

        if color == 'Wild' and value == '4':
            next_player = self.players[(self.current_player + self.direction) % self.num_players]
            for _ in range(4):
                if self.deck :
                    next_player.hand.append(self.deck.pop())
                else :
                    self.regenerate_deck()
            return

        if color == 'Wild' and value != '4':
            return
        else :
            self.current_color, self.current_value = color, value

        if len(player.hand) != 0 :
            self.current_player = (self.current_player + self.direction) % self.num_players

    def is_valid_move(self, player, card, top_card):
        if (card == None) : return False

        if top_card :
            if top_card == 'Wild' or top_card == 'Wild Draw Four' :
                return player.hand

        color, value = self.get_card_info(card)
        current_color, current_value = self.current_color, self.current_value

        top_color, top_value = self.get_card_info(top_card)
        if color == top_color : return True
        if value == top_value : return True

        if 'Wild' in color:
            return True
        
        if 'Wild' in color and value == '4':
            return True

        if value is not None:
            if 'Draw Two' in value:
                return 'Draw Two' in current_value
            return color == current_color or value == current_value

        return False


    def get_card_info(self, card):
        if card is None : return 
        parts = card.split()
        if len(parts) == 2:
            return parts[0], parts[1]
        elif len(parts) == 3 :
            if (parts[2] == 'Two') :
                return parts[0], 'Draw Two'
            else :
                return parts[0], '4'
        else:
            return parts[0], None

    def get_current_state(self): #Debug utils
        return {
            'current_player': self.current_player,
            'current_color': self.current_color,
            'current_value': self.current_value,
            'discard_pile': self.discard_pile,
            'players_hands': [player.hand for player in self.players],
        }

class Player:
    def __init__(self):
        self.hand = []

if __name__ == "__main__":
    num_players = 2
    uno_game = UnoGame(num_players)
    uno_game.deal_initial_cards()
    first_card = uno_game.start_card()
    uno_game.discard_pile.append(first_card)
    color, value = uno_game.get_card_info(first_card)
    uno_game.current_color = color
    uno_game.current_value = value
    print("First Card", first_card)
    print('------------------------')
    print()

    run_time = True

    while (run_time == True):
        #time.sleep(0.5)
        current_player = uno_game.players[uno_game.current_player]
        #print(uno_game.get_current_state())
        print(f"Player {uno_game.current_player + 1}'s Turn")
        print(f"{uno_game.current_player + 1}'s Hand: {current_player.hand}")
        
        if uno_game.discard_pile:
            top_card = uno_game.discard_pile[-1]
            print(f"Top Card: ", top_card)
        else:
            print("Discard pile is empty.")

        valid_moves = [card for card in current_player.hand if uno_game.is_valid_move(current_player, card, top_card)]
        
        if valid_moves:
            print(f"Valid Moves: {valid_moves}")
            selected_card = random.choice(valid_moves)
            print(f"Playing: {selected_card}")
            uno_game.play(selected_card)
            print()
            print('---------------------------')
            print()
        else:
            if uno_game.deck :
                print("No valid moves. Drawing a card.")
                current_player.hand.append(uno_game.deck.pop())
                print()
            else:
                uno_game.regenerate_deck()

        if len(current_player.hand) == 0:
            print(f"Player {uno_game.current_player + 1} wins!")
            run_time = False
