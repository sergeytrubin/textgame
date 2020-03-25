import os
import sys
import random
from time import sleep
from pyfiglet import Figlet


# Clear the screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    sleep(1)


# Typing effect function
def typing_effect(line, speed):
    for char in line:
        sleep(speed)
        sys.stdout.write(char)
        sys.stdout.flush()
    sleep(0.5)


# Check that user input is correct
def verify_user_input(choice_range):
    c = [x for x in range(1, choice_range + 1)]
    while True:
        typing_effect("Make choice ({}-{}): ".format(c[0], c[len(c)-1]), 0.05)
        user_input = input()
        try:
            if int(user_input) not in c:
                print('Invalid choice. Enter choice...')
            else:
                return int(user_input)
        except ValueError:
            print('Invalid choice. Enter choice...')


# Generate random stats, health and power
def generate_stats(character):
    stats = {}
    stats['Strength'] = random.randint(9, 18)
    stats['Dexterity'] = random.randint(9, 18)
    stats['Constitution'] = random.randint(9, 18)
    stats['Intellect'] = random.randint(9, 18)

    if user_char == 'WARRIOR':
        stats['Intellect'] = stats['Intellect'] - random.randint(1, 5)
        stats['Dexterity'] = stats['Dexterity'] - random.randint(1, 5)
        stats['Strength'] = stats['Strength'] + random.randint(1, 3)
        health = (stats['Constitution'] + stats['Strength']) * 30
        power = stats['Strength'] * 10
    if user_char == 'WIZARD':
        stats['Strength'] = stats['Intellect'] - random.randint(1, 5)
        stats['Dexterity'] = stats['Dexterity'] - random.randint(1, 5)
        stats['Intellect'] = stats['Intellect'] + random.randint(1, 3)
        health = (stats['Constitution'] + stats['Intellect']) * 30
        power = stats['Intellect'] * 10
    if user_char == 'ROGUE':
        stats['Intellect'] = stats['Intellect'] - random.randint(1, 5)
        stats['Constitution'] = stats['Dexterity'] - random.randint(1, 5)
        stats['Dexterity'] = stats['Dexterity'] + random.randint(1, 3)
        health = (stats['Constitution'] + stats['Dexterity']) * 30
        power = stats['Dexterity'] * 10
    else:
        health = (stats['Constitution'] + stats['Strength']) * 40
        power = stats['Strength'] * 15
    return stats, health, power


# Fight damage multiplier with probability for a critical hit
def damage_modificator(power):
    modificator = 0
    modificator = random.randint(1, 10)
    if modificator == 10:
        typing_effect('  Critical hit!\n', 0.05)
        power = power * 4
    else:
        power = power * (1 + 0.1 * modificator)
    return power


# Test of character health. If = 0 stop the fight
def health_status(hero_health, enemy_health):
    if hero_health <= 0:
        clear_screen()
        typing_effect(custom_fig.renderText(
            '\nYou have lost...\nGame Over!\n'), 0.005)
        sleep(2)
        restart_game()
    elif enemy_health <= 0:
        clear_screen()
        typing_effect(custom_fig.renderText(
            '\nThe enemy is defited. You are victorious!\n'), 0.005)
        typing_effect(health_status_text, 0.05)
        sleep(2)
        restart_game()


# Restart or end of the game
def restart_game():
    # clear_screen()
    typing_effect('\n\nPLAY AGAIN - press "1"\n', 0.05)
    typing_effect('QUIT - press "2"\n\n', 0.05)
    game_choice = verify_user_input(2)
    if game_choice == 2:
        sys.exit(typing_effect('Goodby...', 0.05))
    game()


# Battle function
def fight(hero_power, hero_health, enemy_power, enemy_health, weapon_name):
    clear_screen()
    typing_effect(custom_fig.renderText('Battle begin!'), 0.005)
    damage = 0
    if weapon_name == 'wooden club':
        typing_effect(fight_text_1, 0.05)
        hero_power = hero_power - 100
    else:
        typing_effect(fight_text_2.format(weapon_name), 0.05)

    while True:
        typing_effect('\n{}, your health is {} HP\n'.format(
            hero_name, round(hero_health, 2)), 0.05)
        typing_effect('{} health is {} HP\n'.format(
            enemy_name, round(enemy_health, 2)), 0.05)
        typing_effect('\nYou attack the enemy with your {}  '.format(
            weapon_name), 0.05)
        typing_effect('(Rolling the damage modificator dice...)\n', 0.05)
        damage = damage_modificator(hero_power)
        typing_effect('{} did {} damage to {}'.format(
            hero_name, round(damage, 2), enemy_name), 0.05)
        enemy_health -= damage
        if health_status(hero_health, enemy_health):
            break
        typing_effect('\n\n{} attacks you  '.format(enemy_name), 0.05)
        typing_effect('(Rolling the damage modificator dice...)\n', 0.05)
        damage = damage_modificator(enemy_power)
        typing_effect('{} did {} damage to {}\n'.format(
            enemy_name, round(damage, 2), hero_name), 0.05)
        hero_health -= damage
        if health_status(hero_health, enemy_health):
            break
        sleep(2)


