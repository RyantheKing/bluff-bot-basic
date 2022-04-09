#import pyttsx3
#from playsound import playsound
#import time
#import subprocess

#def play(path):
#    subprocess.call(["ffplay", "-nodisp", "-autoexit", path])

def make_order(num_players, starting_player):
    return [(i*num_players+starting_player)%13+1 for i in range(13)]

#engine = pyttsx3.init()
#voices = engine.getProperty('voices')
#rate = engine.getProperty('rate')
#engine.setProperty('rate', 125)
#speech = "I have played 3 8s"
#engine.save_to_file(speech, 'output.wav')
#engine.runAndWait()
#play('output.wav')

num_players = int(input('Enter # of players: ')) #user input
hand = list(map(int, input('Enter hand seperated by spaces: ').split())) #user input
jokers = True
starting_player = int(input('Enter # of starting player: ')) #user input
possible_player_cards = [[] for i in range(num_players)]
player_card_count = [(54 if jokers else 52)//num_players for i in range(num_players)]
known_pile_cards = []
pile_cards_size = 0
possible_pile_cards = []
playing = True
possible_player_cards[0] = hand
player_card_count[0] = len(hand)
to_play = []
locked_in = False
first = True
order_list = make_order(num_players, starting_player)
print(order_list)
if starting_player!=0:
    known_pile_cards.append(1)
    to_play = [1]
while playing:
    for real_card in order_list:
        print('Card in play:', real_card)
        print('Pile:', known_pile_cards, possible_pile_cards, pile_cards_size)
        print('Hands:', possible_player_cards, player_card_count)
        for i in range(num_players):
            player_card_count[0] = len(hand)
            turn = (i+starting_player)%num_players
            if turn == 0:
                to_play.clear()
                index = order_list.index(real_card)
                next_turns = order_list[index:]+order_list[:index]
                remaining_play = len(set(hand)-{0})+hand.count(0)
                remaining_order = next_turns[:remaining_play]
                print(set(remaining_order)-set(hand))
                if len(set(remaining_order)-set(hand)) <= hand.count(0):
                    locked_in = True
                    print("LOCKED IN!")
                if real_card in hand:
                    if starting_player==0 and first:
                        to_play = [1]
                    else:
                        to_play = [j for j in hand if j==real_card]
                    lied = False
                    print('Play: ', to_play)
                else:
                    if locked_in:
                        to_play = [0]
                        lied = False
                    else:
                        backwards = next_turns.copy()
                        backwards.reverse()
                        for k in backwards:
                            if k in hand:
                                if hand.count(k)>1 and len(hand)!=min(player_card_count) and all([i.count(real_card)<=1 for i in possible_player_cards]):
                                    to_play = [k,k]
                                else:
                                    to_play = [k]
                                break
                        lied = True
                    print('Play: ', to_play, 'Call as', len(to_play), str(real_card)+"'s")
                known_pile_cards.extend(to_play)
                pile_cards_size += len(to_play)
                player_card_count[0] = len(hand)
                for x in to_play: # remove played cards from hand
                    hand.remove(x) # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                bs_called = input('Was called? (y/n): ').lower()=='y' #user input
                if bs_called and lied:
                    pile_cards_size = 0
                    known_pile_cards = []
                    possible_pile_cards = []
                    picked_up = list(map(int, input('Enter picked up cards seperated by spaces: ').split())) #user input
                    hand.extend(picked_up)
                elif bs_called and (not lied):
                    pile_cards_size = 0
                    who_called = int(input('Enter the # of the player who called: ')) # user input
                    possible_player_cards[who_called].extend(known_pile_cards)
                    possible_player_cards[who_called].extend(possible_pile_cards)
                    known_pile_cards = []
                    possible_pile_cards = []

            else:
                number_claimed = int(input('How many cards did they play?: '))#user input
                pile_cards_size += number_claimed
                player_card_count[turn] -= number_claimed
                if ((real_card+turn-1)%13+1) in possible_player_cards[turn]:
                    for x in [(real_card+turn-1)%13+1]*number_claimed: # remove played cards from hand
                        try:
                            possible_player_cards[turn].remove(x) # ^^^^^^^^^^^^^^^^^^^^^^^^
                        except:
                            print('played more than expected')
                        possible_pile_cards.append(x)
                bs_called = input('Was called? (y/n): ').lower()=='y' #user input
                if ((hand.count((real_card+turn-1)%13+1) + known_pile_cards.count((real_card+turn-1)%13+1) + number_claimed)>4 and (pile_cards_size<=20)) or ((player_card_count[turn] <= 5) and (pile_cards_size<=5) and (possible_pile_cards.count((real_card+turn-1)%13+1) + known_pile_cards.count((real_card+turn-1)%13+1) + hand.count((real_card+turn-1)%13+1) + sum([i.count((real_card+turn-1)%13+1) for e,i in enumerate(possible_player_cards) if e!=turn]))>4):
                    print('ATTENTION: You should call BS')
                if bs_called:
                    lied = input('Was it a lie? (y/n): ').lower()=='y' #user input
                    if lied:
                        player_card_count[turn] += pile_cards_size
                        possible_player_cards[turn].extend(known_pile_cards)
                        possible_player_cards[turn].extend(possible_pile_cards)
                    else:
                        who_called = int(input('Enter the # of the player who called: ')) # user input
                        if who_called == 0:
                            picked_up = list(map(int, input('Enter picked up cards seperated by spaces: ').split())) #user input
                            hand.extend(picked_up)
                        else:
                            player_card_count[who_called] += pile_cards_size
                            possible_player_cards[who_called].extend(known_pile_cards)
                            possible_player_cards[who_called].extend(possible_pile_cards)
                    pile_cards_size = 0
                    known_pile_cards = []
                    possible_pile_cards = []
                #call bs if the cards exist probably elsewhere and they have less than 5 cards or are known to be in hand or in deck (if jokers are involved only do so with 5 or less cards in the deck)
            first = False