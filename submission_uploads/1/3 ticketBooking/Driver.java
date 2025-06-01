import java.util.*;

public class Driver {
    public void processTestCase(List<String> lines) {
        // Use a scanner built on the test case lines joined by newline
        Scanner sc = new Scanner(String.join("\n", lines));
        BookingSystem bs = new BookingSystem();
        
        // Read Cities
        int numCities = sc.nextInt();
        sc.nextLine();
        for (int i = 0; i < numCities; i++) {
            String cityName = sc.nextLine().trim();
            bs.cities.put(cityName, new City(cityName));
        }
        
        // Read Theatres
        int numTheatres = sc.nextInt();
        sc.nextLine();
        for (int i = 0; i < numTheatres; i++) {
            int theatreId = sc.nextInt();
            String theatreName = sc.next();
            String cityName = sc.next();
            sc.nextLine();
            City city = bs.cities.get(cityName);
            Theatre theatre = new Theatre(theatreId, theatreName, city);
            bs.theatres.put(theatreId, theatre);
        }
        
        // Read Halls
        int numHalls = sc.nextInt();
        sc.nextLine();
        for (int i = 0; i < numHalls; i++) {
            int hallId = sc.nextInt();
            int theatreId = sc.nextInt();
            int numSeats = sc.nextInt();
            sc.nextLine();
            // Next line contains space-separated seat types
            String[] seatTypes = sc.nextLine().trim().split(" ");
            List<Seat> seatList = new ArrayList<>();
            for (int s = 0; s < numSeats; s++) {
                Seat seat = new Seat(s + 1, seatTypes[s]);
                seatList.add(seat);
            }
            Hall hall = new Hall(hallId, bs.theatres.get(theatreId), seatList);
            bs.halls.put(hallId, hall);
        }
        
        // Read Movies
        int numMovies = sc.nextInt();
        sc.nextLine();
        for (int i = 0; i < numMovies; i++) {
            int movieId = sc.nextInt();
            String movieName = sc.next();
            sc.nextLine();
            Movie movie = new Movie(movieId, movieName);
            bs.movies.put(movieId, movie);
        }
        
        // Read Shows
        int numShows = sc.nextInt();
        sc.nextLine();
        for (int i = 0; i < numShows; i++) {
            int showId = sc.nextInt();
            int movieId = sc.nextInt();
            int theatreId = sc.nextInt();
            int hallId = sc.nextInt();
            String time = sc.next();
            double price = sc.nextDouble();
            sc.nextLine();
            Show show = new Show(showId, bs.movies.get(movieId), bs.theatres.get(theatreId), bs.halls.get(hallId), time, price);
            bs.shows.put(showId, show);
        }
        
        // Read Users
        int numUsers = sc.nextInt();
        sc.nextLine();
        for (int i = 0; i < numUsers; i++) {
            int userId = sc.nextInt();
            String userName = sc.next();
            sc.nextLine();
            User user = new User(userId, userName);
            bs.users.put(userId, user);
        }
        
        // Read Operations
        int numOps = sc.nextInt();
        sc.nextLine();
        for (int i = 0; i < numOps; i++) {
            String opLine = sc.nextLine().trim();
            String[] tokens = opLine.split(" ");
            String op = tokens[0];
            if (op.equals("FIND_SHOWS")) {
                String cityName = tokens[1];
                String movieName = "";
                if (tokens.length > 2) {
                    movieName = tokens[2];
                }
                List<Integer> showList = bs.findShows(cityName, movieName);
                StringBuilder sb = new StringBuilder();
                for (int id : showList) {
                    sb.append(id).append(" ");
                }
                System.out.println(sb.toString().trim());
            } else if (op.equals("SHOW_SEATS")) {
                int showId = Integer.parseInt(tokens[1]);
                System.out.println(bs.showSeats(showId));
            } else if (op.equals("BOOK_SEATS")) {
                int userId = Integer.parseInt(tokens[1]);
                int showId = Integer.parseInt(tokens[2]);
                int count = Integer.parseInt(tokens[3]);
                List<Integer> seatNumbers = new ArrayList<>();
                for (int j = 0; j < count; j++) {
                    seatNumbers.add(Integer.parseInt(tokens[4 + j]));
                }
                System.out.println(bs.bookSeats(userId, showId, seatNumbers));
            }
        }
    }
}