def door_choice():
    # clear_screen()
    typing_effect("{}, where do you want to go?\n".format(hero_name), 0.05)
    typing_effect(
        '1. Left door (where the enemy ...) \n2. Right door\n', 0.05)
    door_choice = verify_user_input(2)
    return door_choice


def find_ring(hero_power):
    if random.randint(1, 2) == 2:
        ring_of_power = random.randint(100, 200)
        hero_power = hero_power + ring_of_power
        typing_effect(hidden_treasure, 0.05)
        typing_effect(no_other_way.format(enemy_name), 0.05)
        typing_effect(attack.format(enemy_name), 0.05)
        fight(hero_power, hero_health, enemy_power, enemy_health, weapon_name)
    else:
        typing_effect("You don't see anything new...\n", 0.05)
        typing_effect("You are back to the room with the cage\n", 0.05)
        cage_room()


def cage_room():
    choice = door_choice()
    if choice == 1:
        enemy_room()
    treasure_room()


def enemy_room():
    global weapon_name
    if weapon_name == '':
        weapon_name = 'wooden club'
    typing_effect(enemy_door.format(enemy_name, enemy_name), 0.05)
    typing_effect(left_room_actions.format(enemy_name), 0.05)
    left_door_action = verify_user_input(2)
    if left_door_action == 1:
        fight(hero_power, hero_health, enemy_power, enemy_health, weapon_name)
    else:
        cage_room()


def treasure_room():
    global weapon_found
    global hero_power
    global weapon_name
    if weapon_found == 0:
        weapon_found = 1
        weapon_name = random.choice(armory[user_char])
        mighty_weapon_power = random.randint(100, 200)
        hero_power = hero_power + mighty_weapon_power
        clear_screen()
        typing_effect(mysterious_door.format(weapon_name), 0.05)
        typing_effect(right_room_choice, 0.05)
        if verify_user_input(2) == 1:
            # door_choice()
            cage_room()
        else:
            find_ring(hero_power)
    elif weapon_found == 1:
        typing_effect(empty_room, 0.05)
        find_ring(hero_power)
        typing_effect(right_room_choice, 0.05)
        if verify_user_input(2) == 1:
            cage_room()
        else:
            find_ring(hero_power)


def game():
    global hero_name
    global hero_health
    global hero_power
    global enemy_name
    global enemy_power
    global enemy_health
    global user_char
    global weapon_found
    global weapon_name
    global custom_fig
    global armory

    # Initializing variables
    # Banner font
    custom_fig = Figlet(font='ogre')

    # Hero selection
    heroes = ['', 'WARRIOR', 'WIZARD', 'ROGUE']

    # Randomly picking the enemy from the list
    enemies = ['Golem', 'Troll', 'Orc']

    # Dict to store the weapons for each class
    armory = {
        'WARRIOR':
        ['Sword of Sharpiness', 'Battle Axe of Mauletar', 'Sword of Balduran'],
        'WIZARD':
        ['Scepter of Radiance', 'Wand of the Heavens', 'Wand of Wonder'],
        'ROGUE':
        ['Soultaker Dagger', 'Moonblade', 'Dagger of the Star']
    }

    # weapon_name
    weapon_found = 0
    weapon_name = ''

    # Game banner
    clear_screen()
    typing_effect(custom_fig.renderText('The Great Escape'), 0.005)

    # Start of the game and character choice
    typing_effect('\n\nGAME START - press "1"\n', 0.05)
    typing_effect('QUIT - press "2"\n\n', 0.05)

    # Ask user to choose what to do
    game_status = verify_user_input(2)

    # Start the game or quit
    if game_status == 2:
        clear_screen()
        sys.exit(typing_effect(
            "Where you are going? Who will save the world?!\n\n", 0.05))

    clear_screen()
    typing_effect(prologue, 0.05)
    clear_screen()

    # Asking user to enter his name
    typing_effect('What is your name, hero? ', 0.05)
    hero_name = input()

    clear_screen()
    typing_effect('Select a character...\n', 0.05)
    print('1. {}\n2. {}\n3. {}'.format(heroes[1], heroes[2], heroes[3]))
    char_choice = verify_user_input(3)
    user_char = heroes[char_choice]

    # User choice of hero
    clear_screen()
    typing_effect('{}, your hero is {}\n'.format(hero_name, user_char), 0.05)

    # Generating hero stats
    typing_effect(
        '{}, rolling the stats of your hero...\n'.format(hero_name), 0.05)
    hero_stats, hero_health, hero_power = generate_stats(user_char)

    # Pringing the generated stats
    typing_effect('Hero stats are:\n', 0.05)

    for key, value in hero_stats.items():
        typing_effect('{}: {}\n'.format(key, value), 0.05)
    sleep(2)

    # Generating enemy
    enemy_name = random.choice(enemies)
    enemy_stats, enemy_health, enemy_power = generate_stats(enemy_name)

    # Begining of the story
    clear_screen()
    typing_effect(story_begins.format(hero_name, enemy_name), 0.05)
    clear_screen()
    typing_effect(escape_from_cell, 0.05)
    clear_screen()
    typing_effect(escape_from_prison.format(enemy_name), 0.05)
    clear_screen()

    # Choice where the player will go and what will find
    cage_room()


