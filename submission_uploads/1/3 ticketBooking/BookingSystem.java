import java.util.*;
  
public class BookingSystem {
    public Map<String, City> cities = new HashMap<>();
    public Map<Integer, Theatre> theatres = new HashMap<>();
    public Map<Integer, Hall> halls = new HashMap<>();
    public Map<Integer, Movie> movies = new HashMap<>();
    public Map<Integer, Show> shows = new HashMap<>();
    public Map<Integer, User> users = new HashMap<>();
    public List<Ticket> tickets = new ArrayList<>();
    
    // Find shows based on city (and optionally movie)
    public List<Integer> findShows(String cityName, String movieName) {
        List<Integer> result = new ArrayList<>();
        for (Show show : shows.values()) {
            if (show.getTheatre().getCity().getName().equals(cityName)) {
                if (movieName.isEmpty() || show.getMovie().getName().equals(movieName)) {
                    result.add(show.getId());
                }
            }
        }
        Collections.sort(result);
        return result;
    }
    
    // Return the current status of seats for a given show
    public String showSeats(int showId) {
        Show show = shows.get(showId);
        if (show == null) return "";
        List<Seat> seats = show.getHall().getSeats();
        StringBuilder sb = new StringBuilder();
        for (Seat seat : seats) {
            sb.append(seat.toString()).append(" ");
        }
        return sb.toString().trim();
    }
    
    // Book seats for a given user and show
    public String bookSeats(int userId, int showId, List<Integer> seatNumbers) {
        Show show = shows.get(showId);
        if (show == null) return "Show not found";
        List<Seat> seats = show.getHall().getSeats();
        Map<Integer, Seat> seatMap = new HashMap<>();
        for (Seat seat : seats) {
            seatMap.put(seat.getSeatNumber(), seat);
        }
        // Check if any requested seat is already booked
        for (int sn : seatNumbers) {
            if (!seatMap.containsKey(sn)) return "Seat " + sn + " not found";
            if (seatMap.get(sn).isBooked()) {
                return "Already booked\n" + showSeats(showId);
            }
        }
        // Book all requested seats
        List<Seat> bookedSeats = new ArrayList<>();
        for (int sn : seatNumbers) {
            Seat seat = seatMap.get(sn);
            seat.book();
            bookedSeats.add(seat);
        }
        Ticket ticket = new Ticket(users.get(userId), show, bookedSeats);
        tickets.add(ticket);
        String ticketInfo = "Ticket " + ticket.getId() + " Booked for User " + userId +
                " for Show " + showId + ": " + bookedSeatsToString(bookedSeats);
        return ticketInfo + "\n" + showSeats(showId);
    }
    
    private String bookedSeatsToString(List<Seat> seats) {
        StringBuilder sb = new StringBuilder();
        sb.append("[");
        for (int i = 0; i < seats.size(); i++) {
            sb.append(seats.get(i).getSeatNumber());
            if (i < seats.size() - 1) sb.append(",");
        }
        sb.append("]");
        return sb.toString();
    }
}
