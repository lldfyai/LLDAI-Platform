public class Player {
    private int id;
    private int position;
    
    public Player(int id) {
        this.id = id;
        this.position = 0;
    }
    
    public int getId() {
        return id;
    }
    
    public int getPosition() {
        return position;
    }
    
    public void setPosition(int pos) {
        this.position = pos;
    }
    
    public void move(int steps) {
        this.position += steps;
    }
}
