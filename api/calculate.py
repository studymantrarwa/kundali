<!doctype html>
<html lang="hi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">

<title>Study Mantra • Kundli Chart</title>

<style>

*{
  box-sizing:border-box;
}

body{
  margin:0;
  padding:12px;
  background:#f5f6fa;
  color:#172033;
  font-family:Arial,sans-serif;
}

.wrap{
  width:100%;
  max-width:850px;
  margin:auto;
}

.card{
  background:#fff;
  border:1px solid #e0e4eb;
  border-radius:18px;
  padding:18px;
  margin-bottom:15px;
  box-shadow:0 7px 25px rgba(0,0,0,.06);
}

h1{
  font-size:24px;
  margin:0 0 5px;
}

h2{
  font-size:20px;
  margin:0 0 15px;
}

.sub{
  color:#667085;
  font-size:13px;
  line-height:1.5;
}

.info-grid{
  display:grid;
  grid-template-columns:repeat(2,1fr);
  gap:10px;
}

.info{
  background:#f7f8fc;
  border:1px solid #e5e7ed;
  border-radius:12px;
  padding:11px;
}

.info b{
  display:block;
  font-size:12px;
  color:#667085;
  margin-bottom:4px;
}

.info span{
  font-size:14px;
  font-weight:700;
}

.chart-wrap{
  width:100%;
  max-width:620px;
  margin:15px auto 5px;
}

.chart{
  width:100%;
  height:auto;
  display:block;
  background:#fff;
  border:1px solid #222;
}

.house-line{
  fill:none;
  stroke:#222;
  stroke-width:2;
}

.house-number{
  font-size:13px;
  fill:#777;
  text-anchor:middle;
  dominant-baseline:middle;
}

.rashi-number{
  font-size:19px;
  font-weight:700;
  fill:#7c3aed;
  text-anchor:middle;
  dominant-baseline:middle;
}

.rashi-name{
  font-size:9px;
  fill:#555;
  text-anchor:middle;
  dominant-baseline:middle;
}

.planet-text{
  font-size:12px;
  font-weight:700;
  fill:#172033;
  text-anchor:middle;
  dominant-baseline:middle;
}

.lagna-text{
  font-size:11px;
  font-weight:700;
  fill:#b3261e;
  text-anchor:middle;
  dominant-baseline:middle;
}

.table-wrap{
  overflow-x:auto;
}

table{
  width:100%;
  border-collapse:collapse;
  font-size:13px;
}

th,
td{
  border-bottom:1px solid #e8eaf0;
  padding:10px 7px;
  text-align:left;
  white-space:nowrap;
}

th{
  background:#f6f7fa;
  font-size:12px;
}

/* =====================================================
   DASHA
===================================================== */

.dasha-title{
  margin-bottom:5px;
}

.dasha-help{
  font-size:12px;
  color:#667085;
  margin-bottom:12px;
  line-height:1.5;
}

.dasha-item{
  border:1px solid #dfe3ea;
  border-radius:13px;
  margin:8px 0;
  overflow:hidden;
  background:#fff;
}

.dasha-head{
  width:100%;
  min-height:58px;
  margin:0;
  padding:10px 12px;
  background:#fafaff;
  color:#172033;
  border:0;
  border-radius:0;
  display:flex;
  align-items:center;
  justify-content:space-between;
  text-align:left;
  cursor:pointer;
}

.dasha-head:hover{
  background:#f5f3ff;
}

.dasha-left{
  min-width:0;
}

.dasha-lord{
  font-size:15px;
  font-weight:700;
}

.dasha-date{
  margin-top:4px;
  font-size:11px;
  color:#667085;
}

.arrow{
  font-size:20px;
  transition:transform .2s;
  flex-shrink:0;
}

.dasha-item.open > .dasha-head .arrow{
  transform:rotate(90deg);
}

.dasha-body{
  display:none;
  padding:0 9px 9px;
  background:#fff;
}

.dasha-item.open > .dasha-body{
  display:block;
}

.antar-item{
  border:1px solid #e4e6ec;
  border-radius:10px;
  margin-top:7px;
  overflow:hidden;
}

.antar-head{
  width:100%;
  min-height:50px;
  margin:0;
  padding:8px 10px;
  background:#f8f9fc;
  color:#172033;
  border:0;
  border-radius:0;
  display:flex;
  align-items:center;
  justify-content:space-between;
  text-align:left;
  cursor:pointer;
}

