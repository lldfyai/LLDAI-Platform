public class Show {
    private int id;
    private Movie movie;
    private Theatre theatre;
    private Hall hall;
    private String time;
    private double price;
    
    public Show(int id, Movie movie, Theatre theatre, Hall hall, String time, double price) {
        this.id = id;
        this.movie = movie;
        this.theatre = theatre;
        this.hall = hall;
        this.time = time;
        this.price = price;
    }
    
    public int getId() {
        return id;
    }
    
    public Movie getMovie() {
        return movie;
    }
    
    public Theatre getTheatre() {
        return theatre;
    }
    
    public Hall getHall() {
        return hall;
    }
    
    public String getTime() {
        return time;
    }
    
    public double getPrice() {
        return price;
    }
}
