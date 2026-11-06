# Code review del repositorio

Revisión técnica del código final del sistema de Gestión de Solicitudes Académicas, con checklist, observaciones, correcciones realizadas y criterios de aceptación.

**Alcance:** los seis módulos (`main.py`, `servicio.py`, `repositorio.py`, `modelos.py`, `validaciones.py`, `errores.py`) y la carpeta `tests/`.
**Cómo se revisó:** lectura completa del código, `pyflakes` (imports y variables sin uso), `pycodestyle` con líneas de hasta 120 caracteres, `coverage` sobre las pruebas automáticas y las métricas de la Etapa 5.
**Quién revisó:** esta revisión la hizo Claude (IA). Falta la lectura de un integrante del grupo; sus comentarios se agregan en la sección "Feedback de integrantes".

## Criterios de aceptación técnica

El código se acepta si cumple todo esto:

1. Las pruebas automáticas pasan completas.
2. `pyflakes` y `pycodestyle` no informan hallazgos.
3. No hay `except` vacíos ni `print`/`input` fuera de `main.py`.
4. El servicio no conoce el archivo (`json`, `os`, `open`): solo el repositorio.
5. Todo lo observado como "Corregir" está corregido en un commit aparte.
6. Lo que no se corrige queda anotado como mejora futura, con su motivo.

**Resultado: aceptado.** Los seis criterios se cumplen al commit de la revisión.

## Checklist

| # | Criterio | Resultado | Evidencia |
| --- | --- | --- | --- |
| 1 | Cada módulo tiene una sola responsabilidad (pantalla, reglas, datos, modelos, validaciones, errores) | Cumple | Estructura de 6 módulos |
| 2 | Las dependencias van en un solo sentido y el servicio depende de interfaces | Cumple | Prueba de reglas de diseño; el servicio recibe los repositorios por constructor |
| 3 | No hay lógica de negocio en `main.py` | Cumple | `main.py` solo pide datos y muestra resultados |
| 4 | Nombres que dicen qué hacen | Cumple | Métrica de nombres de 1 o 2 letras: 20 a 1 (queda `id`, nombre del dominio) |
| 5 | Funciones cortas | Cumple | Lógica más larga: 15 líneas; con `main.py`, 18 |
| 6 | Sin textos ni números mágicos | Cumple | `Estado`, `Prioridad`, `PLAZO_MINIMO_DIAS`, `TIPOS` |
| 7 | Sin código duplicado | Cumple | Una sola validación de legajo, una sola lectura y una sola escritura de archivo |
| 8 | Líneas de hasta 120 caracteres y sin imports sin usar | Corregido | Hallazgo 1, commit "Review: estilo y limpieza" |
| 9 | Sin `except` vacíos | Cumple | Métrica: 11 a 0; prueba de reglas de diseño |
| 10 | Los errores del usuario se informan con un mensaje claro | Corregido | Correcciones 1 a 3 de la Etapa 5 y hallazgo 3 |
| 11 | Un fallo de archivo no destruye datos ni da mensajes falsos | Corregido | Correcciones 3 y hallazgo 2 |
| 12 | Las pruebas pasan, son repetibles y no dependen de datos reales | Cumple | 31 pruebas; datos de partida propios |
| 13 | Las pruebas cubren el código | Cumple | 100 % de líneas (pruebas de unidad y de caja negra juntas); no mide ramas |
| 14 | Las pruebas detectan errores | Cumple | 4 de 5 cambios hechos a propósito fueron detectados (Etapa 6) |
| 15 | Los datos de ejemplo son sintéticos y no hay credenciales ni rutas absolutas | Cumple | Datos inventados; la ruta del archivo es relativa al programa |
| 16 | Docstrings en las funciones públicas | Observación | Mejora futura 1 |
| 17 | Escritura del archivo a prueba de cortes | Observación | Mejora futura 2 |
| 18 | Historial de commits claro, un cambio por commit | Cumple | 22 commits con mensajes descriptivos |
| 19 | Uso de IA declarado en los commits y en el informe | Cumple | Línea `Co-Authored-By` en cada commit |
| 20 | README actualizado con la estructura nueva | Pendiente | Se completa en la etapa de documentación |
| 21 | Tags de cada etapa | Pendiente | Falta `etapa-docs` |

## Observaciones y correcciones

| # | Hallazgo | Gravedad | Qué se hizo |
| --- | --- | --- | --- |
| 1 | `pyflakes` y `pycodestyle`: un import sin usar, 10 líneas de más de 120 caracteres y una función asignada con `lambda` | Baja | Corregido: commit "Review: estilo y limpieza". Sin cambios de comportamiento |
| 2 | Si fallaba la escritura de `datos.json`, el mensaje decía "No se modifico nada", pero una escritura fallida puede dejar el archivo a medias | Media | Corregido: la escritura tiene su propio mensaje, que no afirma eso. Se agregaron 8 pruebas del repositorio |
| 3 | Escribir letras en vez de un número en un ID se convertía en silencio en el ID 0, y desde la corrección 1 mostraba `No existe la solicitud con ID 0`, que confunde | Media | Corregido: ahora muestra `ID invalido`. Se agregaron los casos c06 y c07 |

## Mejoras futuras (no se hicieron)

1. **Docstrings:** las funciones públicas no tienen. No se agregaron porque los nombres son claros y el sistema es chico, pero convendría documentar el contrato de `TipoSolicitud` y de los repositorios.
2. **Escritura del archivo a prueba de cortes:** se escribe directamente sobre `datos.json`. Si el programa se corta justo en ese momento, el archivo puede quedar incompleto. Se resuelve escribiendo en un archivo temporal y renombrándolo.
3. **Lecturas repetidas:** cada operación lee el archivo completo, y registrar una solicitud lo lee varias veces. Es aceptable para este volumen de datos y se hereda del original.
4. **Legajo con dígitos Unicode:** `isdigit()` acepta caracteres como `²`. Se hereda del original y cambiarlo altera el comportamiento.
5. **Área vacía:** el campo "Área" se acepta vacío, igual que en el original.
6. **Tamaño de `modelos.py`:** reúne enums, entidades y tipos en 116 líneas. Si crece, conviene separarlo.

