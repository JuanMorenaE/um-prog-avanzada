# Entregable 4 - CI/CD: estado y pendientes

> Revisión hecha el 12/11/2026 contra el enunciado "Prog. Avanzada 2026 - Entregable 4 - CI_CD - V2".
> Última actualización: 12/11/2026, después del commit `fe5c741` (pollSCM + etapa Package).
> Grupo de **3 personas**, así que el **Anexo UAT es obligatorio**.
> Repo: `entregables/entregable_4` (rama `develop`).

**Fechas**
- Presentación en clase: 13/11 - 16/11 (grupo Lunes y Viernes) o 17/11 (grupo Martes y Miércoles). Tienen que estar los 3.
- Entrega por Moodle: **17/11 a las 12:00**.

---

## Estado del pipeline

```
git push ─► Build ─► Test ─► Package ─► Integración ─► Deploy UAT ─► ⏸ Aprobación ─► Deploy Producción
            ✅        ✅       ✅          ❌              ❌             ❌               ❌
```

---

## ✅ Lo que ya está bien

| Requisito | Estado |
|---|---|
| Java + Spring | ✅ Spring Boot 4.1.2, Java 21 |
| Pipeline declarativo versionado con el código (*pipeline as code*) | ✅ `Jenkinsfile` en el repo |
| Disparo automático ante cambios en GitHub | ✅ `triggers { pollSCM('H/2 * * * *') }` en el Jenkinsfile |
| Etapa Build | ✅ `clean compile` |
| Etapa Test | ✅ `test` (unitarias) |
| Etapa Package | ✅ `package`: genera `target/mini-web-0.0.1-SNAPSHOT.jar` |
| Jenkins muestra los resultados de los tests | ✅ `junit` en `post { always }` |
| Funciona en Windows y Mac/Linux | ✅ la función `mvnw()` usa `isUnix()` para elegir `sh` o `bat` |
| No choca con el puerto de Jenkins | ✅ la app corre en el puerto 8081 (Jenkins usa 8080) |
| Git + GitHub | ✅ repo en GitHub, trabajo en `develop` (sincronizado con `origin/develop`) |
| Los tests pasan | ✅ última corrida: 1 test, 0 fallos |

---

## ❌ Lo que falta

### 1. La aplicación (funcional)

- [ ] **Elegir el dominio** de la app (catálogo de videojuegos, adopción de mascotas, conciertos u otro).
- [ ] Implementar **al menos dos módulos con funcionalidades sencillas**. Hoy es una sola página "Mini Web".
- [ ] Decidir qué significa "sistema formado por varios módulos": Maven multi-módulo o paquetes/funcionalidades dentro de una sola app. **Justificarlo en el PDF.**
- [ ] Persistencia: hoy no hay ninguna. Es opcional, pero si se van a "registrar" cosas hace falta una base de datos (por ejemplo H2) o un archivo.
- [ ] Detalle chico: `HomeController` pasa el atributo `mensaje`, pero `index.html` no lo usa (el texto está fijo como "Mensaje de ejemplo").
- [ ] *(Opcional, ayuda en la demo)* Perfiles `application-uat.properties` y `application-prod.properties` para que la página muestre "Ambiente: UAT" o "Ambiente: PRODUCCIÓN".

### 2. Tests

- [ ] Hoy solo existe `contextLoads()`, una prueba mínima de que la app arranca.
- [ ] **Pruebas unitarias de cada módulo.**
- [ ] **Pruebas de integración** (por ejemplo `@SpringBootTest` + `MockMvc`).
- [ ] *(Recomendado)* Separar unitarias e integración: surefire para las unitarias y failsafe para las de integración (clases `*IT.java`). Así se ven como etapas distintas en Jenkins.
  - Las de failsafe corren en la fase **`verify`**, que viene **después** de `package`.

### 3. Pipeline (lo central del entregable)

- [x] ~~Disparo automático~~: `pollSCM('H/2 * * * *')` en el Jenkinsfile.
  - [ ] Correr el job **una vez a mano** ("Build Now") para que Jenkins registre el trigger.
  - [ ] **Sacar el Poll SCM configurado en la interfaz** del job, para que quede solo el del Jenkinsfile.
  - [ ] Verificar en el job: "Poll SCM" marcado y el menú **"Git Polling Log"** visible.
- [x] ~~Etapa Package~~.
  - [ ] *(Mejora)* Usar `package -DskipTests`: hoy `package` vuelve a correr todos los tests, que ya corrieron en la etapa `Test`.
  - [ ] *(Opcional)* `archiveArtifacts artifacts: 'entregable_4/target/*.jar', fingerprint: true` para guardar el jar de cada build en Jenkins.
