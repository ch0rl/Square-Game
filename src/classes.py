import pygame
from typing import Tuple
from multipledispatch import dispatch


class Wall:
    """Base Wall Class"""
    def __init__(self,
                 left: int,
                 top: int,
                 width: int,
                 height: int
                 ) -> None:
        """Base Wall Class
        
        Args:
            left (int): x-coordinate of the top-left corner
            top (int): y-coordinate of the top-left corner
            width (int): Width of the wall
            height (int): Height of the wall
        """
        self.rect = pygame.rect.Rect(left, top, width, height)


class Entity:
    """Base Entity Class"""
    def __init__(self,
            pos: Tuple[int, int],
            colour: Tuple[int, int],
            width: int
        ) -> None:
        self.colour = colour
        self.rect = pygame.rect.Rect(*pos, width, width)
    
    def move(self, vector: Tuple[int, int]) -> None:
        """Apply `vector` to position
        
        Args:
            vector (tuple[int, int]): 2D vector of movement
        """
        x, y = vector
        self.rect.x += x
        self.rect.y += y

    @dispatch(Wall)
    def collides_with(self, wall: Wall) -> bool:
        """Returns whether the entity is colliding with a wall
        
        Args:
            wall (Wall): The wall to check collisions with

        Return:
            (bool) Whether the entity is colliding with the wall
        """

        x1, x2 = self.rect.x, wall.rect.x
        y1, y2 = self.rect.y, wall.rect.y
        width1, width2 = self.rect.width, wall.rect.width
        height1, height2 = self.rect.height, wall.rect.height

        return (
            x2 - width1 < x1 < x2 + width2 and
            y2 - height1 < y1 < y2 + height2
        )

    @dispatch(int, int, int, int)
    def collides_with(self, top: int, left: int, width: int, height: int) -> bool:
        """Returns whether the entity is colliding with an arbitrary, rectangle, entity
        
        Args:
            top (int): The x of the top-left of the entity
            left (int): The y of the top-left of the entity
            width (int): The width of the entity
            height (int): The height of the entity

        Return:
            (bool) Whether the entity is colliding with the entity
        """

        x1, x2 = self.rect.x, top
        y1, y2 = self.rect.y, left
        width1, width2 = self.rect.width, width
        height1, height2 = self.rect.height, height

        return (
            x2 - width1 < x1 < x2 + width2 and
            y2 - height1 < y1 < y2 + height2
        )


class Player(Entity):
    """Base Player Class"""
    def __init__(self,
            pos: Tuple[int, int],
            colour: Tuple[int, int] = (25, 93, 242),
            width: int = 10,
            lives: int = 1
        ) -> None:
        """Base Player Class
        
        Args:
            pos (tuple[int, int]): Start position
            colour (tuple[int, int] = (25, 93, 242): Colour of the player
            width (int = 10): Width of the player
            health (int = 100): Health of the player
        """
        super().__init__(pos, colour, width)

        self.lives = lives
        self.alive = True

    def hurt(self) -> None:
        """Remove a life from player"""
        self.lives -= 1
        if self.lives < 0:
            self.lives = 0
            self.alive = False


class Projectile(Entity):
    """Base Projectile Class"""
    def __init__(self,
            pos: Tuple[int, int],
            dir: Tuple[int, int],
            colour: Tuple[int, int] = (243, 171, 17),
            width: int = 5,
            damage: int = 10
        ) -> None:
        """Base Projectile Class
        
        Args:
            pos (tuple[int, int]): Start position
            dir (tuple[int, int]): 2D vector of movement
            colour (tuple[int, int] = (243, 171, 17): Colour of the projectile
            width (int = 5): Width of the projectile
            damage (int = 10): Damage of the projectile
        """
        super().__init__(pos, colour, width)

        self.damage = damage
        self.dir = dir

    def move(self) -> None:
        """Move projectile"""
        x, y = self.dir
        self.rect.x += x
        self.rect.y += y
