## **[1]. Ticket Booking System**  
**Solved Status:** ✅ Solved  
**Difficulty:** 🔴 Hard
**Topics:** `Management`, `Controllers`, `Simulation`  

---

### **Problem Description**  
You are required to design and implement a Ticket Booking System for a movie theatre. The system should allow operations such as finding shows based on city and movie, displaying available seats for a show, and booking seats.  
The system consists of multiple classes including (but not limited to):

- **User** – Represents a user of the system.
- **Theatre** – Represents a theatre located in a city.
- **Movie** – Represents a movie.
- **BookingSystem** – Handles the core operations such as finding shows, displaying seats, and booking seats.


## Operations

1. **FIND_SHOWS**:  
   - **Input Format:** `FIND_SHOWS <CityName> [MovieName]`  
   - **Output:** A line containing space-separated show IDs that match the city (and, if given, the movie).

2. **SHOW_SEATS**:  
   - **Input Format:** `SHOW_SEATS <ShowID>`  
   - **Output:** A single line listing each seat in the hall as:  
     `<seatNumber>-<type>-<status>` (where status is either *Empty* or *Booked*), separated by spaces.

3. **BOOK_SEATS**:  
   - **Input Format:** `BOOK_SEATS <UserID> <ShowID> <NumberOfSeats> <SeatNumber1> <SeatNumber2> ...`  
   - **Output:**  
     - If all requested seats are available, book them, generate a ticket, and print:  
       `Ticket <TicketID> Booked for User <UserID> for Show <ShowID>: [<seat1>,<seat2>,...]`  
       followed by a new line with the updated seats status (as in the SHOW_SEATS operation).  
     - If any requested seat is already booked, output:  
       `Already booked`  
       followed by a new line displaying the current seat status.

---

### **Input Format**  
Each test case in the input file is structured as follows (each test case is separated by a blank line):

1. **Cities:**  
   - First line: `<Number of Cities>`  
   - Next lines: Each line contains a city name.

2. **Theatres:**  
   - Next line: `<Number of Theatres>`  
   - Next lines: Each theatre’s details:  
     `<TheatreID> <TheatreName> <CityName>`

3. **Halls:**  
   - Next line: `<Number of Halls>`  
   - For each hall:  
     - A line with: `<HallID> <TheatreID> <Number of Seats>`  
     - Next line: Space-separated list of seat types for that hall.

4. **Movies:**  
   - Next line: `<Number of Movies>`  
   - Next lines: Each movie’s details:  
     `<MovieID> <MovieName>`

5. **Shows:**  
   - Next line: `<Number of Shows>`  
   - Next lines: Each show’s details:  
     `<ShowID> <MovieID> <TheatreID> <HallID> <Time> <Price>`

6. **Users:**  
   - Next line: `<Number of Users>`  
   - Next lines: Each user’s details:  
     `<UserID> <UserName>`

7. **Operations:**  
   - Next line: `<Number of Operations>`  
   - Next lines: Each operation command as specified above. 

---

### **Output Format**  
Refer to the operations and their specific output formats

---

### **Example 1**  
#### **Input:**  
```yaml
2
CityA
CityB
2
1 PVR CityA
2 Inox CityB
2
1 1 5
Silver Gold Platinum Silver Gold
2 2 4
Gold Platinum Gold Platinum
2
1 Avengers
2 Inception
2
1 1 1 18:00 250.0
2 2 2 20:00 300.0
2
1 Alice
2 Bob
3
FIND_SHOWS CityA
SHOW_SEATS 1
FIND_SHOWS CityB Inception
```

#### **Output:**  
```yaml
1
1-Silver-Empty 2-Gold-Empty 3-Platinum-Empty 4-Silver-Empty 5-Gold-Empty
2
```


### **Example 2**  
#### **Input:**  
```yaml
1
CityX
1
1 Cineplex CityX
1
1 1 3
Silver Gold Platinum
1
1 Interstellar
1
1 1 1 18:00 300.0
2
1 Charlie
2 Dave
3
SHOW_SEATS 1
BOOK_SEATS 1 1 2 2 3
BOOK_SEATS 2 1 1 2
```

#### **Output:**  
```yaml
1-Platinum-Empty 2-Platinum-Empty 3-Gold-Empty 4-Silver-Empty
Ticket 1 Booked for User 1 for Show 1: [2,3]
1-Platinum-Booked 2-Platinum-Empty 3-Gold-Booked 4-Silver-Empty
Already booked
1-Platinum-Booked 2-Platinum-Empty 3-Gold-Booked 4-Silver-Empty
```