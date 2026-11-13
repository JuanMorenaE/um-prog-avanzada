package uy.edu.um.miniweb;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc;
import org.springframework.test.web.servlet.MockMvc;
import uy.edu.um.miniweb.game.*;
import uy.edu.um.miniweb.genre.*;
import uy.edu.um.miniweb.config.CatalogData;
import static org.junit.jupiter.api.Assertions.*;
import static org.hamcrest.Matchers.containsString;
import static org.hamcrest.Matchers.hasSize;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest(properties = {"spring.datasource.url=jdbc:h2:mem:integration;DB_CLOSE_DELAY=-1", "spring.jpa.hibernate.ddl-auto=create-drop"})
@AutoConfigureMockMvc
class CatalogIntegrationTest {
    @Autowired MockMvc mvc;
    @Autowired GameRepository games;
    @Autowired GenreRepository genres;
    @Autowired CatalogData catalogData;
    @Test void descriptionDoesNotSwallowFormFieldsAndPreservesInputAfterValidation() throws Exception {
        String empty = mvc.perform(get("/juegos/nuevo")).andExpect(status().isOk())
            .andReturn().getResponse().getContentAsString(java.nio.charset.StandardCharsets.UTF_8);
        assertDescriptionField(empty, "");

        String invalid = mvc.perform(post("/juegos").param("title", "").param("description", "Una descripción de prueba."))
            .andExpect(status().isOk()).andExpect(model().attributeHasFieldErrors("gameForm", "title"))
            .andReturn().getResponse().getContentAsString(java.nio.charset.StandardCharsets.UTF_8);
        assertDescriptionField(invalid, "Una descripción de prueba.");
    }

    private void assertDescriptionField(String html, String expected) {
        var textarea = java.util.regex.Pattern.compile("<textarea\\b[^>]*id=\"description\"[^>]*>(.*?)</textarea>", java.util.regex.Pattern.DOTALL).matcher(html);
        assertTrue(textarea.find(), "El campo Descripción debe tener su etiqueta de cierre.");
        assertEquals(expected, org.unbescape.html.HtmlEscape.unescapeHtml(textarea.group(1).strip()));
        for (String control : new String[]{"id=\"studio\"", "id=\"releaseYear\"", "id=\"genreId\"", "id=\"platform\"", "Guardar juego"}) {
            assertTrue(html.indexOf(control, textarea.end()) >= textarea.end(), "El control debe quedar fuera de Descripción: " + control);
        }
    }

