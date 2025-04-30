// Optional: Represents a cell on the board which could hold snake or ladder info.
public class Cell {
    private int number;
    // jump is the destination cell if a snake or ladder is present (0 if none)
    private int jump;
    
    public Cell(int number) {
        this.number = number;
        this.jump = 0;
    }
    
    public int getNumber() {
        return number;
    }
    
    public void setJump(int jump) {
        this.jump = jump;
    }
    
    public boolean hasJump() {
        return jump != 0;
    }
    
    public int getJump() {
        return jump;
    }
}
