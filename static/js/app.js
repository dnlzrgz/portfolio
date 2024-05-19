const root = document.documentElement;
const footer = document.querySelector(".footer");

const updateTheme = (isDark) => {
  if (isDark) {
    root.style.setProperty("--background", "#0a0a0a");
    root.style.setProperty("--foreground", "#fafafa");
    root.style.setProperty("--gray", "#ebebeb");

    footer?.classList.add("footer--dark");
  } else {
    root.style.setProperty("--background", "#ffffff");
    root.style.setProperty("--foreground", "#000000");
    root.style.setProperty("--gray", "#474747");

    footer?.classList.remove("footer--dark");
  }
};

const initializeThemeToggle = () => {
  const toggle = document.getElementById("toggle");

  if (toggle) {
    const savedTheme = localStorage.getItem("theme");
    let isDark = false;

    if (savedTheme) {
      isDark = savedTheme === "dark";
    } else {
      isDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
    }

    toggle.checked = isDark;
    updateTheme(isDark);

    toggle.addEventListener("change", (e) => {
      const isChecked = e.target.checked;
      updateTheme(isChecked);
      localStorage.setItem("theme", isChecked ? "dark" : "light");
    });
  }
};

document.addEventListener("DOMContentLoaded", initializeThemeToggle);
document.body.addEventListener("htmx:afterSwap", initializeThemeToggle);
