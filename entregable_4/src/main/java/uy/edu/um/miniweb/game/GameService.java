package uy.edu.um.miniweb.game;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.validation.annotation.Validated;
import jakarta.validation.Valid;
import org.springframework.web.server.ResponseStatusException;
import org.springframework.http.HttpStatus;
import uy.edu.um.miniweb.genre.GenreService;
import java.util.List;

@Service
@Validated
@Transactional(readOnly = true)
public class GameService {

    private final GameRepository repository;
    private final GenreService genres;

    public GameService(GameRepository repository, GenreService genres) {
        this.repository = repository;
        this.genres = genres;
    }

    public List<Game> search(String q, Long genreId) {
        return repository.search(q == null ? "" : q.strip(), genreId);
    }

    public long count() {
        return repository.count();
    }

    public Game featured() {
        return repository.findFirstByFeaturedTrueOrderByIdAsc().orElse(null);
    }

    public Game get(Long id) {
        return repository.findById(id)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Juego no encontrado"));
    }

    @Transactional
    public Game create(@Valid GameForm form) {
        return repository.save(new Game(form, genres.get(form.getGenreId())));
    }
}
