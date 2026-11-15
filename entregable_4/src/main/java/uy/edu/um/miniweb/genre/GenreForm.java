package uy.edu.um.miniweb.genre;

import jakarta.validation.constraints.*;

public class GenreForm {

    @NotBlank(message = "Escribí un nombre para el género.")
    @Size(max = 40, message = "Usá hasta 40 caracteres.")
    private String name;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }
}
