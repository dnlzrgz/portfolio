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
  cols = 16,
  rows = 24,
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

  const minXY = padding;
  const maxX = viewportWidth - padding;
  const maxY = viewportHeight - padding;

  for (let i = 0; i < widgets.length; i++) {
    const widget = widgets[i];
    const widgetWidth = widget.offsetWidth;
    const widgetHeight = widget.offsetHeight;

    const randomRow = (Math.random() * rows) | 0;
    const randomCol = (Math.random() * cols) | 0;
    const baseX = randomCol * cellWidth + (cellWidth - widgetWidth) / 2;
    const baseY = randomRow * cellHeight + (cellHeight - widgetHeight) / 2;
    const randomX = Math.max(minXY, Math.min(baseX, maxX - widgetWidth));
    const randomY = Math.max(minXY, Math.min(baseY, maxY - widgetHeight));

    widget.style.left = `${randomX}px`;
    widget.style.top = `${randomY}px`;
  }
};

randomlyPositionWidgets();
