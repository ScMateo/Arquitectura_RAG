# Plan de Validación y Definición de Métricas

> **Versión:** 1.0 (borrador para revisión) | **Fecha:** 2026-10-18
> **Alcance:** prototipo del sistema RAG de consulta sobre hojas de vida CvLAC.
> Este documento define *cómo* se medirá la calidad del sistema y *qué* se medirá. No contiene resultados; estos se registrarán en un informe posterior (`INFORME_RESULTADOS.md`).

---

## 1. Objetivo y Alcance

El propósito de este documento es establecer el plan de validación del sistema de recuperación aumentada por generación (RAG) construido como alternativa al buscador tradicional de CvLAC, de modo que sea posible responder, de forma argumentada y reproducible, tres preguntas:

1. **¿El sistema es correcto y útil?** Es decir, si sus respuestas son acordes con la información de las hojas de vida y si entregan la información solicitada.
2. **¿En qué grado cumple cada historia de usuario (HU-01 a HU-10)?** Traduciendo cada criterio de aceptación a una métrica medible y a un umbral de referencia.
3. **¿Qué tan eficiente es el sistema?** En términos de latencia, tiempo a la primera respuesta y consumo de recursos (CPU y memoria).

La validación se organiza en dos momentos. Un primer momento **técnico**, que se ejecuta sobre el prototipo actual (backend, sin interfaz) y que es el objeto de este plan. Un segundo momento **con usuarios**, que requiere la interfaz web y una encuesta de satisfacción (HU-01-3); dicho momento se documenta aquí como fuera de alcance inmediato y se abordará después.

### 1.1 Alcance de esta versión

| Incluido | Excluido (fase posterior) |
|---|---|
| Evaluación automática de recuperación y generación | Encuesta de satisfacción de usuarios (HU-01-3) |
| Métricas de rendimiento (latencia y recursos) | Comparación contra el buscador actual de CvLAC |
| Cumplimiento funcional de HU-02 a HU-10 | Criterios de interfaz (HU-01, presentación de HU-03/HU-10) |
| Corpus sintético de evaluación | Corpus real de CvLAC (21 investigadores o más) |

La decisión de excluir la comparación con el buscador tradicional se adopta porque no se dispone de acceso programático ni de condiciones controladas para medirlo de forma justa. La calidad se evaluará, en cambio, contra el estado del arte de la evaluación de sistemas RAG (sección 2).

---

## 2. Marco de Referencia

La evaluación de un sistema RAG no puede reducirse a una sola cifra: se compone de dimensiones independientes que deben medirse por separado (recuperación, generación, comportamiento y eficiencia). Este plan adopta las métricas consolidadas en la literatura y las alinea con dos trabajos de referencia del mismo tipo:

- **RAGAS** (Es et al., 2023): marco de evaluación automática de sistemas RAG que define las dimensiones de fidelidad (*faithfulness*), relevancia de la respuesta y calidad del contexto.
- **Métricas clásicas de recuperación de información** (Manning et al., 2008): `Precision@K`, `Recall@K`, `MRR@K` y `nDCG@K`.
- **MTEB** (Muennighoff et al., 2023): referencia de facto para tareas de recuperación, que adopta `nDCG@10`.
- **Trabajos de referencia consultados**: Comyn Rodríguez (2025), *Sistema Multiagente basado en RAG para Asistencia en el Manejo de la Diabetes* (UPM), que evalúa con RAGAS sobre un conjunto *Ground Truth*; y Sánchez Maya (2026), *Sistema RAG para la gestión de documentos en Fintic* (UNAD), que emplea métricas de recuperación (`Precision@K`, `Recall@K`, `MRR`, `nDCG`) y de generación, además de latencia.

De estos trabajos se adoptan tres principios:

1. **Evaluación multidimensional:** recuperación y generación se miden con métricas distintas y complementarias.
2. **Verdad de referencia (*ground truth*):** sin un conjunto de respuestas/elementos de referencia no es posible medir la corrección; solo la fidelidad puede medirse sin él.
3. **Reproducibilidad:** condiciones fijas (modelo, temperatura, corpus, consultas) y repetición de mediciones.

