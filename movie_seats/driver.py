import sys
from seats import SeatManager
from models import SeatManagerInterface

def main():

    manager: SeatManagerInterface = SeatManager()

    if len(sys.argv) < 2:
        print("Invalid number of arguments. Must provide filename.")
        exit(1)

    filename = sys.argv[1]
    print(f"Starting to process {filename}...\n")

    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            (group_id, num_seats) = parse_line(line)
            manager.assign_seats(group_id, num_seats)
    
    print("Done. Writing to output.txt...")

    with open("output.txt", "w") as file:
        file.write(manager.print_tickets())
    print("final seating: \n")
    print(manager)
    # except Exception:
    #     print("Invalid file given. Must provide full path relative to the root of directory.")


def parse_line(line:str):
    split_line = line.split(" ")
    return (split_line[0], int(split_line[1]))

if __name__ == "__main__":
    main()

