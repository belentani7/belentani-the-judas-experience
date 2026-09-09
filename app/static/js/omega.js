async function tickHud() {
  try {
    const res = await fetch("/api/hud");
    if (!res.ok) return;
    const hud = await res.json();
    const bar = document.querySelector(".hud-bar span");
    if (bar) {
      bar.textContent = `LAT:${hud.lat}°N·LON:${hud.lon}°E·FREQ:${hud.freq}·NODE:${hud.node}`;
    }
  } catch (_) {
    /* offline kernel */
  }
}

setInterval(tickHud, 15000);
