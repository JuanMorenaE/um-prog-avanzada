# Entregable 4 - CI/CD: estado y pendientes

> Revisión hecha el 12/11/2026 contra el enunciado "Prog. Avanzada 2026 - Entregable 4 - CI_CD - V2".
> Grupo de **3 personas**, así que el **Anexo UAT es obligatorio**.
> Repo: `entregables/entregable_4` (rama `develop`).

**Fechas**
- Presentación en clase: 13/11 - 16/11 (grupo Lunes y Viernes) o 17/11 (grupo Martes y Miércoles). Tienen que estar los 3.
- Entrega por Moodle: **17/11 a las 12:00**.

---

## ✅ Lo que ya está bien

| Requisito | Estado |
|---|---|
| Java + Spring | ✅ Spring Boot 4.1.2, Java 21 |
| Pipeline declarativo versionado con el código (*pipeline as code*) | ✅ `Jenkinsfile` en el repo |
| Etapas de build y test | ✅ `Build` (`clean compile`) y `Test` (`test`) |
| Jenkins muestra los resultados de los tests | ✅ `junit` en `post { always }` |
| Funciona en Windows y Mac/Linux | ✅ la función `mvnw()` usa `isUnix()` para elegir `sh` o `bat` |
| No choca con el puerto de Jenkins | ✅ la app corre en el puerto 8081 (Jenkins usa 8080) |
| Git + GitHub | ✅ repo en GitHub, trabajo en `develop` |
| Los tests pasan | ✅ última corrida: 1 test, 0 fallos |

---

## ❌ Lo que falta

### 1. La aplicación (funcional)

- [ ] **Elegir el dominio** de la app (catálogo de videojuegos, adopción de mascotas, conciertos u otro).
- [ ] Implementar **al menos dos módulos con funcionalidades sencillas**. Hoy es una sola página "Mini Web".
- [ ] Decidir qué significa "sistema formado por varios módulos": Maven multi-módulo o paquetes/funcionalidades dentro de una sola app. **Justificarlo en el PDF.**
- [ ] Persistencia: hoy no hay ninguna. Es opcional, pero si se van a "registrar" cosas hace falta una base de datos (por ejemplo H2) o un archivo.
- [ ] Detalle chico: `HomeController` pasa el atributo `mensaje`, pero `index.html` no lo usa (el texto está fijo como "Mensaje de ejemplo").

### 2. Tests

- [ ] Hoy solo existe `contextLoads()`, una prueba mínima de que la app arranca.
- [ ] **Pruebas unitarias de cada módulo.**
- [ ] **Pruebas de integración** (por ejemplo `@SpringBootTest` + `MockMvc`).
- [ ] *(Recomendado)* Separar unitarias e integración: surefire para las unitarias y failsafe para las de integración (clases `*IT.java`). Así se ven como etapas distintas en Jenkins.

### 3. Pipeline (lo central del entregable)

- [ ] **Etapa de empaquetado** (`package`, genera el `.jar`).
- [ ] **Etapa de deploy** a un **ambiente simulado de producción** (una carpeta local o un contenedor Docker). Hoy el pipeline termina en los tests.
- [ ] **Disparo automático en cada cambio del repo de GitHub.** El `Jenkinsfile` no tiene `triggers {}`.
  - Puede estar configurado en la interfaz del job. Verificarlo.
  - Si Jenkins corre en local, un webhook de GitHub no llega a `localhost` sin un túnel (ngrok o similar). `pollSCM` es la opción más simple.
- [ ] Por tener todas las entregas en el mismo repo (`entregables/`):
  - El job tiene que apuntar a `entregable_4/Jenkinsfile` (Script Path).
  - Cualquier push a otras entregas también lo dispara. Se puede evitar con `when { changeset 'entregable_4/**' }`.
- [ ] *(Opcional)* Ya está Actuator en el `pom.xml`: el deploy podría terminar consultando `/actuator/health` para confirmar que la app levantó.

### 4. Anexo UAT (obligatorio, somos 3)

- [ ] Ambiente de **desarrollo** separado de los de UAT y producción.
- [ ] Ambiente **UAT** (aceptación de usuarios), separado de producción, donde se puedan hacer pruebas manuales. Por ejemplo otra carpeta u otro contenedor, en otro puerto (8082, por ejemplo).
- [ ] Paso de **aprobación manual en Jenkins** (`input`) antes de desplegar a producción, para que alguien entre a Jenkins y apruebe la versión.
- [ ] **Simular un error encontrado en UAT** y documentar las acciones a tomar: rechazar la aprobación, crear la rama del fix, volver a pasar por el pipeline, etc.

Flujo esperado:

```
push → Build → Tests unitarios → Tests de integración → Package
     → Deploy UAT → pruebas manuales → [Aprobación en Jenkins] → Deploy Producción
```

### 5. Git colaborativo

- [ ] Hoy todos los commits de `entregable_4` son de una sola persona. Para que se note el trabajo colaborativo:
  - [ ] Cada integrante hace commits con su propia cuenta.
  - [ ] Usar ramas de feature y Pull Requests hacia `develop`.
  - [ ] Hacer el merge `develop` → `main` cuando corresponda (hoy `main` no tiene el `Jenkinsfile`; está solo en `develop`).

### 6. Entregables

- [ ] **README** en `entregable_4`. El `HELP.md` actual es el que genera Spring Initializr y además está en el `.gitignore`.
- [ ] **Informe PDF** con, como mínimo:
  - [ ] a. Arquitectura de la solución.
  - [ ] b. Decisiones tomadas y su justificación (qué app eligieron, lenguaje, módulos, persistencia, tipo de ambiente simulado, etc.).
  - [ ] c. Instructivo de ejecución.
  - [ ] d. Breve resumen de los errores encontrados al ejecutar el pipeline y cómo se solucionaron.
    - Ya hubo fallos (commits "fix Jenkinsfile"). **Sacar esos errores del historial de builds de Jenkins ahora**, antes de que se pierdan.
  - [ ] e. Conclusiones y dificultades encontradas.
- [ ] **Zip** con nombre `Entregable4Apellido1Apellido2Apellido3.zip` que contenga el código fuente, el pipeline, el README y el PDF.

### 7. Defensa en clase (preparar la demo)

- [ ] Mostrar la arquitectura, la estructura del proyecto y una explicación breve del pipeline.
- [ ] Ejecutar la app y mostrar brevemente cómo funciona.
- [ ] **Caso 1 – Integración exitosa:** hacer un push, ver que el pipeline arranca solo, termina bien y la app aparece en producción (pasando por UAT y la aprobación).
- [ ] **Caso 2 – Fallo en las pruebas:** romper un test, ver que el pipeline falla y **no despliega**, y explicar cómo se procede. Para poder mostrarlo, primero tiene que existir la etapa de deploy.
- [ ] **Caso UAT:** mostrar un error encontrado en UAT, el rechazo en Jenkins y las acciones a tomar.
- [ ] Ensayarlo antes con Jenkins levantado y los 3 integrantes presentes.

---

## Prioridad sugerida

1. Pipeline: etapas de package y deploy, más el disparo automático.
2. App con dos módulos y sus tests (unitarias + integración).
3. Ambiente UAT con aprobación manual (`input`) antes de producción.
4. README y PDF (incluido el registro de errores del pipeline).
5. Ensayo de la demo y armado del zip.