---

## 3. Dimensiones de Evaluación

| Dimensión | Pregunta que responde | Sección |
|---|---|---|
| D1. Recuperación | ¿El sistema encuentra los fragmentos correctos? | 6.1 |
| D2. Generación | ¿La respuesta es fiel, pertinente y correcta? | 6.2 |
| D3. Rendimiento | ¿Cuánto tarda y cuántos recursos consume? | 6.3 |
| D4. Comportamiento funcional | ¿Cumple el comportamiento exigido por cada HU? | 6.4 |

---

## 4. Corpus de Evaluación

### 4.1 Decisión: corpus sintético de 50 investigadores

Se adopta un **corpus sintético de 50 investigadores** diseñado específicamente para la evaluación. Esta decisión se justifica por cuatro razones:

1. **Control de la verdad de referencia.** Al construir el corpus se conoce con exactitud qué investigador pertenece a qué temática, lo que permite definir conjuntos de elementos relevantes por consulta sin depender de un etiquetado externo.
2. **Potencia estadística suficiente.** Con 50 perfiles y consultas cuyos conjuntos relevantes son pequeños (2 a 8 investigadores), las métricas `Precision@K` y `Recall@K` con `K = 5` y `K = 10` resultan discriminativas y no se saturan.
3. **Cobertura de las 20 consultas de prueba.** Las consultas generales, relacionales y comparativas exigen varios perfiles por temática y "distractores" cercanos (perfiles parcialmente relacionados); 50 investigadores permiten cubrir las ocho temáticas objetivo con densidad suficiente.
4. **Viabilidad.** Es un número que puede autorizarse de forma realista y verificarse manualmente, a diferencia de un corpus grande cuya etiquetación sería inabordable en el tiempo del proyecto.

El corpus real de CvLAC se incorporará posteriormente como corpus de contraste (validez ecológica), manteniendo el corpus sintético como banco de pruebas controlado.

### 4.2 Composición

Los 50 investigadores se distribuyen entre ocho temáticas, de modo que las consultas de prueba tengan elementos relevantes y distractores:

| Temática | N.º | Relación con las consultas |
|---|---|---|
| Inteligencia artificial | 10 | generales, relacionales, comparativas |
| Aprendizaje automático | 8 | generales, relacionales |
| Procesamiento de lenguaje natural | 6 | relacionales (con IA) |
| Visión por computador | 6 | relacionales (con IA) |
| Ciencia / análisis de datos | 8 | generales |
| Desarrollo de software | 8 | generales, comparativas |
| Salud pública | 6 | generales |
| Energías renovables | 6 | relacionales |

Se garantiza **solapamiento intencional** entre temáticas (por ejemplo, investigadores de IA que también trabajan en PLN o visión) para que las consultas relacionales tengan respuestas no triviales, y **perfiles de frontera** (investigadores con una sola coincidencia) para penalizar la recuperación por palabra clave sin contexto.

### 4.3 Estructura de cada registro

Cada investigador se representa conforme al contrato CSV (`REGLAS_DATOS_CSV.md`), con las 23 columnas. Se poblarán al menos las secciones de mayor prioridad: `identificacion`, `formacion_academica`, `experiencia_profesional`, `articulos` y `proyectos`, y de forma variable el resto, para reproducir la heterogeneidad real de CvLAC descrita en `ANALISIS_ESTRUCTURA_CVLAC.md`.

Adicionalmente el corpus incluirá, de forma deliberada:

- **Variabilidad de extensión:** registros con cantidades de caracteres muy distintas, desde secciones breves hasta descripciones extensas, para reproducir la heterogeneidad real de CvLAC y evitar que la segmentación, la recuperación y la generación se beneficien de una longitud uniforme.
- **Variantes de denominación** (acrónimos y nombres completos de instituciones y grupos) para soportar la evaluación de HU-09.
- **Registros con enlaces `url_cvlac`** válidos, para evaluar HU-03.
- **Perfiles incompletos** (ausencia de secciones), para evaluar el comportamiento ante información insuficiente (HU-04-5).

