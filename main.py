import pygame # type: ignore
import sys
from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state, log_event
from player import Player
from shot import Shot

pygame.init()

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    asteroids = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    updatable = pygame.sprite.Group()
    
    Asteroid.containers = (asteroids, drawable, updatable)
    AsteroidField.containers = (updatable)
    Player.containers = (drawable, updatable)
    Shot.containers = (drawable, shots, updatable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroidfield = AsteroidField()

    dt = 0

    while True:
        log_state()
        
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                return

        updatable.update(dt)

        for asteroid in asteroids:
            if Asteroid.collides_with(asteroid, player):
                log_event("player_hit")
                print("Game over!")
                sys.exit()
            
            for shot in shots:
                if Shot.collides_with(shot, asteroid):
                    log_event("asteroid_shot")
                    Asteroid.split(asteroid)
                    Shot.kill(shot)

        screen.fill("black")
        for item in drawable:
            item.draw(screen)
        pygame.display.flip()   

        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()
