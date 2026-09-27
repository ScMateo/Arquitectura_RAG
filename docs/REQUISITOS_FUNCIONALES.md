# Requisitos funcionales

Para la identificación, planeación y análisis de los requisitos funcionales esenciales para el desarrollo del proyecto, se tienen en cuenta las necesidades de los usuarios que actualmente hacen uso del sistema de búsqueda de la plataforma CvLAC. A partir de estas necesidades, se plantean diez historias de usuario, cada una de las cuales representa una necesidad identificada y define una funcionalidad que será considerada para su implementación y posterior validación dentro del prototipo desarrollado.

## Épicas del proyecto

Teniendo en cuenta que el desarrollo del proyecto y las funcionalidades a implementar están enfocadas en diferentes áreas y contextos dentro del aplicativo, se establecen las siguientes cuatro categorías que serán llamadas épicas en las cuales se contendrán las diferentes historias de usuario y tareas a realizar.

| Identificador épica | Descripción de historias |
|---|---|
| HE.001 | Interfaz y estilo |
| HE.002 | Funcionalidad |
| HE.003 | Consultas |
| HE.004 | Razonamiento |

# Historias de usuario

## Historia 01 – Experiencia de usuario

**Yo como:** Investigador.  
**Quiero:** una interfaz de uso simple y con buen aspecto visual.  
**Para:** que la búsqueda de información sea fácil e intuitiva.

### Criterios de aceptación

1. Al ingresar al buscador, el usuario debe poder identificar visualmente el campo destinado a realizar consultas y los elementos principales de la interfaz.
2. El usuario debe poder realizar una consulta sin requerir instrucciones externas para identificar el mecanismo básico de búsqueda.
3. Se realizará una encuesta de satisfacción a los usuarios de prueba y al menos el 75 % deberá valorar favorablemente la facilidad de uso y presentación visual de la interfaz.

## Historia 02 – Pocos ítems

**Yo como:** Investigador.  
**Quiero:** poder buscar la información relacionada a una o más hojas de vida a través de un único campo.  
**Para:** que la búsqueda sea más fácil y rápida, sin necesidad de llenar múltiples filtros o etiquetas.

### Criterios de aceptación

1. La interfaz debe disponer de un único campo destinado al ingreso de la consulta.
2. El usuario debe poder introducir consultas relacionadas con diferentes atributos de las hojas de vida, como nombre, institución, formación o área de investigación.
3. El sistema debe generar una respuesta relacionada con los términos y condiciones expresados en la consulta.
4. Cuando la consulta corresponda a información disponible en la base de datos, la respuesta debe contener información relacionada con dicha información registrada.

## Historia 03 – Link de Hoja de vida

**Yo como:** Investigador.  
**Quiero:** que se entregue el link de las hojas de vida referenciadas.  
**Para:** poder observarlas y analizarlas de forma completa.

### Criterios de aceptación

1. Al solicitar la información de un investigador se entrega al final también el enlace de la hoja de vida de donde se referenció.
2. El enlace debe ser completo y listo para copiar y pegar.
3. Al presionar el enlace se debe redireccionar directamente a la hoja de vida.
4. La redirección debe ser a la página correcta, no a ninguna otra.

## Historia 04 – Consulta específica (sobre un investigador)

**Yo como:** Investigador.  
**Quiero:** consultar información específica de la hoja de vida de un investigador a partir de una pregunta o solicitud.  
**Para:** obtener únicamente la información relevante para mi investigación, de acuerdo con los aspectos solicitados.

### Criterios de aceptación

1. El usuario debe poder realizar una consulta utilizando el nombre de un investigador y uno o varios aspectos específicos de su hoja de vida.
2. El sistema debe identificar al investigador mencionado y recuperar información relacionada con la solicitud realizada.
3. La respuesta debe contener información correspondiente a los aspectos solicitados por el usuario.
4. Cuando el usuario establezca restricciones o condiciones en la consulta, estas deben ser consideradas en la generación de la respuesta.
5. Si no existe información suficiente para responder la consulta, el sistema debe indicarlo explícitamente en lugar de generar información no encontrada en la fuente.

## Historia 05 – Consulta general (sobre varios investigadores)

**Yo como:** Investigador.  
**Quiero:** poder consultar la información de toda la base de datos de acuerdo a temáticas o alguna otra instrucción.  
**Para:** solo recibir como respuesta aquella información de interés o de utilidad para mi investigación.

### Criterios de aceptación

