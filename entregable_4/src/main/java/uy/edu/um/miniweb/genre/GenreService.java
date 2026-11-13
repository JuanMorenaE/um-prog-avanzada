package uy.edu.um.miniweb.genre;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.server.ResponseStatusException;
import org.springframework.http.HttpStatus;
import java.util.List;

@Service
@Transactional(readOnly = true)
public class GenreService {
    private final GenreRepository repository;
    public GenreService(GenreRepository repository) { this.repository = repository; }
    public List<Genre> list() { return repository.findAllByOrderByNameAsc(); }
    public Genre get(Long id) {
        return repository.findById(id).orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Género no encontrado"));
    }
    @Transactional
    public Genre create(String name) {
        String clean = name == null ? "" : name.strip();
        if (clean.isEmpty() || clean.length() > 40) throw new IllegalArgumentException("El nombre debe tener entre 1 y 40 caracteres.");
        if (repository.existsByNameIgnoreCase(clean)) throw new IllegalArgumentException("Ese género ya existe.");
        return repository.save(new Genre(clean));
    }
}
