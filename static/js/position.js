{
  /**
   * Randomly positions each window/widget within a defined grid layout,
   * simulating the appearance of a real operating system desktop.
   **/
  const windows = document.querySelectorAll(".window");

  const cols = 24;
  const rows = 24;

  const viewportWidth = window.innerWidth;
  const viewportHeight = window.innerHeight;

  const cellWidth = viewportWidth / cols;
  const cellHeight = viewportHeight / rows;

  const padding = 20;

  const positions = Array.from(windows).map((win) => {
    const winWidth = win.offsetWidth;
    const winHeight = win.offsetHeight;

    const randomRow = Math.floor(Math.random() * rows); // Use rows directly
    const randomCol = Math.floor(Math.random() * cols); // Use cols directly

    const randomX = Math.min(
      randomCol * cellWidth + (cellWidth - winWidth) / 2 + padding,
      viewportWidth - winWidth - padding,
    );
    const randomY = Math.min(
      randomRow * cellHeight + (cellHeight - winHeight) / 2 + padding,
      viewportHeight - winHeight - padding,
    );

    return {
      win,
      x: Math.max(randomX, padding),
      y: Math.max(randomY, padding),
    };
  });

  positions.forEach(({ win, x, y }) => {
    win.style.left = `${x}px`;
    win.style.top = `${y}px`;
  });
}
