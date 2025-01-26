{
  const chars = "↑↓←→↖↗↘↙↔↕";
  const rootStyles = getComputedStyle(document.documentElement);
  const colors = [
    rootStyles.getPropertyValue("--primary-light").trim(),
    rootStyles.getPropertyValue("--primary").trim(),
    rootStyles.getPropertyValue("--primary-dark").trim(),
    rootStyles.getPropertyValue("--orange-dark").trim(),
    rootStyles.getPropertyValue("--orange").trim(),
    rootStyles.getPropertyValue("--orange-light").trim(),
  ];
  let white = rootStyles.getPropertyValue("--white").trim();

  if (
    window.matchMedia &&
    window.matchMedia("(prefers-color-scheme: dark)").matches
  ) {
    white = rootStyles.getPropertyValue("--black").trim();
  }

  let circles = [];
  let gridSize = 20;
  let grid = [];

  function setup() {
    const { offsetWidth, offsetHeight } = document.getElementById("abstract");
    const canvas = createCanvas(offsetWidth, offsetHeight);

    canvas.parent("abstract");

    gridSize = Math.min(width, height) / 20;
    grid = createGrid();
  }

  function draw() {
    background(white);
    drawGrid();

    for (let i = 0; i < circles.length; i++) {
      circles[i].update();
      circles[i].display();
      checkCollision(circles[i]);
    }

    circles = circles.filter((circle) => !circle.isFinished());
  }

  function mousePressed(event) {
    if (mouseX >= 0 && mouseX <= width && mouseY >= 0 && mouseY <= height) {
      event.preventDefault();
      event.stopPropagation();

      let newCircle = new Circle(mouseX, mouseY);
      circles.push(newCircle);
    }
  }

  function createGrid() {
    const rows = Math.floor(height / gridSize) + 2;
    const cols = Math.floor(width / gridSize) + 2;
    const grid = [];

    for (let i = 0; i < rows; i++) {
      for (let j = 0; j < cols; j++) {
        grid.push({
          x: j * gridSize,
          y: i * gridSize,
          textSize: 30,
          charIndex: 0,
          color: colors[0],
          text: "◤",
        });
      }
    }

    return grid;
  }

  function drawGrid() {
    for (let i = 0; i < grid.length; i++) {
      fill(grid[i].color);
      noStroke();
      textSize(grid[i].textSize);
      text(grid[i].text, grid[i].x, grid[i].y);
    }
  }

  function checkCollision(circle) {
    for (let i = 0; i < grid.length; i++) {
      const { x: centerX, y: centerY, radius } = circle;

      let rectX = grid[i].x + gridSize / 2;
      let rectY = grid[i].y + gridSize / 2;
      let a = atan2(rectY - centerY, rectX - centerX);
      let rX = centerX + radius * Math.cos(a);
      let rY = centerY + radius * Math.sin(a);
      let cc = width;

      if (dist(rectX, rectY, centerX, centerY) <= circle.radius) {
        grid[i].color = color(10);
        charIndex = int(
          map(dist(rectX, rectY, rX, rY), 0, cc, 0, chars.length),
        );

        if (dist(rectX, rectY, rX, rY) > cc) {
          grid[i].color = colors[0];
          grid[i].text = "◤";
        } else {
          colorIndex = int(
            map(dist(rectX, rectY, rX, rY), 0, cc, 0, colors.length),
          );

          grid[i].color = colors[colorIndex];
          grid[i].text = chars[charIndex];
        }
      }
    }
  }

  class Circle {
    constructor(x, y) {
      this.x = x;
      this.y = y;
      this.radius = 1;
    }

    update() {
      this.radius += 5;
    }

    display() {
      noFill();
      stroke(0, 0);
      ellipse(this.x, this.y, this.radius, this.radius);
    }

    isFinished() {
      return this.radius >= width * 3;
    }
  }
}
