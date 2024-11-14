/**
 * Enables draggable-like effect for elements with the class "widget".
 * Is only activated if the viewport width is greater than or equal to the specified width threshold.
 *
 * @param {number} widthThreshold - The minimum viewport width (in pixels) required to enable dragging. Default is 768 pixels.
 */
const addDraggable = (widthThreshold = 768) => {
  const viewportWidth = window.innerWidth;

  if (viewportWidth < widthThreshold) {
    return;
  }

  const widgets = document.querySelectorAll(".widget");
  let zIndex = 1;

  const bringToFront = (widget) => {
    zIndex += 1;
    widget.style.zIndex = zIndex;
  };

  const handleDrag = (widget, e, isTouchEvent) => {
    const title = widget.querySelector(".title");
    title.classList.add("is-dragging");

    const left = widget.offsetLeft;
    const top = widget.offsetTop;
    const startX = isTouchEvent ? e.touches[0].pageX : e.pageX;
    const startY = isTouchEvent ? e.touches[0].pageY : e.pageY;

    const drag = (e) => {
      e.preventDefault();
      const pageX = isTouchEvent ? e.touches[0].pageX : e.pageX;
      const pageY = isTouchEvent ? e.touches[0].pageY : e.pageY;
      widget.style.left = left + (pageX - startX) + "px";
      widget.style.top = top + (pageY - startY) + "px";
    };

    const endDrag = () => {
      title.classList.remove("is-dragging");
      document.removeEventListener(
        isTouchEvent ? "touchmove" : "mousemove",
        drag,
      );
      document.removeEventListener(
        isTouchEvent ? "touchend" : "mouseup",
        endDrag,
      );
    };

    document.addEventListener(isTouchEvent ? "touchmove" : "mousemove", drag);
    document.addEventListener(isTouchEvent ? "touchend" : "mouseup", endDrag);
  };

  widgets.forEach((widget) => {
    const title = widget.querySelector(".title");

    const bringToFrontHandler = () => bringToFront(widget);
    widget.addEventListener("mousedown", bringToFrontHandler);
    widget.addEventListener("touchstart", bringToFrontHandler);

    title.addEventListener("mousedown", (e) => handleDrag(widget, e, false));

    title.addEventListener("touchstart", (e) => {
      bringToFront(widget);
      handleDrag(widget, e, true);
    });
  });
};

addDraggable();
