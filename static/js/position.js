/**
 * Randomly positions each widget within a defined grid layout,
 * simulating the appearance of a real operating system desktop.
 *
 * @param {number} widthThreshold - The minimum viewport width (in pixels) required to enable positioning. Default is 768 pixels.
 * @param {number} cols - The number of columns in the grid layout. Default is 24.
 * @param {number} rows - The number of rows in the grid layout. Default is 12.
 * @param {number} padding - The padding (in pixels) around the widgets. Default is 20 pixels.
 */
const randomlyPositionWidgets = (
  widthThreshold = 768,
  cols = 24,
  rows = 12,
  padding = 20,
) => {
  const viewportWidth = window.innerWidth;
  const viewportHeight = window.innerHeight;

  if (viewportWidth < widthThreshold) {
    return;
  }

  const widgets = document.querySelectorAll(".widget");

  const cellWidth = viewportWidth / cols;
  const cellHeight = viewportHeight / rows;

  const positions = Array.from(widgets).map((widget) => {
    const widgetWidth = widget.offsetWidth;
    const widgetHeight = widget.offsetHeight;

    const randomRow = Math.floor(Math.random() * rows);
    const randomCol = Math.floor(Math.random() * cols);

    const randomX = Math.min(
      randomCol * cellWidth + (cellWidth - widgetWidth) / 2 + padding,
      viewportWidth - widgetWidth - padding,
    );
    const randomY = Math.min(
      randomRow * cellHeight + (cellHeight - widgetHeight) / 2 + padding,
      viewportHeight - widgetHeight - padding,
    );

    return {
      widget,
      x: Math.max(randomX, padding),
      y: Math.max(randomY, padding),
    };
  });

  positions.forEach(({ widget, x, y }) => {
    widget.style.left = `${x}px`;
    widget.style.top = `${y}px`;
  });
};

randomlyPositionWidgets();
