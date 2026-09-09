from __future__ import annotations

LAB_CATEGORIES = ["IMAGE", "VIDEO", "AUDIO", "CODE", "AGENTS", "PSYCHE"]

LAB_MODULES = [
    {"id": "neural-chat", "name": "NEURAL CHAT", "cat": "AGENTS", "blurb": "JUDAS_CORE // LIVE"},
    {"id": "vision-forge", "name": "VISION FORGE", "cat": "IMAGE", "blurb": "IMAGE_GEN // FLUX"},
    {"id": "beat-forge", "name": "BEAT FORGE", "cat": "AUDIO", "blurb": "TONE.JS LIVE dark pop / R&B"},
    {"id": "tarot-oracle", "name": "TAROT ORACLE", "cat": "PSYCHE", "blurb": "3 cartas · 22 arcanos"},
    {"id": "dream-decoder", "name": "DREAM DECODER", "cat": "PSYCHE", "blurb": "ONIRIC_SCAN"},
    {"id": "darvo-detector", "name": "DARVO DETECTOR", "cat": "PSYCHE", "blurb": "MANIPULATION_SCAN"},
    {"id": "song-writer", "name": "SONG WRITER", "cat": "AUDIO", "blurb": "LYRIC_FORGE dark pop"},
    {"id": "archetype-scan", "name": "ARCHETYPE SCAN", "cat": "PSYCHE", "blurb": "5 firmas"},
    {"id": "psyche-scan", "name": "PSYCHE SCAN", "cat": "PSYCHE", "blurb": "DEEP_ANALYSIS"},
    {"id": "prompt-improver", "name": "PROMPT IMPROVER", "cat": "CODE", "blurb": "OPTIMIZER for Vision Forge"},
    {"id": "video-drift", "name": "CRYSTAL DRIFT", "cat": "VIDEO", "blurb": "Motion / glitch timeline"},
    {"id": "agent-swarm", "name": "ENJAMBRE", "cat": "AGENTS", "blurb": "Multi-agent creative ops"},
]


def by_category(cat: str | None = None):
    if not cat or cat == "TODOS":
        return LAB_MODULES
    return [m for m in LAB_MODULES if m["cat"] == cat]
