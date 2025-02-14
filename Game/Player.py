import pygame as pg
import math
from settings import *

class Player:
    def __init__(self, x, y):
        self.image = pg.image.load("player.png")
        self.sword_image=pg.image.load("sword.png")
        self.width = 50
        self.height = 75
        self.image = pg.transform.scale(self.image, (self.width, self.height))
        self.sword_image = pg.transform.scale(self.sword_image, (75,75))
        self.original_image = self.image  # Store the original image for rotation
        self.x = x
        self.sound2 = pg.mixer.Sound("sword-sound-260274.mp3")
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.attack_range = 300
        self.attack_size = 300
        self.attack_area = None
        self.damage = False
        self.last_attack_time = 0
        self.invincible_time = 0  # Time when the player last became invincible
        self.invincible_duration = 1000  # Invincible duration in milliseconds (1 second)

    def move(self, dx, dy, game_background):
        # First, check horizontal movement (x-axis)
        if not self.is_colliding_with_wall(self.x + dx, self.y, game_background):
            self.x += dx

        # Then, check vertical movement (y-axis)
        if not self.is_colliding_with_wall(self.x, self.y + dy, game_background):
            self.y += dy

        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.draw_sword(screen)
        
    def draw_sword(self, screen):
        # Get the vector from the player to the mouse
        mouse_x, mouse_y = pg.mouse.get_pos()
        dx = mouse_x - (self.x + self.width / 2)
        dy = mouse_y - (self.y + self.height / 2)
    
        # Calculate the angle to rotate the sword
        angle = math.atan2(dy, dx)
    
        # Rotate the sword image
        rotated_sword = pg.transform.rotate(self.sword_image, math.degrees(angle))
        rotated_sword_rect = rotated_sword.get_rect()
    
        # Number of swords and distance between each sword
        num_swords = 5
        sword_spacing = self.attack_range / num_swords
        
    
        
        # Draw the swords, each one a little closer than the previous one
        for i in range(num_swords):
            distance = self.attack_range - i * sword_spacing
            # Calculate the sword's position
            sword_x = self.x + self.width / 2 + math.cos(angle) * distance
            sword_y = self.y + self.height / 2 + math.sin(angle) * distance
    
            rotated_sword_rect.center = (sword_x, sword_y)
            if i != 0:
                screen.blit(rotated_sword, rotated_sword_rect)
    def get_rect(self):
        return self.rect

    def handle_input(self, keys, game_background, speed):
        dx, dy = 0, 0

        # Handle vertical and horizontal movements
        if keys[pg.K_w]:
            dy = -speed
        if keys[pg.K_s]:
            dy = speed
        if keys[pg.K_a]:
            dx = -speed
        if keys[pg.K_d]:
            dx = speed
        
        # Handle movement while checking collisions
        self.move(dx, dy, game_background)
        
        # Get mouse position correctly using Pygame
        mouse_pos = pg.mouse.get_pos()  # This fetches the mouse position as a tuple (x, y)

        # Rotate player to face the mouse
        self.face_mouse(mouse_pos)

    def face_mouse(self, mouse_pos):
        # Get the vector from the player to the mouse
        mouse_x, mouse_y = mouse_pos  # Unpack the tuple (x, y)
        dx = mouse_x - (self.x + self.width / 2)
        dy = mouse_y - (self.y + self.height / 2)

        # Calculate angle
        angle = math.atan2(dy, dx)  # Angle to the mouse in radians
        self.angle = angle  # Store angle for other calculations

    def take_damage(self):
        # The player takes damage if they aren't invincible
        current_time = pg.time.get_ticks()
        if not self.is_invincible():  # If player is not currently invincible
            self.damage = True
            self.invincible_time = current_time  # Set invincible time to current time
        else:
            self.damage = False  # Player is invincible, so no damage is taken

    def is_invincible(self):
        # Check if player is invincible (last 1 second after taking damage)
        current_time = pg.time.get_ticks()
        return current_time - self.invincible_time < self.invincible_duration  # 1000ms = 1 second

    def attack(self, enemies):
        player_center_x = self.x + self.width / 2
        player_center_y = self.y + self.height / 2

        # Create the attack area (adjust the width with attack_range)
        attack_area = pg.Surface((self.attack_range, self.attack_size))  # Width is attack_range
        attack_area.fill((255, 0, 0, 100))  # Red color with transparency (RGBA)

        # Rotate the attack area based on the player's facing direction
        attack_area = pg.transform.rotate(attack_area, math.degrees(self.angle))  # Rotate by angle in degrees
        attack_area_rect = attack_area.get_rect()

        # Position the rotated attack area at the center of the player
        attack_area_rect.center = (player_center_x, player_center_y)

        # Check if enemies are iterable (i.e., list of enemies)
        if isinstance(enemies, list):  # If it's a list of enemies
            for enemy in enemies:
                if attack_area_rect.colliderect(enemy.get_rect()):
                    enemy.take_damage()
        else:  # If it's a single enemy
            if attack_area_rect.colliderect(enemies.get_rect()):
                enemies.take_damage()

        return attack_area_rect

    def check_collision(self, enemies, attack_cooldown):
        current_time = pg.time.get_ticks()  # Get the current time in milliseconds

        if pg.mouse.get_pressed()[0] and current_time - self.last_attack_time >= attack_cooldown:
            # Attack only if enough time has passed since the last attack
            self.attack(enemies)
            self.sound2.play()
            # Update the last attack time
            self.last_attack_time = current_time

    def is_colliding_with_wall(self, x, y, game_background):
        # Get the four corners of the player’s new position
        corners = [
            (x, y),  # Top-left
            (x + self.width, y),  # Top-right
            (x, y + self.height),  # Bottom-left
            (x + self.width, y + self.height)  # Bottom-right
        ]

        # Check if any of these corners collide with a wall (represented by 1 in the layout)
        for corner in corners:
            left = corner[0] // TILE_SIZE
            top = corner[1] // TILE_SIZE

            # Ensure we're within bounds of the tile map layout
            if 0 <= top < len(game_background.get_layout()) and 0 <= left < len(game_background.get_layout()[0]):
                if game_background.get_layout()[top][left] == 1 or game_background.get_layout()[top][left] == 8:
                    return True  # Collision detected

        return False  # No collision
