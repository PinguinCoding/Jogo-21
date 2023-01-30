import storage
from random import choice
from time import sleep
# imports
time = 0.75
opponentHandHold = list()
# important variables


def start_game():
    pile = storage.cheap
    # put the pile on the table
    buy_card('player', pile)
    buy_card('opponent', pile)
    # first draw for every one
    show_game('table')
    # show the table
    line('Your turn!')
    turn_player = player_game(pile)
    sleep(time)
    # player first turn
    line('Your opponent turn!')
    turn_opponent = opponent_game(pile)
    sleep(time)
    # opponent first turn
    while turn_player is None or turn_opponent is None:
        show_game('table', False)

        line('Your turn!')
        turn_player = player_game(pile)
        sleep(time)

        line('Your opponent turn!')
        turn_opponent = opponent_game(pile)
        sleep(time)
    # all rounds
    if turn_player > 21 and turn_opponent <= 21:
        show_game('table', False, True)
        sleep(time + 1)
        line('I am sorry, you lost the game!')
    # if the player pass 21 and the opponent didn't
    elif turn_opponent > 21 and turn_player <= 21:
        show_game('table', False, True)
        sleep(time + 1)
        line('Congratulations! You won the game!')
    # if the opponent pass 21 and the player didn't
    elif turn_opponent < turn_player <= 21:
        show_game('table', False, True)
        sleep(time + 1)
        line('Congratulations! You won the game!')
    # if they both didn't pass 21 and the player sum is bigger than it's opponent
    elif turn_player < turn_opponent <= 21:
        show_game('table', False, True)
        sleep(time + 1)
        line('I am sorry, you lost the game!')
    # if they both didn't pass 21 and the opponent sum is bigger than the player
    elif turn_opponent == turn_player <= 21:
        show_game('table', False, True)
        sleep(time + 1)
        line('It is a tie!')
    # if they both didn't pass 21 and there sum is equal
    elif 21 < turn_player < turn_opponent:
        show_game('table', False, True)
        sleep(time + 1)
        line('Congratulations! You won the game!')
    # if they both pass 21 but the player sum is closer to 21
    elif 21 < turn_opponent < turn_player:
        show_game('table', False, True)
        sleep(time + 1)
        line('I am sorry, you lost the game!')
    # if they both pass 21 but the opponent sum is closer to 21
    elif 21 < turn_opponent == turn_player:
        show_game('table', False, True)
        sleep(time + 1)
        line('It is a tie!')
    # if they both pass 21 and there sum is equal


def player_game(current_pile):
    playerSum = storage.playerGame['sum']

    while True:
        sleep(time)
        print('You may [pass] or [buy]')
        op = str(input('What will you do? ')).strip().upper()

        while op not in 'BUYPASS':
            op = str(input('You need to write "pass" or "buy" ')).strip().upper()

        if op == 'BUY' and test_buy('player'):
            sleep(time)
            buy_card('player', current_pile)
            show_game('player')
            return None

        elif op == 'PASS':
            print('Pass option')
            print('=' * 50)
            return playerSum


def opponent_game(current_pile):
    while True:
        handOpponent = storage.opponentGame['currentHand']
        sumOpponent = storage.opponentGame['sum']
        handPlayer = storage.playerGame['currentHand'][:]
        handPlayer.remove(handPlayer[0])
        PlayerSum = storage.playerGame['sum'] - storage.playerGame['currentHand'][0]
        # remove the first of the sum

        if sumOpponent < 21 and test_buy('opponent') and analyze(handOpponent, handPlayer, sumOpponent, PlayerSum):
            sleep(time)
            buy_card('opponent', current_pile, False)
            sleep(time)
            show_game('opponent')
            return None

        else:
            sleep(time + 1)
            print('Your opponent has pass his turn')
            sleep(time)
            return sumOpponent


