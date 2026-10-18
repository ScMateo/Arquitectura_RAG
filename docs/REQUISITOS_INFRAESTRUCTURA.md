# Requisitos Técnicos y de Infraestructura

Continuando con la planeación del proyecto, se definen los requisitos técnicos y de infraestructura necesarios para el procesamiento y el almacenamiento de la información. Esta definición complementa la selección de herramientas realizada previamente y establece las condiciones bajo las cuales dichas herramientas se ejecutarán, se almacenarán los datos y se organizará el entorno de trabajo.

El propósito de este documento es determinar, para cada dimensión de la infraestructura, las alternativas disponibles y la decisión adoptada, de manera que toda elección sea trazable a un requisito funcional o a una restricción del proyecto.

## 1. Criterios de Evaluación

Los criterios que rigen el análisis se derivan de las historias de usuario y de las restricciones generales del proyecto.

| Criterio | Descripción | Origen |
|---|---|---|
| C1 | Disponibilidad y persistencia de la información recuperada y del contexto conversacional | HU-07, HU-10 |
| C2 | Trazabilidad entre la información recuperada y su fuente de origen | HU-10 |
| C3 | Ejecución sobre hardware sin aceleración por GPU (procesamiento en CPU) | Restricción de hardware |
| C4 | Presupuesto limitado, con preferencia por herramientas gratuitas y de software libre | Restricción de presupuesto |
| C5 | Reproducibilidad del entorno: ejecución idéntica en cualquier máquina | Reproducibilidad del experimento |
| C6 | Mantenibilidad: modularidad y bajo acoplamiento entre componentes | Reglas del proyecto |
| C7 | Adaptabilidad: posibilidad de evolucionar hacia un despliegue en red | Escalabilidad futura |

## 2. Análisis por Dimensión

### 2.1 Modelo de Despliegue

El modelo de despliegue determina la forma en que el sistema se pone en ejecución. Se consideran las siguientes alternativas:

| Modelo | Reproducibilidad | Complejidad | Costo | Decisión |
|---|---|---|---|---|
| Instalación directa (venv + npm) | Baja | Baja | Gratuito | Fase de desarrollo |
| **Docker + Docker Compose** | Alta | Media | Gratuito | Seleccionado |
| Servidor en la nube (máquina virtual) | Alta | Media-alta | De pago | Evolución futura |
| Plataforma gestionada (Hugging Face Spaces) | Media | Media | Gratuito (CPU) | Alternativa |

Se selecciona **Docker + Docker Compose** como modelo de despliegue objetivo. Los argumentos son los siguientes:

- Garantiza que el sistema se ejecute de manera idéntica en cualquier máquina, al definir el entorno mediante contenedores (criterio C5).
- No implica costo de licenciamiento ni de infraestructura (criterio C4).
- La definición del despliegue mediante un archivo de composición permite trasladar posteriormente el sistema a un servidor en la nube sin modificar su estructura (criterio C7).

La instalación directa se mantiene como entorno de desarrollo por su menor complejidad, mientras que el servidor en la nube se documenta como evolución para una etapa posterior en la que el sistema deba ser accesible a múltiples usuarios.

### 2.2 Arquitectura de Servicios

La arquitectura de servicios define cómo se organizan y comunican los componentes del sistema. Se consideran las siguientes alternativas:

| Arquitectura | Acoplamiento | Complejidad operativa | Decisión |
|---|---|---|---|
| Monolito (proceso único) | Alto | Baja | Descartada |
| Microservicios | Bajo | Alta | Descartada |
| **Monolito modular + servicio vectorial** | Bajo | Media | Seleccionada |

Se selecciona la arquitectura de **monolito modular con el servicio vectorial separado**. Los argumentos son los siguientes:

- La lógica de negocio se organiza en módulos desacoplados dentro de un único proceso (servidor), conforme a los principios de arquitectura limpia (criterio C6).
- La base de datos vectorial seleccionada (Qdrant) es, por su naturaleza, un servicio independiente, por lo que el sistema se compone de tres unidades: el cliente, el servidor y el servicio vectorial.
- La arquitectura de microservicios se descarta por resultar desproporcionada para la escala del proyecto y por introducir complejidad operativa sin una ventaja equivalente (criterios C4 y C6).

Esta organización mantiene un acoplamiento bajo y, al distribuir los componentes en unidades separadas, facilita la medición del comportamiento del sistema, lo que es coherente con la adaptabilidad a un enfoque de red (criterio C7).

### 2.3 Modelo de Procesamiento

El procesamiento comprende la generación de embeddings, la búsqueda vectorial y la generación de respuestas. Se distingue entre el procesamiento por lotes (ingesta de documentos) y el procesamiento en tiempo real (consulta).

| Etapa | Lugar de ejecución | Justificación |
|---|---|---|
| Generación de embeddings (ingesta y consulta) | CPU local | Criterios C3 y C4 |
| Búsqueda vectorial | Servicio Qdrant (local) | Decisión de herramienta |
| Generación de respuestas | API de Gemini (internet) | Decisión de herramienta |

