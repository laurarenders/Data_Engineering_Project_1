// import { connect } from "./connection.js";
const connect = import("./connection.js");

function weergaveBedrijven(bedrijfsnaam) {

  const connection = connect;

  let bedrijven = [bedrijfsnaam, "HoGent", "Boston Dynamics", "UGent"]; // Bij connectie met db dit in commentaar, querry er onder uit commentaar
  // let bedrijven = bedrijven(bedrijfsnaam) // Met spreadoperator nog omzetten naar array
  // Controleren of bedrijf is gevonden, anders gepaste boodschap

  let title = document.getElementById("title");
  let h1 = document.createElement("h1");
  let text = document.createTextNode(`Bedrijven die de zoekterm "${bedrijfsnaam}" bevatten`);

  h1.append(text);
  title.append(h1);

  bedrijven.forEach((elem, ind, val) => {
    let table = document.getElementById("bedrijven");

    let nieuweRij = document.createElement("tr");
    if(ind % 2 == 0) {
      nieuweRij.style.backgroundColor = "#837569";
      nieuweRij.style.color = "white";
    }
    else {
      nieuweRij.style.backgroundColor = "#f2f2f2";
    }

    let aGedetaileerd = document.createElement("a");
    aGedetaileerd.setAttribute("id", elem);
    aGedetaileerd.href = `./gedetailleerd.html`;
    aGedetaileerd.style.fontWeight = "900";
    if(ind % 2 == 0) {
      aGedetaileerd.setAttribute("class", "linkToDetailedInfoEven");
    }
    else {
      aGedetaileerd.setAttribute("class", "linkToDetailedInfoOdd");

    }

    let tdGemeente = document.createElement("td");
    let gemeente = document.createTextNode("Gemeente van " + elem); // Wordt de querry om de gemeente uit het bedrijf te halen
    tdGemeente.append(gemeente);

    let tdBedrijf = document.createElement("td");
    let bedrijf = document.createTextNode(elem);
    tdBedrijf.append(bedrijf);
    aGedetaileerd.append(tdBedrijf)

    let tdOndernemingsnummer = document.createElement("td");
    let ondernemingsnummer = document.createTextNode("Ondernemingsnummer van " + elem); // Wordt de querry om de gemeente uit het bedrijf te halen
    tdOndernemingsnummer.append(ondernemingsnummer);

    nieuweRij.append(tdGemeente);
    nieuweRij.append(aGedetaileerd);
    nieuweRij.append(tdOndernemingsnummer);

    table.append(nieuweRij);

    aGedetaileerd.onclick = () => {
      localStorage.setItem("bedrijfsnaam", aGedetaileerd.id);
    };
  });

};

let bedrijfsnaam = localStorage.getItem("zoekterm");

weergaveBedrijven(bedrijfsnaam)