1. El usuario puede especificar la información precisa o generalizada que necesita de toda la base de datos.
2. La respuesta que entregue el sistema debe haber tenido en cuenta las restricciones o filtrados solicitados.
3. La respuesta debe contener únicamente información relacionada con los criterios establecidos en la consulta y presentar los investigadores identificados de manera diferenciada.

## Historia 06 – Adaptación frente a las preguntas

**Yo como:** Investigador.  
**Quiero:** poder solicitar información de forma libre y sin una estructura preestablecida.  
**Para:** cuando se necesita información de acuerdo a temáticas, temas específicos, temas generales, variados, de tal forma que el sistema se adapte a las preguntas no convencionales.

### Criterios de aceptación

1. El sistema se debe adaptar a la pregunta realizada, si es que le piden información de un investigador en específico o si por el contrario la pregunta es de alguna cualidad en general, como profesión, temas trabajados, formación, etc.
2. La respuesta debe ser coherente y relacionada a la pregunta.
3. En caso de que la pregunta tenga en cuenta uno o más investigadores, o también uno o más campos, la respuesta debe ser coherente con lo solicitado.

## Historia 07 – Análisis de información

**Yo como:** Investigador.  
**Quiero:** ayuda con el análisis de la información de la respuesta.  
**Para:** comprender de mejor manera lo obtenido, salir de dudas sobre alguno de los incisos, frases u oración.

### Criterios de aceptación

1. Las respuestas de las preguntas deben estar organizadas y legibles.
2. Permitir realizar alguna pregunta sobre la información presentada.
3. Las preguntas y dudas deben ser respondidas de forma correcta, argumentadas y, de ser necesario, explicadas con la profundidad que solicite el usuario.
4. El sistema debe guardar en su memoria temporal el contexto de por lo menos las últimas 5 respuestas y preguntas realizadas.

## Historia 08 – Resumen

**Yo como:** Investigador.  
**Quiero:** que el sistema me brinde un resumen de la información encontrada.  
**Para:** poder analizar la información relevante, en caso de obtener una respuesta demasiado extensa.

### Criterios de aceptación

1. El usuario puede solicitar que se le proporcione un resumen de una hoja de vida en específico o de una respuesta.
2. El resumen debe conservar los datos principales necesarios para comprender la información solicitada y no debe introducir información que no esté presente en la respuesta o fuente resumida.
3. El resumen se debe adaptar a la solicitud e indicaciones del usuario.

## Historia 09 – Razonar acrónimos o etiquetas

**Yo como:** Investigador.  
**Quiero:** que el sistema pueda identificar y relacionar acrónimos, abreviaturas y diferentes denominaciones utilizadas para referirse a una misma entidad, investigador, tema o institución dentro de las hojas de vida.  
**Para:** recuperar la información relacionada aunque la consulta y los registros de CvLAC utilicen diferentes formas de nombrarla.

### Criterios de aceptación

1. Cuando una entidad aparezca registrada mediante un nombre completo y una abreviatura reconocible, el sistema debe poder relacionar ambas denominaciones durante la recuperación de información.
2. Una consulta realizada utilizando un acrónimo o abreviatura debe recuperar información relacionada cuando dicha información esté registrada utilizando su denominación equivalente.
3. El sistema no debe considerar como equivalentes dos términos cuando no exista evidencia suficiente de que hacen referencia a la misma entidad o concepto.
4. La respuesta generada debe conservar la denominación utilizada en la fuente cuando esta sea relevante para identificar correctamente la información.
5. La capacidad de relacionar denominaciones diferentes debe ser evaluada mediante consultas de prueba previamente definidas.

## Historia 10 – Referenciación de la información

**Yo como:** Investigador.  
**Quiero:** conocer de qué hoja de vida proviene la información utilizada para generar una respuesta.  
**Para:** poder verificar y analizar la información obtenida.

### Criterios de aceptación

1. La respuesta debe indicar las hojas de vida utilizadas como fuente de información.
2. Cada fuente debe estar asociada con el investigador correspondiente.
3. El usuario debe poder acceder a la hoja de vida utilizada como referencia.
4. Las fuentes mostradas deben corresponder con la información empleada para generar la respuesta.

# Matriz de trazabilidad

A continuación se define y establece la matriz de trazabilidad, con el fin de presentar la relación e importancia entre las épicas, historias de usuario, funcionalidades, información requerida y actividades del proyecto.

