package uy.edu.um.miniweb.game;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.*;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.web.server.ResponseStatusException;
import uy.edu.um.miniweb.genre.*;
import java.util.Optional;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class GameServiceTest {
    @Mock GameRepository repository;
    @Mock GenreService genres;
    @InjectMocks GameService service;
    @Test void createsGameLinkedToExistingGenre() {
        Genre genre = new Genre("Aventura");
        when(genres.get(1L)).thenReturn(genre);
        when(repository.save(any())).thenAnswer(i -> i.getArgument(0));
        GameForm f = new GameForm();
        f.setTitle("  Un mundo  "); f.setDescription(" Historia "); f.setStudio(" Estudio "); f.setGenreId(1L);
        Game game = service.create(f);
        assertEquals("Un mundo", game.getTitle());
        assertEquals("Historia", game.getDescription());
        assertSame(genre, game.getGenre());
    }
    @Test void normalizesSearchAndPassesGenreFilter() {
        service.search("  ORBIT  ", 3L);
        verify(repository).search("ORBIT", 3L);
        service.search(null, null);
        verify(repository).search("", null);
    }
    @Test void missingGameReturnsNotFound() {
        when(repository.findById(999L)).thenReturn(Optional.empty());
        assertEquals(404, assertThrows(ResponseStatusException.class, () -> service.get(999L)).getStatusCode().value());
    }
}
