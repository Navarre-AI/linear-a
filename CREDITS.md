# Credits

This project stands on other people's work. Every source below is credited
with what it gave, and with the licence or permission that applies.

The licence split for this repository is in [LICENSE](LICENSE). The default is
CC BY 4.0. SigLA-derived paths are CC BY-NC-SA 4.0.

## Databases and corpora

### SigLA: The Signs of Linear A

Ester Salgarella and Simon Castellan, <https://sigla.phis.me/>.

Gave: the palaeographical database. Per-position sign data, readings and
`certain` flags for 772 documents. The sign tracings and crops. The structured
corpus under `linear_a/data/sources/sigla/`.

Licence: Creative Commons Attribution-NonCommercial-ShareAlike 4.0
International (CC BY-NC-SA 4.0).
Summary: <https://creativecommons.org/licenses/by-nc-sa/4.0/>
Legal code: <https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode>

Required credit line, verbatim:

> Sign drawings from SigLA: The Signs of Linear A, a palaeographical database,
> by Ester Salgarella and Simon Castellan (https://sigla.phis.me/), licensed
> under CC BY-NC-SA 4.0.

The database paper: Salgarella, E., and Castellan, S. (2021). SigLA: signs of
Linear A.

The ShareAlike term reaches derivatives, and it reaches measurements computed
from the SigLA material. Section 2 of [LICENSE](LICENSE) names the paths.

### GORILA

Godart, L., and Olivier, J.-P. (1976 to 1985). *Recueil des inscriptions en
lineaire A* (GORILA), vols. 1 to 5. Etudes Cretoises 21. Ecole francaise
d'Athenes.

Gave: the document sigla (the `HT 31`, `KH 5`, `ZA 8` naming convention that
every document id in this repository follows), the sign index and the Linear B
name column in volume 5, the concordances, and the plate page references.

Status: in copyright. Cited only. No page scan and no text of GORILA is
included in this repository. The extracted index tables under
`linear_a/data/gorila_*` record facts (row values, concordance rows, plate page
numbers), not GORILA's own expression.

### RILA Supplement 1

Del Freo, M., and Zurbach, J. (2024). *Recueil des inscriptions en lineaire A.
Supplement 1*. Etudes Cretoises 21.6. Ecole francaise d'Athenes.

Gave: the document list that the corpus is checked against, and the reading of
SKO Zc 2.

Status: in copyright. Cited only. No text of the supplement is included.

### John G. Younger, Linear A Texts

John G. Younger. *Linear A Texts and Inscriptions in phonetic transcription and
Commentary* and *Linear A Lexicon* (2024 snapshots).

Gave: readings, glosses and per-document commentary. The site codes and site
names used in the map layer follow GORILA and Younger.

Status: his copyright. Cited and quoted briefly with attribution. The
commentary is not republished in full.

### lineara.xyz

Robert Hogan, <https://lineara.xyz>.

Gave: the mirror that this project used as a source of readings and of
sign-value mappings, and the alias keys that resolve six RILA Supplement 1
documents.

Status: no licence file upstream, so no grant to redistribute. The verbatim
upstream dataset files were removed from this repository on 2026-09-18. See
`linear_a/data/sources/lineara/README.md`.

The photographs and facsimiles in that mirror are not included here. Their
image rights are largely Ecole francaise d'Athenes, recorded upstream as
"(c) Ecole Francaise d'Athenes", and they are marked not for publication or
redistribution.

### INSCRIBE

INSCRIBE project, Universita di Bologna. Copyright 2023.

Gave: the 3D model inventory. Museum, inventory number and find spot per
object.

Status: linked only. No model and no description text is included.

## Scholarship cited for specific results

### Fraction values

Corazza, M., Ferrara, S., Montecchi, B., Tamburini, F., and Valerio, M.
(2021). The mathematical values of fraction signs in the Linear A script.

Gave: the proposed mathematical values of the fraction signs.

Status: cited. Journal, volume and pages are not yet confirmed from the source.

### Other works cited

Davis, B. (2010). *Aegean pre-alphabetic writing*. Survey and overview.

Duhoux, Y. Readings and analyses of the Linear A texts, cited throughout the
benchmarks and the analysis notes.

Salgarella, E. (2020). *Wine ideogram AB131*. Logogram and commodity study.

The full citation list, with the other works this project reads, is in
[BIBLIOGRAPHY.md](BIBLIOGRAPHY.md). Every PDF stays in the private companion
repository under the copyright of its authors and publishers.

## Standards

### Unicode Consortium

The Linear A block (U+10600 to U+1077F) and the Unicode Character Database.

Gave: the codepoints, the sign names and the sign order used by the crosswalk
and by every `unicode_text` field.

Status: Unicode Terms of Use. Attribution given.

## Map and relief data

### Natural Earth

<https://www.naturalearthdata.com/about/terms-of-use/>

Gave: the 1:10m Land coastline that the Crete outline is simplified from, and
the Natural Earth II raster used for the alternative relief.

Status: public domain.

### Wikidata

Gave: the site coordinates, from property P625.

Status: CC0.

### NASA Blue Marble: Next Generation

Gave: the land colour and the sea of the relief raster.

Status: public domain (NASA). Credit requested: NASA Earth Observatory,
Reto Stockli.
<https://science.nasa.gov/earth/earth-observatory/blue-marble-next-generation/>

### Copernicus DEM GLO-30

Gave: the hillshade of the relief raster.

Status: free for the general public, attribution required. Attribution line,
verbatim:

> Relief: NASA Blue Marble: Next Generation (public domain, NASA Earth
> Observatory, R. Stockli). Hillshade from Copernicus DEM GLO-30, produced
> using Copernicus WorldDEM-30 (c) DLR e.V. 2010-2014 and (c) Airbus Defence
> and Space GmbH 2014-2018 provided under COPERNICUS by the European Union and
> ESA; all rights reserved.

The registry also asks for: "Copernicus Digital Elevation Model (DEM) was
accessed on 2026-09-07 from https://registry.opendata.aws/copernicus-dem".

### Map attribution line

For the outline and the site points, verbatim:

> Map outline: Natural Earth (public domain). Site coordinates: Wikidata
> (CC0). Site codes after GORILA and J. G. Younger, Linear A Texts.

One site coordinate is an exception: Ayios Stephanos, from Hope Simpson and
Janko, SMEA.

## Software

The analysis code in this repository uses these third-party libraries:

| Library | Use | Licence |
|---|---|---|
| Pillow (PIL) | image reading and raster work | MIT-CMU |
| PyMuPDF (`fitz`) | PDF text and image extraction | AGPL-3.0 |
| ImageHash | perceptual hashing of image crops | BSD-2-Clause |

Tesseract is not used by any script in this repository. Nothing else outside
the Python standard library is imported.

## A reader

A reader of the repository reported the pseudo-word defect by email on
2026-09-17 and asked for nothing. The report was correct on every point. The
reader is not named here, by choice.

## This project

Matt Navarre. Copyright 2026. The project's own code, text, analyses and
generated data are CC BY 4.0. See [LICENSE](LICENSE).

Suggested citation:

> Navarre, M. (2026). Minoan Linear A – Computational Research Project.
> https://github.com/Navarre-AI/linear-a · https://lineara.eu
