import java.util.*;

public class Hall {
    private int id;
    private Theatre theatre;
    private List<Seat> seats;
    
    public Hall(int id, Theatre theatre, List<Seat> seats) {
        this.id = id;
        this.theatre = theatre;
        this.seats = seats;
    }
    
    public int getId() {
        return id;
    }
    
    public Theatre getTheatre() {
        return theatre;
    }
    
    public List<Seat> getSeats() {
        return seats;
    }
}
