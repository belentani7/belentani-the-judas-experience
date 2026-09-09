from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.experience import ExperienceChapter
from app.models.release import Release
from app.models.tenant import Tenant
from app.models.user import User
from app.models.work import Work
from app.services import hash_password

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
