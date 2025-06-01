import java.util.*;

public class Ticket {
    private static int idCounter = 1;
    private int id;
    private User user;
    private Show show;
    private List<Seat> seats;
    
    public Ticket(User user, Show show, List<Seat> seats) {
        this.id = idCounter++;
        this.user = user;
        this.show = show;
        this.seats = seats;
    }
    
    public int getId() {
        return id;
    }
    
    public User getUser() {
        return user;
    }
    
    public Show getShow() {
        return show;
    }
    
    public List<Seat> getSeats() {
        return seats;
    }
}
