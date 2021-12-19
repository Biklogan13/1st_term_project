# 1st_term_project 
By Krylovskiy Ilia, Kozyrev Ivan and Kozlov Nikolai

A documentation for the Deep Space Pylots game.

Software requirements:

Python IDE with Python 3.9 or older and following libraries:

- pygame 2.0.2 or older
- random
- math
- os
- copy

In-game controls:

- Acceleration upwards – W
- Acceleration to the left – A
- Acceleration downwards – S
- Acceleration to the right – D
- Select autocannon – 1
- Select plasma cannon – 2
- Select laser – 3
- Weaponry aiming – mouse movement
- Fire – Mouse1
- Use Super – Space
- Exit to main menu – Esc

Buttons in main menu:

- Play – resume playing the game.
- Shop – go to the shop menu.
- Exit – closes the game.

Buttons in shop:

- Cosmetics – go to submenu in which you can select background images
- Upgrades – go to submenu un which you can purchase ship upgrades
- Ships – go to submenu in which you can purchase new ships
- Buy (conic shape in Upgrades submenu) – buys an item and spends corresponding amount of money on it.
- Select – if an item is purchased but unused, uses it.
- Selected – is displayed instead of Select if an item is being used.

In-game object descriptions:

- Spaceship – a unit which player controls, can freely move around the screen.

Enemies

- Mine – a mine which moves from above the screen, can collide with the spaceship and be shot.
- Kamikaze – an enemy which homes onto the spaceship, can be collided with and shot.
- Standart enemy – an enemy which moves from above the screen in a quarter-circle, then shoots bullets in direction of the spaceship, after that moves in a quarter-circle to below the screen, can be collided with and shot.
- Heavy enemy – an enemy which moves from above the screen, then turns in direction of the spaceship and starts shooting missiles, can be collided with and shot.
- Enemy carrier – an enemy which moves in a circle above the screen launching kamikazes when in sight, can be collided with and shot.
- Missile – enemy missile which homes onto the spaceship, can be collided with and shot.

Weaponry:

- Bullet – a projectile which travels in a straight line with a slight scatter, can be collided with, disappears after impact.
- Plasma ball – a projectile which travels in a straight line, can be collided with, passes through enemies.
- Laser – a beam which passes through enemies, can be collided with.
- Light ring – a Super which destroys every enemy present on the screen.

Supplementary:

- Coin – a coin which drops after enemy destruction, can be picked up if the spaceship is close enough.

Gameplay:

The goal of the game is to earn as much money as possible. The player is to shoot down periodically spawning enemies while dodging them and projectiles they launch. Projectiles which the spaceship launches damage enemies. Projectiles which are launched by enemies damage the spaceship. An enemy can be rammed, but the spaceship will take damage. Destroying enemies charges the Super scale, charge can be spent on activating Supers. Coins earned from destroying enemies can be spent on items in the Shop.
