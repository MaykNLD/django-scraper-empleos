"""
scraper.py — Obtiene ofertas de trabajo de APIs públicas gratuitas.

Fuentes utilizadas:
- Arbeitnow: https://arbeitnow.com/api/job-board-api (sin auth, sin límite)
- Remotive:  https://remotive.com/api/remote-jobs   (sin auth, sin límite)
"""
import httpx
import logging
from datetime import datetime, date

logger = logging.getLogger('jobs')

ARBEITNOW_URL = "https://arbeitnow.com/api/job-board-api"
REMOTIVE_URL  = "https://remotive.com/api/remote-jobs?category=software-dev&limit=100"
TIMEOUT       = 20.0


def fetch_arbeitnow() -> list[dict]:
    """Obtiene ofertas de Arbeitnow — API pública sin autenticación."""
    try:
        with httpx.Client(timeout=TIMEOUT) as client:
            resp = client.get(ARBEITNOW_URL)
            resp.raise_for_status()
            jobs = resp.json().get("data", [])
            logger.info(f"Arbeitnow: {len(jobs)} ofertas recibidas")
            return [_normalize_arbeitnow(j) for j in jobs]
    except httpx.HTTPError as e:
        logger.error(f"Error Arbeitnow: {e}")
        return []
    except Exception as e:
        logger.error(f"Error inesperado Arbeitnow: {e}")
        return []


def fetch_remotive() -> list[dict]:
    """Obtiene ofertas de Remotive — API pública sin autenticación."""
    try:
        with httpx.Client(timeout=TIMEOUT) as client:
            resp = client.get(REMOTIVE_URL)
            resp.raise_for_status()
            jobs = resp.json().get("jobs", [])
            logger.info(f"Remotive: {len(jobs)} ofertas recibidas")
            return [_normalize_remotive(j) for j in jobs]
    except httpx.HTTPError as e:
        logger.error(f"Error Remotive: {e}")
        return []
    except Exception as e:
        logger.error(f"Error inesperado Remotive: {e}")
        return []


def fetch_all() -> list[dict]:
    """Llama a todas las fuentes y combina resultados."""
    arbeitnow = fetch_arbeitnow()
    remotive  = fetch_remotive()
    all_jobs  = arbeitnow + remotive
    logger.info(f"Total obtenido: {len(all_jobs)} ofertas de {len([x for x in [arbeitnow, remotive] if x])} fuentes")
    return all_jobs


# ── Normalizadores ────────────────────────────────────────────────────────────

def _parse_date(raw: str) -> date | None:
    """Intenta parsear una fecha en formatos ISO comunes."""
    if not raw:
        return None
    for fmt in ('%Y-%m-%dT%H:%M:%S%z', '%Y-%m-%dT%H:%M:%SZ', '%Y-%m-%d'):
        try:
            return datetime.strptime(raw[:19], fmt[:len(raw[:19])]).date()
        except ValueError:
            continue
    return None


def _normalize_arbeitnow(job: dict) -> dict:
    return {
        "external_id": f"arbeitnow_{job.get('slug', job.get('id', ''))}",
        "source":      "arbeitnow",
        "title":       job.get("title", "")[:500],
        "company":     job.get("company_name", "")[:255],
        "location":    job.get("location", "")[:255],
        "description": job.get("description", ""),
        "tags":        job.get("tags", []),
        "salary":      "",
        "url":         job.get("url", "")[:1000],
        "remote":      job.get("remote", False),
        "date_posted": _parse_date(str(job.get("created_at", ""))),
    }


def _normalize_remotive(job: dict) -> dict:
    return {
        "external_id": f"remotive_{job.get('id', '')}",
        "source":      "remotive",
        "title":       job.get("title", "")[:500],
        "company":     job.get("company_name", "")[:255],
        "location":    job.get("candidate_required_location", "Remote")[:255],
        "description": job.get("description", ""),
        "tags":        job.get("tags", []),
        "salary":      job.get("salary", "")[:100] if job.get("salary") else "",
        "url":         job.get("url", "")[:1000],
        "remote":      True,  # Remotive solo tiene trabajos remotos
        "date_posted": _parse_date(str(job.get("publication_date", ""))),
    }
