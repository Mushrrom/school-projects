import random
import os
import time

global health, enemy_health, gamelog
health = 100
enemy_health = 100
gamelog = []


def print_game():
    os.system('cls' if os.name == "nt" else "clear")  # Clear screen

    # Print enemy health bar
    enemy_health_dash = ''.join('-' for _ in range(round(enemy_health/5)))
    enemy_health_space = ''.join(' ' for _ in range(20-round(enemy_health/5)))
    print(f"Enemy's health: [\033[31m{enemy_health_dash}{enemy_health_space}\033[0m] {enemy_health}/100")

    # Print player health bar
    healthdash = ''.join('-' for _ in range(round(health/5)))
    healthspace = ''.join(' ' for _ in range(20-round(health/5)))
    print(f"Your health: [\033[31m{healthdash}{healthspace}\033[0m] {health}/100")

    # Print the game log
    print("\n Game log:")
    print("-----------------------------------------------------------------")
    # Print all items in the game log
    for i in gamelog:
        print(i)

    # Print new lines so game log area stays same
    for _ in range(10-len(gamelog)):
        print("")
    print("-----------------------------------------------------------------")


print_game()
while enemy_health > 0 and health > 0:

    ah = input("attack or heal: ").lower()

    if ah.startswith("a"): # player attack
        dmg = random.randint(0, 20)
        gamelog.insert(0, f"> \033[32mYou atttacked and did {dmg} damage\033[0m")
        enemy_health -= dmg
        enemy_health = max(enemy_health, 0)  # Set enemy health to 0 if it's less than 0
    else: # Player heal
        heal_amount = random.randint(0, 10)
        gamelog.insert(0, f"> \033[32mYou healed and got {heal_amount} health\033[0m")
        health += heal_amount
        health = min(health, 100) # Set health to 100 if greater than 100

    # delete values from end of game log if len > 10
    if len(gamelog) > 10:
        gamelog = gamelog[:10]

    print_game()

    # Because we are attacking the enemy first we break if enemy is dead
    if enemy_health <= 0: break

    print("Enemy's turn...")

    time.sleep(2)

    # Do enemy damage to player
    enemy_dmg = random.randint(0, 30)
    gamelog.insert(0, f"> \033[31mEnemy attacked and did {enemy_dmg} damage\033[0m")
    health -= enemy_dmg

    health = max(health, 0) # Set player health to 0 if less than 033

    # delete values from end of game log if len > 10 
    if len(gamelog) > 10:
        gamelog = gamelog[:10]

    print_game()


print("\nPlayer won!" if enemy_health <= health else "\nEnemy won :(") # Handle winner

