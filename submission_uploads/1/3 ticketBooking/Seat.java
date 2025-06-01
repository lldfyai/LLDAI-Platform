public class Seat {
    private int seatNumber;
    private String type; // Silver, Gold, Platinum
    private boolean booked;
    
    public Seat(int seatNumber, String type) {
        this.seatNumber = seatNumber;
        this.type = type;
        this.booked = false;
    }
    
    public int getSeatNumber() {
        return seatNumber;
    }
    
    public String getType() {
        return type;
    }
    
    public boolean isBooked() {
        return booked;
    }
    
    public void book() {
        this.booked = true;
    }
    
    public String getStatus() {
        return booked ? "Booked" : "Empty";
    }
    
    public String toString() {
        return seatNumber + "-" + type + "-" + getStatus();
    }
}
