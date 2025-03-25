## **[1]. Snakes And Ladders**  
**Solved Status:** ✅ Solved  
**Difficulty:** 🟠 Medium  
**Topics:** `Game`, `Board`, `Simulation`  

---

### **Problem Description**  
Snakes and ladders is a classic game played on an **n × n board** by **m players**. Players take turns rolling the dice on the board in a **round-robin manner** and move their peice to reach the end of the board. The game continues until one player wins.  

You are given a board game with snakes and ladders. The board has a given size and several special moves defined by snakes and ladders. _n_ players take turns to roll a dice. For each dice roll, the corresponding player moves forward by the given dice value. If the player lands exactly on the starting point of a ladder or on the head of a snake, they immediately move to the corresponding end position. The game stops as soon as a player lands exactly on the final cell of the board, and that player is declared the winner.

The game should display the board's state **after every move**.

Once a player wins, the system should **display the winner's name** and stop further moves.  

---

### **Input Format**  
The input is provided in an `Input.txt` file containing multiple test cases. Each test case is separated by a blank line. For each test case, the format is as follows:

1. **Line 1:** Two space-separated integers:  
   `boardSize numPlayers`
2. **Line 2:** Two space-separated integers:  
   `numSnakes numLadders`
3. **Next numSnakes lines:** Each contains two space-separated integers representing a snake’s head and tail:  
   `snakeHead snakeTail`
4. **Next numLadders lines:** Each contains two space-separated integers representing a ladder’s start and end:  
   `ladderStart ladderEnd`
5. **Next line:** An integer representing the number of dice rolls:  
   `numRolls`
6. **Next numRolls lines:** Each line contains an integer (1-6) denoting a dice roll value. 

Players take turns **in the order they were listed**.  

---

### **Output Format**  
For each test case, after each dice roll, print a line with the positions of all players in the following format:

Player 1:<pos1> Player 2:<pos2> ... Player n:<posn>


When a player wins (i.e. lands exactly on the board size), immediately print an extra line:

Player X wins

After finishing one test case, leave one blank line before the next test case output. Once all test cases have been processed, your program should compare the generated output against the expected output from `Output.txt` using the provided output comparator.

---

### **Constraints**  
- `3 ≤ n ≤ 10` → Board size  
- `2 ≤ m ≤ 5` → Number of players  
- `1 ≤ a, b ≤ n` → Valid board positions  
- Players **must** place their marks in **round-robin order**.  

---

### **Example 1: Normal Gameplay**  
#### **Input:**  
```yaml
30 2
1 1
28 14
3 21
7
2
1
1
6
6
6
3
```

#### **Output:**  
```yaml
Player 1:2 Player 2:0
Player 1:2 Player 2:1
Player 1:21 Player 2:1
Player 1:21 Player 2:7
Player 1:27 Player 2:7
Player 1:27 Player 2:13
Player 1:30 Player 2:13
Player 1 wins
```

#### **Explanation:**

1. **Roll 1 (Player 1, value 2):**  
   Position: 0 + 2 = 2  
   _Output:_ `Player 1:2 Player 2:0`
2. **Roll 2 (Player 2, value 1):**  
   Position: 0 + 1 = 1  
   _Output:_ `Player 1:2 Player 2:1`
3. **Roll 3 (Player 1, value 1):**  
   Position: 2 + 1 = 3 → ladder triggers (3→21)  
   _Output:_ `Player 1:21 Player 2:1`
4. **Roll 4 (Player 2, value 6):**  
   Position: 1 + 6 = 7  
   _Output:_ `Player 1:21 Player 2:7`
5. **Roll 5 (Player 1, value 6):**  
   Position: 21 + 6 = 27  
   _Output:_ `Player 1:27 Player 2:7`
6. **Roll 6 (Player 2, value 6):**  
   Position: 7 + 6 = 13  
   _Output:_ `Player 1:27 Player 2:13`
7. **Roll 7 (Player 1, value 3):**  
   Position: 27 + 3 = 30 (exact board size) → Player 1 wins  
   _Output:_  
Player 1:30 Player 2:13 Player 1 wins


### **Example 2: Invalid Move Handling**  
#### **Input:**  
```yaml
20 2
1 1
18 5
3 15
5
3
4
2
5
3
```

#### **Output:**  
```yaml
Player 1:15 Player 2:0
Player 1:15 Player 2:4
Player 1:17 Player 2:4
Player 1:17 Player 2:9
Player 1:20 Player 2:9
Player 1 wins
```

#### **Explanation:**

1. **Roll 1 (Player 1, value 3):**  
   Position: 0 + 3 = 3 → ladder triggers (3→15)  
   _Output:_ `Player 1:15 Player 2:0`
2. **Roll 2 (Player 2, value 4):**  
   Position: 0 + 4 = 4  
   _Output:_ `Player 1:15 Player 2:4`
3. **Roll 3 (Player 1, value 2):**  
   Position: 15 + 2 = 17  
   _Output:_ `Player 1:17 Player 2:4`
4. **Roll 4 (Player 2, value 5):**  
   Position: 4 + 5 = 9  
   _Output:_ `Player 1:17 Player 2:9`
5. **Roll 5 (Player 1, value 3):**  
   Position: 17 + 3 = 20 (exact board size) → Player 1 wins  
   _Output:_  
Player 1:20 Player 2:9 Player 1 wins