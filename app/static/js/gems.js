document.addEventListener("DOMContentLoaded", () => {
  const gems = document.querySelectorAll("[data-gem]");
  const key = "judas-gems";
  const saved = new Set(JSON.parse(localStorage.getItem(key) || "[]"));
  gems.forEach((g) => {
    if (saved.has(g.dataset.gem)) g.classList.add("active");
    g.addEventListener("click", () => {
      g.classList.toggle("active");
      const next = [...document.querySelectorAll("[data-gem].active")].map((n) => n.dataset.gem);
      localStorage.setItem(key, JSON.stringify(next));
    });
  });
});