- [ ] **Etapa de pruebas de integración** (cuando existan los tests).
- [ ] **Etapa Deploy UAT** (carpeta `~/ambientes/uat`, puerto 8082). Ver la sección *Ambientes y deploy*.
- [ ] **Etapa Aprobación** (`input` con `timeout`). Ver la sección *Ambientes y deploy*.
- [ ] **Etapa Deploy Producción** (carpeta `~/ambientes/prod`, puerto 8083).
- [ ] *(Recomendado)* Una función `deploy(carpeta, puerto)`, como `mvnw()`, para no repetir el código entre UAT y producción.
- [ ] *(Opcional)* Evitar que pushes a otras entregas disparen este pipeline: "Polling ignores commits in certain paths" (región incluida `entregable_4/.*`) en la configuración Git del job, o `when { changeset 'entregable_4/**' }`.

### 4. Anexo UAT (obligatorio, somos 3)

- [ ] Ambiente de **desarrollo**: la máquina de cada uno (IntelliJ o `./mvnw spring-boot:run`, puerto 8081).
- [ ] Ambiente **UAT**: carpeta y puerto propios, levantado por Jenkins.
- [ ] Paso de **aprobación manual en Jenkins** (`input`) antes de desplegar a producción.
- [ ] **Simular un error encontrado en UAT** y documentar las acciones a tomar: rechazar en Jenkins, corregir en una rama, volver a pasar por el pipeline, etc.

### 5. Git colaborativo

- [ ] Hoy todos los commits de `entregable_4` son de una sola persona. Para que se note el trabajo colaborativo:
  - [ ] Cada integrante hace commits con su propia cuenta.
  - [ ] Usar ramas de feature y Pull Requests hacia `develop`.
  - [ ] Hacer el merge `develop` → `main` cuando corresponda (hoy `main` no tiene el `Jenkinsfile`; está solo en `develop`).
- [ ] Revisar qué rama escucha el job de Jenkins (`*/develop` o `*/main`): solo los pushes a esa rama disparan el pipeline.

### 6. Entregables

- [ ] **README** en `entregable_4`. El `HELP.md` actual es el que genera Spring Initializr y además está en el `.gitignore`.
- [ ] **Informe PDF** con, como mínimo:
  - [ ] a. Arquitectura de la solución (incluir el diagrama de Jenkins + ambientes).
  - [ ] b. Decisiones tomadas y su justificación. Candidatas:
    - qué app eligieron, el lenguaje y cómo dividieron los módulos
    - persistencia
    - pollSCM en lugar de webhook (Jenkins local, sin URL pública)
    - ambientes simulados con carpetas + puertos en lugar de Docker
    - un solo `.jar` promovido entre ambientes
    - Jenkins en lugar de GitHub Actions
  - [ ] c. Instructivo de ejecución.
  - [ ] d. Breve resumen de los errores encontrados al ejecutar el pipeline y cómo se solucionaron.
    - Ya hubo fallos (commits "fix Jenkinsfile"). **Sacar esos errores del historial de builds de Jenkins ahora**, antes de que se pierdan.
    - Error típico a documentar si aparece: la app se cae al terminar el build porque Jenkins mata sus procesos (se soluciona con `JENKINS_NODE_COOKIE=dontKillMe`).
  - [ ] e. Conclusiones y dificultades encontradas.
- [ ] **Zip** con nombre `Entregable4Apellido1Apellido2Apellido3.zip` que contenga el código fuente, el pipeline, el README y el PDF.

### 7. Defensa en clase (preparar la demo)

- [ ] Mostrar la arquitectura, la estructura del proyecto y una explicación breve del pipeline.
- [ ] Ejecutar la app y mostrar brevemente cómo funciona.
- [ ] **Caso 1 – Integración exitosa:** hacer un push, ver que el pipeline arranca solo, despliega en UAT (8082), se aprueba en Jenkins y llega a producción (8083).
- [ ] **Caso 2 – Fallo en las pruebas:** romper un test, ver que el pipeline falla y **no despliega** (UAT y producción quedan con la versión anterior), y explicar cómo se procede.
- [ ] **Caso UAT:** encontrar un error en UAT, apretar "Abortar" en Jenkins (producción no se toca), corregir y volver a pasar por el pipeline.
- [ ] Mostrar que, mientras se espera la aprobación, UAT y producción tienen versiones distintas.
- [ ] Ensayarlo antes con Jenkins levantado y los 3 integrantes presentes.

---

## Conceptos aclarados

### Cómo detecta Jenkins los cambios (pollSCM)

- GitHub **no le avisa** a Jenkins. Es **Jenkins el que pregunta** cada cierto tiempo.
- En cada consulta, Jenkins compara el último commit de la rama configurada con el commit del último build. Si es distinto, lanza un build nuevo.
- Cada consulta se ve en el job, en **"Git Polling Log"**.
- **Por qué pollSCM y no webhook:** un webhook necesita que GitHub pueda llegar a Jenkins. Como Jenkins corre en `localhost`, eso requeriría un túnel (ngrok o similar). Con pollSCM **no hay que instalar nada más**.
- Polling necesita un build previo para comparar: la primera vez se corre el job a mano.

