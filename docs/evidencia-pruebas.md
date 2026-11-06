# Evidencia de pruebas antes/después

Generado por `tests/evidencia.py`: corre los mismos escenarios sobre el código original (tag `estado-inicial`) y sobre el código refactorizado, con los mismos datos de partida (`tests/datos_base.json`).

## Comportamiento que no debe cambiar: 16 de 16 escenarios idénticos

| Escenario | Qué se prueba | Salida | Código de salida | datos.json guardado | Resultado |
| --- | --- | --- | --- | --- | --- |
| s01_salir | Abrir el programa y salir | igual | igual | igual | sin cambios |
| s02_responsables | Ver la lista de responsables | igual | igual | igual | sin cambios |
| s03_registrar_valido | Registrar una solicitud valida y buscarla | igual | igual | igual | sin cambios |
| s04_plazos | Plazo calculado para cada tipo y prioridad | igual | igual | igual | sin cambios |
| s05_validaciones | Datos invalidos: legajo, nombre, email, tipo, prioridad, descripcion | igual | igual | igual | sin cambios |
| s06_estados_validos | Cambios de estado permitidos | igual | igual | igual | sin cambios |
| s07_estados_no_permitidos | Cambios de estado no permitidos | igual | igual | igual | sin cambios |
| s08_asignar | Asignar responsables | igual | igual | igual | sin cambios |
| s09_busquedas | Busquedas por estado, tipo y legajo (validas e invalidas) | igual | igual | igual | sin cambios |
| s10_reportes | Reporte basico con y sin legajo | igual | igual | igual | sin cambios |
| s11_opciones_invalidas | Opciones de menu invalidas | igual | igual | igual | sin cambios |
| s12_flujo_completo | Flujo completo: registrar, procesar, asignar, finalizar, reportar | igual | igual | igual | sin cambios |
| s13_estudiante_existente | Registrar con un legajo de estudiante ya existente | igual | igual | igual | sin cambios |
| s14_sin_archivo | Primer uso: datos.json no existe | igual | igual | igual | sin cambios |
| s15_datos_vacios | datos.json con listas vacias | igual | igual | igual | sin cambios |
| s16_ids_con_huecos | IDs con huecos (el nuevo ID sigue al mayor) | igual | igual | igual | sin cambios |

## Fallas conocidas que se corrigieron a propósito

| Caso | Qué se prueba | Antes (código original) | Después (código refactorizado) |
| --- | --- | --- | --- |
| c01 | Cambiar el estado de una solicitud que no existe (ID 99) | no muestra ningún mensaje | muestra `No existe la solicitud con ID 99`; el programa sigue funcionando; datos.json queda igual |
| c02 | Asignar un responsable que no existe (ID 99) | el programa se corta con `TypeError: 'NoneType' object is not subscriptable` | muestra `No existe el responsable con ID 99`; el programa sigue funcionando; datos.json queda igual |
| c03 | Asignar a una solicitud que no existe (ID 99) | no muestra ningún mensaje | muestra `No existe la solicitud con ID 99`; el programa sigue funcionando; datos.json queda igual |
| c04 | Pedir el reporte con datos.json danado | muestra el reporte como si no hubiera datos (Total: 0) | muestra `No se pudo leer datos.json: el archivo esta danado o no es accesible. No se modifico nada.`; el programa sigue funcionando; datos.json queda igual |
| c05 | Registrar una solicitud con datos.json danado | pisa datos.json (queda con 1 solicitud) | muestra `No se pudo leer datos.json: el archivo esta danado o no es accesible. No se modifico nada.`; el programa sigue funcionando; datos.json queda igual |
| c06 | Cambiar estado escribiendo letras en vez de un ID | no muestra ningún mensaje | muestra `ID invalido`; el programa sigue funcionando; datos.json queda igual |
| c07 | Asignar responsable escribiendo letras en vez de un ID | no muestra ningún mensaje | muestra `ID invalido`; el programa sigue funcionando; datos.json queda igual |
