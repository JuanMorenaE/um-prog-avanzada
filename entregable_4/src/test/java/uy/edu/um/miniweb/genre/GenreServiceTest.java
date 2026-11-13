package uy.edu.um.miniweb.genre;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.*;
import org.mockito.junit.jupiter.MockitoExtension;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class GenreServiceTest {
    @Mock GenreRepository repository;
    @InjectMocks GenreService service;
    @Test void trimsNamesBeforeSaving() {
        when(repository.save(any())).thenAnswer(i -> i.getArgument(0));
        assertEquals("Estrategia", service.create("  Estrategia  ").getName());
        verify(repository).existsByNameIgnoreCase("Estrategia");
    }
    @Test void rejectsDuplicateNamesIgnoringCase() {
        when(repository.existsByNameIgnoreCase("rpg")).thenReturn(true);
        assertThrows(IllegalArgumentException.class, () -> service.create("rpg"));
        verify(repository, never()).save(any());
    }
    @Test void rejectsBlankAndLongNames() {
        assertThrows(IllegalArgumentException.class, () -> service.create("  "));
        assertThrows(IllegalArgumentException.class, () -> service.create("x".repeat(41)));
        verifyNoInteractions(repository);
    }
}
