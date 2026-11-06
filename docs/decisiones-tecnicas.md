# Decisiones técnicas

| Decisión | Por qué |
| --- | --- |
| Pruebas de caja negra antes de refactorizar | Demuestran que el comportamiento no cambió, sin depender de la estructura interna. |
| Un refactoring por commit, con pruebas pasando | Si algo falla, se sabe qué cambio lo causó y se puede volver atrás. |
| Separar en capas (consola, servicio, repositorio) | Las reglas no dependen de `print`, `input` ni del archivo; se pueden probar solas (SRP, DIP). |
| Mantener las clases de tipo de solicitud | Agregar un tipo no obliga a tocar el servicio (OCP) y todos se usan igual (LSP). Un diccionario era más corto pero perdía eso. |
| Mantener 3 interfaces de repositorio | Cada parte depende solo de lo que usa (ISP). Es la decisión más discutible: suma código. |
| Unir las excepciones propias (de 6 a 4) | Varias tenían muy poco uso; se evitó la sobreingeniería. |
| Los tests usan `tests/datos_base.json` | Antes fallaban si `datos.json` cambiaba por uso manual. |
| Separar "refactorizar" de "corregir" | Las 3 correcciones (solicitud, responsable y JSON dañado) son commits aparte, para no mezclar con cambios de estructura. |

