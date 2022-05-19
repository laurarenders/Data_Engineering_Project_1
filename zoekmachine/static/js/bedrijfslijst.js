function weergaveBedrijven(bedrijfsnaam) {
  let bedrijvenlist = localStorage.getItem("zoektermresults");

  // let char = String.fromCharCode(65);
  let bedrijven = [];
  let sublist = [];
  let value = "";

  [...bedrijvenlist].forEach((elem, ind, arr) => {
    if(elem !== "[" && elem !== "]" && elem !== ","){
      value += elem;
    }

    if(elem === "," && arr[ind+2] !== "[") {
      if(value !== "") {
        sublist.push(value.trim());
        value = "";
      }
    }

    if(elem === "]") {
      if(sublist !== []) {
        sublist.push(value.trim())
        bedrijven.push(sublist)
        value = ""
        sublist = []
      }
    }
  })

  console.log(bedrijvenlist)
  let bedrijfsnamenPlusGemeentesnumbers = bedrijven.slice(0, bedrijven.length-3)
  let bedrijfsnamennumbers = bedrijven.slice(0, bedrijfsnamenPlusGemeentesnumbers.length / 2)
  let gemeentennumbers = bedrijven.slice(bedrijfsnamennumbers.length + 1, bedrijfsnamenPlusGemeentesnumbers.length)
  let ondernemingsnummers = bedrijven[bedrijven.length - 2]

  console.log(bedrijfsnamenPlusGemeentesnumbers)
  console.log(bedrijfsnamennumbers)
  console.log(gemeentennumbers)
  console.log(ondernemingsnummers)

  let bedrijfsnamenlist = []
  let gemeentenlist = []
  let naam = "";

  bedrijfsnamennumbers.forEach(elem => {
    elem.forEach(e => {
      naam += String.fromCharCode(e)
    })
    bedrijfsnamenlist.push(naam)
    naam = ""
  });

  gemeentennumbers.forEach(elem => {
    elem.forEach(e => {
      naam += String.fromCharCode(e)
    })
    gemeentenlist.push(naam)
    naam = ""
  });

  let title = document.getElementById("title");
  let h1 = document.createElement("h1");
  let text = document.createTextNode(`Bedrijven die de zoekterm "${bedrijfsnaam}" bevatten`);

  h1.append(text);
  title.append(h1);

  bedrijfsnamenlist.forEach((elem, ind, arr) => {
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
    aGedetaileerd.href = `/gedetailleerd.html?bedrijf=${elem}`;
    aGedetaileerd.style.fontWeight = "900";
    if(ind % 2 == 0) {
      aGedetaileerd.setAttribute("class", "linkToDetailedInfoEven");
    }
    else {
      aGedetaileerd.setAttribute("class", "linkToDetailedInfoOdd");

    }

    let tdGemeente = document.createElement("td");
    let gemeente = document.createTextNode(gemeentenlist[ind]); // Wordt de querry om de gemeente uit het bedrijf te halen
    tdGemeente.append(gemeente);

    let tdBedrijf = document.createElement("td");
    let bedrijf = document.createTextNode(elem);
    tdBedrijf.append(bedrijf);
    aGedetaileerd.append(tdBedrijf)

    let tdOndernemingsnummer = document.createElement("td");
    let ondernemingsnummer = document.createTextNode(ondernemingsnummers[ind]); // Wordt de querry om de gemeente uit het bedrijf te halen
    tdOndernemingsnummer.append(ondernemingsnummer);

    nieuweRij.append(tdGemeente);
    nieuweRij.append(aGedetaileerd);
    nieuweRij.append(tdOndernemingsnummer);

    table.append(nieuweRij);

    aGedetaileerd.onclick = () => {
      localStorage.setItem("bedrijfsnaam", aGedetaileerd.id);
    };
  });

  // ------------------------------------------------ Niet gevonden ------------------------------------------------
  if(bedrijfsnamenlist.length === 0) {
    document.getElementById("bedrijven").innerHTML=""
    document.getElementById("title").innerText=""

    container = document.getElementById("containerBedrijfslijst")
  
    let h1 = document.createElement("h1");
    let text = document.createTextNode(`Niets gevonden...`);
  
    h1.append(text);
    container.append(h1);
  }
// ------------------------------------------------ Niet gevonden ------------------------------------------------

};

let bedrijfsnaam = localStorage.getItem("zoekterm");

if(!window.location.search)
  window.location.href = `/bedrijfslijst.html?bedrijven=${bedrijfsnaam}`;
weergaveBedrijven(bedrijfsnaam)
