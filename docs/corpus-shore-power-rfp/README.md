# Corpus Christi Area Power Infrastructure — Shore Power RFP Overview

`corpus-area-power-infrastructure.html` is a self-contained, print-ready **4-page** overview
prepared in support of **our proposal to perform the shore-power (cold ironing) feasibility study**
for the Port of Corpus Christi. It frames our understanding of the problem and the scope the study
will evaluate — it is not a final engineering design, and the figures shown are the planning-level
questions the study will resolve. It includes an inline **SVG location map** (no external assets)
oriented to the USACE Corpus Christi Ship Channel Improvement Project — showing the labeled channel
reaches (Entrance/Jetty, Lower Bay, Upper Bay, Inner Harbor, and the La Quinta branch), berth
locations, the AEP Texas 138 kV ring, the 345 kV backbone, key substations, and in-zone generation.

## Files

- `corpus-area-power-infrastructure.html` — editable source; print / "Save as PDF" for a 4-page Letter document.
- `corpus-area-power-infrastructure.docx` — Word version (same content; the map is embedded as a high-resolution
  image since Word does not render inline SVG reliably across versions).

> **Pending asset — Figure 2 (storm-surge map):** Section 5 references an NWS storm-surge inundation map
> (100-yr annual exceedance probability) for the Corpus Christi inner harbor. The graphic is currently a
> placeholder. To embed it, drop the image at `assets/storm-surge-corpus.png` (HTML) / `storm-surge-corpus.png`
> next to `generate-docx.py` (Word) and re-render. Inline-pasted images are not accessible to the build — attach
> the file so it lands on disk.

## How to use

- **HTML:** open in any browser, then Print / "Save as PDF" — print CSS paginates it cleanly to 4 pages (Letter).
- **Word:** open the `.docx` directly in Microsoft Word or Google Docs. Page breaks separate the four pages;
  exact pagination can vary slightly by Word version/printer, so confirm before final distribution.

## Contents

1. Regional grid context (ERCOT South/Coastal zone, AEP Texas/ETT, in-zone generation)
2. Channel reaches, berths & power assets — embedded SVG map (USACE CIP geometry)
3. Phased buildout — 2 berths → 20 berths (~10 MW → ~100 MW)
4. ERCOT interconnection for loads of this size (NPRR1234 / PGRR115, LLIS)
5. Transmission reliability & the Hurricane Harvey benchmark; coastal storm-surge exposure (NWS SLOSH / USACE CHS)
6. Resiliency measures & backup power (N-1, BESS, standby gen, microgrid/islanding, storm hardening)

## Key planning figures

| Item | Value |
| --- | --- |
| Typical load per berth (planning) | ~5 MW (HVSC at 6.6/11 kV, IEC/IEEE 80005-1) |
| Phase 1 pilot (2 berths) | ~8–12 MW, distribution-level |
| Full build (20 berths) | ~90–120 MW, dedicated 138 kV substation |
| ERCOT modeling threshold | ≥ 25 MW |
| ERCOT Large Load Interconnection Study (LLIS) threshold | ≥ 75 MW aggregate at a single site |
| LLIS study fee | ~$14,000 per request |

## Sources

- USACE Galveston District / Port Corpus Christi — *Corpus Christi Ship Channel Improvement Project*, Summer Stakeholder Partnering Forum (Aug 14, 2019) — channel reaches, dimensions, and CIP contracts. (Provided as the `09_Stakeholder_Meeting_08142019` PDF.)
- [Port of Corpus Christi — Completes Milestone Ship Channel Improvement Project](https://portofcc.com/port-of-corpus-christi-completes-milestone-ship-channel-improvement-project-reinforcing-u-s-as-leader-in-energy-exports/)
- [ERCOT — Large Load Integration](https://www.ercot.com/services/rq/large-load-integration)
- [ERCOT — Large Load Interconnection Process Q&A (PDF)](https://www.ercot.com/files/docs/2025/12/24/Large-Load-Interconnection-Process-Q-A.pdf)
- [ERCOT — NPRR1234 issue page](https://www.ercot.com/mktrules/issues/NPRR1234)
- [EPE Consulting — ERCOT's Large Load Interconnection Process Now Approved](https://epeconsulting.com/epe-intelligence/news/ercots-large-load-interconnection-process-now-approved-by-ercots-board-of-directors)
- [Zero-Emission Grid — NPRR1234 & PGRR115: What Large-Load Developers Must Know](https://www.zeroemissiongrid.com/insights-press-zeg-blog/nprr-1234-pgrr-115/)
- [AEP Transmission — Texas Projects](https://www.aeptransmission.com/texas/)
- [Electric Transmission Texas — Barney Davis project](http://www.ettexas.com/Projects/BarneyDavis)
- [CPS Energy closes acquisition of Talen Energy gas plants (Corpus Christi)](https://newsroom.cpsenergy.com/cps-energy-closes-on-previously-announced-acquisition-of-talen-energy-gas-plants-in-corpus-christi-and-laredo/)
- [Power Engineering — CPS Energy gas portfolio acquisition](https://www.power-eng.com/gas/turbines/cps-energy-beefs-up-natural-gas-fleet-with-785-million-transaction/)
- [Cold ironing — overview (Wikipedia)](https://en.wikipedia.org/wiki/Cold_ironing)
- [U.S. EIA — Hurricane Harvey caused electric system outages and affected wind generation in Texas](https://www.eia.gov/todayinenergy/detail.php?id=32892)
- [Utility Dive — AEP CEO: Harvey 'devastated' transmission, distribution system in south Texas](https://www.utilitydive.com/news/aep-ceo-harvey-devastated-transmission-distribution-system-in-south-tex/504043/)
- [T&D World — AEP Texas Overcomes Hurricane Destruction](https://www.tdworld.com/electric-utility-operations/article/20970767/aep-texas-overcomes-hurricane-destruction)
- [ERCOT — Responds to Hurricane Harvey](https://www.ercot.com/help/harvey)
- [NWS — Storm surge / SLOSH (Maximum of Maximums) inundation mapping](https://www.nhc.noaa.gov/nationalsurge/)
- [USACE — Coastal Hazards System (CHS)](https://chs.erdc.dren.mil/)

> Figures are planning-level approximations for RFP framing. Substation positions on the map are
> schematic and not to scale; a surveyed GIS alignment should be developed during preliminary engineering.
