import pygame as pg
import math
import heapq
import random
from settings import *
class Enemy:
    def __init__(self, x, y, speed=3, hp=10, image="enemy.png", delay=1000, erange=400):
        self.e=random.randint(1,2)
        if self.e==1:
            self.hp = hp
            self.speed = speed
            self.width = 80
            self.height = 80
        elif self.e==2:
            self.hp = 5
            self.speed = 5
            self.width = 100
            self.height = 100
            image="speed.png"
        self.ehp=self.hp
        self.image = pg.image.load(image)
        self.image = pg.transform.scale(self.image, (self.width, self.height))
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.delay = delay
        self.range = erange
        self.roaming_timer = pg.time.get_ticks()
        self.target_x = self.x
        self.target_y = self.y

    def get_rect(self):
        return self.rect

    def calculate_distance(self, player):
        dx = self.rect.centerx - player.rect.centerx
        dy = self.rect.centery - player.rect.centery
        return math.sqrt(dx**2 + dy**2)

    def move_towards(self, target_x, target_y, enemies, game_background):
        dx = target_x - self.rect.x
        dy = target_y - self.rect.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance > 0:
            dx /= distance
            dy /= distance

        new_x = self.rect.x + dx * self.speed
        new_y = self.rect.y + dy * self.speed

        if self.is_near_wall(game_background):
            self.move_away_from_wall(game_background)
        else:
            if not self.check_collision_with_other_enemies(new_x, new_y, enemies):
                self.rect.x = new_x
                self.rect.y = new_y

    def is_near_wall(self, game_background):
        left = self.rect.left // TILE_SIZE
        right = self.rect.right // TILE_SIZE
        top = self.rect.top // TILE_SIZE
        bottom = self.rect.bottom // TILE_SIZE

        if game_background.get_layout()[top][left] == 1 or \
           game_background.get_layout()[top][right] == 1 or \
           game_background.get_layout()[bottom][left] == 1 or \
           game_background.get_layout()[bottom][right] == 1 or \
           game_background.get_layout()[top][left] == 8 or \
           game_background.get_layout()[top][right] == 8 or \
           game_background.get_layout()[bottom][left] == 8 or \
           game_background.get_layout()[bottom][right] == 8:
            return True
        return False

    def move_away_from_wall(self, game_background):
        left = self.rect.left // TILE_SIZE
        right = self.rect.right // TILE_SIZE
        top = self.rect.top // TILE_SIZE
        bottom = self.rect.bottom // TILE_SIZE

        move_direction = pg.Vector2(0, 0)

        if game_background.get_layout()[top][left] == 1 or game_background.get_layout()[top][right] == 1:
            move_direction.y = 1
        if game_background.get_layout()[bottom][left] == 1 or game_background.get_layout()[bottom][right] == 1:
            move_direction.y = -1
        if game_background.get_layout()[top][left] == 1 or game_background.get_layout()[bottom][left] == 1:
            move_direction.x = 1
        if game_background.get_layout()[top][right] == 1 or game_background.get_layout()[bottom][right] == 1:
            move_direction.x = -1

        if move_direction.length() > 0:
            move_direction.normalize_ip()
            self.rect.x += move_direction.x * self.speed
            self.rect.y += move_direction.y * self.speed

    def check_collision_with_other_enemies(self, new_x, new_y, enemies):
        for enemy in enemies:
            if enemy != self:
                if enemy.rect.colliderect(pg.Rect(new_x, new_y, self.width, self.height)):
                    return True
        return False

    def draw(self, screen):
        # Draw the enemy
        screen.blit(self.image, self.rect)
        # Draw the enemy's health above them
        self.draw_health(screen)

    def draw_health(self, screen):
        # Draw the health bar above the enemy
        health_bar_width = 30
        health_bar_height = 5
        health_percent = self.hp / self.ehp
        health_bar = pg.Rect(self.rect.centerx - health_bar_width // 2, self.rect.top - 10, health_bar_width, health_bar_height)

        # Draw the background of the health bar (empty)
        pg.draw.rect(screen, (0, 0, 0), health_bar)

        # Draw the filled part based on the enemy's HP
        filled_health_bar = pg.Rect(self.rect.centerx - health_bar_width // 2, self.rect.top - 10, health_bar_width * health_percent, health_bar_height)
        pg.draw.rect(screen, (255, 0, 0), filled_health_bar)

    def check_collision(self, player):
        if self.rect.colliderect(player.get_rect()):
            player.take_damage()

    def take_damage(self):
        self.hp -= 1


    def follow_player(self, player, game_background, enemies):
        if self.calculate_distance(player) <= self.range:
            path = self.a_star_pathfinding(game_background, player.rect.centerx, player.rect.centery)

            if path and len(path) > 1:
                next_tile = path[1]
                self.target_x = next_tile[0] * TILE_SIZE
                self.target_y = next_tile[1] * TILE_SIZE
            elif path:
                next_tile = path[0]
                self.target_x = next_tile[0] * TILE_SIZE
                self.target_y = next_tile[1] * TILE_SIZE

        self.move_towards(self.target_x, self.target_y, enemies, game_background)

    def a_star_pathfinding(self, game_background, goal_x, goal_y):
        start = (self.rect.centerx // TILE_SIZE, self.rect.centery // TILE_SIZE)
        goal = (goal_x // TILE_SIZE, goal_y // TILE_SIZE)

        open_list = []
        closed_list = set()
        came_from = {}

        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}

        heapq.heappush(open_list, (f_score[start], start))

        while open_list:
            _, current = heapq.heappop(open_list)

            if current == goal:
                return self.reconstruct_path(came_from, current)

            closed_list.add(current)

            for neighbor in self.get_neighbors(current):
                if neighbor in closed_list:
                    continue

                if not self.is_walkable(neighbor, game_background):
                    continue

                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)

                    if not any(neighbor == item[1] for item in open_list):
                        heapq.heappush(open_list, (f_score[neighbor], neighbor))

        return []

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_neighbors(self, node):
        x, y = node
        neighbors = [
            (x, y - 1),  # Up
            (x, y + 1),  # Down
            (x - 1, y),  # Left
            (x + 1, y),  # Right
            (x - 1, y - 1),  # Up-left
            (x + 1, y - 1),  # Up-right
            (x - 1, y + 1),  # Down-left
            (x + 1, y + 1)   # Down-right
        ]
        return neighbors

    def is_walkable(self, node, game_background):
        x, y = node
        if 0 <= x < len(game_background.get_layout()[0]) and 0 <= y < len(game_background.get_layout()):
            return game_background.get_layout()[y][x] != 1
        return False

    def reconstruct_path(self, came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path


class NormalEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, speed=3, hp=10, image="enemy.png")
#IDK HOW TO FIX IT SRRY

