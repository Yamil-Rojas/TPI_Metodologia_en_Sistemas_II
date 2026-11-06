# Gestión de Solicitudes Académicas

Sistema de consola en Python para registrar y seguir solicitudes académicas de estudiantes (certificados, equivalencias y bajas de materia). Los datos se guardan en un archivo JSON.

Este repositorio es el Trabajo Práctico Integrador de **Metodología de Sistemas II** (UTN, Tecnicatura Universitaria en Programación, modalidad a distancia). El objetivo no es agregar funciones: es **refactorizar** un sistema existente y reducir su **deuda técnica** sin cambiar lo que hace.

Todos los datos del repositorio son **sintéticos** (inventados).

## Descripción

El sistema original tenía todo mezclado: menú, reglas de negocio y acceso al archivo en pocas funciones largas. El repositorio muestra el proceso completo: diagnóstico, refactorings seguros con pruebas antes y después, code review y conclusiones.

## Instalación

Requisitos: **Python 3.10 o superior**. No hay dependencias externas.

```bash
git clone <URL-del-repositorio>
cd <carpeta-del-repositorio>
python main.py
```

## Funcionalidades

Al ejecutar `python main.py` aparece este menú:

| Opción | Qué hace |
| --- | --- |
| 1 | Registrar solicitud (estudiante, tipo, prioridad) |
| 2 | Cambiar estado (pendiente, en proceso, finalizada) |
| 3 | Asignar responsable |
| 4 | Buscar solicitudes |
| 5 | Reporte básico |
| 6 | Ver responsables |
| 0 | Salir |

Tipos de solicitud: certificado (5 días de plazo base), equivalencia (15) y baja de materia (3).

## Tecnologías

- Python 3 (biblioteca estándar: `json`, `dataclasses`, `abc`, `enum`)
- `unittest` para las pruebas
- Git y GitHub para el historial y los tags de cada etapa

## Estructura del proyecto

```text
main.py            Consola: menú, print e input (única capa que los usa)
servicio.py        Reglas de negocio (no conoce la consola ni el archivo)
repositorio.py     Acceso a datos.json (interfaces + implementación JSON)
modelos.py         Entidades, enumeraciones y tipos de solicitud
errores.py         Excepciones propias
validaciones.py    Validación de legajo y mensajes de error
datos.json         Datos de ejemplo (sintéticos)
tests/             Pruebas automáticas y herramientas de evidencia
docs/              Documentación de las etapas
```

Las capas dependen en una sola dirección: `main` → `servicio` → `repositorio`. El servicio recibe el repositorio por parámetro (inversión de dependencias).

## Pruebas

```bash
python -m unittest discover -s tests
```

Son 31 pruebas. Incluyen pruebas de caja negra que ejecutan el programa con entradas simuladas y comparan la salida con un resultado de referencia, y pruebas de unidad del servicio y del repositorio. Usan su propio `tests/datos_base.json`, así que no dependen del `datos.json` de uso manual.

## Etapas y tags

| Tag | Qué contiene |
| --- | --- |
| `estado-inicial` | Sistema base, antes de refactorizar |
| `etapa-diagnostico` | Calidad, deuda técnica y smells |
| `etapa-refactoring` | Refactorings aplicados |
| `estado-refactorizado` | Código final refactorizado |
| `etapa-pruebas` | Pruebas antes/después y evidencia |
| `etapa-docs` | Documentación final |

Para ver el cambio completo: `git diff estado-inicial estado-refactorizado`.

## Documentación (`/docs`)

- [`docs/code-review.md`](docs/code-review.md): checklist de code review, hallazgos y mejoras futuras.
- [`docs/evidencia-pruebas.md`](docs/evidencia-pruebas.md): comparación de comportamiento antes y después.
- [`docs/decisiones-tecnicas.md`](docs/decisiones-tecnicas.md): decisiones de diseño y por qué se tomaron.
- [`docs/uso-de-ia.md`](docs/uso-de-ia.md): declaración del uso de IA.

## Equipo

Maximiliano Rojas, Franco y Santiago. *(Completar apellidos y la contribución de cada integrante.)*
