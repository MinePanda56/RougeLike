#!/bin/bash
#
#BleedingEdge.sh for Mint Copyright (C)Talon Saylor
#Works only with zenity and notify-osd Installed!
#
#
#To run go into your game folder and enter terminal, then in the terminal type python3 rougelike.py
#Push "O" for skill point tree and "I" for inventory
#
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation,
#
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#No Warranty or guarantee of suitability exists for this software
#Use at your own risk. The author is not responsible if your system breaks.
#
#You should have received a copy of the GNU General Public License
#along with this program. If not, see <http://www.gnu.org/licenses/>.
#Arduino, Blu-Ray, Brave, Celestia, Chrome, Cinelerra, CLI Companion, Dolphin, Firefox, GetDeb, gImageReader, Google, GUFW, Hunspell, Linux, Microsoft, Minetest, Mint, ModemManager, PDF, PlayDeb, Remobo IPN, Samba, Simple Screen Recorder, Steam, StepMania, Ubuntu, Ubuntu Tweak, Wii, Wiithon, Wordnet, Y-PPA-Manager, and Zeal are trademarks of their respective owners.  No endorsement by any trademark holder is stated or implied.
import pygame as pg
import random
import sys
from Player import *
from Enemy import *
from settings import *
from Background import *
from items import *
from Boss import *
class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((RES))
        self.clock = pg.time.Clock()
        self.bg = pg.image.load("doors.webp")
        self.GameOver = pg.image.load("GameOver.png")
        self.bg = pg.transform.scale(self.bg, (RES))
        self.GameOver = pg.transform.scale(self.GameOver, (RES))
        self.display_info = pg.display.Info()
        self.FULLSCREEN = 0
        self.player = Player(x=780, y=700)
        self.gamebg = GameBackground()
        self.enemies = []
        self.PH = 1
        self.PPH=0
        self.LS=1
        self.SP=0
        self.map=0
        self.fredfaz=1
        self.pprr=1
        self.alive = 0
        self.pick=10
        self.sound1 = pg.mixer.Sound("8bit Dungeon Level.mp3") 
        self.sound1.play(999999999)
        self.money=8
        self.xp=0
        self.bossph=1
        self.Emoney=0
        self.spawnrate1=0
        self.spawnrate2=0
        self.lv=1
        self.BossTank=BossTank()
        self.BossSpeed=BossSpeed()
        self.BossSummon=BossSummon()
        self.pcc=1
        self.LLS=1
        self.speed=6
        self.attack_cooldown = 750 
        self.stop_enemy_spawn = False  # Added flag to stop enemy spawn when all enemies are dead
        self.door_rolled = False


        self.door_images = ["camp.png", "fight.png", "shop.png", "boss.png", "treasure.png", "Lifetrader.png", "chance.png"]
        self.DF1, self.DF2, self.DF3, self.selected_images = self.load_and_scale_images()

        # Define door positions (for example)
        self.door_positions = [(300, 50), (700, 50), (1100, 50)]

    def load_and_scale_images(self):
        selected_images = random.sample(self.door_images, 3)
        image1 = pg.image.load(selected_images[0])
        image2 = pg.image.load(selected_images[1])
        image3 = pg.image.load(selected_images[2])

        # Scale the images down (for example, scale to 200x100 pixels)
        scaled_image1 = pg.transform.scale(image1, (200, 100))
        scaled_image2 = pg.transform.scale(image2, (200, 100))
        scaled_image3 = pg.transform.scale(image3, (200, 100))

        return scaled_image1, scaled_image2, scaled_image3, selected_images

    def reset_game(self):
        global click
        global Charm_of_Pain
        global Weights
        global Necklace_of_growth
        global hp
        self.BossTank=BossTank()
        Weights=0
        Charm_of_Pain=0
        Necklace_of_growth=0
        self.SP=0
        click = 0
        hp=10
        self.pprr=1
        self.speed=6
        self.PH = 1
        self.PPH=0
        self.LS=1
        self.pcc=1
        self.bossph=1
        self.alive = 0
        self.money=8
        self.xp=0
        self.lv=1
        self.LLS=1
        self.Emoney=0
        self.spawnrate1=0
        self.spawnrate2=0
        self.attack_cooldown = 500 
        self.player = Player(x=780, y=700)  
        self.gamebg = GameBackground()  
        self.enemies = []  
        self.door_rolled = False  ake your data and AI to the next level with Databricks – free trial on AWS, Azure, or Google Cloud. Create production-ready Generative AI apps that are accurate, secure, and tailored to your business. Simplify data ingestion from hundreds of sources with effortless ETL automation. Plus, tap into instant, elastic serverless compute during your trial (available on AWS/Azure). Sign up with your work email now to unlock premium trial perks and transform how you work with data – don’t wait!

        self.stop_enemy_spawn = False

    def update(self):
        global click
        global damage
        global hp
        global Necklace_of_growth
        global long_double_sword
        global Weights
        global Charm_of_Pain
        keys=pg.key.get_pressed()
        if keys[pg.K_i]:
            if Necklace_of_growth==1:
                print("Necklace of growth:\nGives you .5 more xp but lose attack range and size")
                print("#################################################")
            if Weights==1:
                print("Weights\nMakes your attack cooldown 1 second")
                print("#################################################")
            if Charm_of_Pain==1:
                print("Charm of pain\nMax Hp limit is reduced to 20")
                print("#################################################")
            if long_double_sword==1:
                print("long_double_sword\nobtained by getting Weights and Charm of pain\nincreases attack range and size")
                print("#################################################")
            if self.PPH==0:
                print("you have no items")
                print("#################################################")
            print("You have: "+str(self.money)+" dollars")
            print("Your level: "+str(self.lv))
            print("Your Hp: "+str(hp))
            print("Xp: "+str(self.xp)+" level up at 100 xp")
            print("#################################################")
        if keys[pg.K_o]:
            print("Skill points: "+str(self.SP)+"\nPress 1.) for 5 of a milisecond off your attack cooldown\nPress 2.) to make less enemies spawn(Can't go bellow 1)\nPress 3.) to make more enemies spawn\nPress 4.) to increase the amount of money gained by killing")
            if keys[pg.K_1]:
                self.attack_cooldown-=5
                if self.SP>=1:
                    self.SP-=1
            elif keys[pg.K_2]:
                self.spawnrate1-=1
                if self.SP>=1:
                    self.SP-=1
            elif keys[pg.K_3]:
                self.spawnrate2+=1
                if self.SP>=1:
                    self.SP-=1
            elif keys[pg.K_4]:
                self.Emoney+=1
                if self.SP>=1:
                    self.SP-=1
        if Charm_of_Pain==1 and Weights==1:
            long_double_sword=1
        else:
            long_double_sword=0
        if self.player.damage==True:ake your data and AI to the next level with Databricks – free trial on AWS, Azure, or Google Cloud. Create production-ready Generative AI apps that are accurate, secure, and tailored to your business. Simplify data ingestion from hundreds of sources with effortless ETL automation. Plus, tap into instant, elastic serverless compute during your trial (available on AWS/Azure). Sign up with your work email now to unlock premium trial perks and transform how you work with data – don’t wait!

            hp-=1
            self.sound4 = pg.mixer.Sound("enemy.mp3")
            self.sound4.play()
            self.player.damage==False
        if self.xp>=100 and Charm_of_Pain!=1:
            self.lv +=1
            self.SP+=1
            hp+=random.randint(1,2)
            self.xp-=100
        if Charm_of_Pain==1:
            while hp>=50:
                hp-=1
            if self.xp>=100:
                self.xp-=100
                self.lv+=1
                hp+=1
        if click != 0:
            if self.PH == 1:
                if self.pick==1:
                    self.map=1
                elif self.pick==2:
                    self.map=2
                elif self.pick==3:
                    self.map=3
                self.gamebg.random(click,self.map)
                self.PH = 0
            self.gamebg.draw(self.screen)
        else:
            self.screen.blit(self.bg, (0, 0))
            self.player = Player(x=780, y=700)
            self.PH = 1ake your data and AI to the next level with Databricks – free trial on AWS, Azure, or Google Cloud. Create production-ready Generative AI apps that are accurate, secure, and tailored to your business. Simplify data ingestion from hundreds of sources with effortless ETL automation. Plus, tap into instant, elastic serverless compute during your trial (available on AWS/Azure). Sign up with your work email now to unlock premium trial perks and transform how you work with data – don’t wait!

        if click==1 or click==3:
            if self.alive==0 and self.player.x>=740 and self.player.x<=785 and self.player.y>=50 and self.player.y<=75:
                click=0
        else:
             if self.player.x>=740 and self.player.x<=785 and self.player.y>=50 and self.player.y<=75:
                click=0
        if Necklace_of_growth==1 and self.LLS==1:
            self.player.attack_range =150
            self.player.attack_size =150
        if long_double_sword==1 and Necklace_of_growth!=1:
            self.player.attack_range = 450
            self.player.attack_size = 450
        elif long_double_sword==1 and Necklace_of_growth==1:
            self.player.attack_range = 350
            self.player.attack_size = 350
        if Weights==1:
            if self.fredfaz==1:
                self.attack_cooldown=1000
                self.fredfaz=0
        # Reroll doors only once when click == 1 and the doors haven't been rolled yet
        if not click == 0 and not self.door_rolled:
            self.DF1, self.DF2, self.DF3, self.selected_images = self.load_and_scale_images()
            self.door_rolled = True  # Set the flag to prevent ake your data and AI to the next level with Databricks – free trial on AWS, Azure, or Google Cloud. Create production-ready Generative AI apps that are accurate, secure, and tailored to your business. Simplify data ingestion from hundreds of sources with effortless ETL automation. Plus, tap into instant, elastic serverless compute during your trial (available on AWS/Azure). Sign up with your work email now to unlock premium trial perks and transform how you work with data – don’t wait!