def analyze(current_hand, player_hand, current_sum, player_sum):
    starting_pile = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    bigCardsPile = [8, 9, 10, 11, 12]
    mediumCardsPile = [5, 6, 7]
    smallCardsPile = [1, 2, 3, 4]
    bigCards = 0
    mediumCards = 0
    smallCards = 0
    hand = current_hand[:]
    allCardTable = player_hand[:]
    risk = 40.0

    for card in hand:
        allCardTable.append(card)

    for card in allCardTable:
        starting_pile.remove(card)

    for i in range(0, len(starting_pile)):
        if starting_pile[i] >= 8:
            bigCards += 1

        elif 5 < starting_pile[i] <= 7:
            mediumCards += 1

        else:
            smallCards += 1

    probability_draw_big_card = (bigCards / len(starting_pile)) * 100
    probability_draw_medium_card = (mediumCards / len(starting_pile)) * 100
    probability_draw_small_card = (smallCards / len(starting_pile)) * 100

    if probability_draw_big_card != 0 and probability_draw_big_card <= risk:
        print('Your opponent is thinking about his next move...')
        sleep(time)
        for card in bigCardsPile:
            if current_sum + card > 21:
                if current_sum < player_sum:
                    return True
                return False
            else:
                return True

    elif probability_draw_medium_card != 0 and probability_draw_medium_card <= risk:
        print('Your opponent is thinking about his next move...')
        sleep(time)
        for card in mediumCardsPile:
            if current_sum + card > 21:
                if current_sum < player_sum:
                    return True
                return False
            else:
                return True

    elif probability_draw_small_card != 0 and probability_draw_small_card <= risk:
        print('Your opponent is thinking about his next move...')
        sleep(time)
        for card in smallCardsPile:
            if current_sum + card > 21:
                if current_sum < player_sum:
                    return True
                return False
            else:
                return True

    else:
        print('Your opponent is thinking about his next move...')
        return False


def buy_card(who, current_pile, first=True):
    if who == 'player':
        pick = choice(current_pile)
        storage.playerGame['currentHand'].append(pick)
        storage.playerGame['sum'] += pick
        current_pile.remove(pick)

    else:
        pick = choice(current_pile)
        storage.opponentGame['currentHand'].append(pick)
        storage.opponentGame['sum'] += pick
        current_pile.remove(pick)

    if first is False:
        print(f'Your opponent bought the card {pick}')
        opponentHandHold.append(pick)


def show_game(who, first=True, end=False):
    playerHand = storage.playerGame["currentHand"]
    playerSum = storage.playerGame["sum"]

    opponentHand = opponentHandHold
    opponentSum = 0

    for card in opponentHand:
        opponentSum += card

    if end:
        if who == 'table':
            sleep(time)
            line(f'\033[33mYour current hand is: {playerHand}\n'
                 f'Your current sum is {playerSum}')
            line(f'Your opponent current hand is: {storage.opponentGame["currentHand"]}\n'
                 f'Your opponent current sum is {storage.opponentGame["sum"]}\033[0;0m')

    if first and end is False:
        if who == 'table':
            sleep(time)
            line(f'\033[33mYour current hand is: {playerHand}\n'
                 f'Your current sum is {playerSum}')
            line(f'Your opponent current hand is: ?\n'
                 f'Your opponent current sum is ?\033[0;0m')

        elif who == 'player':
            sleep(time)
            line(f'\033[34mYour current hand is: {playerHand}\n'
                 f'Your current sum is {playerSum}\033[0;0m')

    elif first is False and end is False:
        if who == 'table':
            sleep(time)
            line(f'\033[33mYour current hand is: {playerHand}\n'
                 f'Your current sum is {playerSum}')
            line(f'Your opponent current hand is: ? + {opponentHand}\n'
                 f'Your opponent current sum is ? + {opponentSum}\033[0;0m')

        elif who == 'player':
            sleep(time)
            line(f'\033[34mYour current hand is: {playerHand}\n'
                 f'Your current sum is {playerSum}\033[0;0m')

        else:
            sleep(time)
            line(f'\033[31mYour opponent current hand is: ? + {opponentHand}\n'
                 f'Your opponent current sum is ? + {opponentSum}\033[0;0m')


def test_buy(who):
    if who == 'player':
        if storage.playerGame['sum'] >= 21:
            line('Your sum has surpass 21, you no long can buy cards')
            return False
        else:
            return True
    else:
        if storage.opponentGame['sum'] >= 21:
            return False
        else:
            return True


def line(msg):
    print('=' * 50)
    print(msg)
    print('=' * 50)


start_game()
