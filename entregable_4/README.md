# SIDEQUEST

Catálogo de videojuegos para PlayStation con fondo carbón, acento lima y portadas oficiales. GTA VI está destacado en la portada y fijado primero en el catálogo. La navegación y los formularios usan Lato, incluida localmente. Inspiración visual: [Freshman en Refero](https://styles.refero.design/style/a6284fcd-fa69-4469-ac40-4239e5b84a39), adaptada al catálogo.

## Requisitos y ejecución

- JDK 21 o superior (configurar `JAVA_HOME` apuntando al JDK).
- Acceso a Internet durante la primera compilación para descargar Maven y las dependencias.
- Ejecutar los comandos desde `entregable_4`.

Windows / PowerShell:

```powershell
.\mvnw.cmd clean verify
java -jar target/mini-web-0.0.1-SNAPSHOT.jar
```

Linux / macOS / Jenkins:

```sh
sh mvnw clean verify
java -jar target/mini-web-0.0.1-SNAPSHOT.jar
```

Abrir **http://localhost:8081**. El puerto 8080 queda reservado para Jenkins. Detener con `Ctrl+C`.
También se puede ejecutar directamente con `mvnw.cmd spring-boot:run` (Windows) o `sh mvnw spring-boot:run`.

No requiere Node, una base de datos instalada ni servicios de imágenes o fuentes externos. Thymeleaf renderiza las páginas en el servidor. El JavaScript solo mejora la vista previa de portada: los formularios funcionan sin él.

## Funcionalidades

- Catálogo inicial con GTA VI, God of War Ragnarök, Marvel's Spider-Man 2, Gran Turismo 7, Elden Ring, The Last of Us Part I, Astro Bot, Resident Evil 4 y Returnal.
- GTA VI aparece primero; las demás entradas se ordenan de la más reciente a la más antigua en el catálogo. Los filtros también se aplican al destacado dentro de la grilla.
- Búsqueda por título o estudio sin distinguir mayúsculas, combinable con filtro por género.
- Detalle individual con descripción, género, plataforma, estudio y año.
- Registro de juegos con validaciones del lado del servidor y selección de portada local.
- Creación y listado de géneros; rechazo de nombres repetidos sin distinguir mayúsculas.
- Mensajes de éxito, errores de campo, estado sin resultados y página de error.
- Diseño adaptable a escritorio y celular, navegación por teclado y soporte de movimiento reducido.

## Arquitectura

Dos módulos funcionales dentro de un único proyecto Maven (monolito modular por paquetes):

```text
uy.edu.um.miniweb
├── genre   Entidad, repositorio JPA, formulario y servicio de géneros
├── game    Entidad, repositorio JPA, formulario y servicio de videojuegos
├── web     Controlador MVC del catálogo y formularios
└── config  Catálogo inicial y migración de ejemplos anteriores
```

Flujo: navegador → controlador MVC → servicios → repositorios Spring Data JPA → H2.
`GameService` consulta `GenreService` para asociar cada juego a un género existente. La relación está protegida por una clave foránea. Las operaciones de escritura son transaccionales.

Tecnologías: Java 21, Spring Boot 4.1.2 (versión que ya tenía el proyecto), Spring MVC, Thymeleaf, Jakarta Validation, Spring Data JPA, H2, JUnit y Mockito.

## Persistencia

La base se guarda en `data/sidequest.mv.db`, relativa a la carpeta desde la que se inicia Java. Los registros sobreviven a los reinicios. Al iniciar se agregan las entradas oficiales que falten, sin duplicarlas. La actualización reemplaza los seis ejemplos ficticios anteriores identificándolos por título y estudio, y conserva las entradas del usuario. Las pruebas utilizan bases H2 en memoria separadas y no modifican el catálogo local.

Para entornos separados, elegir un puerto y una ubicación distinta de la base:

```powershell
java -jar target/mini-web-0.0.1-SNAPSHOT.jar --server.port=8082 --spring.datasource.url=jdbc:h2:file:./data-uat/sidequest
```

Se admiten las variables `PORT` y `DB_URL`. No iniciar dos procesos con el mismo archivo H2. No versionar ni incluir `data/`, `.m2/` o `target/` en la entrega de código fuente.

## Pruebas e integración con CI

`clean verify` compila, ejecuta las pruebas y produce el JAR ejecutable. Si alguna prueba falla, Maven devuelve un código distinto de cero. Reportes JUnit: `target/surefire-reports/TEST-*.xml`; artefacto: `target/mini-web-0.0.1-SNAPSHOT.jar`. Salud de la aplicación: `GET /actuator/health` devuelve un JSON con `"status":"UP"` cuando está disponible.

La suite contiene pruebas unitarias de ambos servicios y pruebas de integración con MockMvc, Thymeleaf y H2 reales: creación de género y juego, búsqueda combinada, renderizado de páginas, recursos estáticos, validaciones, género inexistente, búsqueda sin resultados y HTTP 404. No hay dependencias de sistemas externos en las pruebas.

El `Jenkinsfile` del equipo compila, ejecuta las pruebas y empaqueta la aplicación; luego despliega el mismo JAR en UAT (8082) y, tras la aprobación manual, en producción (8083). Cada ambiente inicia Java desde su propia carpeta, por lo que el archivo H2 también queda separado. El desarrollo local usa 8081 y Jenkins usa 8080. El disparador consulta GitHub cada minuto.

## Recorrido para la presentación

1. Abrir el catálogo, ver GTA VI destacado, buscar `Spider-Man` y probar el filtro Carreras.
2. Abrir un juego para mostrar su detalle.
3. Entrar en Géneros y crear `Estrategia`.
4. Agregar un juego con ese género, elegir portada y mostrar el resultado.
5. Reiniciar la aplicación y comprobar que el juego sigue en el catálogo.
6. Mostrar `clean verify` y sus reportes para integrar la aplicación al pipeline.

Alcance: aplicación académica local sin autenticación. Al registrar juegos se puede elegir una de las seis portadas abstractas incluidas; las entradas oficiales usan imágenes locales descargadas de PlayStation. No hay carga de archivos ni compras. Cada ficha oficial enlaza al sitio del juego. Fuentes, atribución de imágenes y licencia de tipografía en [SOURCES.md](SOURCES.md).