El corpus, sus conjuntos relevantes y las respuestas de referencia se versionarán junto al código.

---

## 5. Conjunto de Consultas

### 5.1 Consultas semilla e instanciación

Se parte de las 20 consultas de prueba definidas en `REQUISITOS_FUNCIONALES.md` (puntuales, generales, relacionales y comparativas). Como en su forma original son plantillas (por ejemplo, "¿Cuál es la formación académica de [investigador]?"), se instancian con nombres y temáticas presentes en el corpus, generando casos concretos.

### 5.2 Tamaño y distribución

Se construye un conjunto de **40 casos de prueba**:

| Tipo | Casos | Propósito |
|---|---|---|
| Puntual | 8 | Consulta sobre un investigador y un aspecto (HU-04) |
| General | 8 | Consulta temática sobre todo el corpus (HU-05) |
| Relacional | 8 | Consulta que cruza dos condiciones (HU-06) |
| Comparativa | 8 | Consulta que compara varios investigadores (HU-06) |
| Negativa | 8 | Consulta sin cobertura en el corpus (HU-04-5) |

Los casos **negativos** son esenciales: permiten medir la **tasa de rechazo** (que el sistema declare información insuficiente en lugar de alucinar), criterio explícito de HU-04-5 y una de las razones de ser del enfoque RAG.

### 5.3 Anotación de cada caso

Cada caso registra: identificador, texto de la consulta, tipo, **conjunto de investigadores relevantes**, **secciones esperadas**, **respuesta de referencia (*ground truth*)** y una nota de dificultad. Esta anotación es la que habilita las métricas de recuperación (sección 6.1) y de corrección (sección 6.2).

---

## 6. Métricas

### 6.1 D1 — Recuperación

Miden si el sistema ubica los fragmentos pertinentes antes de generar la respuesta. Todas se calculan sobre los fragmentos recuperados, tomando como relevante un fragmento cuyo investigador y sección coincidan con los anotados en el caso.

| Métrica | Definición | Fórmula (resumen) |
|---|---|---|
| `Precision@K` | Proporción de fragmentos relevantes entre los `K` primeros | relevantes@K / K |
| `Recall@K` | Proporción de fragmentos relevantes recuperados del total | relevantes@K / total relevantes |
| `MRR@K` | Inverso de la posición del primer fragmento relevante | (1/U) Σ 1/rank_i |
| `nDCG@K` | Relevancia con descuento por posición | DCG@K / IDCG@K |
| `Recall de autores@K` | Cobertura de investigadores relevantes en el top-K (consultas abiertas) | autores relevantes@K / autores relevantes |

Las métricas anteriores son a nivel de **fragmento** y son adecuadas cuando el caso apunta a un único investigador y sección (casos puntuales y comparativos). Para las consultas **generales y relacionales** ("¿qué investigadores trabajan en X?") el conjunto de fragmentos relevantes es enorme (decenas o cientos), por lo que el `Recall` a nivel de fragmento queda estructuralmente bajo aunque la respuesta sea correcta; en esos casos la recuperación se mide a nivel de **autor** mediante el `Recall de autores@K`.

**Selección de `K`.** Se reporta con `K = 5` y `K = 10`. El valor `K = 10` se adopta como principal por coherencia con la categoría *Retrieval* de MTEB (`nDCG@10`); `K = 5` se incluye porque refleja cuánta información realmente llega al modelo en la parte alta del orden (el sistema envía hasta 15 fragmentos, de modo que un acierto fuera del top-10 difícilmente influye en la respuesta).

### 6.2 D2 — Generación

Evalúan la respuesta final. Se adopta el conjunto de métricas de RAGAS, que es el estándar en trabajos comparables:

| Métrica | Qué mide | Requiere ground truth |
|---|---|---|
| `Faithfulness` | Si la respuesta se deriva únicamente del contexto recuperado | No |
| `Answer Relevancy` | Si la respuesta atiende realmente la pregunta | No |
| `Context Precision` | Proporción de fragmentos recuperados que son útiles | Sí (relevancia) |
| `Context Recall` | Cobertura del contexto frente a la respuesta de referencia | Sí |
| `Context Entity Recall` | Cobertura de entidades clave (nombres, instituciones) | Sí |
| `Answer Correctness` | Exactitud factual frente a la referencia | Sí |
| `Answer Similarity` | Similitud semántica con la respuesta de referencia | Sí |

