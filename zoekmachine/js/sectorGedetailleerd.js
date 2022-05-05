"use strict";

let gekozenSector = localStorage.getItem("sector")

let container = document.getElementById("container")

let h1 = document.createElement("h1");
let title = document.createTextNode(`Gedetailleerd overzicht van ${gekozenSector}`);
h1.append(title);

container.append(h1);
