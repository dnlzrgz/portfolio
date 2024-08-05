/**
 * Dark/Light theme switch
 **/
const switchTheme = document.querySelector("[data-js-switch-theme]");
const prefersDarkScheme = window.matchMedia(
  "(prefers-color-scheme: dark)",
).matches;

const toggleTheme = () => {
  if (switchTheme.checked || prefersDarkScheme) {
    switchTheme.checked = true;
    document.documentElement.classList.add("dark");
    return;
  }

  document.documentElement.classList.remove("dark");
};

window.addEventListener("load", toggleTheme);
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
