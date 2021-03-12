# Movie Theater Seating Challenge

- takes in reservating requests
- movie theater is 10 rows x 20 seats
- goal to MAXIMIZE:
  1. Satisfaction
  2. Safety

**Satisfaction** - quality of the seats.
**Safety** - the further away from other people/minimum of three seats or one row.

## Requirements

- Executable from the command line
- Reads a file for input
- Writes a file for output

Input File Format:

```shell
<Reservation ID> <number of seats>
<Reservation ID> <number of seats>
<Reservation ID> <number of seats>
```

Output File Format:

```shell
<Reservation ID> <Seat>,<Seat>,...
<Reservation ID> <Seat>,<Seat>,...
<Reservation ID> <Seat>,<Seat>,...
```

## Usage

From the root of the directory

```shell
> python movie_seats\driver.py tests\inputs\input01.txt
```

## Notes

**Heuristics**
We have two heuristics to maximize for. Out of the two, safety is easier to calculate. Saftey will be a measurement of how far a person is from other people who are not in their group (The further, the higher the score). However, satisfaction is subjective. For this problem I will make assumptions that will allow the program to make an educated guess about satisfaction. Satisfaction will be calculated by the [manhattan distance][0] from ~2/3 of the way to the back/center seats.

The reason for choosing this location is:

1. From experience people tend to prefer towards the back rather than towards the front
2. Google search yields [articles][1] explaining sound quality at this spot is the best

**Assignment Order**
There are a number of ways that processing the tickets could be handled. Either seats could be assigned one request at a time, or all requests can be handled at once and seats can be assigned at the end. In this solution, seats will be assigned one request at a time. This means that the earlier people request tickets, they will be given the best possible seats. There are a few main reasons for this:

1. Users who purchase tickets earlier should be rewarded with the best seats.
2. This will make the algorithm more simple to implement as seats will be locked in once assigned.

If seats are assigned at the end, the algorithm could be optimized to produce the best possible score. However, this could also lead to unexpected behavior. For example, if there are many requests for tickets but one request is for a large party (up to the number of seats in the theater), the algorithm could see that assigning the large party first would yield the best score. This would be good as a score but is a bad behavior in the real world, because it will automatically kick out everyone else even if they requested tickets well in advance.

**Refunds**
At any point a refund can be requested. The seats should be marked as freed, and the algorithm should handle this accordingly.

**Edge Cases**
If a request for a group of seats is greater than the number of seats in a row. We will not handle this case. If not everyone can be seated together, the user should break their request into smaller groups. The same can be applied to a request for a number of seats that can no longer be handled. The user should be given the choice whether they want to go at all or split their group into smaller groups.

[0]: https://en.wikipedia.org/wiki/Taxicab_geometry
[1]: https://en.wikipedia.org/wiki/Taxicab_geometry
