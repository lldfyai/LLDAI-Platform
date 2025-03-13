import java.util.*;

public class Board {
    private int size;
    // Maps a cell with a snake/ladder to its destination cell
    private Map<Integer, Integer> transitions;
    
    public Board(int size) {
        this.size = size;
        transitions = new HashMap<>();
    }
    
    public int getSize() {
        return size;
    }
    
    // Add a snake or ladder transition from start cell to end cell
    public void addTransition(int start, int end) {
        transitions.put(start, end);
    }
    
    public boolean hasTransition(int pos) {
        return transitions.containsKey(pos);
    }
    
    public int getTransition(int pos) {
        return transitions.get(pos);
    }
}
