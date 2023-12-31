#world.py
import pygame

class World():
    def __init__(self, data, map_image):
        self.tile_map = []
        self.waypoints = []
        self.moveofJSON = 0
        self.level_data = data
        self.image = map_image

    def process_data(self):
        #Das JSON nach dem Sektor polyline durchsuchen und zurückgeben
        for layer in self.level_data["layers"]:
            if layer["name"] == "tilemap":
                self.tile_map = layer["data"]
            elif layer["name"] == "waypoints":
                for obj in layer["objects"]:
                    self.moveofJSON = obj.get("x")
                    waypoint_data = obj["polyline"]
                    self.process_waypoints(waypoint_data)

    def process_waypoints(self, data):
        #Die einzelnen Wegpunkte raussuchen und als Wegpunkt speichern
        for point in data: 
            temp_x = point.get("x")
            temp_x = temp_x + self.moveofJSON
            temp_y = point.get("y")
            self.waypoints.append((temp_x, temp_y))
        

    def draw(self, surface):
        surface.blit(self.image, (0,0))
        