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
