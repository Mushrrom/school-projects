import random
import os
import time

global health, ehealth, gamelog
health = 100
ehealth = 100
gamelog = []


def print_game():
    os.system('cls' if os.name == "nt" else "clear")  # Clear screen

    # Print enemy health bar
    ehealthdash = ''.join('-' for _ in range(round(ehealth/5)))
    ehealthspace = ''.join(' ' for _ in range(20-round(ehealth/5)))
    print(f"Enemy's health: [\033[31m{ehealthdash}{ehealthspace}\033[0m] {ehealth}/100")

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
while ehealth > 0 and health > 0:

    ah = input("attack or heal: ")

    if ah.startswith("a"): # Attack
        dmg = random.randint(0, 20)
        gamelog.insert(0, f"> \033[32mYou atttacked and did {dmg} damage\033[0m")
        ehealth -= dmg
        if ehealth < 0: ehealth = 0
    else: # Heal
        heal_amount = random.randint(0, 10)
        gamelog.insert(0, f"> \033[32mYou healed and got {heal_amount} health\033[0m")
        health += heal_amount
        if health > 100: health = 100

    # Print game log after player turn
    if len(gamelog) > 10:
        gamelog = gamelog[:10]
    print_game()

    if ehealth <= 0: break

    print("Enemy's turn...")

    time.sleep(2)

    enemy_dmg = random.randint(0, 30)
    gamelog.insert(0, f"> \033[31mEnemy attacked and did {enemy_dmg} damage\033[0m")
    health -= enemy_dmg

    if health < 0: health = 0

    # Print game log after enemy turn
    if len(gamelog) > 10:
        gamelog = gamelog[:10]
    print_game()


print("\nPlayer won!" if ehealth <= health else "\nEnemy won :(") # Handle winner
