package uy.edu.um.miniweb.config;

import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;
import uy.edu.um.miniweb.game.*;
import uy.edu.um.miniweb.genre.*;
import java.time.LocalDate;
import java.util.Map;

/** Updates the supplied catalog without resetting games or genres added by the user. */
@Component
public class CatalogData implements CommandLineRunner {
    private final GameRepository games;
    private final GenreRepository genres;
    public CatalogData(GameRepository games, GenreRepository genres) { this.games = games; this.genres = genres; }

    @Override @Transactional
    public void run(String... args) {
        Map<String, String> previousExamples = Map.of(
            "NOIR SIGNAL", "Midnight Bureau", "SUMMIT", "Northbound", "ECHO CHAMBER", "Soft Circuit",
            "AFTER BLOOM", "Moss & Moon", "DUNE WALKER", "Sandpaper Studio", "ORBITAL / 09", "Quiet Planet");
        games.findAll().stream()
            .filter(g -> g.getStudio().equals(previousExamples.get(g.getTitle())))
            .forEach(games::delete);
        games.flush();

        add("Grand Theft Auto VI", "Jason y Lucia recorren Vice City y el estado de Leonida en una historia de crimen y mundo abierto.", "Rockstar Games", 2026, "gta-vi", "Mundo abierto", "grand-theft-auto-vi", true);
        add("Returnal", "Selene queda atrapada en un planeta hostil. Cada muerte reinicia un ciclo de combate, exploración y escenarios cambiantes.", "Housemarque", 2021, "returnal", "Shooter", "returnal", false);
        add("Resident Evil 4", "Leon S. Kennedy busca a la hija del presidente en una aldea europea. Remake del clásico de terror y acción.", "Capcom", 2023, "resident-evil", "Terror", "resident-evil-4-remake", false);
        add("Astro Bot", "Astro recorre planetas, rescata a su tripulación y usa nuevas habilidades en una aventura de plataformas.", "Team Asobi", 2024, "astro-bot", "Plataformas", "astro-bot", false);
        add("The Last of Us Part I", "Joel y Ellie cruzan Estados Unidos después de una pandemia. Reconstrucción del juego original para PS5.", "Naughty Dog", 2022, "last-of-us", "Supervivencia", "the-last-of-us-part-i", false);
        add("Elden Ring", "Explorá las Tierras Intermedias, enfrentá a sus semidioses y construí tu personaje en un RPG de mundo abierto.", "FromSoftware", 2022, "elden-ring", "RPG", "elden-ring", false);
        add("Gran Turismo 7", "Coleccioná autos, obtené licencias y competí en circuitos reales y originales en el simulador de conducción de Polyphony Digital.", "Polyphony Digital", 2022, "gran-turismo", "Carreras", "gran-turismo-7", false);
        add("Marvel's Spider-Man 2", "Peter Parker y Miles Morales se enfrentan a Kraven y Venom mientras protegen Nueva York.", "Insomniac Games", 2023, "spider-man", "Aventura", "marvels-spider-man-2", false);
        add("God of War Ragnarök", "Kratos y Atreus viajan por los nueve reinos mientras se acerca el Ragnarök. Combate y mitología nórdica.", "Santa Monica Studio", 2022, "god-of-war", "Acción", "god-of-war-ragnarok", false);
    }

    private void add(String title, String description, String studio, int year, String cover, String genreName, String slug, boolean featured) {
        // Match both title and studio so a user-created entry never prevents initial catalog setup.
        Game game = games.findAllByTitleIgnoreCase(title).stream().filter(g -> g.getStudio().equals(studio)).findFirst().orElse(null);
        if (game == null) {
            Genre genre = genres.findAllByOrderByNameAsc().stream().filter(g -> g.getName().equalsIgnoreCase(genreName))
                .findFirst().orElseGet(() -> genres.save(new Genre(genreName)));
            GameForm f = new GameForm();
            f.setTitle(title); f.setDescription(description); f.setStudio(studio); f.setReleaseYear(year);
            f.setPlatform("PlayStation"); f.setCover(cover);
            game = new Game(f, genre);
        }
        game.setCatalogDetails(featured, featured ? LocalDate.of(2026, 11, 19) : null, "https://www.playstation.com/en-us/games/" + slug + "/");
        games.save(game);
    }
}
