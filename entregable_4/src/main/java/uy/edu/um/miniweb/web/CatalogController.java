package uy.edu.um.miniweb.web;

import jakarta.validation.Valid;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;
import org.springframework.web.server.ResponseStatusException;
import uy.edu.um.miniweb.game.*;
import uy.edu.um.miniweb.genre.*;
import java.util.List;

@Controller
public class CatalogController {
    private final GameService games;
    private final GenreService genres;
    public CatalogController(GameService games, GenreService genres) { this.games = games; this.genres = genres; }
    @ModelAttribute("genres") public List<Genre> genres() { return genres.list(); }
    @ModelAttribute("covers") public List<String> covers() { return List.of("orbit", "dunes", "bloom", "echo", "summit", "noir"); }
    @ModelAttribute("platforms") public List<String> platforms() { return List.of("PC", "PlayStation", "Xbox", "Nintendo Switch", "Multiplataforma"); }
    @GetMapping("/")
    public String catalog(@RequestParam(defaultValue = "") String q, @RequestParam(required = false) Long genre, Model model) {
        model.addAttribute("games", games.search(q, genre));
        model.addAttribute("total", games.count());
        model.addAttribute("featured", games.featured());
        model.addAttribute("q", q);
        model.addAttribute("selectedGenre", genre);
        return "index";
    }
    @GetMapping("/juegos/nuevo")
    public String newGame(Model model) { model.addAttribute("gameForm", new GameForm()); return "game-form"; }
    @PostMapping("/juegos")
    public String createGame(@Valid @ModelAttribute GameForm gameForm, BindingResult result, RedirectAttributes redirect) {
        if (result.hasErrors()) return "game-form";
        Game game;
        try { game = games.create(gameForm); }
        catch (ResponseStatusException ex) { result.rejectValue("genreId", "invalid", "Ese género no existe. Elegí otro."); return "game-form"; }
        redirect.addFlashAttribute("success", "Juego agregado.");
        return "redirect:/juegos/" + game.getId();
    }
    @GetMapping("/juegos/{id}")
    public String detail(@PathVariable Long id, Model model) { model.addAttribute("game", games.get(id)); return "game-detail"; }
    @GetMapping("/generos")
    public String genrePage(Model model) { model.addAttribute("genreForm", new GenreForm()); return "genres"; }
    @PostMapping("/generos")
    public String createGenre(@Valid @ModelAttribute GenreForm genreForm, BindingResult result, RedirectAttributes redirect) {
        if (result.hasErrors()) return "genres";
        try { genres.create(genreForm.getName()); }
        catch (IllegalArgumentException ex) { result.rejectValue("name", "duplicate", ex.getMessage()); return "genres"; }
        redirect.addFlashAttribute("success", "Género creado.");
        return "redirect:/generos";
    }
}
