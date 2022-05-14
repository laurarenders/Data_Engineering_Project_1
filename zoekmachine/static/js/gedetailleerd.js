function weergaveBedrijf(gekozenBedrijf) {

  let title = document.getElementById("title");
  let h1 = document.createElement("h1");
  let text = document.createTextNode(`Gedetailleerd overzicht van "${gekozenBedrijf}"`);

  h1.append(text);
  title.append(h1);

};

let gekozenBedrijf = localStorage.getItem("bedrijfsnaam");

weergaveBedrijf(gekozenBedrijf)