further rerolls during this session

        if click == 0:
            self.screen.blit(self.bg, (0, 0))  # Show the pre-game background image

        # Draw doors when click == 0, but no reroll
        if click == 0:
            self.screen.blit(self.DF1, self.door_positions[0])
            self.screen.blit(self.DF2, self.door_positions[1])
            self.screen.blit(self.DF3, self.door_positions[2])

        # Display game over screen if player's hp is 0
        if hp <= 0:
            self.reset_game()
            self.sound3 = pg.mixer.Sound("gameover.mp3") 
            self.sound3.play(0)

        # When click == 1, reset doors and player position
        if click != 0:
            # Reset the player's position when the game starts
            self.player.draw(self.screen)

        # Handle player movement and interaction with enemies
        if click != 0:
            self.player.handle_input(pg.key.get_pressed(), self.gamebg, self.speed)


        # Handle enemy actions: follow player, check collisions, etc.
        if click == 1:
            for enemy in self.enemies[:]:  # Iterate over a copy of the enemies list to avoid modification errors
                if enemy.hp >= 0:
                    # If the player is within range, follow the player
                    if enemy.calculate_distance(self.player) <= 300:
                        enemy.follow_player(self.player, self.gamebg, self.enemies)

                    enemy.check_collision(self.player)
                    self.player.check_collision(self.enemies,self.attack_cooldown)

                # Check if the enemy is defeated and update self.alive
                if enemy.hp <= 0:
                    self.alive -= 1 
                    self.enemies.remove(enemy)
                    self.money+=random.randint(1,10)
                    self.money+=self.Emoney
                    xpgain=random.randint(1,10)
                    if Necklace_of_growth==1:
                        xpgain*=1.5
                    self.xp=self.xp+xpgain

            # Stop spawning new enemies if all enemies are defeated
            if not self.enemies:  # No enemies left
                self.stop_enemy_spawn = True  # Prevent furtherake your data and AI to the next level with Databricks – free trial on AWS, Azure, or Google Cloud. Create production-ready Generative AI apps that are accurate, secure, and tailored to your business. Simplify data ingestion from hundreds of sources with effortless ETL automation. Plus, tap into instant, elastic serverless compute during your trial (available on AWS/Azure). Sign up with your work email now to unlock premium trial perks and transform how you work with data – don’t wait!
 spawning of enemies

            # Draw each remaining enemy on the screen
            for enemy in self.enemies:
                if enemy.hp >= 0:
                    enemy.draw(self.screen)
        elif click==3:
            if self.bossph==1:
                self.random=random.randint(1,1)
                self.bossph=0
            self.pick=self.random
            if self.pick==1:
                if self.pprr==1:
                    self.alive=1
                    self.BossTank.x=0
                    self.BossTank.y=0
                    self.pprr=0
                if self.BossTank.hp>=1:
                    self.prrpr=1
                    self.BossTank.draw(self.screen)
                    self.BossTank.draw_health(self.screen)
                    self.BossTank.update(self.player,self.gamebg)
                    self.player.check_collision(self.BossTank,self.attack_cooldown)
                else:
                    self.alive=0
                    if self.prrpr==1:
                        xpgain=random.randint(50,100)
                        self.money+=random.randint(10,20)
                        self.money+=self.Emoney
                        self.prrpr=0
                        if Necklace_of_growth==1:
                            xpgain*=1.5
                        self.xp+=xpgain
            if self.pick==2:
                if self.pprr==1:
                    self.alive=1
                    self.BossSpeed.x=0
                    self.BossSpeed.y=0
                    self.pprr=0
                if self.BossSpeed.hp>=1:
                    self.prrpr=1
                    self.BossSpeed.draw(self.screen)
                    self.BossSpeed.draw_health(self.screen)
                    self.BossSpeed.update(self.player,self.gamebg)
                    self.player.check_collision(self.BossSpeed,self.attack_cooldown)
                    current_time = pg.time.get_ticks()
                else:
                    self.alive=0
                    if self.prrpr==1:
                        xpgain=random.randint(50,100)
                        self.money+=random.randint(10,20)
                        self.money+=self.Emoney
                        self.prrpr=0
                        if Necklace_of_growth==1:
                            xpgain*=1.5
                        self.xp+=xpgain
            if self.pick==3:
                if self.pprr==1:
                    self.alive=1
                    self.BossSummon.x=0
                    self.BossSummon.y=0ake your data and AI to the next level with Databricks – free trial on AWS, Azure, or Google Cloud. Create production-ready Generative AI apps that are accurate, secure, and tailored to your business. Simplify data ingestion from hundreds of sources with effortless ETL automation. Plus, tap into instant, elastic serverless compute during your trial (available on AWS/Azure). Sign up with your work email now to unlock premium trial perks and transform how you work with data – don’t wait!

                    self.pprr=0
                if self.BossSummon.hp>=1:
                    self.prrpr=1
                    self.BossSummon.draw(self.screen)
                    self.BossSummon.draw_health(self.screen)
                    self.BossSummon.update(self.player)
                    self.player.check_collision(self.BossSummon,self.attack_cooldown)
                else:
                    self.alive=0
                    if self.prrpr==1:
                        xpgain=random.randint(50,100)
                        self.money+=random.randint(10,20)
                        self.money+=self.Emoney
                        self.prrpr=0
                        if Necklace_of_growth==1:
                            xpgain*=1.5
                        self.xp+=xpgain
        pg.display.flip()  # Update the display
        self.clock.tick(FPS)  # Maintain the frame rate
        pg.display.set_caption(f'{self.clock.get_fps():.1f}')  # Show the FPS in the title

    def check_events(self):
        keys = pg.key.get_pressed()

        # Toggle fullscreen mode with the 'f' key
        if keys[pg.K_f] and self.FULLSCREEN != 1:
            self.bg = pg.transform.scale(self.bg, (3200, 1800))
            self.screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
            self.FULLSCREEN = 1
        elif keys[pg.K_f] and self.FULLSCREEN != 0:
            self.screen = pg.display.set_mode((RES))
            self.bg = pg.transform.scale(self.bg, (RES))
            self.DF1 = pg.transform.scale(self.DF1, (200, 100))
            self.DF2 = pg.transform.scale(self.DF2, (200, 100))
            self.DF3 = pg.transform.scale(self.DF3, (200, 100))
            self.FULLSCREEN = 0

        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()  # Quit Pygame properly
                sys.exit()  # Exit the program


            self.imgclick(event)

    def imgclick(self, event):
        global Necklace_of_growth
        global Charm_of_Pain
        global Weights
        global roomenter
        global click
        keys=pg.key.get_pressed()
        mx, my = pg.mouse.get_pos()
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if click == 0:
                    if my >= 200 and my <= 650:
                        if mx >= 270 and mx <= 530:
                            if self.selected_images[0] == "fight.png":
                                click = 1
                            elif self.selected_images[0] == "camp.png":
                                click = 2
                            elif self.selected_images[0] == "boss.png":
                                click = 3
                            elif self.selected_images[0] == "chance.png":
                                click = 4
                            elif self.selected_images[0] == "Lifetrader.png":
                                click = 5
                            elif self.selected_images[0] == "shop.png":
                                click = 6
                            elif self.selected_images[0] == "treasure.png":
                                click = 7
                        elif mx >= 670 and mx <= 930:
                            if self.selected_images[1] == "fight.png":
                                click = 1
                            elif self.selected_images[1] == "camp.png":
                                click = 2
                            elif self.selected_images[1] == "boss.png":
                                click = 3
                            elif self.selected_images[1] == "chance.png":
                                click = 4
                            elif self.selected_images[1] == "Lifetrader.png":
                                click = 5
                            elif self.selected_images[1] == "shop.png":
                                click = 6
                            elif self.selected_images[1] == "treasure.png":
                                click = 7
                        elif mx >= 1070 and mx <= 1330:
                            if self.selected_images[2] == "fight.png":
                                click = 1
                            elif self.selected_images[2] == "camp.png":
                                click = 2
                            elif self.selected_images[2] == "boss.png":
                                click = 3
                            elif self.selected_images[2] == "chance.png":
                                click = 4
                            elif self.selected_images[2] == "Lifetrader.png":
                                click = 5
                            elif self.selected_images[2] == "shop.png":
                                click = 6
                            elif self.selected_images[2] == "treasure.png":
                                click = 7

        # When a door is clicked, spawn enemies randomly
        if click == 1 and not self.enemies and not self.stop_enemy_spawn:  # Ensure no enemies exist and stop spawning if they are all dead
            self.num_enemies = random.randint(1, 6)
            self.num_enemies+=self.spawnrate1+self.spawnrate2
            if self.num_enemies<=0:
                self.num_enemies=1
            self.enemies = []
            min_distance = 50
            self.alive = 0
            for _ in range(self.num_enemies):
                self.alive = self.alive + 1
                valid_position = False
                while not valid_position:
                    x = random.randint(100, 1500)
                    y = random.randint(100, 500)
                    valid_position = True
                    for enemy in self.enemies:
                        distance = ((enemy.x - x) ** 2 + (enemy.y - y) ** 2) ** 0.5
                        if distance < min_distance:
                            valid_position = False
                            break
                enemy_type=Enemy
                self.enemies.append(enemy_type(x, y)) 
        elif click == 6:
            if self.pcc == 1:
                self.pick = random.randint(1, 3)
                if self.pick == 1:
                    self.cost1 = random.randint(1, 5)
                    self.item1 = "Weights"
                    self.item2 = "Weights"
                elif self.pick == 2:
                    self.cost1 = random.randint(1, 5)
                    self.item1 = "Charm Of Pain"
                    self.item2 = "Charm Of Pain"
                elif self.pick == 3:
                    self.cost1 = random.randint(1, 5)
                    self.item1 = "Necklace of Growth"
                    self.item2 = "Necklace of Growth"
                
                # Ensure item2 is different from item1
                while self.item2 == self.item1:
                    self.pick2 = random.randint(1, 3)
                    if self.pick2 == 1:
                        self.cost2 = random.randint(1, 5)
                        self.item2 = "Weights"
                        self.item3 = "Weights"
                    elif self.pick2 == 2:
                        self.cost2 = random.randint(1, 5)
                        self.item2 = "Charm Of Pain"
                        self.item3 = "Charm Of Pain"
                    elif self.pick2 == 3:
                        self.cost2 = random.randint(1, 5)
                        self.item2 = "Necklace of Growth"
                        self.item3 = "Necklace of Growth"
        
                # Ensure item3 is different from item1 and item2
                while self.item3 == self.item1 or self.item3 == self.item2:
                    self.pick3 = random.randint(1, 3)
                    if self.pick3 == 1:
                        self.cost3 = random.randint(1, 5)
                        self.item3 = "Weights"
                    elif self.pick3 == 2:
                        self.cost3 = random.randint(1, 5)
                        self.item3 = "Charm Of Pain"
                    elif self.pick3 == 3:
                        self.cost3 = random.randint(1, 5)
                        self.item3 = "Necklace of Growth"
                
                self.pcc = 0
                
                # Ensure you do not allow buying items that are already owned
                if self.item1 == "Weights" and Weights == 1:
                    self.item1 = "Nothing"
                if self.item1 == "Charm Of Pain" and Charm_of_Pain == 1:
                    self.item1 = "Nothing"
                if self.item1 == "Necklace of Growth" and Necklace_of_growth == 1:
                    self.item1 = "Nothing"
                
                if self.item2 == "Weights" and Weights == 1:
                    self.item2 = "Nothing"
                if self.item2 == "Charm Of Pain" and Charm_of_Pain == 1:
                    self.item2 = "Nothing"
                if self.item2 == "Necklace of Growth" and Necklace_of_growth == 1:
                    self.item2 = "Nothing"
                
                if self.item3 == "Weights" and Weights == 1:
                    self.item3 = "Nothing"
                if self.item3 == "Charm Of Pain" and Charm_of_Pain == 1:
                    self.item3 = "Nothing"
                if self.item3 == "Necklace of Growth" and Necklace_of_growth == 1:
                    self.item3 = "Nothing"
        
            if self.player.y >= 140 and self.player.y <= 230:
                # Item 1 check (x range: 80 to 140)
                if self.player.x >= 80 and self.player.x <= 140:
                    if self.item1 != "Nothing" and self.item1 != "Bought":
                        print(f"This item is: {self.item1} and cost: {str(self.cost1)} 'Y' to buy")
                    elif self.item1 == "Bought":
                        print("You have bought this item")
                    else:
                        print("Nothing")
                    
                    if keys[pg.K_y] and self.money - self.cost1 >= 0:
                        if self.item1 == "Weights" and Weights == 0:
                            self.money -= self.cost1
                            Weights = 1
                            self.PPH = 1
                            self.item1 = "Bought"
                        elif self.item1 == "Charm Of Pain" and Charm_of_Pain == 0:
                            self.money -= self.cost1
                            Charm_of_Pain = 1
                            self.PPH = 1
                            self.item1 = "Bought"
                        elif self.item1 == "Necklace of Growth" and Necklace_of_growth == 0:
                            self.money -= self.cost1
                            Necklace_of_growth = 1
                            self.PPH = 1
                            self.item1 = "Bought"
            
                # Item 2 check (x range: 180 to 240)
                if self.player.x >= 180 and self.player.x <= 240:
                    if self.item2 != "Nothing" and self.item2 != "Bought":
                        print(f"This item is: {self.item2} and cost: {str(self.cost2)} 'Y' to buy")
                    elif self.item2 == "Bought":
                        print("You have bought this item")
                    else:
                        print("Nothing")
            
                    if keys[pg.K_y] and self.money - self.cost2 >= 0:
                        if self.item2 == "Weights" and Weights == 0:
                            self.money -= self.cost2
                            Weights = 1
                            self.PPH = 1
                            self.item2 = "Bought"
                        elif self.item2 == "Charm Of Pain" and Charm_of_Pain == 0:
                            self.money -= self.cost2
                            Charm_of_Pain = 1
                            self.PPH = 1
                            self.item2 = "Bought"
                        elif self.item2 == "Necklace of Growth" and Necklace_of_growth == 0:
                            self.money -= self.cost2
                            Necklace_of_growth = 1
                            self.PPH = 1
                            self.item2 = "Bought"
            
                # Item 3 check (x range: 280 to 340)
                if self.player.x >= 280 and self.player.x <= 340:
                    if self.item3 != "Nothing" and self.item3 != "Bought":
                        print(f"This item is: {self.item3} and cost: {str(self.cost3)} 'Y' to buy")
                    elif self.item3 == "Bought":
                        print("You have bought this item")
                    else:
                        print("Nothing")
            
                    if keys[pg.K_y] and self.money - self.cost3 >= 0:
                        if self.item3 == "Weights" and Weights == 0:
                            self.money -= self.cost3
                            Weights = 1
                            self.PPH = 1
                            self.item3 = "Bought"
                        elif self.item3 == "Charm Of Pain" and Charm_of_Pain == 0:
                            self.money -= self.cost3
                            Charm_of_Pain = 1
                            self.PPH = 1
                            self.item3 = "Bought"
                        elif self.item3 == "Necklace of Growth" and Necklace_of_growth == 0:
                            self.money -= self.cost3
                            Necklace_of_growth = 1
                            self.PPH = 1
                            self.item3 = "Bought"

        elif click==7:
            a=0
            b=0
            c=0
            if self.player.x>=730 and self.player.x<=800 and self.player.y>=300 and self.player.y<=400:
                if self.rr==1:
                    pick=random.randint(1,3)
                    while pick==1 and Charm_of_Pain==1:
                        pick=random.randint(1,3)
                        a=1
                    while pick==2 and Weights==1:
                        pick=random.randint(1,3)
                        b=1
                    while pick==3 and Necklace_of_growth==1:
                        pick=random.randint(1,3)
                        c=1
                    if a==1 and b==1 and c==1:
                        print("No more items")
                    if pick==1:
                        Charm_of_Pain=1
                        self.PPH=1
                    elif pick==2:
                        Weights=1
                        self.PPH=1
                    elif pick==3:
                        Necklace_of_growth=1
                        self.PPH=1
                self.rr=2
        elif click == 0:
            self.BossTank=BossTank()
            self.pprr=1
            self.bossph=1
            self.pcc=1
            self.rr=1
            self.enemies = []
            self.door_rolled = False
            self.stop_enemy_spawn = False  # Reset the enemy spawn flag when restarting
        if click==2 or click==4 or click==5:
            print("Not done!!!!!!!!!!!!!!!!!!!!!!!!!!")

    def begin(self):
        global roomenter
        if click == 0:
            self.DF1, self.DF2, self.DF3, self.selected_images = self.load_and_scale_images()
        else:
            self.player.draw(self.screen)
        for enemy in self.enemies:
            if enemy.Hp >= 0:
                enemy.draw(self.screen)

        if roomenter == 1:
            global reroll
        elif roomenter == 2:
            global reroll2
        elif roomenter == 3:
            global reroll3

    def run(self):
        while True:
            self.check_events()  # Handle input events
            self.update()  # Update game state and render the screen

if __name__ == '__main__':
    game = Game()
    game.run()
