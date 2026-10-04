package display;

import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Objects;

// Contiene valores copiados, nunca referencias a los actores de la simulacion.
public record EventoDisplay(long numero, long milisegundos, String mensaje, boolean abierto,
        Map<String, String> actores, Map<Integer, String> mesas, Map<String, Integer> colas) {
    public EventoDisplay {
        Objects.requireNonNull(mensaje);
        actores = Collections.unmodifiableMap(new LinkedHashMap<>(actores));
        mesas = Collections.unmodifiableMap(new LinkedHashMap<>(mesas));
        colas = Collections.unmodifiableMap(new LinkedHashMap<>(colas));
    }
}
