document.documentElement.classList.add("js");

document.addEventListener("keydown", (event) => {
  if (event.key === "Tab") {
    document.body.classList.add("using-keyboard");
  }
});

document.addEventListener("mousedown", () => {
  document.body.classList.remove("using-keyboard");
});

const navToggle = document.querySelector("[data-nav-toggle]");
const siteNav = document.querySelector("[data-site-nav]");

if (navToggle && siteNav) {
  const syncNav = (open) => {
    navToggle.setAttribute("aria-expanded", String(open));
    siteNav.dataset.open = String(open);
  };

  syncNav(false);

  navToggle.addEventListener("click", () => {
    syncNav(siteNav.dataset.open !== "true");
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      syncNav(false);
      navToggle.focus();
    }
  });
}