| Épica | Historia de usuario | Característica / Funcionalidad | Razón / Resultado | Información requerida | Actividades |
|---|---|---|---|---|---|
| **HE.001** | **HU-01**<br><br>**Yo como:** Investigador.<br>**Quiero:** una interfaz de uso simple y con buen aspecto visual.<br>**Para:** que la búsqueda de información sea fácil e intuitiva. | Interfaz de consulta, campo de búsqueda, presentación organizada de resultados y navegación hacia fuentes. | Búsqueda de información fácil e intuitiva. | — | - Construcción de interfaz<br>- Selección de usuarios<br>- Implementación controlada de la arquitectura<br>- Recopilación de percepciones |
| **HE.001** | **HU-02**<br><br>**Yo como:** Investigador.<br>**Quiero:** poder buscar la información relacionada a una o más hojas de vida a través de un único campo.<br>**Para:** que la búsqueda sea más fácil y rápida, sin necesidad de llenar múltiples filtros o etiquetas. | Mecanismo de consulta mediante un único campo e información consolidada de las hojas de vida. | Búsqueda más fácil y rápida sin múltiples filtros o etiquetas. | Información consolidada de las hojas de vida y mecanismo de consulta mediante un único campo. | - Definición y documentación de los requisitos funcionales<br>- Análisis de requerimientos técnicos y funcionales<br>- Diseño detallado de la arquitectura modular del sistema<br>- Construcción de interfaz |
| **HE.002** | **HU-03**<br><br>**Yo como:** Investigador.<br>**Quiero:** que se entregue el link de las hojas de vida referenciadas.<br>**Para:** poder observarlas y analizarlas de forma completa. | Entrega de enlaces correspondientes a las hojas de vida referenciadas. | Permitir observar y analizar las hojas de vida de forma completa. | URL asociada a cada hoja de vida de CvLAC. | - Caracterización y clasificación de la información<br>- Desarrollo de los componentes para la extracción y preprocesamiento<br>- Implementación del mecanismo de generación |
| **HE.002** | **HU-08**<br><br>**Yo como:** Investigador.<br>**Quiero:** que el sistema me brinde un resumen de la información encontrada.<br>**Para:** poder analizar la información relevante, en caso de obtener una respuesta demasiado extensa. | Generación de resúmenes de la información recuperada. | Facilitar el análisis de información relevante cuando la respuesta sea extensa. | Contenido recuperado de una o varias hojas de vida y respuestas generadas. | - Integración de los LLM<br>- Implementación controlada de la arquitectura<br>- Recopilación de percepciones |
| **HE.002** | **HU-10**<br><br>**Yo como:** Investigador.<br>**Quiero:** conocer de qué hoja de vida proviene la información utilizada para generar una respuesta.<br>**Para:** poder verificar y analizar la información obtenida. | Referenciación de las fuentes utilizadas para generar la respuesta. | Permitir verificar y analizar la información obtenida. | URL, identificación de fuente y relación entre información recuperada y hoja de vida. | - Caracterización y clasificación de la información<br>- Desarrollo de los componentes para la extracción y preprocesamiento<br>- Implementación del mecanismo de generación<br>- Estructuración de consultas de prueba<br>- Análisis estadístico de resultados |
| **HE.003** | **HU-04**<br><br>**Yo como:** Investigador.<br>**Quiero:** poder consultar la información de las hojas de vida.<br>**Para:** solo recibir como respuesta aquella información de interés o de utilidad para mi investigación. | Consulta y recuperación de información específica de las hojas de vida. | Recibir únicamente información de interés o utilidad para la investigación. | Identificación, formación, experiencia, proyectos, producción, reconocimientos y demás información del investigador. | - Caracterización y clasificación de la información<br>- Definición y documentación de los requisitos funcionales<br>- Definición de la estrategia de segmentación y modelo de embeddings<br>- Diseño detallado de la arquitectura modular del sistema<br>- Desarrollo de los componentes para la extracción y preprocesamiento<br>- Implementación de base de datos vectorial<br>- Integración de los LLM |
| **HE.003** | **HU-05**<br><br>**Yo como:** Investigador.<br>**Quiero:** poder consultar la información de toda la base de datos de acuerdo a temáticas o alguna otra instrucción.<br>**Para:** solo recibir como respuesta aquella información de interés o de utilidad para mi investigación. | Consulta y recuperación de información de múltiples hojas de vida de acuerdo con temáticas o instrucciones. | Obtener únicamente información relevante para la investigación. | Información de múltiples hojas de vida: áreas, formación, experiencia, proyectos y producción. | - Caracterización y clasificación de la información<br>- Definición y documentación de los requisitos funcionales<br>- Definición de la estrategia de segmentación y modelo de embeddings<br>- Diseño detallado de la arquitectura modular del sistema<br>- Desarrollo de los componentes para la extracción y preprocesamiento<br>- Implementación de base de datos vectorial<br>- Integración de los LLM |
| **HE.004** | **HU-06**<br><br>**Yo como:** Investigador.<br>**Quiero:** poder solicitar información de forma libre y sin una estructura preestablecida.<br>**Para:** cuando se necesita información de acuerdo a temáticas, temas específicos, temas generales, variados, de tal forma que el sistema se adapte a las preguntas no convencionales. | Interpretación y atención de consultas realizadas mediante lenguaje natural y sin estructura preestablecida. | Adaptarse a preguntas no convencionales sobre diferentes temáticas. | Información de las diferentes categorías del corpus y relaciones semánticas necesarias para interpretar lenguaje natural. | - Caracterización y clasificación de la información<br>- Definición y documentación de los requisitos funcionales<br>- Análisis de requerimientos técnicos y funcionales<br>- Definición de la estrategia de segmentación y modelo de embeddings<br>- Definición de la estrategia de normalización<br>- Diseño detallado de la arquitectura modular del sistema<br>- Desarrollo de los componentes para la extracción y preprocesamiento<br>- Implementación de base de datos vectorial<br>- Integración de los LLM |
| **HE.004** | **HU-07**<br><br>**Yo como:** Investigador.<br>**Quiero:** ayuda con el análisis de la información de la respuesta.<br>**Para:** comprender de mejor manera lo obtenido, salir de dudas sobre alguno de los incisos, frases u oración. | Gestión del contexto conversacional y análisis de la información presentada. | Comprender mejor la información obtenida y resolver dudas sobre la respuesta. | Información recuperada, historial conversacional y contexto de interacciones anteriores. | - Diseño del mecanismo de gestión del contexto conversacional<br>- Integración de los LLM<br>- Implementación del manejo del contexto conversacional<br>- Implementación controlada de la arquitectura |
| **HE.004** | **HU-09**<br><br>**Yo como:** Investigador.<br>**Quiero:** un sistema que razone y relacione las etiquetas, acrónimos y abreviaturas.<br>**Para:** que no haya pérdida de información al momento de recibir la respuesta de una pregunta. | Identificación y relación de etiquetas, acrónimos, abreviaturas y variantes de escritura. | Evitar pérdida de información al realizar consultas con diferentes denominaciones. | Nombres, abreviaturas, acrónimos y variantes de escritura presentes en CvLAC. | - Definición de la estrategia de normalización<br>- Desarrollo de los componentes para la extracción y preprocesamiento<br>- Integración de los LLM |