### Expresión cron: `H/2 * * * *`

Son **5 campos**, siempre:

```
H/2   *     *     *     *
│     │     │     │     └── día de la semana  (0-7, domingo = 0 o 7)
│     │     │     └──────── mes               (1-12)
│     │     └────────────── día del mes        (1-31)
│     └──────────────────── hora              (0-23)
└────────────────────────── minuto            (0-59)
```

- `*` = todos los valores de ese campo.
- Un número solo (`5`) = **en** ese valor exacto, no "cada 5".
- `*/N` o `H/N` = **cada** N de la unidad del campo.
- `H` = Jenkins elige el punto de arranque (entre 0 y N-1), calculado a partir del nombre del job. **Siempre es el mismo** para ese job. Sirve para repartir la carga cuando hay muchos jobs.
- `H/1` es lo mismo que `*` (con "cada 1" no hay nada que elegir).

| Expresión | Qué hace |
|---|---|
| `* * * * *` | cada minuto (ideal para la demo) |
| `H/2 * * * *` | cada 2 minutos (lo que usamos) |
| `H/5 * * * *` | cada 5 minutos |
| `0 * * * *` | cada hora, en punto |
| `H * * * *` | cada hora, en un minuto fijo que elige Jenkins |
| `* 1 * * *` | ⚠️ cada minuto, pero solo entre la 1:00 y la 1:59 de la mañana |
| `H 9 * * 1-5` | una vez por día a las 9 (en un minuto que elige Jenkins), de lunes a viernes |

### Un solo Jenkins

- El Jenkinsfile **no crea el job**. Una vez por cada Jenkins hay que:
  1. Crear el job ("New Item → Pipeline").
  2. Configurarlo como "Pipeline script from SCM": URL del repo, rama y Script Path `entregable_4/Jenkinsfile`.
  3. Correrlo una vez a mano.
- Después, el trigger y las etapas salen del Jenkinsfile, sin tocar la interfaz.
- **Alcanza con un solo Jenkins** (por ejemplo el de Juan). Los compañeros solo hacen `git push`, y ese Jenkins detecta los cambios sin importar quién los hizo.
- Jenkins **no es un ambiente**: es el que **lleva** la app a cada ambiente.

### Dónde corre cada cosa

- **GitHub** solo guarda el código, incluido el Jenkinsfile.
- **Jenkins** (en la máquina local) se baja el código y ejecuta todo: build, tests, package y deploy.
- Las pruebas corriendo *en* GitHub sería **GitHub Actions**, que no aplica porque el enunciado pide Jenkins. Se puede mencionar en el PDF como alternativa evaluada.

### Maven: fases y `-B`

```
validate → compile → test → package → verify → install → deploy
```

- Pedir una fase ejecuta también todas las anteriores. Por eso `package` vuelve a correr los tests si no se usa `-DskipTests`.
- `-B` (batch mode): sin barras de progreso ni preguntas, así el log de Jenkins queda limpio.

---

## Ambientes y deploy

### Qué es un ambiente simulado

Todo corre **en la misma máquina**. Cada ambiente es **la misma app (el mismo `.jar`), copiada en una carpeta distinta y corriendo en un puerto distinto**.

```
                    ┌──────────────────────┐
                    │  Jenkins (uno solo)  │
                    │   localhost:8080     │
                    └──────────┬───────────┘
                               │ copia el .jar y lo levanta
                ┌──────────────┴──────────────┐
                ▼                             ▼
   ┌─────────────────────────┐   ┌─────────────────────────┐
   │ Ambiente UAT            │   │ Ambiente Producción     │
   │ carpeta ~/ambientes/uat │   │ carpeta ~/ambientes/prod│
   │ app en localhost:8082   │   │ app en localhost:8083   │
   └─────────────────────────┘   └─────────────────────────┘
```

| Ambiente | Carpeta | Puerto | Quién lo levanta |
|---|---|---|---|
| Jenkins (no es un ambiente) | — | 8080 | — |
| Desarrollo | el repo en cada máquina | 8081 | cada uno, desde IntelliJ o `./mvnw spring-boot:run` |
| UAT | `~/ambientes/uat/` | 8082 | Jenkins, automáticamente |
| Producción | `~/ambientes/prod/` | 8083 | Jenkins, después de la aprobación |

En la vida real, UAT y producción serían servidores separados. Acá se simulan con carpetas y puertos, como permite el enunciado.

### UAT = User Acceptance Testing

Es el ambiente de "testing" del proyecto: ahí **personas** prueban la app **a mano**, como lo haría el usuario.

