(function hudClock() {
  const bar = document.querySelector(".hud-bar");
  if (!bar) return;
  const time = document.createElement("span");
  time.id = "hud-time";
  bar.appendChild(time);
  const tick = () => {
    time.textContent = "TIME:" + new Date().toISOString().slice(11, 19) + "Z";
  };
  tick();
  setInterval(tick, 1000);
})();
