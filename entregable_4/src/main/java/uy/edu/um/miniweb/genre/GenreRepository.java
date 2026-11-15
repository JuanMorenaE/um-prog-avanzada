package uy.edu.um.miniweb.genre;

import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface GenreRepository extends JpaRepository<Genre, Long> {

    List<Genre> findAllByOrderByNameAsc();

    boolean existsByNameIgnoreCase(String name);
}
