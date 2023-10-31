import time

import pygame

import src.ships.bullet

def updateEnemies(enemiesList: list, enemiesSurface: pygame.surface, player: src.ships.player.newPlayer, bulletsList: list):
    """Updates the enemies positions & shoots bullets from enemies

    Args:
        enemiesList (list): the list of enemies currently in the game.
        enemiesSurface (pygame.surface): The surface to render the enemies to.
        player (src.ships.player.newPlayer): The player object.
        bulletsList (list): The list of bullets in the game.

    Returns:
        list: The updated bullets list
    """

    # Clear the enemies from the surface
    for enemy in enemiesList:
        enemy.clearEnemy(enemiesSurface)

    for enemy in enemiesList:
        enemy.rotateEnemy(player.position[0], player.position[1])
        enemy.moveEnemy(6)
        enemy.renderEnemy(enemiesSurface)
        if enemy.frames % 30 == 0:
            bulletsList.append(src.ships.bullet.newBullet([enemy.position[0], enemy.position[1]],
                                                          30, enemy.angle, "enemy"))

    return bulletsList

def updateBullets(bulletsList: list, enemiesSurface: pygame.surface, enemiesList: list,
                  player: src.ships.player.newPlayer, score: int, combo: int, lastHitTime: int):
    """Updates the bullets that are currently in the game

    Args:
        enemiesList (list): the list of enemies currently in the game.
        enemiesSurface (pygame.surface): The surface to render the enemies to.
        player (src.ships.player.newPlayer): The player object.
        bulletsList (list): The list of bullets in the game.
        score (int): The current game score
        combo (int): The current combo amount
        lastHitTime (int): Time time the enemy was last hit

    Returns:
        int: Updated score amount
        int: Updated combo amount
    """

    for count, bullet in enumerate(bulletsList):
        bullet.clearBullet(enemiesSurface)
        bullet.moveBullet()
        bulletCollision = bullet.checkCollisions(player, enemiesList)
        bullet.render(enemiesSurface)
        if bulletCollision[0] == True:
            if bulletCollision[1] >= 0:
                enemiesList[bulletCollision[1]].clearEnemy(enemiesSurface)
                enemiesList.pop(bulletCollision[1])
                score += 100*combo
                combo += 1
                lastHitTime = time.time()

            bullet.clearBullet(enemiesSurface)
            bulletsList.pop(count)
            break

        if bullet.distance > 100:
            bullet.clearBullet(enemiesSurface)
            bulletsList.pop(count)
            break

    return score, combo, lastHitTime