.antar-head:hover{
  background:#f3f4f8;
}

.antar-left{
  min-width:0;
}

.antar-lord{
  font-size:13px;
  font-weight:700;
}

.antar-date{
  margin-top:3px;
  color:#667085;
  font-size:10px;
}

.antar-body{
  display:none;
  padding:7px;
  background:#fff;
}

.antar-item.open > .antar-body{
  display:block;
}

.pratyantar-item{
  display:flex;
  justify-content:space-between;
  align-items:center;
  gap:8px;
  padding:8px 9px;
  border-bottom:1px solid #edf0f4;
  font-size:11px;
}

.pratyantar-item:last-child{
  border-bottom:0;
}

.pratyantar-lord{
  font-weight:700;
}

.pratyantar-date{
  color:#667085;
  text-align:right;
  white-space:nowrap;
}

.empty{
  padding:15px;
  border-radius:10px;
  background:#f7f8fb;
  color:#667085;
  font-size:13px;
}

.error{
  color:#b3261e;
}

.back{
  display:inline-block;
  text-decoration:none;
  color:#fff;
  background:#7c3aed;
  padding:10px 15px;
  border-radius:10px;
  font-size:13px;
  font-weight:700;
  margin-bottom:15px;
}

.note{
  margin-top:10px;
  font-size:11px;
  line-height:1.5;
  color:#667085;
}

@media(max-width:600px){

  body{
    padding:8px;
  }

  .card{
    padding:13px;
    border-radius:15px;
  }

  .info-grid{
    grid-template-columns:1fr;
  }

  h1{
    font-size:21px;
  }

  h2{
    font-size:18px;
  }

  .planet-text{
    font-size:11px;
  }

  .rashi-number{
    font-size:17px;
  }

  .dasha-lord{
    font-size:14px;
  }

  .pratyantar-item{
    flex-direction:column;
    align-items:flex-start;
  }

  .pratyantar-date{
    text-align:left;
  }

}

</style>
</head>

<body>

<div class="wrap">

<a class="back" href="/kundli.html">
← नई Kundli बनाएँ
</a>

<div class="card">

<h1>🔱 Study Mantra Kundli</h1>

<div id="personSubtitle" class="sub">
Kundli details
</div>

</div>


<!-- =====================================================
     BASIC INFORMATION
===================================================== -->

<div class="card">

<h2>जन्म विवरण</h2>

<div id="personInfo" class="info-grid"></div>

</div>


<!-- =====================================================
     D1 CHART
===================================================== -->

<div class="card">

<h2>राशि कुंडली — D1</h2>

<div class="sub">
North Indian Style • Lahiri
</div>

<div class="chart-wrap">

<svg
 id="d1Chart"
 class="chart"
 viewBox="0 0 600 600"
 xmlns="http://www.w3.org/2000/svg"
 aria-label="D1 Kundli"
></svg>

</div>

</div>


<!-- =====================================================
     D9 CHART
===================================================== -->

<div class="card">

<h2>नवांश कुंडली — D9</h2>

<div class="sub">
Navamsa Chart
</div>

<div class="chart-wrap">

<svg
 id="d9Chart"
 class="chart"
 viewBox="0 0 600 600"
 xmlns="http://www.w3.org/2000/svg"
 aria-label="D9 Kundli"
></svg>

</div>

</div>


<!-- =====================================================
     BASIC ASTROLOGY
===================================================== -->

<div class="card">

<h2>मुख्य जानकारी</h2>

<div id="basicInfo" class="info-grid"></div>

</div>


<!-- =====================================================
     PLANETS
===================================================== -->

<div class="card">

<h2>ग्रह स्थिति</h2>

<div class="table-wrap">

<table>

<thead>

<tr>
<th>ग्रह</th>
<th>राशि</th>
<th>डिग्री</th>
<th>भाव</th>
</tr>

</thead>

<tbody id="planetTable"></tbody>

</table>

</div>

</div>


<!-- =====================================================
     VIMSHOTTARI DASHA
===================================================== -->

<div class="card">

<h2 class="dasha-title">
विम्शोत्तरी महादशा
</h2>

<div class="dasha-help">
किसी Mahadasha पर tap करें → Antardasha देखें।
फिर Antardasha पर tap करें → Pratyantardasha देखें।
</div>

<div id="dashaContainer">

<div class="empty">
दशा डेटा लोड हो रहा है...
</div>

