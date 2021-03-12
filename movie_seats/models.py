from abc import ABC, ABCMeta, abstractmethod
from typing import List, Tuple

class SeatManagerInterface(ABC):
    __metaclass__ = ABCMeta

    @classmethod
    def version(cls):
        return f'{cls} 1.0.0'
    
    @abstractmethod
    def assign_seats(self, id: str, num_seats: int) -> bool: raise NotImplementedError

    @abstractmethod
    def find_best_seats(self, num_seats: int): raise NotImplementedError

    @abstractmethod
    def reserve_seats(self, id: str, seats: List[Tuple[int, int]]): raise NotImplementedError

    @abstractmethod
    def print_tickets(self) -> str: raise NotImplementedError