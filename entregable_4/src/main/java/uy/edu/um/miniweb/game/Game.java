package uy.edu.um.miniweb.game;

import jakarta.persistence.*;
import uy.edu.um.miniweb.genre.Genre;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.Set;

@Entity
public class Game {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 80)
    private String title;

    @Column(nullable = false, length = 1200)
    private String description;

    @Column(nullable = false, length = 60)
    private String studio;

    private int releaseYear;
    private String platform;
    private String cover;

    @Column(nullable = false, columnDefinition = "boolean default false")
    private boolean featured;

    private LocalDate releaseDate;
    private String officialUrl;

    @ManyToOne(optional = false, fetch = FetchType.EAGER)
    private Genre genre;

    protected Game() {
    }

    public Game(GameForm form, Genre genre) {
        this.title = form.getTitle().strip();
        this.description = form.getDescription().strip();
        this.studio = form.getStudio().strip();
        this.releaseYear = form.getReleaseYear();
        this.platform = form.getPlatform();
        this.cover = form.getCover();
        this.genre = genre;
    }

    public Long getId() {
        return id;
    }

    public String getTitle() {
        return title;
    }

    public String getDescription() {
        return description;
    }

    public String getStudio() {
        return studio;
    }

    public int getReleaseYear() {
        return releaseYear;
    }

    public String getPlatform() {
        return platform;
    }

    public String getCover() {
        return cover;
    }

    public Genre getGenre() {
        return genre;
    }

    public boolean isFeatured() {
        return featured;
    }

    public boolean isUpcoming() {
        return releaseDate != null && releaseDate.isAfter(LocalDate.now());
    }

    public String getReleaseLabel() {
        if (releaseDate == null) {
            return String.valueOf(releaseYear);
        }
        return (isUpcoming() ? "Próximamente · " : "")
                + releaseDate.format(DateTimeFormatter.ofPattern("dd/MM/yyyy"));
    }

    public String getOfficialUrl() {
        return officialUrl;
    }

    public String getCoverPath() {
        return Set.of("gta-vi", "god-of-war", "spider-man", "gran-turismo", "elden-ring",
                        "last-of-us", "astro-bot", "resident-evil", "returnal").contains(cover)
                ? "/images/games/" + cover + ".jpg"
                : "/images/" + cover + ".svg";
    }

    public void setCatalogDetails(boolean featured, LocalDate releaseDate, String officialUrl) {
        this.featured = featured;
        this.releaseDate = releaseDate;
        this.officialUrl = officialUrl;
    }
}
