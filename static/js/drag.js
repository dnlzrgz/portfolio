{
  /**
   * Adds a draggable effect to the windows/widgets in the home page.
   **/

  const windows = document.querySelectorAll(".window");
  let zIndex = 1;

  windows.forEach((win) => {
    const title = win.querySelector(".title");

    win.addEventListener("mousedown", () => {
      zIndex += 1;
      win.style.zIndex = zIndex;
    });

    title.addEventListener("mousedown", (e) => {
      title.classList.add("is-dragging");

      let left = win.offsetLeft;
      let top = win.offsetTop;

      let startX = e.pageX;
      let startY = e.pageY;

      const drag = (e) => {
        e.preventDefault();
        win.style.left = left + (e.pageX - startX) + "px";
        win.style.top = top + (e.pageY - startY) + "px";
      };

      const mouseUp = () => {
        title.classList.remove("is-dragging");

        document.removeEventListener("mousemove", drag);
        document.removeEventListener("mouseup", mouseUp);
      };

      document.addEventListener("mousemove", drag);
      document.addEventListener("mouseup", mouseUp);
    });
  });
}
