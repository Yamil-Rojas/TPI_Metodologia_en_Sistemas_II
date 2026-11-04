# Sistema de Gestión de Solicitudes Académicas

Trabajo Práctico Integrador de **Metodología de Sistemas II** (Tecnicatura Universitaria en Programación, UTN).

El proyecto parte de un sistema pequeño que **funciona correctamente pero tiene mala calidad interna**. El objetivo del TPI es diagnosticarlo, refactorizarlo y demostrar con evidencia que el comportamiento externo se mantiene igual.

> **Aviso:** la versión `estado-inicial` contiene deuda técnica y code smells **intencionales**. No es un ejemplo de buenas prácticas: es el punto de partida del trabajo.

## Descripción

Aplicación de consola para administrar las solicitudes que los estudiantes hacen a la institución (certificados, equivalencias, bajas de materia). Permite registrar una solicitud, hacerla avanzar de estado, asignarle un responsable, buscarla y obtener un reporte.

Todos los datos del repositorio son **sintéticos**: nombres, legajos y correos son inventados.

## Funcionalidades

| # | Operación | Qué hace |
|---|---|---|
| 1 | Registrar solicitud | Valida los datos, calcula el plazo según tipo y prioridad y guarda la solicitud en estado pendiente |
| 2 | Cambiar estado | Avanza una solicitud de pendiente a en proceso y de en proceso a finalizada. No permite retroceder ni saltar estados |
| 3 | Asignar responsable | Asigna un responsable (y su área) a una solicitud |
| 4 | Buscar solicitudes | Filtra por estado, por tipo o por legajo |
| 5 | Reporte básico | Muestra la cantidad de solicitudes por estado y, opcionalmente, las de un legajo |
| 6 | Ver responsables | Lista los responsables disponibles |

### Valores válidos

- **Tipo:** `cert` (certificado), `equi` (equivalencia), `baja` (baja de materia)
- **Estado:** `pen` (pendiente), `pro` (en proceso), `fin` (finalizada)
- **Prioridad:** `1` (alta), `2` (media), `3` (baja)
- **Legajo:** 5 dígitos

## Tecnologías

- Python 3 (sin librerías externas)
- Persistencia en un archivo JSON (`datos.json`)
- Interfaz por consola

## Instalación y uso

Requisito: tener Python 3 instalado.

```bash
git clone <URL-del-repositorio>
cd <carpeta-del-repositorio>
python main.py
```

En algunos sistemas el comando es `python3 main.py`.

Al ejecutarlo aparece un menú numerado. Se elige la opción escribiendo su número y respondiendo lo que se pida. La opción `0` cierra el programa.

## Estructura del repositorio

```
.
├── main.py        # Menú por consola
├── sistema.py     # Lógica del sistema
├── datos.json     # Datos de ejemplo (sintéticos)
├── README.md
└── docs/          # Checklist de code review, evidencias y decisiones técnicas
```

## Versiones (tags)

| Tag | Qué representa | Estado |
|---|---|---|
| `estado-inicial` | Sistema base con problemas de diseño | Disponible |
| `etapa-diagnostico` | Diagnóstico de deuda técnica y code smells | Pendiente |
| `etapa-refactoring` | Refactorings aplicados | Pendiente |
| `etapa-pruebas` | Pruebas y verificación antes/después | Pendiente |
| `etapa-docs` | Documentación y code review | Pendiente |
| `estado-refactorizado` | Versión final refactorizada | Pendiente |

Para ver una versión puntual:

```bash
git checkout estado-inicial
```

Para volver a la última versión: `git checkout main`.

## Integrantes

- Reynoso Franco
- Rodriguez Santiago
- Rojas Maximiliano

**Materia:** Metodología de Sistemas II · **Comisión:** 13