</div>

<div class="note">
दशा गणना जन्म समय, स्थान, Lahiri sidereal Moon और Vimshottari system पर आधारित है।
</div>

</div>


<!-- =====================================================
     ERROR
===================================================== -->

<div
 id="pageError"
 class="card error"
 style="display:none"
></div>


</div>


<script>

/* ========================================================
   CONSTANTS
======================================================== */

const SIGNS = [
  "Aries",
  "Taurus",
  "Gemini",
  "Cancer",
  "Leo",
  "Virgo",
  "Libra",
  "Scorpio",
  "Sagittarius",
  "Capricorn",
  "Aquarius",
  "Pisces"
];

const SIGNS_HI = [
  "मेष",
  "वृषभ",
  "मिथुन",
  "कर्क",
  "सिंह",
  "कन्या",
  "तुला",
  "वृश्चिक",
  "धनु",
  "मकर",
  "कुंभ",
  "मीन"
];

const PLANET_HI = {
  Sun:"सूर्य",
  Moon:"चंद्र",
  Mars:"मंगल",
  Mercury:"बुध",
  Jupiter:"गुरु",
  Venus:"शुक्र",
  Saturn:"शनि",
  Rahu:"राहु",
  Ketu:"केतु"
};

const DASHA_HI = {
  Ketu:"केतु",
  Venus:"शुक्र",
  Sun:"सूर्य",
  Moon:"चंद्र",
  Mars:"मंगल",
  Rahu:"राहु",
  Jupiter:"गुरु",
  Saturn:"शनि",
  Mercury:"बुध"
};


/* ========================================================
   HELPERS
======================================================== */

function $(id){
  return document.getElementById(id);
}


