public class Theatre {
    private int id;
    private String name;
    private City city;
    
    public Theatre(int id, String name, City city) {
        this.id = id;
        this.name = name;
        this.city = city;
    }
    
    public int getId() {
        return id;
    }
    
    public String getName() {
        return name;
    }
    
    public City getCity() {
        return city;
    }
}
