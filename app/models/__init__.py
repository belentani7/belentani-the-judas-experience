from app.models.entities import ExperienceChapter, Gem, Release, Tenant, User, Work, uid


CANONICAL_TENANT = Tenant(
    id="ten_belentani",
    slug="belentani",
    name="BELENTANI // OMEGA CORE",
)


SEED_USER = User(
    id="usr_pedro",
    tenant_id=CANONICAL_TENANT.id,
    email="studio@belentani.es",
    password_hash="omega",  # stub — demo only
    display_name="Pedro Marcos Santos Belentani",
    role="artist",
)


WORKS = [
    Work(
        id=uid("wrk"),
        tenant_id=CANONICAL_TENANT.id,
        title="Therapist",
        kind="single",
        status="live",
        synopsis="Electrónica industrial que disecciona la psique. La herida se vuelve estructura.",
        frequency="432Hz",
        platform="Spotify",
        href="https://belentani.es",
    ),
    Work(
        id=uid("wrk"),
        tenant_id=CANONICAL_TENANT.id,
        title="Mon Amour",
        kind="single",
        status="live",
        synopsis="Dark pop y R&B visceral. Una declaración de amor en medio del caos digital.",
        frequency="432Hz",
        platform="Apple Music",
        href="https://belentani.es",
    ),
    Work(
        id=uid("wrk"),
        tenant_id=CANONICAL_TENANT.id,
        title="Apaga a Luz",
        kind="single",
        status="live",
        synopsis="Soul y pulso cautivador. El cristal absorbe la luz y la devuelve como memoria.",
        frequency="432Hz",
        platform="Spotify",
        href="https://belentani.es",
    ),
    Work(
        id=uid("wrk"),
        tenant_id=CANONICAL_TENANT.id,
        title="Lento",
        kind="single",
        status="archive",
        synopsis="R&B alternativo. La vulnerabilidad radical como mecanismo de supervivencia.",
        frequency="432Hz",
        platform="YouTube",
        href="https://belentani.es",
    ),
    Work(
        id=uid("wrk"),
        tenant_id=CANONICAL_TENANT.id,
        title="I Wrote a Song",
        kind="session",
        status="studio",
        synopsis="Judas Studio Session. El registro se convierte en canción; la canción, en comunidad.",
        frequency="432Hz",
        platform="SoundCloud",
        href="https://belentani.es",
    ),
    Work(
        id=uid("wrk"),
        tenant_id=CANONICAL_TENANT.id,
        title="The Judas Experience",
        kind="experience",
        status="omega",
        synopsis="Experiencia inmersiva de ciencia ficción emocional: neón, desierto, glitch y transmutación.",
        frequency="432Hz",
        platform="buildao.space / belentani.es",
        href="/judas",
    ),
]


RELEASES = [
    Release(
        id=uid("rel"),
        tenant_id=CANONICAL_TENANT.id,
        title="JUDAS ERA (COMPLETE)",
        year=2026,
        catalog="BEL-ERA-01",
        tracks=["Therapist", "Mon Amour", "Apaga a Luz", "Lento", "Heart Breaking"],
    ),
    Release(
        id=uid("rel"),
        tenant_id=CANONICAL_TENANT.id,
        title="MON AMOUR & ORIGINS",
        year=2025,
        catalog="BEL-ESS-02",
        tracks=["Mon Amour", "Origins"],
    ),
]


CHAPTERS = [
    ExperienceChapter(
        id="ch_01",
        index=1,
        code="FASE_01",
        title="La herida se convierte en arquitectura viva",
        body="Belentani diseña una obra inmersiva donde la imagen, el sonido y el cristal comparten una misma respiración. Judas aparece como tensión dramática; el autor y su visión siguen al centro.",
        prompt="Cristal esmerilado. Rojo neón. Desierto. Glitch.",
    ),
    ExperienceChapter(
        id="ch_02",
        index=2,
        code="FASE_02",
        title="El mito no reemplaza al autor; lo intensifica",
        body="La Era Judas es un universo artístico. Sus símbolos no describen hechos biográficos: organizan una estética de tensión, memoria y poder creativo.",
        prompt="Doble figura. Autoría total. Ecosistema vivo.",
    ),
    ExperienceChapter(
        id="ch_03",
        index=3,
        code="FASE_03",
        title="El diamante no es un objeto; es una memoria cristalizada",
        body="La pieza funciona como llave simbólica: una arquitectura de luz que recoge la tensión entre sombra, deseo y supervivencia.",
        prompt="Llave dorada. Frecuencia 432. Transmisión activa.",
    ),
    ExperienceChapter(
        id="ch_04",
        index=4,
        code="FASE_04",
        title="El beso como umbral",
        body="Judas funciona como una máscara dramática: deseo, quiebre y eco. No es el centro; es el borde que empuja la obra a moverse.",
        prompt="Máscara. Umbral. Quiebre.",
    ),
    ExperienceChapter(
        id="ch_05",
        index=5,
        code="FASE_05",
        title="Ser muchos para poder seguir siendo uno",
        body="Input: la traición recibida. Data: el dolor archivado. Output: la voz transmutada. Hack: la sanación conceptual.",
        prompt="Zion. Guerrero y ángel. Código Judas.",
    ),
]


GEMS = [
    Gem(id="gem_01", code="GEMA_01", name="PEDRO", archetype="LA ROCA", glyph="⬡"),
    Gem(id="gem_02", code="GEMA_02", name="MARCOS", archetype="EL CRONISTA", glyph="◉"),
    Gem(id="gem_03", code="GEMA_03", name="SANTOS", archetype="LA ANTENA", glyph="⌬"),
    Gem(id="gem_04", code="GEMA_04", name="BELENTANI", archetype="EL ARTEFACTO", glyph="▣"),
    Gem(id="gem_05", code="GEMA_05", name="THE HUMAN", archetype="LA INTERFAZ", glyph="⏣"),
]


PILLARS = [
    {
        "title": "Autoría total",
        "body": "Belentani define el texto, el sonido y la dirección visual.",
    },
    {
        "title": "Doble figura",
        "body": "El autor y el personaje conviven para amplificar la tensión narrativa.",
    },
    {
        "title": "Cristal y neón",
        "body": "La estética traduce pulsión, memoria y magnetismo visual.",
    },
    {
        "title": "Ecosistema vivo",
        "body": "Cada módulo aporta una pieza al mismo cuerpo creativo.",
    },
    {
        "title": "Transmutación",
        "body": "La herida se convierte en escena, ritmo y presencia.",
    },
]
