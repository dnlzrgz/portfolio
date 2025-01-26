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

    const fragment = document.createDocumentFragment();
    const firstDay = new Date(year, month, 1).getDay(); // 0 = Sunday, 1 = Monday, ..., 6 = Saturday
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    for (let i = 0; i < firstDay; i++) {
      const emptyCell = document.createElement("li");
      emptyCell.className = "calendar__day empty";
      fragment.appendChild(emptyCell);
    }

    for (let day = 1; day <= daysInMonth; day++) {
      const dayCell = document.createElement("li");
      dayCell.className = "calendar__day";
      dayCell.textContent = day;

      if (
        day === today.getDate() &&
        month === today.getMonth() &&
        year === today.getFullYear()
      ) {
        dayCell.className = "calendar__day today";
      }

      fragment.appendChild(dayCell);
    }

    daysList.innerHTML = "";
    daysList.appendChild(fragment);
  };

  nextButton.addEventListener("click", () => {
    currentMonth = (currentMonth + 1) % 12;
    currentYear += currentMonth === 0 ? 1 : 0;
    renderCalendar(currentMonth, currentYear);
  });

  prevButton.addEventListener("click", () => {
    currentMonth = (currentMonth - 1 + 12) % 12;
    currentYear -= currentMonth === 11 ? 1 : 0;
    renderCalendar(currentMonth, currentYear);
  });

  renderCalendar(currentMonth, currentYear);
}