`Faithfulness` es la métrica central para el objetivo de "evitar alucinaciones": se complementa con la **tasa de alucinación** (`1 − Faithfulness`). Como métricas auxiliares de texto se pueden reportar `ROUGE` y `BERTScore` (empleadas en Sánchez Maya, 2026), aunque las métricas semánticas de RAGAS son preferibles sobre `BLEU`/`ROUGE` porque capturan equivalencias de significado.

### 6.3 D3 — Rendimiento

Se miden la latencia y el consumo de recursos, en dos escenarios (consulta e ingesta).

| Métrica | Descripción |
|---|---|
| Latencia por etapa | Clasificación, embedding de consulta, búsqueda + re-ranking y generación |
| Latencia extremo a extremo | Suma de etapas, por consulta |
| Percentiles | `P50` y `P95` por etapa y global |
| Tiempo a la primera respuesta (TTFT) | Con el endpoint en modo *streaming* |
| Velocidad de generación | Tokens por segundo |
| CPU | Uso promedio y pico durante la consulta y durante la ingesta |
| Memoria | RAM pico del proceso durante la consulta y la ingesta |
| Índice | Número de puntos y tiempo total de indexación del corpus |
| Concurrencia | Latencia con N consultas simultáneas (prueba de carga básica) |

Las mediciones de latencia excluyen el tiempo de carga del modelo (calentamiento previo).

### 6.4 D4 — Comportamiento funcional

Métricas específicas derivadas de los criterios de aceptación:

| Métrica | HU asociada | Descripción |
|---|---|---|
| Tasa de rechazo negativo | HU-04-5 | % de consultas sin cobertura respondidas con "información insuficiente" |
| Tasa de alucinación | HU-04-5, RT-7 | % de respuestas con contenido no sustentado por el contexto |
| Diferenciación de investigadores | HU-05-3 | % de respuestas generales que identifican a cada investigador por separado |
| Exactitud de enlaces | HU-03 | % de enlaces de hoja de vida correctos y completos |
| Resolución de acrónimos | HU-09 | % de consultas con acrónimo que recuperan su denominación equivalente |
| Fidelidad del resumen | HU-08 | % de resúmenes sin información ajena a la fuente |
| Cobertura del historial | HU-07 | % de preguntas de seguimiento resueltas usando el contexto previo |

---

## 7. Verdad de Referencia (*Ground Truth*)

### 7.1 Decisión: construcción por diseño + verificación humana

Se adopta un *ground truth* **construido por diseño y verificado manualmente**, en lugar de delegarlo por completo a un modelo. El procedimiento es:

1. **Origen por diseño:** como el corpus es sintético, el conjunto de investigadores y secciones relevantes de cada caso se define al crear el corpus; no se infiere a posteriori.
2. **Redacción de respuestas de referencia:** para cada caso se redacta la respuesta correcta usando exclusivamente la información del corpus.
3. **Verificación humana:** un subconjunto (≥ 30 % de los casos) se revisa por dos anotadores independientes; se reporta el acuerdo entre jueces con el coeficiente **kappa de Cohen**, exigiendo un acuerdo sustancial (κ ≥ 0.7) para considerar fiable el etiquetado.

### 7.2 Papel del LLM como juez

El LLM como juez se emplea **solo como complemento** (para métricas RAGAS que lo requieren, como `Answer Relevancy`), nunca como única fuente de verdad, y se **valida contra las anotaciones humanas** en el subconjunto revisado. Esta precaución evita la circularidad (usar un modelo para juzgar a otro modelo sin control humano) y es defendible ante un comité.

---

## 8. Matriz de Cumplimiento por Historia de Usuario

Traduce cada criterio evaluable (sin interfaz) a una métrica y a un umbral. La columna **HU-01 y los criterios de presentación** se difieren a la validación con usuarios.

