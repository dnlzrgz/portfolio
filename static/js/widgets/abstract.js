{
  const chars = "↑↓←→↖↗↘↙↔↕";
  const colors = [
    "#dc8a78",
    "#dd7878",
    "#ea76cb",
    "#8839ef",
    "#d20f39",
    "#e64553",
    "#fe640b",
    "#df8e1d",
    "#40a02b",
    "#179299",
    "#04a5e5",
    "#209fb5",
    "#1e66f5",
    "#7287fd",
  ];
  const len_colors = colors.length;

  let circles = [];
  let gridSpacing = 0;
  let gridSize = 20;
  let grid = [];
  let charIndex = 0;
  let colorIndex = 0;

  function setup() {
    const canvas = createCanvas(400, 400);
    canvas.parent("abstract");

    gridSize = min(width, height) / 20;

    grid = createGrid();
  }

  function draw() {
    background("#fff");
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
    let rows = floor(height / (gridSize + gridSpacing)) + 2;
    let cols = floor(width / (gridSize + gridSpacing)) + 2;
    let grid = [];

    for (let i = 0; i < rows; i++) {
      for (let j = 0; j < cols; j++) {
        grid.push({
          x: j * (gridSize + gridSpacing),
          y: i * (gridSize + gridSpacing),
          textSize: 30,
          charIndex: 0,
          color: colors[len_colors - 1],
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
      let centerX = circle.x;
      let centerY = circle.y;
      let radius = circle.radius;

      let rectX = grid[i].x + gridSize / 2;
      let rectY = grid[i].y + gridSize / 2;

      let a = atan2(rectY - centerY, rectX - centerX);

      let rX = centerX + radius * cos(a);
      let rY = centerY + radius * sin(a);

      let cc = width;
      if (dist(rectX, rectY, centerX, centerY) <= circle.radius) {
        grid[i].color = color(10);
        charIndex = int(
          map(dist(rectX, rectY, rX, rY), 0, cc, 0, chars.length),
        );

        if (dist(rectX, rectY, rX, rY) > cc) {
          grid[i].color = colors[len_colors - 1];
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
