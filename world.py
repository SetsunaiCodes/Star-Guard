#world.py
import pygame
import random
import constants as c
from enemy_data import ENEMY_SPAWN_DATA

class World():
    def __init__(self, data, map_image):
        self.level = 1
        self.health = c.HEALTH
        self.money = c.MONEY
        self.tile_map = []
        self.waypoints = []
        self.moveofJSON = 0
        self.level_data = data
        self.image = map_image
        self.enemy_list = []
        self.spawned_enemies = 0
        self.killed_enemies = 0
        self.missed_enemies = 0

    def process_data(self):
        for layer in self.level_data["layers"]:
            if layer["name"] == "tilemap":
                self.tile_map = layer["data"]
            elif layer["name"] == "waypoints":
                for obj in layer["objects"]:
                    self.moveofJSON = obj.get("x")
                    waypoint_data = obj["polyline"]
                    self.process_waypoints(waypoint_data)

    def process_waypoints(self, data):
        for point in data: 
            temp_x = point.get("x")
            temp_x = temp_x + self.moveofJSON
            temp_y = point.get("y")
            self.waypoints.append((temp_x, temp_y))
        
    def process_enemies(self):
        print("process enemies gestartet")
        enemies = ENEMY_SPAWN_DATA[self.level-1]
        for enemy_type in enemies:
            print("Sorte hinzugefügt")
            #Speichern wie viele Gegner ich von welcher Sorte brauche
            enemies_to_spawn = enemies[enemy_type]
            #Gegnerinstanzen erstellen
            for enemy in range(enemies_to_spawn):
                print("Gegner in Liste hinzugefügt")
                self.enemy_list.append(enemy_type)
        #Randomizing enemies
        random.shuffle(self.enemy_list)
        print("randomisierung abgeschlossen")


    def check_level_complete(self):
        if(self.killed_enemies + self.missed_enemies) == len(self.enemy_list):
            return True

    def reset_level(self):
        self.enemy_list = []
        self.spawned_enemies = 0
        self.killed_enemies = 0
        self.missed_enemies = 0



    def draw(self, surface):
        surface.blit(self.image, (0,0))
        