| HU | Criterio de aceptación | Métrica | Método | Umbral |
|---|---|---|---|---|
| HU-02-3 | Generar respuesta relacionada con la consulta | `Answer Relevancy` | RAGAS sobre 40 casos | ≥ 0.80 |
| HU-02-4 | Responder con información registrada | `Faithfulness` | RAGAS | ≥ 0.85 |
| HU-03-1/4 | Entregar el enlace de la hoja de vida correcta | Exactitud de enlaces | Validación automática del `url_cvlac` de las fuentes | 100 % |
| HU-04-2 | Identificar al investigador y recuperar lo pedido | `Recall@5` en consultas puntuales | Recuperación | ≥ 0.75 |
| HU-04-3 | Responder sobre el aspecto solicitado | `Answer Correctness` (puntuales) | RAGAS | ≥ 0.70 |
| HU-04-5 | Indicar cuando no hay información suficiente | Tasa de rechazo negativo | 8 casos sin cobertura | ≥ 0.90 |
| HU-05-2 | Aplicar las restricciones de la consulta | `Precision@10` (generales) | Recuperación | ≥ 0.60 |
| HU-05-3 | Diferenciar investigadores identificados | Diferenciación de investigadores | Revisión sobre 8 casos generales | ≥ 0.90 |
| HU-06-1 | Adaptarse a pregunta libre (un/os investigador/es) | `Answer Correctness` (relacionales) | RAGAS | ≥ 0.65 |
| HU-06-2/3 | Respuesta coherente con lo solicitado | `Answer Relevancy` (relacionales) | RAGAS | ≥ 0.80 |
| HU-07-1 | Respuestas organizadas y legibles | Revisión cualitativa estructurada | Rúbrica 1–5 | ≥ 4.0 |
| HU-07-2/3 | Responder preguntas de seguimiento | Cobertura del historial | Casos multi-turno | ≥ 0.80 |
| HU-08-1/2 | Resumir sin introducir información ajena | Fidelidad del resumen | Revisión + `Faithfulness` | ≥ 0.90 |
| HU-09-1/2 | Relacionar acrónimos y equivalencias | Resolución de acrónimos | Casos con acrónimo | ≥ 0.80 |
| HU-10-1/4 | Indicar las hojas de vida usadas como fuente | Correspondencia fuente–respuesta | Revisión de `sources` vs. contexto usado | ≥ 0.95 |

Los umbrales se justifican en la sección 11 y son ajustables tras la primera medición.

---

## 9. Instrumentación Requerida

Para poder calcular las métricas, el prototipo necesita instrumentación mínima (trabajo de código acotado, sin alterar la arquitectura). Se adopta la **Opción A**: la medición vive en el paquete `backend/evaluation/` y envuelve a los colaboradores desde el *runner*, sin tocar el código de producción.

1. **Temporizadores por etapa** (`evaluation/timing.py`, `StageTimer` + `instrument`): envuelven `normalize`, `analyze_query`, `embed_query`, `search` y `rerank`; la generación y el TTFT se miden en el *runner* iterando el *stream*.
2. **Muestreo de recursos** (`evaluation/timing.py`, `ResourceMonitor`) con `psutil` (CPU % y RAM pico).
3. **Script de evaluación** (`scripts/evaluate.py` → `evaluation/runner.py`): indexa el corpus en una colección dedicada (`cvlac_eval`), ejecuta los 40 casos, calcula las métricas de recuperación y eficiencia y escribe `data/processed/evaluation_results.csv`.
4. **Cálculo de métricas de generación**: `evaluation/judge.py` implementa un juez LLM inspirado en RAGAS (`faithfulness`, `answer_relevancy`, `answer_correctness`) usando el propio `ILLMProvider`, de modo que no se añade la dependencia de RAGAS y el cálculo queda reproducible dentro del *stack* del proyecto. Se activa con `--judge`.
5. **Registro reproducible**: cada corrida guarda el corpus, el modelo, temperaturas y `top_k` vigentes; los resultados van a `data/processed/evaluation_results.csv`.

Además, `scripts/evaluate.py --stub-llm` ejecuta el harness con un LLM simulado (analizador heurístico de nombres + generación fija) para validar la mecánica y las métricas de recuperación **sin consumir cuota de la API**.

