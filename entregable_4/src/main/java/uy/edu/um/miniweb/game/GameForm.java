package uy.edu.um.miniweb.game;

import jakarta.validation.constraints.*;

public class GameForm {
    @NotBlank(message = "El título es obligatorio.")
    @Size(max = 80)
    private String title;
    @NotBlank(message = "Contanos de qué trata el juego.")
    @Size(max = 1200)
    private String description;
    @NotBlank(message = "Indicá el estudio creador.")
    @Size(max = 60)
    private String studio;
    @NotNull(message = "Indicá el año.")
    @Min(1950)
    @Max(2100)
    private Integer releaseYear = 2026;
    @NotNull(message = "Elegí un género.")
    private Long genreId;
    @NotBlank
    @Pattern(regexp = "PC|PlayStation|Xbox|Nintendo Switch|Multiplataforma", message = "Elegí una plataforma válida.")
    private String platform = "PC";
    @NotBlank
    @Pattern(regexp = "orbit|dunes|bloom|echo|summit|noir", message = "Elegí una portada de la colección.")
    private String cover = "orbit";

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getStudio() {
        return studio;
    }

    public void setStudio(String studio) {
        this.studio = studio;
    }

    public Integer getReleaseYear() {
        return releaseYear;
    }

    public void setReleaseYear(Integer releaseYear) {
        this.releaseYear = releaseYear;
    }

    public Long getGenreId() {
        return genreId;
    }

    public void setGenreId(Long genreId) {
        this.genreId = genreId;
    }

    public String getPlatform() {
        return platform;
    }

    public void setPlatform(String platform) {
        this.platform = platform;
    }

    public String getCover() {
        return cover;
    }

    public void setCover(String cover) {
        this.cover = cover;
    }
}
