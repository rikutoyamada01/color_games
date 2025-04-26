from abc import ABC, abstractmethod
import pygame as pg

class Resizable(ABC):
    @abstractmethod
    def update_position(self, screen_size: tuple[int, int]) -> None:
        pass

    @abstractmethod
    def draw(self) -> None:
        pass
