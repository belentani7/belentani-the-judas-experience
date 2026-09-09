document.addEventListener("keydown", (e) => {
  if (e.key === "j" && !e.metaKey && !e.ctrlKey) {
    const first = document.querySelector(".chapter");
    if (first) first.scrollIntoView({ behavior: "smooth" });
  }
});
