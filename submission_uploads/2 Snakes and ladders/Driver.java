import java.util.*;

public class Driver {
    public void processTestCase(List<String> lines) {
        int index = 0;
        // Read board size and number of players
        String[] firstLine = lines.get(index++).split(" ");
        int boardSize = Integer.parseInt(firstLine[0]);
        int numPlayers = Integer.parseInt(firstLine[1]);
        
        // Create the game board
        Board board = new Board(boardSize);
        
        // Read the number of snakes and ladders
        String[] secondLine = lines.get(index++).split(" ");
        int numSnakes = Integer.parseInt(secondLine[0]);
        int numLadders = Integer.parseInt(secondLine[1]);
        
        // Process snakes (transitions from snake head to tail)
        for (int i = 0; i < numSnakes; i++) {
            String[] snakeLine = lines.get(index++).split(" ");
            int snakeHead = Integer.parseInt(snakeLine[0]);
            int snakeTail = Integer.parseInt(snakeLine[1]);
            board.addTransition(snakeHead, snakeTail);
        }
        
        // Process ladders (transitions from ladder start to end)
        for (int i = 0; i < numLadders; i++) {
            String[] ladderLine = lines.get(index++).split(" ");
            int ladderStart = Integer.parseInt(ladderLine[0]);
            int ladderEnd = Integer.parseInt(ladderLine[1]);
            board.addTransition(ladderStart, ladderEnd);
        }
        
        // Number of dice rolls
        int numRolls = Integer.parseInt(lines.get(index++));
        
        // Initialize players
        List<Player> players = new ArrayList<>();
        for (int i = 0; i < numPlayers; i++) {
            players.add(new Player(i + 1));
        }
        
        Dice dice = new Dice();
        int currentPlayerIndex = 0;
        boolean gameWon = false;
        
        // Process each dice roll
        for (int i = 0; i < numRolls; i++) {
            int rollValue = Integer.parseInt(lines.get(index++));
            if (!gameWon) {
                Player currentPlayer = players.get(currentPlayerIndex);
                int currentPos = currentPlayer.getPosition();
                int newPos = currentPos + dice.roll(rollValue);
                
                // Move only if the new position does not exceed board size
                if (newPos <= board.getSize()) {
                    currentPlayer.setPosition(newPos);
                }
                
                // Check for snake or ladder at the new position
                if (board.hasTransition(currentPlayer.getPosition())) {
                    currentPlayer.setPosition(board.getTransition(currentPlayer.getPosition()));
                }
                
                // Print the positions of all players
                StringBuilder sb = new StringBuilder();
                for (Player p : players) {
                    sb.append("Player ").append(p.getId()).append(":").append(p.getPosition()).append(" ");
                }
                System.out.println(sb.toString().trim());
                
                // Check if the current player has won
                if (currentPlayer.getPosition() == board.getSize()) {
                    System.out.println("Player " + currentPlayer.getId() + " wins");
                    gameWon = true;
                }
                
                // Move to the next player (round-robin)
                currentPlayerIndex = (currentPlayerIndex + 1) % numPlayers;
            }
        }
    }
}