function escapeHtml(value){

  return String(value ?? "")
    .replace(/&/g,"&amp;")
    .replace(/</g,"&lt;")
    .replace(/>/g,"&gt;")
    .replace(/"/g,"&quot;")
    .replace(/'/g,"&#039;");

}


function number(value){

  const n = Number(value);

  return Number.isFinite(n) ? n : 0;

}


function formatDegree(value){

  return number(value).toFixed(2) + "°";

}


function formatDate(value){

  if(!value){
    return "-";
  }

  try{

    const d = new Date(value);

    if(Number.isNaN(d.getTime())){
      return String(value);
    }

    return d.toLocaleDateString(
      "en-IN",
      {
        day:"2-digit",
        month:"short",
        year:"numeric"
      }
    );

  }catch(e){

    return String(value);

  }

}


function planetName(name){

  return DASHA_HI[name] || name || "-";

}


function signNumber(value){

  const n = Number(value);

  if(Number.isFinite(n)){

    if(n >= 0 && n <= 11){
      return n;
    }

  }

  return 0;

}


/* ========================================================
   NORTH INDIAN HOUSE GEOMETRY
======================================================== */

function getHousePolygons(){

  return [

    "300,0 450,150 300,300 150,150",

    "0,0 300,0 150,150",

    "0,0 150,150 0,300",

    "0,300 150,150 300,300 150,450",

    "0,300 150,450 0,600",

    "0,600 150,450 300,600",

    "150,450 300,300 450,450 300,600",

    "300,600 450,450 600,600",

    "600,600 450,450 600,300",

    "600,300 450,150 300,300 450,450",

    "600,300 450,150 600,0",

    "600,0 300,0 450,150"

  ];

}


function getHouseCenters(){

  return [

    {x:300,y:150},
    {x:150,y:75},
    {x:65,y:215},
    {x:150,y:300},
    {x:65,y:385},
    {x:150,y:525},
    {x:300,y:450},
    {x:450,y:525},
    {x:535,y:385},
    {x:450,y:300},
    {x:535,y:215},
    {x:450,y:75}

  ];

}


/* ========================================================
   SVG HELPERS
======================================================== */

function svgElement(
  tag,
  attrs
){

  const el =
    document.createElementNS(
      "http://www.w3.org/2000/svg",
      tag
    );

  Object.keys(attrs || {}).forEach(
    key => {

      el.setAttribute(
        key,
        attrs[key]
      );

    }
  );

  return el;

}


function addText(
  svg,
  text,
  x,
  y,
  className
){

  const el =
    svgElement(
      "text",
      {
        x:x,
        y:y,
        class:className
      }
    );

  el.textContent = text;

  svg.appendChild(el);

  return el;

}


/* ========================================================
   D1 HOUSE DATA
======================================================== */

function buildD1Houses(data){

  const houses =
    Array.from(
      {length:12},
      () => ({
        planets:[]
      })
    );

  const asc =
    data &&
    data.lagna
      ? signNumber(data.lagna.sign)
      : 0;


  const planets =
    Array.isArray(data.planets)
      ? data.planets
      : [];


  planets.forEach(
    planet => {

      let house =
        Number(planet.house);

      if(
        !Number.isFinite(house) ||
        house < 1 ||
        house > 12
      ){

        const sign =
          signNumber(planet.sign);

        house =
          ((sign - asc + 12) % 12) + 1;

      }

      houses[house - 1]
        .planets
        .push(planet);

    }
  );


  return {
    ascendantSign:asc,
    houses:houses
  };

}


/* ========================================================
   D9 HOUSE DATA
======================================================== */

function buildD9Houses(data){

  const houses =
    Array.from(
      {length:12},
      () => ({
        planets:[]
      })
    );


  const d9 =
    data &&
    data.d9 &&
    Array.isArray(data.d9.planets)
      ? data.d9.planets
      : [];


  let ascD9 = 0;


  if(
    data &&
    data.lagna &&
    Number.isFinite(
      Number(data.lagna.longitude)
    )
  ){

    const lon =
      Number(
        data.lagna.longitude
      );

    const normalized =
      ((lon % 360) + 360) % 360;

    const sign =
      Math.floor(
        normalized / 30
      );

    const deg =
      normalized % 30;

    const part =
      Math.min(
        8,
        Math.floor(
          deg / (30 / 9)
        )
      );

    ascD9 =
      (sign * 9 + part) % 12;

  }


  d9.forEach(
    planet => {

      const sign =
        signNumber(
          planet.sign
        );

      const house =
        ((sign - ascD9 + 12) % 12) + 1;

      houses[house - 1]
        .planets
        .push(planet);

    }
  );


  return {
    ascendantSign:ascD9,
    houses:houses
  };

}


/* ========================================================
   DRAW CHART
======================================================== */

function drawChart(
  svgId,
  data,
  isD9
){

  const svg =
    $(svgId);

  if(!svg){
    return;
  }


  svg.innerHTML = "";


  const geometry =
    isD9
      ? buildD9Houses(data)
      : buildD1Houses(data);


  const polygons =
    getHousePolygons();

  const centers =
    getHouseCenters();


  svg.appendChild(
    svgElement(
      "rect",
      {
        x:0,
        y:0,
        width:600,
        height:600,
        fill:"white",
        stroke:"#222",
        "stroke-width":"2"
      }
    )
  );


  polygons.forEach(
    (points,index) => {

      svg.appendChild(
        svgElement(
          "polygon",
          {
            points:points,
            class:"house-line"
          }
        )
      );

      addText(
        svg,
        "H" + (index + 1),
        centers[index].x,
        centers[index].y - 34,
        "house-number"
      );

    }
  );


  /* Rashi */

  for(
    let house = 1;
    house <= 12;
    house++
  ){

    const sign =
      (
        geometry.ascendantSign
        + house
        - 1
      ) % 12;


    const c =
      centers[house - 1];


    addText(
      svg,
      String(sign + 1),
      c.x,
      c.y - 12,
      "rashi-number"
    );


    addText(
      svg,
      SIGNS_HI[sign],
      c.x,
      c.y + 6,
      "rashi-name"
    );

  }


  /* Planets */

  geometry.houses.forEach(
    (houseData,index) => {

      if(
        !houseData ||
        !Array.isArray(
          houseData.planets
        )
      ){
        return;
      }


      const planets =
        houseData.planets;


      const c =
        centers[index];


      planets.forEach(
        (planet,pIndex) => {

          const row =
            Math.floor(
              pIndex / 2
            );

          const col =
            pIndex % 2;


          let x =
            c.x - 27 + col * 54;

          let y =
            c.y + 24 + row * 15;


          x =
            Math.max(
              20,
              Math.min(
                580,
                x
              )
            );


          y =
            Math.max(
              15,
              Math.min(
                585,
                y
              )
            );


          const label =
            PLANET_HI[
              planet.name
            ] ||
            planet.name ||
            "";


          addText(
            svg,
            label,
            x,
            y,
            "planet-text"
          );

        }
      );

    }
  );


  /* Lagna */

  const firstCenter =
    centers[0];


  addText(
    svg,
    "लग्न",
    firstCenter.x,
    firstCenter.y + 39,
    "lagna-text"
  );

}


/* ========================================================
   PERSON INFO
======================================================== */

function renderPersonInfo(data){

  const input =
    data &&
    data.input
      ? data.input
      : {};


  $("personSubtitle").textContent =
    (
      input.name ||
      "Kundli"
    )
    +
    " • "
    +
    (
      input.place ||
      ""
    );


  const items = [

    [
      "नाम",
      input.name || "-"
    ],

    [
      "जन्म तारीख",
      input.date || "-"
    ],

    [
      "जन्म समय",
      input.time || "-"
    ],

    [
      "जन्म स्थान",
      input.place || "-"
    ],

    [
      "Latitude",
      Number.isFinite(Number(input.lat))
        ? Number(input.lat).toFixed(5)
        : "-"
    ],

    [
      "Longitude",
      Number.isFinite(Number(input.lon))
        ? Number(input.lon).toFixed(5)
        : "-"
    ],

    [
      "Timezone",
      input.timezone || "-"
    ]

  ];


  $("personInfo").innerHTML =
    items.map(
      item =>

        '<div class="info">' +

        "<b>" +
        escapeHtml(item[0]) +
        "</b>" +

        "<span>" +
        escapeHtml(item[1]) +
        "</span>" +

        "</div>"

    ).join("");

}


/* ========================================================
   BASIC INFO
======================================================== */

function renderBasicInfo(data){

  const lagna =
    data &&
    data.lagna
      ? data.lagna
      : {};


  const nak =
    data &&
    data.nakshatra
      ? data.nakshatra
      : {};


  const astronomy =
    data &&
    data.astronomy
      ? data.astronomy
      : {};


  const items = [

    [
      "लग्न",
      lagna.sign_name ||
      (
        Number.isFinite(
          Number(lagna.sign)
        )
        ? SIGNS[
            signNumber(lagna.sign)
          ]
        : "-"
      )
    ],

    [
      "लग्न डिग्री",
      formatDegree(
        lagna.degree
      )
    ],

    [
      "नक्षत्र",
      nak.name || "-"
    ],

    [
      "नक्षत्र पाद",
      nak.pada
        ? String(nak.pada)
        : "-"
    ],

    [
      "नक्षत्र स्वामी",
      nak.lord
        ? planetName(nak.lord)
        : "-"
    ],

    [
      "Ayanamsha",
      Number.isFinite(
        Number(
          astronomy.ayanamsha
        )
      )
      ? Number(
          astronomy.ayanamsha
        ).toFixed(6) + "°"
      : "-"
    ]

  ];


  $("basicInfo").innerHTML =
    items.map(
      item =>

        '<div class="info">' +

        "<b>" +
        escapeHtml(item[0]) +
        "</b>" +

        "<span>" +
        escapeHtml(item[1]) +
        "</span>" +

        "</div>"

    ).join("");

}


/* ========================================================
   PLANET TABLE
======================================================== */

function renderPlanetTable(data){

  const planets =
    data &&
    Array.isArray(data.planets)
      ? data.planets
      : [];


  if(!planets.length){

    $("planetTable").innerHTML =
      '<tr><td colspan="4">Planet data उपलब्ध नहीं है।</td></tr>';

    return;

  }


  $("planetTable").innerHTML =
    planets.map(
      planet => {

        const sign =
          planet.sign_name ||
          SIGNS[
            signNumber(
              planet.sign
            )
          ];


        return (

          "<tr>" +

          "<td>" +
          escapeHtml(
            PLANET_HI[
              planet.name
            ] ||
            planet.name
          ) +
          "</td>" +

          "<td>" +
          escapeHtml(sign) +
          "</td>" +

          "<td>" +
          escapeHtml(
            formatDegree(
              planet.degree
            )
          ) +
          "</td>" +

          "<td>" +
          escapeHtml(
            planet.house || "-"
          ) +
          "</td>" +

          "</tr>"

        );

      }
    ).join("");

}


/* ========================================================
   DASHA DATA NORMALIZER
======================================================== */

function getMahadashaArray(data){

  if(
    !data ||
    !data.vimshottari
  ){
    return [];
  }


  const v =
    data.vimshottari;


  if(
    Array.isArray(
      v.mahadasha
    )
  ){
    return v.mahadasha;
  }


  if(
    Array.isArray(
      v.periods
    )
  ){
    return v.periods;
  }


  if(
    Array.isArray(
      v.dashas
    )
  ){
    return v.dashas;
  }


  return [];

}


function getAntardashaArray(maha){

  if(!maha){
    return [];
  }


  if(
    Array.isArray(
      maha.antardasha
    )
  ){
    return maha.antardasha;
  }


  if(
    Array.isArray(
      maha.antardashas
    )
  ){
    return maha.antardashas;
  }


  if(
    Array.isArray(
      maha.antar
    )
  ){
    return maha.antar;
  }


  return [];

}


function getPratyantarArray(antar){

  if(!antar){
    return [];
  }


  if(
    Array.isArray(
      antar.pratyantardasha
    )
  ){
    return antar.pratyantardasha;
  }


  if(
    Array.isArray(
      antar.pratyantardashas
    )
  ){
    return antar.pratyantardashas;
  }


  if(
    Array.isArray(
      antar.pratyantar
    )
  ){
    return antar.pratyantar;
  }


  return [];

}


/* ========================================================
   CREATE PRATYANTAR
======================================================== */

function createPratyantarRow(
  period
){

  const row =
    document.createElement(
      "div"
    );

  row.className =
    "pratyantar-item";


  const name =
    document.createElement(
      "div"
    );

  name.className =
    "pratyantar-lord";


  name.textContent =
    dashaPlanetName(
      period.lord
    )
    +
    (
      period.lord
        ? " (" + period.lord + ")"
        : ""
    );


  const date =
    document.createElement(
      "div"
    );

  date.className =
    "pratyantar-date";


  date.textContent =
    formatDate(
      period.start
    )
    +
    " → "
    +
    formatDate(
      period.end
    );


  row.appendChild(name);
  row.appendChild(date);


  return row;

}


/* ========================================================
   DASH PLANET NAME
======================================================== */

function dashaPlanetName(
  lord
){

  return DASHA_HI[
    lord
  ] ||
  lord ||
  "-";

}


/* ========================================================
   CREATE ANTARDASHA
======================================================== */

function createAntardashaElement(
  antar
){

  const item =
    document.createElement(
      "div"
    );

  item.className =
    "antar-item";


  const head =
    document.createElement(
      "button"
    );

  head.type = "button";

  head.className =
    "antar-head";


  const left =
    document.createElement(
      "div"
    );

  left.className =
    "antar-left";


  const lord =
    document.createElement(
      "div"
    );

  lord.className =
    "antar-lord";


  lord.textContent =
    dashaPlanetName(
      antar.lord
    )
    +
    " Antardasha"
    +
    (
      antar.lord
        ? " (" + antar.lord + ")"
        : ""
    );


  const date =
    document.createElement(
      "div"
    );

  date.className =
    "antar-date";


  date.textContent =
    formatDate(
      antar.start
    )
    +
    " → "
    +
    formatDate(
      antar.end
    );


  left.appendChild(lord);
  left.appendChild(date);


  const arrow =
    document.createElement(
      "span"
    );

  arrow.className =
    "arrow";

  arrow.textContent =
    "›";


  head.appendChild(left);
  head.appendChild(arrow);


  const body =
    document.createElement(
      "div"
    );

  body.className =
    "antar-body";


  const pratyantar =
    getPratyantarArray(
      antar
    );


  if(
    !pratyantar.length
  ){

    const empty =
      document.createElement(
        "div"
      );

    empty.className =
      "empty";

    empty.textContent =
      "Pratyantardasha data उपलब्ध नहीं है।";

    body.appendChild(empty);

  }else{

    pratyantar.forEach(
      period => {

        body.appendChild(
          createPratyantarRow(
            period
          )
        );

      }
    );

  }


  head.addEventListener(
    "click",
    function(){

      item.classList.toggle(
        "open"
      );

    }
  );


  item.appendChild(head);
  item.appendChild(body);


  return item;

}


/* ========================================================
   CREATE MAHADASHA
======================================================== */

function createMahadashaElement(
  maha
){

  const item =
    document.createElement(
      "div"
    );

  item.className =
    "dasha-item";


  const head =
    document.createElement(
      "button"
    );

  head.type = "button";

  head.className =
    "dasha-head";


  const left =
    document.createElement(
      "div"
    );

  left.className =
    "dasha-left";


  const lord =
    document.createElement(
      "div"
    );

  lord.className =
    "dasha-lord";


  lord.textContent =
    dashaPlanetName(
      maha.lord
    )
    +
    " Mahadasha"
    +
    (
      maha.lord
        ? " (" + maha.lord + ")"
        : ""
    );


  const date =
    document.createElement(
      "div"
    );

  date.className =
    "dasha-date";


  date.textContent =
    formatDate(
      maha.start
    )
    +
    " → "
    +
    formatDate(
      maha.end
    );


  left.appendChild(lord);
  left.appendChild(date);


  const arrow =
    document.createElement(
      "span"
    );

  arrow.className =
    "arrow";

  arrow.textContent =
    "›";


  head.appendChild(left);
  head.appendChild(arrow);


  const body =
    document.createElement(
      "div"
    );

  body.className =
    "dasha-body";


  const antardasha =
    getAntardashaArray(
      maha
    );


  if(
    !antardasha.length
  ){

    const empty =
      document.createElement(
        "div"
      );

    empty.className =
      "empty";

    empty.textContent =
      "इस Mahadasha का Antardasha data उपलब्ध नहीं है।";

    body.appendChild(empty);

  }else{

    antardasha.forEach(
      antar => {

        body.appendChild(
          createAntardashaElement(
            antar
          )
        );

      }
    );

  }


  head.addEventListener(
    "click",
    function(){

      item.classList.toggle(
        "open"
      );

    }
  );


  item.appendChild(head);
  item.appendChild(body);


  return item;

}


/* ========================================================
   RENDER DASHA
======================================================== */

function renderDasha(
  data
){

  const container =
    $("dashaContainer");


  if(!container){
    return;
  }


  container.innerHTML =
    "";


  const mahadasha =
    getMahadashaArray(
      data
    );


  if(
    !Array.isArray(mahadasha) ||
    mahadasha.length === 0
  ){

    const empty =
      document.createElement(
        "div"
      );

    empty.className =
      "empty";

    empty.textContent =
      "Mahadasha data उपलब्ध नहीं है।";

    container.appendChild(
      empty
    );

    return;

  }


  mahadasha.forEach(
    maha => {

      if(
        !maha ||
        typeof maha !== "object"
      ){
        return;
      }


      container.appendChild(
        createMahadashaElement(
          maha
        )
      );

    }
  );


  if(
    !container.children.length
  ){

    const empty =
      document.createElement(
        "div"
      );

    empty.className =
      "empty";

    empty.textContent =
      "Dasha data पढ़ा नहीं जा सका।";

    container.appendChild(
      empty
    );

  }

}


/* ========================================================
   LOAD DATA
======================================================== */

function loadKundli(){

  let raw = null;


  try{

    raw =
      localStorage.getItem(
        "studyMantraLastKundli"
      );

  }catch(error){

    console.error(
      "localStorage error",
      error
    );

  }


  if(!raw){

    showPageError(
      "Kundli data नहीं मिला। पहले Kundli calculate करें।"
    );

    return null;

  }


  try{

    const data =
      JSON.parse(
        raw
      );


    if(
      !data ||
      typeof data !== "object"
    ){

      throw new Error(
        "Invalid Kundli data"
      );

    }


    return data;

  }catch(error){

    console.error(
      error
    );

    showPageError(
      "Kundli data पढ़ने में error आया। कृपया फिर से Kundli calculate करें।"
    );

    return null;

  }

}


/* ========================================================
   ERROR
======================================================== */

function showPageError(
  message
){

  const el =
    $("pageError");


  if(!el){
    return;
  }


  el.style.display =
    "block";


  el.textContent =
    message;

}


/* ========================================================
   RENDER ALL
======================================================== */

function renderAll(
  data
){

  try{

    renderPersonInfo(
      data
    );


    renderBasicInfo(
      data
    );


    renderPlanetTable(
      data
    );


    drawChart(
      "d1Chart",
      data,
      false
    );


    drawChart(
      "d9Chart",
      data,
      true
    );


    renderDasha(
      data
    );

  }catch(error){

    console.error(
      "Chart render error:",
      error
    );


    showPageError(
      "Chart render karte waqt error aaya: "
      +
      (
        error.message ||
        error
      )
    );

  }

}


/* ========================================================
   START
======================================================== */

document.addEventListener(
  "DOMContentLoaded",
  function(){

    const data =
      loadKundli();


    if(data){

      renderAll(
        data
      );

    }

  }
);

</script>

</body>
</html>
