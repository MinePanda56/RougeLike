import pygame as pg
import math
import random
from settings import *
mapp=0
class BossTank:
    global mapp
    mapp=1
    def __init__(self, x=200, y=200, delay=1000, behind_screen=False):
        self.image = pg.image.load('BossTank.png')  # Boss image
        self.width = 150
        self.height = 150
        self.x = x
        self.y = y
        self.image = pg.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hp = 10  # Boss health
        self.speed = 20  # Movement speed
        self.target_x = x  # Initial target coordinates (start at the boss's current position)
        self.target_y = y

        # Load and initialize shield
        self.shield_image = pg.image.load('shield.png')
        self.shield_image = pg.transform.scale(self.shield_image, (50, 50))  # Resize the shield
        self.shield_angles = [i * (360 / 10) for i in range(10)]  # 10 shields, spaced evenly
        self.shield_radius = 60  # Radius of the shield around the boss

        # Flags to track whether shields are active, and each shield has 3 HP
        self.shields_active = [True] * 10  # All shields are initially active
        self.shields_hp = [3] * 10  # Each shield starts with 3 HP

        # Optional: Spawn behind the screen if behind_screen is True
        if behind_screen:
            self.rect.x = -self.rect.width  # Spawn behind the left side of the screen
            self.rect.y = random.randint(0, pg.display.get_surface().get_height())  # Random y position

    def get_rect(self):
        return self.rect

    def calculate_distance(self, player):
        dx = self.rect.centerx - player.rect.centerx
        dy = self.rect.centery - player.rect.centery
        return math.sqrt(dx**2 + dy**2)

    def move_towards(self, target_x, target_y, game_background):
        dx = target_x - self.rect.x
        dy = target_y - self.rect.y
        distance = math.sqrt(dx**2 + dy**2)
        self.speed -= 1
        if self.speed <= -5:
            self.speed = 10
        if distance > 0:
            dx /= distance
            dy /= distance
            # Prevent clipping into walls
            if not self.is_near_wall(game_background):
                self.rect.x += dx * self.speed
                self.rect.y += dy * self.speed
            else:
                self.move_away_from_wall(game_background)

    def update(self, player, game_background):
        # Calculate the distance to the player
        distance = self.calculate_distance(player)

        # If the player is too close, move away from the player
        if distance < 50:  # Adjust this distance as necessary
            self.move_away_from(player.rect.centerx, player.rect.centery)
        else:
            # Otherwise, move towards the player
            self.move_towards(player.rect.centerx, player.rect.centery, game_background)

        # Ensure the boss doesn’t clip into walls
        if self.is_near_wall(game_background):
            self.move_away_from_wall(game_background)

        # Check for collision with the player
        self.check_collision(player)

        # Update shield positions and rotation
        self.update_shields()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.draw_shields(screen)  # Draw shields around the boss

    def draw_health(self, screen):
        # Draw the health bar above the boss
        health_bar_width = 50
        health_bar_height = 5
        health_percent = self.hp / 10  # Max HP of the boss is 20
        health_bar = pg.Rect(self.rect.centerx - health_bar_width // 2, self.rect.top - 10, health_bar_width, health_bar_height)

        # Draw the background of the health bar (empty)
        pg.draw.rect(screen, (0, 0, 0), health_bar)

        # Draw the filled part based on the boss's HP
        filled_health_bar = pg.Rect(self.rect.centerx - health_bar_width // 2, self.rect.top - 10, health_bar_width * health_percent, health_bar_height)
        pg.draw.rect(screen, (255, 0, 0), filled_health_bar)

    def take_damage(self, damage=1):
        # First, try to reduce shield HP if shields are active
        for i in range(10):
            if self.shields_active[i]:
                # Apply damage to the shield
                self.shields_hp[i] -= damage
                if self.shields_hp[i] <= 0:
                    self.shields_active[i] = False  # Deactivate shield if HP reaches 0
                    self.shields_hp[i] = 0  # Ensure shield HP doesn't go below 0
                return  # Stop applying damage after hitting a shield

        # If no shields are active, apply damage to the boss's HP
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0  # Ensure health doesn't go below 0

    def check_collision(self, player):
        if self.rect.colliderect(player.get_rect()):
            player.take_damage()

    def is_near_wall(self, game_background):
        left = self.rect.left // TILE_SIZE
        right = self.rect.right // TILE_SIZE
        top = self.rect.top // TILE_SIZE
        bottom = self.rect.bottom // TILE_SIZE

        # Check if any of the boss's tiles are near a wall (denoted by 1 in the layout)
        return (
            game_background.get_layout()[top][left] == 1 or
            game_background.get_layout()[top][right] == 1 or
            game_background.get_layout()[bottom][left] == 1 or
            game_background.get_layout()[bottom][right] == 1 or 
            game_background.get_layout()[top][left] == 8 or
            game_background.get_layout()[top][right] == 8 or
            game_background.get_layout()[bottom][left] == 8 or
            game_background.get_layout()[bottom][right] == 8
        )

    def move_away_from_wall(self, game_background):
        left = self.rect.left // TILE_SIZE
        right = self.rect.right // TILE_SIZE
        top = self.rect.top // TILE_SIZE
        bottom = self.rect.bottom // TILE_SIZE

        move_direction = pg.Vector2(0, 0)

        # Perform a raycast in four directions (up, down, left, right) to check for walls
        if game_background.get_layout()[top][left] == 1 or game_background.get_layout()[top][right] == 1:
            move_direction.y = 1  # Move down if stuck at the top
        if game_background.get_layout()[bottom][left] == 1 or game_background.get_layout()[bottom][right] == 1:
            move_direction.y = -1  # Move up if stuck at the bottom
        if game_background.get_layout()[top][left] == 1 or game_background.get_layout()[bottom][left] == 1:
            move_direction.x = 1  # Move right if stuck on the left side
        if game_background.get_layout()[top][right] == 1 or game_background.get_layout()[bottom][right] == 1:
            move_direction.x = -1  # Move left if stuck on the right side

        # Adjust the position away from walls
        if move_direction.length() > 0:
            move_direction.normalize_ip()
            self.rect.x += move_direction.x * self.speed
            self.rect.y += move_direction.y * self.speed

        # Prevent out of bounds (screen boundaries)
        screen_width = pg.display.get_surface().get_width()
        screen_height = pg.display.get_surface().get_height()

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > screen_width:
            self.rect.right = screen_width

        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > screen_height:
            self.rect.bottom = screen_height

    def update_shields(self):
        # Rotate the shields around the boss
        for i in range(10):
            self.shield_angles[i] += 5  # Each shield rotates
            if self.shield_angles[i] >= 360:
                self.shield_angles[i] = 0  # Reset to 0 after a full rotation

    def draw_shields(self, screen):
        # Draw shields only if they are active
        for i in range(10):
            if self.shields_active[i]:
                shield_x = self.rect.centerx + self.shield_radius * math.cos(math.radians(self.shield_angles[i]))
                shield_y = self.rect.centery + self.shield_radius * math.sin(math.radians(self.shield_angles[i]))
                shield_rect = self.shield_image.get_rect(center=(shield_x, shield_y))
                screen.blit(self.shield_image, shield_rect)


class BossSpeed:
    global mapp
    mapp=2
    
    def __init__(self, x=800, y=200, delay=1000, behind_screen=False):
        self.image = pg.image.load('BossSpeed.png')  # Boss image
        self.width = 100
        self.height = 100
        self.x = x
        self.y = y
        self.image = pg.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hp = 15  # Boss health
        self.speed = 50  # Movement speed
        self.target_x = x
        self.target_y = y

        # Optional: Spawn behind the screen if behind_screen is True
        if behind_screen:
            self.rect.x = -self.rect.width  # Spawn behind the left side of the screen
            self.rect.y = random.randint(0, pg.display.get_surface().get_height())  # Random y position

    def get_rect(self):
        return self.rect

    def calculate_distance(self, player):
        dx = self.rect.centerx - player.rect.centerx
        dy = self.rect.centery - player.rect.centery
        return math.sqrt(dx**2 + dy**2)

    def move_away_from(self, target_x, target_y, game_background):
        dx = self.rect.centerx - target_x
        dy = self.rect.centery - target_y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            # Normalize direction vector
            dx /= distance
            dy /= distance

            # Check for nearby walls and adjust the movement direction accordingly
            move_direction = pg.Vector2(dx, dy)

            # If near a wall, try to find an alternative direction
            if self.is_near_wall(game_background):
                move_direction = self.find_safe_direction(game_background)

            # Move the boss away from the player (or in a safe direction)
            self.rect.x += move_direction.x * self.speed
            self.rect.y += move_direction.y * self.speed

    def find_safe_direction(self, game_background):
        # Try all possible directions and return the best one (away from player but not into walls)
        possible_directions = [
            pg.Vector2(1, 0),   # Right
            pg.Vector2(-1, 0),  # Left
            pg.Vector2(0, 1),   # Down
            pg.Vector2(0, -1),  # Up
            pg.Vector2(1, 1),   # Down-right diagonal
            pg.Vector2(-1, 1),  # Down-left diagonal
            pg.Vector2(1, -1),  # Up-right diagonal
            pg.Vector2(-1, -1)  # Up-left diagonal
        ]
        
        best_direction = pg.Vector2(0, 0)  # Default to no movement
        for direction in possible_directions:
            test_rect = self.rect.copy()
            test_rect.x += direction.x * self.speed
            test_rect.y += direction.y * self.speed

            if not self.is_near_wall_in_direction(test_rect, game_background):
                best_direction = direction
                break

        return best_direction

    def is_near_wall_in_direction(self, test_rect, game_background):
        # Get the layout dimensions
        layout = game_background.get_layout()
        layout_width = len(layout[0])  # Number of columns
        layout_height = len(layout)  # Number of rows

        # Calculate the grid positions of the new rectangle
        left = test_rect.left // TILE_SIZE
        right = test_rect.right // TILE_SIZE
        top = test_rect.top // TILE_SIZE
        bottom = test_rect.bottom // TILE_SIZE

        # Clamp the coordinates to ensure they are within bounds
        left = max(0, min(left, layout_width - 1))
        right = max(0, min(right, layout_width - 1))
        top = max(0, min(top, layout_height - 1))
        bottom = max(0, min(bottom, layout_height - 1))

        # Check if there is a wall in any of the directions
        return (
            game_background.get_layout()[top][left] == 1 or
            game_background.get_layout()[top][right] == 1 or
            game_background.get_layout()[bottom][left] == 1 or
            game_background.get_layout()[bottom][right] == 1 or 
            game_background.get_layout()[top][left] == 8 or
            game_background.get_layout()[top][right] == 8 or
            game_background.get_layout()[bottom][left] == 8 or
            game_background.get_layout()[bottom][right] == 8
        )

    def update(self, player, game_background):
        # Check the distance to the player
        distance = self.calculate_distance(player)

        # If the player is too close, move away from the player
        if distance < 500:  # Adjust this distance as necessary
            self.move_away_from(player.rect.centerx, player.rect.centery, game_background)

        # Check for collision with the player
        self.check_collision(player)

        # Ensure the boss doesn’t clip into walls
        self.check_and_push_back_within_bounds()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def draw_health(self, screen):
        # Draw the health bar above the boss
        health_bar_width = 50
        health_bar_height = 5
        health_percent = self.hp / 15  # Max HP of the boss is 15
        health_bar = pg.Rect(self.rect.centerx - health_bar_width // 2, self.rect.top - 10, health_bar_width, health_bar_height)

        # Draw the background of the health bar (empty)
        pg.draw.rect(screen, (0, 0, 0), health_bar)

        # Draw the filled part based on the boss's HP
        filled_health_bar = pg.Rect(self.rect.centerx - health_bar_width // 2, self.rect.top - 10, health_bar_width * health_percent, health_bar_height)
        pg.draw.rect(screen, (255, 0, 0), filled_health_bar)

    def take_damage(self, damage=1):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0  # Ensure health doesn't go below 0

    def check_collision(self, player):
        if self.rect.colliderect(player.get_rect()):
            player.take_damage()

    def is_near_wall(self, game_background):
        left = self.rect.left // TILE_SIZE
        right = self.rect.right // TILE_SIZE
        top = self.rect.top // TILE_SIZE
        bottom = self.rect.bottom // TILE_SIZE

        # Check if any of the boss's tiles are near a wall (denoted by 1 in the layout)
        return (
            game_background.get_layout()[top][left] == 1 or
            game_background.get_layout()[top][right] == 1 or
            game_background.get_layout()[bottom][left] == 1 or
            game_background.get_layout()[bottom][right] == 1
        )

    def check_and_push_back_within_bounds(self):
        screen_width = pg.display.get_surface().get_width()
        screen_height = pg.display.get_surface().get_height()

        # Ensure the boss stays within bounds
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > screen_width:
            self.rect.right = screen_width

        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
class BossSummon:
    global mapp
    mapp = 3
    
    def __init__(self, delay=1000, behind_screen=False):
        self.image = pg.image.load('BossSummoner.png')  # Boss image
        self.width = 225
        self.height = 300
        self.x=45
        self.y=60
        self.no=0
        self.image = pg.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.hp = 10  # Boss health

    def get_rect(self):
        return self.rect
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        if self.x<=1300 and self.no==0:
            self.x+=7
        else:
            self.no=1
            self.x-=7
            if self.x<=25:
                self.no=0
            
    def check_collision(self, player):
        if self.rect.colliderect(player.get_rect()):
            player.take_damage()
            
    def update(self, player):
        self.check_collision(player)
    def draw_health(self, screen):
        # Draw the health bar above the boss
        health_bar_width = 100
        health_bar_height = 15
        health_percent = self.hp / 10  
        health_bar = pg.Rect(self.rect.centerx - health_bar_width // 2, self.rect.top - 10, health_bar_width, health_bar_height)

        # Draw the background of the health bar (empty)
        pg.draw.rect(screen, (0, 0, 0), health_bar)

        # Draw the filled part based on the boss's HP
        filled_health_bar = pg.Rect(self.rect.centerx - health_bar_width // 2, self.rect.top - 10, health_bar_width * health_percent, health_bar_height)
        pg.draw.rect(screen, (255, 0, 0), filled_health_bar)
        
    def take_damage(self, damage=1):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0 