Para la generación de embeddings se consideraron tres alternativas: el procesamiento en CPU local, el procesamiento en GPU y el uso de una API de embeddings en la nube.

| Opción | Decisión | Motivo |
|---|---|---|
| **CPU local** | Seleccionada | Compatible con el hardware disponible (C3) y sin costo (C4) |
| GPU local | Descartada | No se dispone de aceleración por GPU |
| API de embeddings en la nube | Descartada | Implica un costo recurrente incompatible con C4 |

El procesamiento se organiza en dos modalidades: una modalidad por lotes, en la que los documentos se procesan y se indexan una única vez durante la ingesta, y una modalidad en tiempo real, en la que cada consulta desencadena la generación del embedding de la pregunta, la búsqueda y la generación de la respuesta.

### 2.4 Almacenamiento de Datos Crudos y Procesados

La información del sistema se presenta en distintos estados: los datos crudos provenientes de la fuente, los datos procesados y el índice vectorial.

| Tipo de dato | Ubicación | Mecanismo de almacenamiento |
|---|---|---|
| Datos crudos (CvLAC) | `data/raw` | Sistema de archivos (CSV) |
| Datos procesados (normalizados) | `data/processed` | Sistema de archivos (CSV) |
| Índice vectorial y metadatos | Servicio Qdrant | Persistencia propia de Qdrant |

Se consideraron dos alternativas para el almacenamiento de los datos estructurados: el sistema de archivos y una base de datos relacional.

| Opción | Decisión | Motivo |
|---|---|---|
| **Sistema de archivos (CSV)** | Seleccionada | Suficiente para el volumen y la estructura de los datos; simple y transparente (C4, C6) |
| Base de datos relacional | Descartada | Introduce una complejidad adicional no requerida; los metadatos se gestionan como payload en Qdrant |

La trazabilidad de la información (criterio C2) se resuelve mediante los metadatos asociados a cada fragmento en el índice vectorial, que vinculan cada elemento con su investigador y su sección de origen, sin necesidad de una base de datos relacional adicional.

### 2.5 Almacenamiento Vectorial

La base de datos vectorial Qdrant puede ejecutarse de distintas maneras. Se consideran las siguientes alternativas:

| Modo de ejecución | Persistencia | Integración con el despliegue | Decisión |
|---|---|---|---|
| Proceso nativo instalado en el host | Sí | Baja | Alternativa |
| **Contenedor (Docker)** | Sí | Alta | Seleccionado |
| Modo embebido (en proceso) | Limitada | Alta | Fase de desarrollo |

Se selecciona la ejecución de Qdrant en un **contenedor Docker**, por su coherencia con el modelo de despliegue seleccionado (criterio C5) y por su facilidad para definir la persistencia mediante volúmenes. El modo embebido se reserva para las pruebas durante el desarrollo, mientras que el proceso nativo se descarta por su menor integración con el entorno reproducido por contenedores.

### 2.6 Persistencia del Contexto Conversacional

El requisito HU-07 exige conservar el contexto de las últimas interacciones. Se consideran las siguientes alternativas para su almacenamiento:

| Mecanismo | Persistencia entre ejecuciones | Complejidad | Decisión |
|---|---|---|---|
| **En memoria por sesión** | No | Baja | Seleccionado |
| Base de datos relacional (SQLite) | Sí | Media | Evolución futura |
| Redis | Sí | Media | Evolución futura |

Se selecciona el almacenamiento **en memoria por sesión**, por su simplicidad y por cumplir el requisito de contexto temporal (criterio C1) sin introducir infraestructura adicional (criterio C4). La persistencia en SQLite o Redis se documenta como evolución en caso de requerirse conservar el historial entre ejecuciones o entre sesiones.

### 2.7 Entornos y Gestión del Almacenamiento

Se definen dos entornos de trabajo, el entorno de desarrollo basado en la instalación directa de las dependencias y el entorno reproducible basado en contenedores. Esta separación permite iterar rápidamente durante el desarrollo y al mismo tiempo, disponer de un entorno estable y reproducible para la verificación y la demostración del sistema.

La persistencia del índice vectorial se gestiona mediante volúmenes definidos en el archivo de composición, lo que evita la pérdida de información al reconstruir los contenedores.

## 3. Resumen de las Decisiones

| Dimensión | Decisión adoptada | Criterios atendidos |
|---|---|---|
| Modelo de despliegue | Docker + Docker Compose | C4, C5, C7 |
| Arquitectura de servicios | Monolito modular + servicio vectorial | C6, C7 |
| Modelo de procesamiento | CPU local + Qdrant + API Gemini | C3, C4 |
| Datos crudos y procesados | Sistema de archivos (CSV) | C2, C4, C6 |
| Almacenamiento vectorial | Qdrant en contenedor Docker | C5 |
| Contexto conversacional | En memoria por sesión | C1, C4 |
| Entornos | Desarrollo (directo) y reproducible (Docker) | C5, C6 |