import src.ships.bullet

def updateEnemies(enemiesList, enemiesSurface, player, bulletsList):

    # Clear the enemies from the surface
    for enemy in enemiesList:
        enemy.clearEnemy(enemiesSurface)

    for enemy in enemiesList:
        enemy.rotateEnemy(player.position[0], player.position[1])
        enemy.moveEnemy(6)
        enemy.renderEnemy(enemiesSurface)
        if enemy.frames % 30 == 0:
            bulletsList.append(src.ships.bullet.newBullet([enemy.position[0], enemy.position[1]],
                                                          50, enemy.angle, "enemy"))

    return bulletsList

def updateBullets(bulletsList, enemiesSurface, enemiesList, player):
    for count, bullet in enumerate(bulletsList):
        bullet.clearBullet(enemiesSurface)
        bullet.moveBullet()
        bullet.checkCollisions(player, enemiesList)
        bullet.render(enemiesSurface)

        if bullet.distance > 100:
            bulletsList.pop(count)

    return bulletsList