La instrumentación respeta `REGLAS_PROYECTO.md` (puertos/interfaces, sin acoplar la medición a la lógica de negocio).

---

## 10. Protocolo Experimental

1. **Entorno:** Qdrant en Docker, embeddings y orquestación en CPU local, LLM vía API. Idéntico en todas las corridas.
2. **Condiciones fijas:** modelo `gemini-3.8-flash`, temperatura 0.0 (clasificación) y 0.5 (generación), `top_k_retrieval = 20`, `top_k_final = 15`.
3. **Calentamiento:** una ejecución previa descartada para cargar el modelo de embeddings.
4. **Repeticiones:** las métricas de rendimiento se promedian sobre 3 corridas por caso (para latencia); las métricas de calidad se calculan sobre una corrida por caso (por costo), y las de latencia usan 3.
5. **Procedimiento:** indexar corpus → ejecutar los 40 casos → registrar salidas → calcular métricas → verificar subconjunto con anotadores.
6. **Registro:** resultados en `data/processed/evaluation_results.csv`; resumen en el informe de resultados.
7. **Cuota de API:** el nivel gratuito de `gemini-3.8-flash` limita a ≈ 20 solicitudes/día. Como cada caso consume 2 (sin juez) o 3 (con juez) solicitudes, la corrida completa de 40 casos requiere una clave con facturación habilitada o repartir la ejecución en varios días. Para validar la mecánica y las métricas de recuperación sin cuota se usa `scripts/evaluate.py --stub-llm`.

### 10.1 Ajuste por cuota y hallazgo derivado

- **Mientras no haya facturación habilitada**, la corrida real se ejecuta sobre un **subconjunto estratificado de 10 casos** (`--per-kind 2`: 2 por tipo), que consume las 20 solicitudes diarias. El conjunto completo de 40 casos queda como objetivo con una clave de pago.
- **Hallazgo y ajuste (re-ranking).** La primera medición (modo `--stub-llm`, 40 casos) mostró que, en las consultas puntuales, el fragmento correcto siempre se recuperaba (`Recall@10 = 1.0`) pero quedaba mal posicionado (`nDCG@10 = 0.50`, `MRR@10 = 0.34`): la prioridad fija de sección (REQUISITOS_RECUPERACION.md §5.3) enterraba la sección realmente preguntada. Se ajustó `WeightedReranker` para que, **solo en consultas a un investigador concreto**, la sección indicada por la consulta (vía `SECTION_KEYWORDS`) pase al frente, manteniendo la prioridad fija para consultas generales. Efecto medido (misma corrida offline): `nDCG@10` puntual 0.50 → **0.74** y `MRR@10` 0.34 → **0.66**.
- **Limitación confirmada.** Las consultas **comparativas** (varios investigadores) obtienen métricas bajas porque el análisis devuelve un único `researcher_name` y la búsqueda filtra por un solo autor; se registran como limitación pendiente de diseño. La métrica de recuperación para consultas generales/relacionales se reporta a nivel de autor (`Recall de autores@10`).

---

## 11. Criterios de Éxito y Umbrales

