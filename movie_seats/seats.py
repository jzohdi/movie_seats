from typing import Dict, List, Tuple
from models import SeatManagerInterface


NUM_ROWS: int = 10
SEATS_PER_ROW: int = 20
SATISFACTION_WEIGHT = 3
SAFETY_WEIGHT = 1
# used for repre
SCRN_PAD = " " * ((SEATS_PER_ROW - 10)//2)
REPRE_INIT = f'  [[{SCRN_PAD}SCREEN{SCRN_PAD}]]\n  {"-"*SEATS_PER_ROW}\n'

"""
seats: a 2D array of 0 if open or 1 if taken
group_map: dict where the keys are the groups id's and the 
           values are a list of tuples where each tuple is (row, col)
           which is a list of the seats assigned to that group
  
"""
class SeatManager(SeatManagerInterface):
    seats: List[List[int]] = [[0]*SEATS_PER_ROW for i in range(NUM_ROWS)]
    group_map: Dict[str, List[Tuple[int, int]]] = {}

    def __init__(self):
        pass

    @staticmethod
    def row_letter(row: int):
        return chr(row + 65)

    """
    returns True if seats were found or False if seats not available
    """
    def assign_seats(self, id: str, num_seats: int) -> bool:
        print(f'Assigning {num_seats} seats to id: {id}...')
        
        if num_seats < 1 or num_seats > SEATS_PER_ROW:
            print(f"Invalid number of seats. minimum: 1 max: {SEATS_PER_ROW}\n")
            return False
        
        find_seats = self.find_best_seats(num_seats)
        if not find_seats:
            print(f'Could not assign seats for group {id}\n')
            return False
        
        self.reserve_seats(id, find_seats)

        print(f'Seats found for group {id}\n')
        return True

    def find_best_seats(self, num_seats):
        best_score = 0
        best_seats = None
        for i in range(len(self.seats)):
            row = self.seats[i]
            for j in range(len(row)):
                seats_to_try = self.get_possible_seats(i, j, num_seats)
                # print("trying seats: ", seats_to_try)
                if not self.can_sit(seats_to_try):
                    # print("seats not valid")
                    continue
                score = self.score_seats(seats_to_try)
                # print("score: ", score)
                if score > best_score or best_seats is None:
                    best_score = score
                    best_seats = seats_to_try
        return best_seats

    def can_sit(self, seats: List[Tuple[int, int]]):
        if not seats:
            return False
        is_available = True

        for (grp, grp_seats) in self.group_map.items():
            for seat in seats:
                if not self.valid_seat(seat, grp_seats):
                    is_available = False

        return is_available
    
    def valid_seat(self, seat, list_of_seats):
        row, col = seat
        # print("comparing seats ", seat, " to groups seats: ", list_of_seats)
        for item in list_of_seats:
            row_dist = abs(row - item[0])
            col_dist = abs(col - item[1]) 
            if row_dist < 2 and col_dist < 4:
                # print("too close. compared to: ", item, " row:", row_dist, " col: ", col_dist)
                return False

        return True

    def get_possible_seats(self, row, col, num):
        if col + num >= SEATS_PER_ROW - 1:
            return []
        seats = []
        for x in range(num):
            seats.append((row, col + x))
        return seats

    def reserve_seats(self, id: str, seats: List[Tuple[int, int]]):
        self.group_map[id] = seats
        for seat in seats:
            (row, col) = seat
            self.seats[row][col] = 1

    """
    score is calculated based on 
     - distance from nearest person 
     - distance to ideal location (2/3) back/center
    """
    def score_seats(self, seats: List[Tuple[int, int]]):
        total_score = 0
        for seat in seats:
            total_score += (self.dist_to_nearest_person(seat) * SAFETY_WEIGHT)
            total_score += (self.dist_to_best_seat(seat) * SATISFACTION_WEIGHT)
        return total_score
    
    """
    Runs BFS from the seat to find the first person
    """
    def dist_to_nearest_person(self, seat: Tuple[int, int]) -> int:
       
        def get_neighbors(row_col):
            (row, col) = row_col
            neighbors = []
            # up
            if row > 0:
                neighbors.append((row - 1, col))
            # down
            if row < NUM_ROWS - 1:
                neighbors.append((row + 1, col))
            # left
            if col > 0:
                neighbors.append((row, col - 1))
            # right:
            if col < SEATS_PER_ROW - 1:
                neighbors.append((row, col + 1))
            return neighbors

        def seat_key(row_col):
            return str(row_col[0]) + " " + str(row_col[1])

        seen = set([seat_key(seat)])
        dist = NUM_ROWS + SEATS_PER_ROW # since this would be the max distance
        queue = [(0, seat)]

        while queue:
            (curr_dist, next_seat) = queue.pop(0)
            if self.seats[next_seat[0]][next_seat[1]] == 1:
                return curr_dist
            neighbors = get_neighbors(next_seat)
            for neighbor in neighbors:
                key = seat_key(neighbor)
                if key not in seen:
                    queue.append((curr_dist+ 1,neighbor))
                    seen.add(key)
        return dist
    """
    Manhattan distance
    """
    def dist_to_best_seat(self, seat: Tuple[int, int]) -> int:
        target = ((NUM_ROWS*2)//3,SEATS_PER_ROW//2)
        dist_to_target = (abs(target[0] - seat[0]), abs(target[1] - seat[1]))
        return 100 - sum(dist_to_target)

    def print_tickets(self):
        def format_seats(seats):
            formatted = ""
            for seat in seats:
                formatted += self.row_letter(seat[0]) + str(seat[1]) + ","
            return formatted[:-1]

        string = ""
        for (grp, seats) in self.group_map.items():
            string += grp + " " + format_seats(seats)
            string += "\n"

        return string

    # note if more rows that 27 need to format row Letter better
    def __repr__(self):
        repre = REPRE_INIT
        for i in range(len(self.seats)):
            repre += SeatManager.row_letter(i) + " "
            row = self.seats[i]
            for seat in row:
                repre += "~" if seat == 0 else "t"
            repre += "\n"
        return repre
