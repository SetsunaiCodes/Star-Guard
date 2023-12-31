#enemy.py
import pygame
from pygame.math import Vector2
import math

class Enemy(pygame.sprite.Sprite):
  def __init__(self, waypoints, image, initial_size=(40,40)):
    pygame.sprite.Sprite.__init__(self)
    self.waypoints = waypoints
    self.pos = Vector2(self.waypoints[0])
    self.target_waypoint = 1
    self.speed = 2
    self.angle = 0
    self.original_image = image
    self.scaled_image = pygame.transform.scale(self.original_image, initial_size)
    self.image = pygame.transform.rotate(self.scaled_image, self.angle)
    self.rect = self.image.get_rect()
    self.rect.center = self.pos

  def update(self):
    self.move()
    self.rotate()

  def move(self):
    #define a target waypoint
    if self.target_waypoint < len(self.waypoints):
      self.target = Vector2(self.waypoints[self.target_waypoint])
      self.movement = self.target - self.pos
    else:
      #enemy has reached the end of the path
      self.kill()

    #calculate distance to target
    dist = self.movement.length()
    #check if remaining distance is greater than the enemy speed
    if dist >= self.speed:
      self.pos += self.movement.normalize() * self.speed
    else:
      if dist != 0:
        self.pos += self.movement.normalize() * dist
      self.target_waypoint += 1

  def rotate(self):
    #Distanz zum nächsten Wegpunkt
    dist = self.target - self.pos
    #Mit dem Abstand zum Wegpunkt kann der Winkel berechnet werden
    self.angle = math.degrees(math.atan2(-dist[1], dist[0]))
    #Bild drehen und auch auch das Rechteck abändern 
    self.image = pygame.transform.rotate(self.scaled_image, self.angle)
    self.rect = self.image.get_rect()
    self.rect.center = self.pos