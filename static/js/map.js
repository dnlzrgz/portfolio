const map = L.map("map", {
  attributionControl: false,
  zoomControl: false,
}).setView([46.51682, 6.62914], 12);

L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {}).addTo(map);
