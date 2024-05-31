const root = document.documentElement;

const themes = {
  dark: {
    "--background": "#0a0a0a",
    "--foreground": "#fafafa",
    "--gray": "#ebebeb",
    "--blue": "#3cbbb1",
  },
  light: {
    "--background": "#fafafa",
    "--foreground": "#0a0a0a",
    "--gray": "#474747",
    "--blue": "#1481ba",
  },
};

const updateTheme = (isDark) => {
  const theme = isDark ? themes.dark : themes.light;
  for (const [key, value] of Object.entries(theme)) {
    root.style.setProperty(key, value);
  }
};

const initializeThemeToggle = () => {
  const toggle = document.getElementById("toggle");
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
};

document.addEventListener("DOMContentLoaded", initializeThemeToggle);
document.body.addEventListener("htmx:afterSwap", initializeThemeToggle);