| | Pruebas automáticas | UAT |
|---|---|---|
| Quién las hace | Jenkins, solo | Personas (el grupo) |
| Dónde | Dentro del pipeline (etapa `Test`), no en un ambiente | En la app levantada en `localhost:8082` |
| Qué verifican | Que el código funciona (unitarias + integración) | Que la app sirve para el usuario |
| Si fallan | El pipeline se corta solo | Alguien aprieta "Abortar" en Jenkins |

En el PDF y la defensa, llamarlo **UAT**, que es el término del enunciado.

### Cómo se cambia el puerto (sin tocar el código)

El `.jar` es **uno solo**. Jenkins le pasa el puerto al arrancarlo, y lo que va por línea de comandos tiene prioridad sobre `application.properties`:

```bash
java -jar app.jar --server.port=8082   # UAT
java -jar app.jar --server.port=8083   # Producción
```

**Buena práctica para el PDF:** se construye una sola vez y el mismo artefacto se promueve entre ambientes. Lo que se aprobó en UAT es exactamente lo que llega a producción.

### Qué hace cada deploy

1. **Bajar** la versión anterior (usando el PID guardado en `app.pid`).
2. **Copiar** el `.jar` nuevo a la carpeta del ambiente.
3. **Levantarlo** en segundo plano con el puerto del ambiente y guardar su PID.
4. **Verificar** que levantó, consultando `/actuator/health`.

Ejemplo de referencia para Mac/Linux:

```groovy
stage('Deploy UAT') {
    steps {
        sh '''
            DIR="$HOME/ambientes/uat"
            mkdir -p "$DIR"

            # 1. bajar la versión anterior (si había una corriendo)
            if [ -f "$DIR/app.pid" ]; then
                kill $(cat "$DIR/app.pid") || true
                sleep 3
            fi

            # 2. copiar el jar nuevo
            cp entregable_4/target/mini-web-0.0.1-SNAPSHOT.jar "$DIR/app.jar"

            # 3. levantarlo en segundo plano y guardar su PID
            cd "$DIR"
            JENKINS_NODE_COOKIE=dontKillMe nohup java -jar app.jar --server.port=8082 > app.log 2>&1 &
            echo $! > app.pid

            # 4. esperar hasta que responda (máx. ~60 segundos)
            for i in $(seq 1 30); do
                curl -sf http://localhost:8082/actuator/health && exit 0
                sleep 2
            done
            echo "La app no levantó en UAT" && exit 1
        '''
    }
}
```

- `app.pid`: número del proceso, para poder bajarlo en el próximo deploy.
- `app.log`: salida de la app, para ver errores.
- **`JENKINS_NODE_COOKIE=dontKillMe`**: sin esto, Jenkins mata la app apenas termina el build.
- ⚠️ Si Jenkins corre **dentro de Docker** o en **Windows**, esto cambia: en Docker, las carpetas y los puertos quedan dentro del contenedor; en Windows, se usa `bat` en lugar de `sh`. **Pendiente confirmar cómo está instalado Jenkins.**

### Quién decide cada paso

```
git push ─► Build ─► Tests ─► Package ─► Deploy UAT ─► ⏸ espera ─► Deploy Producción
  (vos)      ╰──────────── automático ────────────╯   (un humano    (automático,
                                                       aprueba en    después de
                                                       Jenkins)      aprobar)
```

| Paso | ¿Quién lo decide? |
|---|---|
| Desarrollo → UAT | **Automático**, si pasan los tests |
| UAT → Producción | **Una persona**, aprobando en Jenkins |
| Hacer el despliegue en sí | **Siempre Jenkins**; nunca se copian archivos a mano |

- Si **fallan los tests**, el pipeline se corta y no se despliega nada.
- Si en UAT se encuentra un error, se aprieta **"Abortar"**: producción no se toca, se corrige, se hace un push nuevo y el ciclo arranca de nuevo.

Etapa de aprobación, de referencia:

```groovy
stage('Aprobación') {
    steps {
        timeout(time: 30, unit: 'MINUTES') {
            input message: '¿Las pruebas en UAT (localhost:8082) están OK? ¿Pasar a Producción?',
                  ok: 'Aprobar'
        }
    }
}
```

El `timeout` aborta el pipeline si nadie responde en 30 minutos, para que no quede colgado.

---

## Prioridad sugerida

1. ~~Disparo automático (pollSCM)~~ ✅ y ~~etapa Package~~ ✅.
2. Deploy UAT → Aprobación → Deploy Producción (confirmar primero cómo está instalado Jenkins).
3. App con dos módulos y sus tests (unitarias + integración), y la etapa de integración en el pipeline.
4. README y PDF (incluido el registro de errores del pipeline).
5. Ensayo de la demo y armado del zip.
