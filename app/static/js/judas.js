document.querySelectorAll("[data-gem]").forEach((btn) => {
  btn.addEventListener("click", async () => {
    const id = btn.getAttribute("data-gem");
    const res = await fetch(`/api/gems/${id}/toggle`, { method: "POST" });
    const data = await res.json();
    btn.classList.toggle("active", data.active);
    const state = btn.querySelector(".state");
    if (state) state.textContent = data.active ? "ACTIVA" : "INACTIVA";
  });
});
