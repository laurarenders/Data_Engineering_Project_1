"use strict";

// Surfen naar bedrijvenlijst
function filterOpBedrijven(bedrijfsnaam) {
  localStorage.setItem("zoekterm", bedrijfsnaam);
  window.location.href = `/bedrijfslijst.html?bedrijven=${bedrijfsnaam}`;
};

// Surfen naar sectorlijsten
function filterOpSector(sector) {
  localStorage.setItem("sector", sector);
  window.location.href = `/sectorlijst.html?sectoren=${sector}`;
}

let zoeken = document.getElementById("submit");
let bedrijfsnaam;
let sector;

// Enter disablen in de form
document.addEventListener('keypress', function (e) {
  if (e.keyCode === 13 || e.which === 13) {
    e.preventDefault();
    return false;
  }

});

// Bepalen naar welke pagina te surfen
zoeken.onclick = () => {
  let path = window.location.pathname;
  let page = path.split("/").pop();

  if (page === "perSector.html") {
    let sector = document.getElementById("sector").value;
    if (sector)
      filterOpSector(sector);
  } else {

    let bedrijfsnaam = document.getElementById("companyname").value;
    if (bedrijfsnaam)
      filterOpBedrijven(bedrijfsnaam);
  }


}

// Wanneer pagina wordt geladen -> clear local storage
window.onload = localStorage.clear();