# Consultas de prueba

Teniendo en cuenta la finalidad actual del buscador integrado en CvLAC y el tipo de búsquedas generales que se realizan dentro de la plataforma se proponen las siguientes consultas para la prueba y verificación de funcionalidad del proyecto:

## Consultas puntuales

1. ¿Cuál es la formación académica de [investigador]?
2. ¿Cuáles son las líneas de investigación de [investigador]?
3. ¿Qué proyectos de investigación ha realizado [investigador]?
4. ¿Cuántos artículos científicos tiene registrados [investigador]?
5. ¿Qué reconocimientos ha recibido [investigador]?

## Consultas generales

1. ¿Qué investigadores trabajan en inteligencia artificial?
2. ¿Qué investigadores tienen experiencia en desarrollo de software?
3. ¿Qué investigadores trabajan en salud pública?
4. ¿Qué investigadores han trabajado en aprendizaje automático?
5. ¿Qué investigadores tienen experiencia en análisis de datos?

## Consultas relacionales

1. ¿Qué investigadores que trabajan en inteligencia artificial también tienen experiencia en procesamiento de lenguaje natural?
2. ¿Qué investigadores han publicado sobre aprendizaje automático y además tienen proyectos relacionados con el tema?
3. ¿Qué investigadores tienen líneas de investigación relacionadas con energías renovables y han participado en proyectos sobre el tema?
4. ¿Qué investigadores tienen publicaciones relacionadas con visión por computador y experiencia en proyectos de inteligencia artificial?
5. ¿Qué investigadores trabajan en un área determinada y tienen formación doctoral relacionada con ella?

## Consultas comparativas

1. ¿Cuál de estos investigadores tiene mayor cantidad de publicaciones relacionadas con inteligencia artificial?
2. ¿Cuál investigador tiene mayor experiencia en el área de desarrollo de software?
3. ¿Qué investigador presenta una trayectoria más cercana al área de inteligencia artificial, considerando su formación, líneas de investigación y producción científica?
4. Entre estos investigadores, ¿cuál tiene mayor experiencia en dirección de trabajos de grado relacionados con desarrollo de software?
5. ¿Qué investigador tiene el perfil más relacionado con inteligencia artificial y por qué?
