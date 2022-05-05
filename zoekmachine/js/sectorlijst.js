// import { connect } from "./connection.js";
const connect = import("./connection.js");

function weergaveSectoren(sector) {

  const connection = connect;

  let sectoren = ["Toerisme", "ICT", "Transport"]; // Bij connectie met db dit in commentaar, querry er onder uit commentaar
  // let bedrijven = bedrijven(bedrijfsnaam) // Met spreadoperator nog omzetten naar array
  // Controleren of bedrijf is gevonden, anders gepaste boodschap

  let title = document.getElementById("title");
  let h1 = document.createElement("h1");
  let text = document.createTextNode(`Sectoren die "${sector}" bevatten`);

  h1.append(text);
  title.append(h1);

  sectoren.forEach((elem, ind, val) => {
    let table = document.getElementById("sectoren");

    let nieuweRij = document.createElement("tr");
    if (ind % 2 == 0) {
      nieuweRij.style.backgroundColor = "#837569";
      nieuweRij.style.color = "white";
    } else {
      nieuweRij.style.backgroundColor = "#f2f2f2";
    }

    let aGedetaileerd = document.createElement("a");
    aGedetaileerd.setAttribute("id", elem);
    aGedetaileerd.href = `./sectorGedetailleerd.html`;
    aGedetaileerd.style.fontWeight = "900";
    if (ind % 2 == 0) {
      aGedetaileerd.setAttribute("class", "linkToDetailedInfoEven");
    } else {
      aGedetaileerd.setAttribute("class", "linkToDetailedInfoOdd");

    }

    let tdSector = document.createElement("td");
    let sector = document.createTextNode(elem);
    tdSector.append(sector);
    aGedetaileerd.append(tdSector);

    nieuweRij.append(aGedetaileerd);

    table.append(nieuweRij);

    aGedetaileerd.onclick = () => {
      localStorage.setItem("sector", aGedetaileerd.id);
    };
  });

};

let sectorNaam = localStorage.getItem("sector");

weergaveSectoren(sectorNaam)