# ==================== MAIN =====================
fight_text_1 = '\nIn your hand you hold your \
 trusty (but not very effective) wooden club.'

fight_text_2 = '\nThe {} shines brightly in your hand \
as you brace yourself for the attack.\n'

health_status_text = (
    'Great! You defeated your first enemy and escaped.\n'
    'You have won in one battle, BUT the war is not over yet.\n'
    'Stay strong as new adventures and battles are expecting you in future.'
)

prologue = (
    'It is said that when war threatens the world, \n'
    'one individual will be selected by prophecy to lead the \n'
    'Shadow Warriors out of Land of Mist and reclaim the freedom \n'
    'which has been stolen.'
)

story_begins = (
    '{}, your own nightmares awaken you, sweat dripping from your brow, \n'
    'you quickly open your eyes only to have your own hopes smashed \n'
    'as you find yourself still locked in the'
    ' cage you have called home for some time now.\n'
    'In your nightmares you being tortured by a mage. \n'
    'Who he is, or what he wants, is a mystery.\n'
    'Soon a {} arrives and announces'
    ' that the complex is under attack.\n'
    'The mage teleports away, '
    'presumably to help defend the complex against the invaders.'
)

escape_from_cell = (
    'You are looking around you with hope to find your way'
    ' out of the prison.\n'
    'Close to your cage you see a wooden club.\n'
    'With some effort, you succeed to reach out'
    ' with your hand and grab the club.\n'
    'You strike the lock of the cage door with the club.\n'
    'Again...\nand again...\n'
    'Finally, you were able to brake the lock and open the door.\n'
    'You are open the door and escape from the cage.'
)


escape_from_prison = (
    'You are look around you and see two doors.\n'
    'The left door is where the {} went in your nightmare.\n'
    'What hides the right door you have no clue.\n'
)

hidden_treasure = (
    'Your eye catches a glint of metal in the corner of the room.\n'
    'You have found the Ring of Power.\n'
    'Suddenly you see a flash of light.\n'
    'then you have been teleported outside of the room.\n'
    'The door is closed and no longer open.\n'
)

enemy_door = (
    "You open the door and see {} standing with his back to you.\n"
    "It seems that, {} don't see you.\n"
    "What is your next action?\n"
)

left_room_actions = (
    '1. Attack the {}.\n'
    '2. Exit the room.\n'
)

mysterious_door = (
    'You entered the room and saw no one inside.\n'
    'In the center of the room you see a treasure chest\n'
    'You have opened the chest and found the mighty {}.\n'
    'What you would like to do next?\n'
)

right_room_choice = (
    '1. Exit the room.\n'
    '2. Have another look in the room\n'
)

empty_room = (
    'You entered again the empty room.\n'
    'Nothing left in a treasure chest\n'
)

no_other_way = (
    'You now have only one way out.\n'
    'You have to defeat the {} in the left room,\n'
    'and free your way out of prison.\n'
)

attack = 'You opened the left door and attacked the {}\n'

game()
