function weergaveSectoren(sector) {
  let sectorenlijst =localStorage.getItem("sectorresults");

  let sectoren = [];
  let sublist = [];
  let value = "";

  [...sectorenlijst].forEach((elem, ind, arr) => {
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
        sectoren.push(sublist)
        value = ""
        sublist = []
      }
    }
  });

  console.log(sectoren)

  let sectorennumbers = sectoren.slice(0, sectoren.length - 1)

  let sectorlijst = [];
  let naam = "";

  sectorennumbers.forEach(elem => {
    elem.forEach(e => {
      naam += String.fromCharCode(e)
    })
    sectorlijst.push(naam)
    naam = ""
  });

  let title = document.getElementById("title");
  let h1 = document.createElement("h1");
  let text = document.createTextNode(`Sectoren die "${sector}" bevatten`);

  h1.append(text);
  title.append(h1);

  sectorlijst.forEach((elem, ind, val) => {
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
    aGedetaileerd.href = `/sectorGedetailleerd.html?sector=${elem}`;
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
      localStorage.setItem("sectornaam", aGedetaileerd.id);
    };
  });

  // ------------------------------------------------ Niet gevonden ------------------------------------------------
  if(sectorlijst.length === 0) {
    document.getElementById("sectoren").innerHTML=""
    document.getElementById("title").innerText=""

    container = document.getElementById("containerSectorlijst")
  
    let h1 = document.createElement("h1");
    let text = document.createTextNode(`Niets gevonden...`);
  
    h1.append(text);
    container.append(h1);
  }
  // ------------------------------------------------ Niet gevonden ------------------------------------------------

};

let sectorNaam = localStorage.getItem("sector");

if(!window.location.search)
  window.location.href = `/sectorlijst.html?sectoren=${sectorNaam}`;
weergaveSectoren(sectorNaam)
