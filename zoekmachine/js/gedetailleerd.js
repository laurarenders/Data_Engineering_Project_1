"use strict";

let gekozenBedrijf = localStorage.getItem("bedrijfsnaam")

let container = document.getElementById("container")

let h1 = document.createElement("h1");
let title = document.createTextNode(`Gedetailleerd overzicht van ${gekozenBedrijf}`);
h1.append(title);

container.append(h1);
