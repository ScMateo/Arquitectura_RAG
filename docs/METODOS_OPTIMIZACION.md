# Estudio y Selección de Métodos para la Optimización del Rendimiento de los LLM

En el siguiente documento se realiza el estudio y la selección de los métodos orientados a optimizar el rendimiento del modelo de lenguaje empleado para la generación de respuestas. La optimización se aborda en cuatro dimensiones: la latencia de respuesta, el costo de uso, la fiabilidad y la calidad de la generación.

El propósito de este documento es identificar, para cada dimensión, las alternativas disponibles, compararlas frente a criterios derivados de los requerimientos del proyecto y adoptar el método más adecuado, distinguiendo entre los métodos que se aplican en la etapa actual y los que se documentan como evolución.

## 1. Criterios de Evaluación

| Criterio | Descripción |
|---|---|
| L1 | Reducción de la latencia de respuesta percibida por el usuario |
| L2 | Reducción del costo de uso de la API |
| L3 | Mejora de la fiabilidad frente a fallos o saturaciones del servicio |
| L4 | Mejora de la calidad de la generación |
| L5 | Complejidad de implementación y mantenibilidad |

## 2. Optimización de la Latencia

### 2.1 Generación Incremental (Streaming)

La generación de la respuesta puede entregarse de manera completa o de manera incremental, a medida que el modelo produce los tokens.

| Método | L1 | L5 | Decisión |
|---|---|---|---|
| Respuesta completa (bloqueante) | Baja | Baja | Descartado |
| **Generación incremental (streaming)** | Alta | Media | Seleccionado |

Se selecciona la **generación incremental**. Este método entrega los primeros fragmentos de la respuesta antes de que el modelo concluya la generación completa, lo que reduce de forma significativa el tiempo de espera percibido por el usuario (criterio L1). Además, al permitir medir el tiempo transcurrido hasta la primera porción de respuesta, habilita la evaluación del desempeño del sistema desde una perspectiva de red, coherente con la adaptabilidad del proyecto. Su complejidad de implementación es moderada (criterio L5).

### 2.2 Reducción del Contexto

El volumen de información enviado al modelo en cada solicitud incide directamente en la latencia, dado que un mayor número de tokens de entrada prolonga el tiempo de procesamiento.

| Método | L1 | L2 | L4 | Decisión |
|---|---|---|---|---|
| Contexto completo (todos los fragmentos) | Baja | Baja | Media | Descartado |
| **Contexto limitado a los fragmentos más relevantes** | Alta | Alta | Adecuada | Seleccionado |

Se selecciona la **limitación del contexto a los fragmentos más relevantes**, en coherencia con el mecanismo de re-ranking definido en etapas previas. Al reducir el número de fragmentos enviados al modelo se acorta el tiempo de procesamiento (criterio L1) y se disminuye el costo de la solicitud (criterio L2), sin comprometer la calidad de la respuesta, dado que únicamente se incluye la información pertinente (criterio L4).

## 3. Optimización del Costo

### 3.1 Caché de Contexto (Prefijo del Sistema)

El modelo de lenguaje se invoca de manera reiterada con un prefijo de sistema que permanece constante. La caché de contexto permite reutilizar el procesamiento de dicho prefijo entre solicitudes.

| Método | L1 | L2 | Decisión |
|---|---|---|---|
| Sin caché de contexto | Baja | Baja | Descartado |
| **Caché del prefijo del sistema** | Alta | Alta | Seleccionado |

Se selecciona la **caché del prefijo del sistema**. Dado que la instrucción de sistema se mantiene invariable entre solicitudes, su almacenamiento en caché evita su reprocesamiento en cada consulta, lo que reduce tanto la latencia como el costo (criterios L1 y L2). Este método no modifica la lógica de generación y se implementa en la capa de acceso al modelo de lenguaje.

### 3.2 Selección del Modelo

El costo y la velocidad de respuesta dependen del modelo seleccionado. La elección del modelo de lenguaje en su versión ligera, documentada en la selección de herramientas, constituye en sí misma un método de optimización de costo y de latencia, al ofrecer un equilibrio entre desempeño y consumo de recursos. Las versiones de mayor capacidad quedan descartadas por su mayor costo, incompatible con las restricciones del proyecto.

## 4. Optimización de la Fiabilidad

### 4.1 Reintentos con Espera Progresiva

Las respuestas del servicio pueden verse afectadas por saturaciones o errores transitorios. El reintento con espera progresiva permite recuperar la operación sin interrumpir el flujo.

| Método | L3 | Decisión |
|---|---|---|
| Sin reintentos | Baja | Descartado |
| **Reintentos con espera exponencial** | Alta | Seleccionado |

Se seleccionan los **reintentos con espera exponencial**. Ante un error transitorio, se reintenta la solicitud aumentando de manera progresiva el intervalo de espera, lo que incrementa la probabilidad de obtener respuesta sin saturar el servicio (criterio L3). Este método se limita a un número máximo de intentos para evitar demoras excesivas.

### 4.2 Límite de Tiempo y Modelo de Respaldo

Para evitar que una falla del servicio bloquee de manera indefinida la aplicación, se establece un límite de tiempo para cada solicitud y se documenta un modelo de respaldo de ejecución local.

| Método | L3 | Decisión |
|---|---|---|
| Sin límite de tiempo | Baja | Descartado |
| **Límite de tiempo (timeout)** | Alta | Seleccionado |
| **Modelo de respaldo local** | Alta | Evolución documentada |

Se selecciona el **límite de tiempo** para las solicitudes al servicio, de modo que una demora excesiva derive en una respuesta de error controlada en lugar de una espera indefinida (criterio L3). El **modelo de respaldo local** se documenta como mecanismo de contingencia, por su capacidad de mantener el servicio ante la indisponibilidad del proveedor, si bien su adopción queda sujeta a las limitaciones de procesamiento en CPU.

## 5. Optimización de la Calidad de la Generación

### 5.1 Parámetros de Generación

La calidad y la estabilidad de la respuesta dependen de los parámetros de muestreo del modelo, en particular de la temperatura. Se selecciona una **configuración diferenciada por tarea**: una temperatura reducida para la clasificación de consultas, que favorece respuestas deterministas y estables, y una temperatura moderada para la generación de respuestas, que permite una redacción natural sin sacrificar la fidelidad al contexto recuperado.

### 5.2 Salida Estructurada

La clasificación de consultas se formaliza mediante una **salida estructurada**, en la que el modelo devuelve una respuesta conforme a un esquema predefinido en lugar de texto libre. Este método mejora la confiabilidad de la clasificación (criterio L4) al eliminar la interpretación de texto libre, y se integra en la capa de acceso al modelo de lenguaje.

## 6. Resumen de las Decisiones

| Dimensión | Método seleccionado | Criterios atendidos |
|---|---|---|
| Latencia | Generación incremental (streaming) | L1 |
| Latencia | Limitación del contexto a los fragmentos relevantes | L1, L2, L4 |
| Costo | Caché del prefijo del sistema | L1, L2 |
| Costo | Modelo en versión ligera | L2 |
| Fiabilidad | Reintentos con espera exponencial | L3 |
| Fiabilidad | Límite de tiempo y respaldo local | L3 |
| Calidad | Parámetros de generación por tarea | L4 |
| Calidad | Salida estructurada en la clasificación | L4 |