    @Test void rendersAllScreensAndLocalAssets() throws Exception {
        for (String path : new String[]{"/", "/generos", "/juegos/nuevo", "/juegos/1"}) {
            mvc.perform(get(path)).andExpect(status().isOk()).andExpect(content().string(containsString("SIDEQUEST")));
        }
        mvc.perform(get("/images/orbit.svg")).andExpect(status().isOk());
        mvc.perform(get("/css/style.css")).andExpect(status().isOk());
        mvc.perform(get("/fonts/lato-400.ttf")).andExpect(status().isOk());
        for (Game game : games.search("", null)) {
            mvc.perform(get(game.getCoverPath())).andExpect(status().isOk());
        }
    }
    @Test void createsGenreThenGameAndFindsItThroughCombinedFilters() throws Exception {
        mvc.perform(post("/generos").param("name", "Integración")).andExpect(status().is3xxRedirection());
        Genre genre = genres.findAll().stream().filter(g -> g.getName().equals("Integración")).findFirst().orElseThrow();
        mvc.perform(post("/juegos").param("title", "Prueba única").param("description", "Dos módulos conectados.")
            .param("studio", "Estudio de prueba").param("releaseYear", "2026").param("genreId", genre.getId().toString())
            .param("platform", "PC").param("cover", "bloom"))
            .andExpect(status().is3xxRedirection()).andExpect(redirectedUrlPattern("/juegos/*"));
        mvc.perform(get("/").param("q", "PRUEBA ÚNICA").param("genre", genre.getId().toString()))
            .andExpect(status().isOk()).andExpect(content().string(containsString("Prueba única")))
            .andExpect(model().attribute("games", hasSize(1)));
        assertEquals(1, games.search("Estudio de prueba", genre.getId()).size());
    }
    @Test void invalidFormsDoNotPersistAndKeepErrorsVisible() throws Exception {
        long count = games.count();
        mvc.perform(post("/juegos").param("title", "").param("releaseYear", "1900").param("cover", "../../x"))
            .andExpect(status().isOk()).andExpect(model().attributeHasFieldErrors("gameForm", "title", "releaseYear", "cover"));
        assertEquals(count, games.count());
        mvc.perform(post("/generos").param("name", " aventura ")).andExpect(status().isOk())
            .andExpect(content().string(containsString("Ese género ya existe.")));
    }
    @Test void unknownGenreCannotCreateGame() throws Exception {
        long count = games.count();
        mvc.perform(post("/juegos").param("title", "Fantasma").param("description", "No debería guardarse")
            .param("studio", "Prueba").param("releaseYear", "2026").param("genreId", "99999").param("platform", "PC").param("cover", "orbit"))
            .andExpect(status().isOk()).andExpect(model().attributeHasFieldErrors("gameForm", "genreId"));
        assertEquals(count, games.count());
    }
    @Test void searchTreatsWildcardCharactersLiterallyAndRendersEmptyState() throws Exception {
        mvc.perform(get("/").param("q", "%_sin_resultados"))
            .andExpect(status().isOk()).andExpect(content().string(containsString("No se encontraron juegos.")));
    }
    @Test void unknownGameReturns404() throws Exception { mvc.perform(get("/juegos/99999")).andExpect(status().isNotFound()); }

    @Test void gtaStaysFirstAfterAddingGamesAndFiltersStillApply() throws Exception {
        Game gta = games.findFirstByFeaturedTrueOrderByIdAsc().orElseThrow();
        Genre racing = genres.findAll().stream().filter(g -> g.getName().equals("Carreras")).findFirst().orElseThrow();
        GameForm form = new GameForm();
        form.setTitle("Carrera de prueba"); form.setDescription("Nueva entrada"); form.setStudio("Estudio nuevo");
        Game added = games.save(new Game(form, racing));
        assertTrue(added.getId() > gta.getId());
        assertEquals(gta.getId(), games.search("", null).getFirst().getId());
        assertTrue(games.search("", racing.getId()).stream().noneMatch(Game::isFeatured));
        assertEquals(1, games.search("Carrera de prueba", racing.getId()).size());
        mvc.perform(get("/")).andExpect(status().isOk()).andExpect(model().attributeExists("featured"))
            .andExpect(content().string(containsString("Ver GTA VI")));
    }

    @Test void catalogUpgradeRemovesOldExamplesPreservesUserGamesAndDoesNotDuplicate() {
        Genre genre = genres.findAll().getFirst();
        GameForm legacy = new GameForm();
        legacy.setTitle("NOIR SIGNAL"); legacy.setStudio("Midnight Bureau"); legacy.setDescription("Ejemplo anterior");
        Game previousExample = games.save(new Game(legacy, genre));
        GameForm custom = new GameForm();
        custom.setTitle("Mi propio juego"); custom.setStudio("Mi estudio"); custom.setDescription("Creado por el usuario");
        Game userGame = games.save(new Game(custom, genre));
        long before = games.count();
        catalogData.run();
        assertFalse(games.existsById(previousExample.getId()));
        assertTrue(games.existsById(userGame.getId()));
        assertEquals(before - 1, games.count());
        catalogData.run();
        assertEquals(before - 1, games.count());
        assertEquals(1, games.findAllByTitleIgnoreCase("Grand Theft Auto VI").size());
    }
}
