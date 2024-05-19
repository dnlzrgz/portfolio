const root = document.documentElement;
const toggle = document.getElementById("toggle");
const footer = document.querySelector("footer");

const updateTheme = (isDark) => {
  if (isDark) {
    root.style.setProperty("--background", "#0a0a0a");
    root.style.setProperty("--foreground", "#fafafa");
    root.style.setProperty("--gray", "#ebebeb");

    footer.classList.add("footer--dark");
  } else {
    root.style.setProperty("--background", "#ffffff");
    root.style.setProperty("--foreground", "#000000");
    root.style.setProperty("--gray", "#474747");

    footer.classList.remove("footer--dark");
  }
};

const prefersDarkScheme = window.matchMedia(
  "(prefers-color-scheme: dark)",
).matches;
toggle.checked = prefersDarkScheme;
updateTheme(prefersDarkScheme);

toggle.addEventListener("change", (e) => {
  updateTheme(e.target.checked);
});