| Métrica | Umbral | Fundamento |
|---|---|---|
| `Faithfulness` | ≥ 0.85 | RAGAS y trabajos comparables sitúan ≥ 0.80 como nivel sólido; se exige un margen mayor por el objetivo anti-alucinación |
| `Answer Relevancy` | ≥ 0.80 | Nivel "bueno" según la práctica de RAGAS |
| `Context Precision` | ≥ 0.80 | Nivel "bueno" según la práctica de RAGAS |
| `Context Recall` | ≥ 0.80 | Nivel "bueno" según la práctica de RAGAS |
| `Answer Correctness` | ≥ 0.70 | Umbral realista observado en trabajos comparables (Comyn Rodríguez obtuvo 0.669 y lo calificó de mejorable) |
| `Answer Similarity` | ≥ 0.80 | Valor alto alcanzado en trabajos comparables (0.850 en Comyn Rodríguez) |
| `Recall@10` | ≥ 0.85 | Exigencia de recuperación alta en un corpus controlado de 50 perfiles |
| `Precision@5` | ≥ 0.70 | Equilibrio entre precisión y recall en la parte alta del ranking |
| `MRR@10` | ≥ 0.75 | El primer resultado relevante debe aparecer, en promedio, en posiciones altas |
| `nDCG@10` | ≥ 0.80 | Referencia de MTEB para tareas de recuperación |
| Tasa de rechazo negativo | ≥ 0.90 | Criterio explícito de HU-04-5 (evitar inventar información) |
| Tasa de alucinación | ≤ 5 % | `1 − Faithfulness`; objetivo primario del enfoque RAG |
| TTFT (P95) | ≤ 2.5 s | Límite perceptivo: por encima de ~2–3 s la interacción deja de sentirse inmediata (Nielsen, 1993) |
| Latencia extremo a extremo (P95) | ≤ 10 s | Límite de tolerancia al flujo de atención (Nielsen, 1993) |
| RAM pico (consulta) | Sin fallo del sistema | Restricción de hardware (C3 de `REQUISITOS_INFRAESTRUCTURA.md`) |

Un resultado se considera **satisfactorio** cuando la métrica alcanza o supera el umbral, **parcial** cuando se encuentra a menos del 10 % del umbral, y **no satisfactorio** en caso contrario. Los umbrales son de referencia y podrán ajustarse de forma justificada tras la primera medición.

---

## 12. Riesgos y Limitaciones

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Validez externa del corpus sintético | Los resultados no reflejan datos reales de CvLAC | Contraste posterior con el corpus real |
| Sesgo del LLM como juez | Métricas de generación infladas o sesgadas | Validación contra anotación humana (κ ≥ 0.7) |
| Ausencia de *baseline* | No se mide la mejora frente al buscador tradicional | Justificada por falta de acceso; se compara contra el estado del arte |
| Costo y latencia de la API | La evaluación completa puede ser lenta o costosa | 40 casos, repeticiones acotadas, caché de respuestas |
| Corpus de 50 perfiles | Menor diversidad que un corpus real | Solapamiento y perfiles de frontera intencionales |
| Cuota de la API del LLM (nivel gratuito ≈ 20 solicitudes/día) | No es posible completar la corrida de 40 casos con juez en un solo día | Clave con facturación habilitada o ejecución por lotes; `--stub-llm` para las métricas de recuperación |

---

## 13. Entregables

1. **Este documento** (`PLAN_VALIDACION.md`), objeto de revisión conjunta.
2. **Corpus sintético de evaluación** (CSV + conjuntos relevantes + *ground truth*).
3. **Instrumentación** (paquete `backend/evaluation/` + CLI `scripts/evaluate.py`).
4. **Resultados** en `data/processed/evaluation_results.csv`.
5. **Informe de resultados** (`INFORME_RESULTADOS.md`) con tablas por métrica y por HU, pendiente de una etapa posterior.

---

## 14. Referencias

- Es, S., James, J., Espinosa-Anke, L., & Schockaert, S. (2023). *RAGAS: Automated Evaluation of Retrieval Augmented Generation.*
- Manning, C. D., Raghavan, P., & Schütze, H. (2008). *Introduction to Information Retrieval.* Cambridge University Press.
- Muennighoff, N., et al. (2023). *MTEB: Massive Text Embedding Benchmark.*
- Nielsen, J. (1993). *Usability Engineering.* Morgan Kaufmann.
- Comyn Rodríguez, J. (2025). *Sistema Multiagente basado en RAG para Asistencia en el Manejo de la Diabetes.* TFG, Universidad Politécnica de Madrid.
- Sánchez Maya, S. (2026). *Sistema de Recuperación Aumentada por Generación (RAG) para la optimización de la gestión y consulta de documentos en Fintic.* Trabajo de grado, UNAD.
- Documentos internos: `REQUISITOS_FUNCIONALES.md`, `REQUISITOS_RECUPERACION.md`, `ARQUITECTURA_MODULAR.md`, `METODOS_OPTIMIZACION.md`, `REGLAS_DATOS_CSV.md`.
