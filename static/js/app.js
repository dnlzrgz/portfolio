/**
 * Dark/Light theme switch
 **/
const switchTheme = document.querySelector("[data-js-switch-theme]");
const prefersDarkScheme = window.matchMedia(
  "(prefers-color-scheme: dark)",
).matches;

const applyTheme = (isDark) => {
  document.documentElement.classList.toggle("dark", isDark);
  switchTheme.checked = isDark;
};

const getCurrentTheme = () => {
  const savedTheme = localStorage.getItem("theme");
  return savedTheme ? savedTheme === "dark" : prefersDarkScheme;
};

const toggleTheme = () => {
  const isDark = switchTheme.checked;
  localStorage.setItem("theme", isDark ? "dark" : "light");
  applyTheme(isDark);
};

window.addEventListener("load", () => {
  applyTheme(getCurrentTheme());
});
switchTheme.addEventListener("change", toggleTheme);

/**
 * Overlay menu
 **/
const menuOverlay = document.querySelector("[data-js-menu]");
const menuOverlayExpand = document.querySelector("[data-js-menu-expand]");
const menuOverlayCollapse = document.querySelector("[data-js-menu-collapse]");

menuOverlayExpand.addEventListener("click", () => {
  menuOverlay.classList.add("open");
  document.body.classList.add("hide-scroll");
});

menuOverlayCollapse.addEventListener("click", () => {
  menuOverlay.classList.remove("open");
  document.body.classList.remove("hide-scroll");
});
