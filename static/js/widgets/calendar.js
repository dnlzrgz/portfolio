{
  const today = new Date();
  let currentMonth = today.getMonth();
  let currentYear = today.getFullYear();

  const monthElement = document.querySelector(
    "[data-js-calendar-current-month]",
  );
  const daysList = document.querySelector(".calendar__days");
  const nextButton = document.querySelector("[data-js-calendar-next]");
  const prevButton = document.querySelector("[data-js-calendar-prev]");

  const renderCalendar = (month, year) => {
    monthElement.textContent = new Date(year, month).toLocaleString("default", {
      month: "long",
      year: "numeric",
    });

    daysList.innerHTML = "";

    const firstDay = new Date(year, month, 1).getDay(); // 0 = Sunday, 1 = Monday, ..., 6 = Saturday
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    for (let i = 0; i < firstDay; i++) {
      const emptyCell = document.createElement("li");
      emptyCell.classList.add("calendar__day", "empty");
      daysList.appendChild(emptyCell);
    }

    for (let day = 1; day <= daysInMonth; day++) {
      const dayCell = document.createElement("li");
      dayCell.classList.add("calendar__day");
      dayCell.textContent = day;

      if (
        day === today.getDate() &&
        month === today.getMonth() &&
        year === today.getFullYear()
      ) {
        dayCell.classList.add("today");
      }

      daysList.appendChild(dayCell);
    }
  };

  nextButton.addEventListener("click", () => {
    currentMonth--;

    if (currentMonth < 0) {
      currentMonth = 11;
      currentYear--;
    }

    renderCalendar(currentMonth, currentYear);
  });

  prevButton.addEventListener("click", () => {
    currentMonth++;

    if (currentMonth > 11) {
      currentMonth = 0;
      currentYear++;
    }

    renderCalendar(currentMonth, currentYear);
  });

  renderCalendar(currentMonth, currentYear);
}
