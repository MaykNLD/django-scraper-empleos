# Django Scraper Empleos 🕸️

![Status](https://img.shields.io/badge/status-active-brightgreen)
![Stack](https://img.shields.io/badge/stack-Django%20%2B%20DRF%20%2B%20Chart.js-blue)
![Python](https://img.shields.io/badge/python-3.10%2B-informational)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

> Un backend robusto en Django que extrae automáticamente ofertas de trabajo remotas de APIs públicas, las normaliza, las sirve a través de una API REST y proporciona un Dashboard analítico moderno.

---

## Para Reclutadores / Tech Leads

> Este proyecto demuestra conocimientos avanzados en Backend con Django:
> - **Automatización y Scraping**: Comandos de Management (`manage.py scrape_jobs`) para consumo asíncrono/síncrono de APIs externas (Remotive, Arbeitnow).
> - **Modelado de Datos Avanzado**: Uso de `update_or_create` para idempotencia, modelado de `ScraperRun` para auditoría y logs de ejecución, indexación (`db_index=True`) para optimización de queries.
> - **API REST Profesional**: Construida con Django REST Framework (DRF), incluyendo paginación, filtros complejos (`django-filter`), y endpoints analíticos personalizados (`@action`).
> - **Dashboard Dinámico**: Integración de Django Templates con Chart.js para visualización de datos en tiempo real (Skills más demandados, porcentajes, etc.).
> - **Arquitectura Limpia**: Separación de lógica de extracción (`scraper.py`), vistas (`views.py`), y modelos (`models.py`).

---

## 🚀 Inicio Rápido (Modo Demo)

El proyecto incluye 200 ofertas de trabajo pre-cargadas (Seed Data) para poder probar el dashboard y la API inmediatamente sin necesidad de configurar scrapers o esperar.

```bash
# 1. Clonar el repositorio
git clone https://github.com/MaykNLD/django-scraper-empleos.git
cd django-scraper-empleos

# 2. Entorno virtual e instalación
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Migraciones y Seed Data
python manage.py migrate
python manage.py load_seed

# 4. Iniciar servidor
python manage.py runserver
```

Visita **http://localhost:8000** para ver el Dashboard.

---

## 🛠️ Comandos del Scraper

Puedes poblar la base de datos con datos reales en cualquier momento usando el scraper integrado.

```bash
# Obtener ofertas de TODAS las fuentes configuradas
python manage.py scrape_jobs

# Obtener ofertas de una fuente específica
python manage.py scrape_jobs --source arbeitnow
python manage.py scrape_jobs --source remotive
```

---

## 🔌 API REST Endpoints

La API proporciona acceso completo a los datos estructurados.

| Endpoint | Método | Descripción |
|---|---|---|
| `/api/jobs/` | GET | Listado paginado de ofertas |
| `/api/jobs/{id}/` | GET | Detalle de una oferta |
| `/api/jobs/stats/` | GET | Estadísticas globales (usado para gráficas) |
| `/api/runs/` | GET | Historial de auditoría del scraper |

**Ejemplos de filtrado:**
- `/api/jobs/?remote=true` (Solo trabajos remotos)
- `/api/jobs/?source=remotive` (Filtrar por fuente)
- `/api/jobs/?title=python` (Búsqueda por título)

---

## 🗄️ Stack Tecnológico

| Capa | Tecnología |
|---|---|
| Framework Principal | Django 5.1 |
| API | Django REST Framework (DRF) |
| Base de Datos | SQLite (Desarrollo) / PostgreSQL (Producción, listo vía `DATABASE_URL`) |
| Frontend | HTML5, CSS3, Chart.js (Django Templates) |
| Peticiones HTTP | `httpx` (para consumo de APIs externas) |

---

*Construido por [Michael Lascano](https://github.com/MaykNLD) · [Portfolio](https://mi-portafolio-beta-one.vercel.app)*
