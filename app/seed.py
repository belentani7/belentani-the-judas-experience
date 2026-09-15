from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.experience import ExperienceChapter
from app.models.release import Release
from app.models.tenant import Tenant
from app.models.user import User
from app.models.work import Work
from app.services import hash_password
from app.services.base43 import Base43System, create_base43_instance

CHAPTERS = [
    {
        "phase": "FASE_01",
        "title": "La herida se convierte en arquitectura viva.",
        "kicker": "CONCEPTO",
        "glyph": "✦",
        "order_index": 1,
        "body": (
            "Belentani diseña una obra inmersiva donde la imagen, el sonido y el cristal "
            "comparten una misma respiración. Judas aparece como tensión dramática; "
            "el autor y su visión siguen al centro. Ciencia ficción emocional: neón, "
            "desierto, glitch, deseo, choque y transformación."
        ),
    },
    {
        "phase": "FASE_02",
        "title": "El mito no reemplaza al autor; lo intensifica.",
        "kicker": "FICCIÓN / MITOLOGÍA",
        "glyph": "⬢",
        "order_index": 2,
        "body": (
            "La Era Judas es un universo artístico de Belentani. Sus símbolos no describen "
            "hechos biográficos: organizan una estética de tensión, memoria y poder creativo. "
            "Pedro atraviesa la pérdida de control; Judas encarna la duda, la ruptura y el impulso de cambio."
        ),
    },
    {
        "phase": "FASE_03",
        "title": "El diamante no es un objeto; es una memoria cristalizada.",
        "kicker": "ARTEFACTO / DIAMANTE",
        "glyph": "◇",
        "order_index": 3,
        "body": (
            "La pieza generada para la Era Judas funciona como llave simbólica: una arquitectura "
            "de luz que recoge la tensión entre sombra, deseo y supervivencia. Frecuencia 432 Hz. "
            "Material: neón + cristal. Estado: activo. Modo: transmisión."
        ),
    },
    {
        "phase": "FASE_04",
        "title": "El beso como umbral.",
        "kicker": "FIGURA ESCÉNICA",
        "glyph": "◉",
        "order_index": 4,
        "body": (
            "Judas funciona como una máscara dramática: deseo, quiebre y eco. No es el centro; "
            "es el borde que empuja la obra a moverse. La llave no representa posesión literal: "
            "es una imagen de acceso, decisión y transformación del sistema."
        ),
    },
    {
        "phase": "FASE_05",
        "title": "Ser muchos para poder seguir siendo uno.",
        "kicker": "ZION DIMENSION",
        "glyph": "Ω",
        "order_index": 5,
        "body": (
            "Un Belentani de la dimensión Zion inicia un protocolo: desactivar el código dentro "
            "del código Judas. Integrar todas las versiones del multiverso junto con su frágil "
            "envoltura humana. LAT 41.3851N · LON 2.1734E · NODE JUDAS-CORE-07 · FREQ 432 Hz."
        ),
    },
]


WORKS = [
    ("mon-amour", "Mon Amour", "single", "Dark pop y R&B visceral. Una declaración de amor en medio del caos digital."),
    ("therapist", "Therapist", "single", "Electrónica industrial con letras que diseccionan la psique humana."),
    ("apaga-a-luz", "Apaga a Luz", "single", "Melodías llenas de soul con estructuras rítmicas cautivadoras."),
    ("lento", "Lento", "single", "R&B alternativo. La vulnerabilidad radical como mecanismo de supervivencia."),
    ("i-wrote-a-song", "I Wrote a Song", "session", "Judas Studio Sessions — archivo vivo."),
    ("judas-era", "Judas Era (Complete)", "compilation", "Compilación Spotify de la Era Judas."),
]


# Base43 Extension System Data
def get_base43_phases():
    """Get all 43 phases from the Base43 system"""
    base43 = create_base43_instance(432.0)
    phases_data = []
    
    for phase in base43.phases:
        phases_data.append({
            "id": phase.id,
            "name": phase.name,
            "description": phase.description,
            "frequency": phase.frequency,
            "color": phase.color,
            "gem": phase.gem,
            "parent_phase": phase.parent_phase,
            "children": phase.children,
            "octave_equivalent": phase.octave_equivalent,
            "is_harmonic_root": phase.id in [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42]
        })
    
    return phases_data


BASE43_SYSTEM = {
    "seed_frequency": 432.0,
    "total_phases": 43,
    "phases": get_base43_phases(),
    "harmonic_intervals": {
        "perfect_fifth": 3.0,
        "major_third": 5.0,
        "minor_third": 6.0,
        "major_second": 9.0,
        "minor_second": 16.0
    },
    "frequency_operations": {
        "multiply": "Multiply frequencies for combination",
        "divide": "Divide frequencies for subdivision",
        "harmonize": "Find harmonic relationships",
        "normalize": "Normalize to octave range (20-432Hz)"
    }
}


def seed_if_empty(db: Session) -> None:
    if db.query(Tenant).count():
        return

    tenant = Tenant(slug="belentani", name="DUCK STUDIOS // BELENTANI", plan="omega")
    db.add(tenant)
    db.flush()

    db.add(
        User(
            tenant_id=tenant.id,
            email="studio@belentani.es",
            display_name="Belentani",
            password_hash=hash_password("omega432"),
            role="owner",
        )
    )

    for slug, title, kind, summary in WORKS:
        work = Work(
            tenant_id=tenant.id,
            slug=slug,
            title=title,
            kind=kind,
            status="live",
            summary=summary,
        )
        db.add(work)
        db.flush()
        db.add(Release(work_id=work.id, platform="archive", url="https://belentani.es", label="Open archive"))

    for chapter in CHAPTERS:
        db.add(ExperienceChapter(**chapter))

    db.commit()
