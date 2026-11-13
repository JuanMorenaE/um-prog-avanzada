package uy.edu.um.miniweb.game;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import java.util.List;

public interface GameRepository extends JpaRepository<Game, Long> {
    @Query("select g from Game g where (:genreId is null or g.genre.id = :genreId) and (locate(lower(:q), lower(g.title)) > 0 or locate(lower(:q), lower(g.studio)) > 0) order by g.featured desc, g.id desc")
    List<Game> search(@Param("q") String q, @Param("genreId") Long genreId);
    List<Game> findAllByTitleIgnoreCase(String title);
    java.util.Optional<Game> findFirstByFeaturedTrueOrderByIdAsc();
}
