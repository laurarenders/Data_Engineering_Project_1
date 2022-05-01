"use strict";

function filterOpBedrijven(bedrijfsnaam) {
  localStorage.setItem("zoekterm", bedrijfsnaam);
  window.location.href="./bedrijfslijst.html";
};

let zoeken = document.getElementById("submit");
let bedrijfsnaam;

document.addEventListener('keypress', function (e) {  // Geen enter in form
  if (e.keyCode === 13 || e.which === 13) {
      e.preventDefault();
      return false;
  }
  
});

zoeken.onclick = () => {
  let bedrijfsnaam = document.getElementById("companyname").value;
  if(bedrijfsnaam)
    filterOpBedrijven(bedrijfsnaam);
}


window.onload = localStorage.clear();
