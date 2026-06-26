from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

ACCENT = RGBColor(0x0B, 0x5D, 0x8F)
ACCENT2 = RGBColor(0x0F, 0x8A, 0x6A)
INK = RGBColor(0x1A, 0x22, 0x30)
MUTED = RGBColor(0x5A, 0x65, 0x73)
SHADE = "F1F5F9"
SHADE_KPI = "EAF1F6"

doc = Document()

# base style
normal = doc.styles["Normal"]
normal.font.name = "Calibri"
normal.font.size = Pt(10)
normal.paragraph_format.space_after = Pt(5)
normal.paragraph_format.line_spacing = 1.12

for section in doc.sections:
    section.top_margin = Inches(0.55)
    section.bottom_margin = Inches(0.5)
    section.left_margin = Inches(0.7)
    section.right_margin = Inches(0.7)


def shade(paragraph, fill):
    pPr = paragraph._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:fill"), fill)
    pPr.append(shd)


def left_border_accent(paragraph, color="0B5D8F"):
    pPr = paragraph._p.get_or_add_pPr()
    pbdr = OxmlElement("w:pBdr")
    left = OxmlElement("w:left")
    left.set(qn("w:val"), "single")
    left.set(qn("w:sz"), "18")
    left.set(qn("w:space"), "8")
    left.set(qn("w:color"), color)
    pbdr.append(left)
    pPr.append(pbdr)


def add_runs(paragraph, segments, size=10, color=INK):
    # segments: list of (text, bold, italic)
    for text, bold, italic in segments:
        r = paragraph.add_run(text)
        r.bold = bold
        r.italic = italic
        r.font.size = Pt(size)
        r.font.color.rgb = color
    return paragraph


def heading(num_title):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(3)
    r = p.add_run(num_title)
    r.bold = True
    r.font.size = Pt(11)
    r.font.color.rgb = ACCENT
    r.font.all_caps = True
    # bottom border
    pPr = p._p.get_or_add_pPr()
    pbdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "8")
    bottom.set(qn("w:space"), "2")
    bottom.set(qn("w:color"), "0B5D8F")
    pbdr.append(bottom)
    pPr.append(pbdr)
    return p


def bullets(items):
    for seg in items:
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.08
        add_runs(p, seg, size=9.5)


def callout(segments, color="0B5D8F"):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(6)
    shade(p, SHADE)
    left_border_accent(p, color)
    add_runs(p, segments, size=9.5)
    return p


# ---------- Title block ----------
title = doc.add_paragraph()
title.paragraph_format.space_after = Pt(1)
r = title.add_run("Corpus Christi Area Power Infrastructure")
r.bold = True
r.font.size = Pt(19)
r.font.color.rgb = ACCENT

sub = doc.add_paragraph()
sub.paragraph_format.space_after = Pt(2)
r = sub.add_run("Shore Power (Cold Ironing) — Overview in support of our Feasibility Study proposal")
r.font.size = Pt(10)
r.font.color.rgb = MUTED

meta = doc.add_paragraph()
meta.paragraph_format.space_after = Pt(6)
r = meta.add_run("Prepared: June 2026   |   Region: ERCOT South / Coastal Zone   |   TDSP/TSP: AEP Texas")
r.font.size = Pt(8.5)
r.font.color.rgb = MUTED
# bottom border under header
pPr = meta._p.get_or_add_pPr()
pbdr = OxmlElement("w:pBdr")
bottom = OxmlElement("w:bottom")
bottom.set(qn("w:val"), "single"); bottom.set(qn("w:sz"), "12"); bottom.set(qn("w:space"), "4"); bottom.set(qn("w:color"), "0B5D8F")
pbdr.append(bottom); pPr.append(pbdr)

# purpose callout
callout([
    ("Purpose of this document. ", True, False),
    ("We are responding to the RFP by proposing to perform the ", False, False),
    ("shore-power feasibility study", True, False),
    (". As a ", False, False),
    ("local firm with more than 30 design professionals based in Corpus Christi", True, False),
    (" — including in-house coastal, electrical, and infrastructure expertise — we bring on-the-ground knowledge of "
     "the port, the AEP Texas grid, and the region's coastal hazards. The material below frames our understanding "
     "of the problem and the scope our study will rigorously evaluate — it is ", False, False),
    ("not", False, True),
    (" a final engineering design. Figures are planning-level and represent the questions the feasibility "
     "study will resolve, not committed values.", False, False),
])

# lede
p = doc.add_paragraph()
add_runs(p, [
    ("This overview summarizes the electrical supply environment serving the Port of Corpus Christi and frames "
     "the phased shore-power buildout our feasibility study will assess — from a ", False, False),
    ("2-berth pilot", True, False),
    (" to a full ", False, False),
    ("20-berth", True, False),
    (" deployment — covering the regional grid, the ERCOT interconnection pathway for loads of this magnitude, "
     "and the resiliency strategy for a hurricane-exposed coastal industrial port.", False, False),
])

# ---------- KPI row ----------
kpis = [("~5 MW", "Typical load / berth"), ("~10 MW", "Phase 1 (2 berths)"),
        ("~100 MW", "Full build (20 berths)"), ("75 MW", "ERCOT Large-Load threshold")]
kt = doc.add_table(rows=1, cols=4)
kt.alignment = WD_TABLE_ALIGNMENT.CENTER
for i, (num, label) in enumerate(kpis):
    cell = kt.rows[0].cells[i]
    # shading
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd"); shd.set(qn("w:val"), "clear"); shd.set(qn("w:fill"), SHADE_KPI); tcPr.append(shd)
    cell.paragraphs[0].text = ""
    pn = cell.paragraphs[0]
    pn.paragraph_format.space_after = Pt(0)
    rn = pn.add_run(num); rn.bold = True; rn.font.size = Pt(14); rn.font.color.rgb = ACCENT
    pl = cell.add_paragraph()
    pl.paragraph_format.space_before = Pt(0)
    rl = pl.add_run(label); rl.font.size = Pt(8); rl.font.color.rgb = MUTED
doc.add_paragraph().paragraph_format.space_after = Pt(2)

# ---------- Section 1 ----------
heading("1. Regional Grid Context")
p = doc.add_paragraph()
add_runs(p, [
    ("The Port of Corpus Christi is the largest U.S. energy-export gateway and sits within the ", False, False),
    ("ERCOT South (Coastal) load zone", True, False),
    (". Transmission and distribution service in Nueces and San Patricio counties is provided primarily by ", False, False),
    ("AEP Texas", True, False),
    (", with portions of the high-voltage backbone owned by ", False, False),
    ("Electric Transmission Texas (ETT)", True, False),
    (". The local network is anchored by a robust ", False, False),
    ("138 kV", True, False),
    (" ring around the inner harbor and a ", False, False),
    ("345 kV", True, False),
    (" backbone tying the area into the broader ERCOT grid. Substantial dispatchable generation sits inside "
     "the load pocket, favorable for both voltage support and resource adequacy:", False, False),
])
bullets([
    [("Barney M. Davis", True, False), (" — ~897 MW gas (units 1974 / 2010)", False, False)],
    [("Nueces Bay", True, False), (" — ~635 MW gas, combined-cycle (2010)", False, False)],
    [("Lon C. Hill", True, False), (" — legacy gas peaking capacity", False, False)],
])
p = doc.add_paragraph()
add_runs(p, [
    ("This ~1.5 GW of in-zone generation (now CPS Energy-owned, acquired from Talen in 2024) means the "
     "shore-power load can be served from a generation-rich pocket rather than a constrained import path. Key "
     "substations relevant to a port-side interconnection include ", False, False),
    ("Holly Road, McKenzie Road, Lon Hill, Nueces Bay, Barney Davis, Naval Base, and Warburton", True, False),
    (" — several within a few miles of the port's principal docks.", False, False),
])
callout([
    ("What our study will test: ", True, False),
    ("our working hypothesis is that a 2-berth pilot (~10 MW) can be served at distribution voltage "
     "(12.47/25 kV) from an existing AEP Texas circuit, while the full 20-berth program (~80–120 MW) warrants a ", False, False),
    ("dedicated port substation", False, True),
    (" fed at 138 kV. The feasibility study will validate both the near-term distribution tap and the long-term "
     "transmission-class delivery point, with order-of-magnitude cost and schedule for each.", False, False),
])

# ---------- Section 2: map ----------
heading("2. Channel Reaches, Berths & Power Assets")
p = doc.add_paragraph()
add_runs(p, [
    ("The Corpus Christi Ship Channel runs ~29 miles from the Gulf entrance to the Viola Turning Basin, with the "
     "La Quinta Channel (~6 miles) branching north (~35 nautical miles of federal channel total). The USACE/Port ", False, False),
    ("Channel Improvement Project (CIP)", True, False),
    (" is deepening it from ", False, False),
    ("47 to 54 ft MLLW", True, False),
    (" and widening it to ", False, False),
    ("530 ft", True, False),
    (" with barge shelves across the Upper Bay. Deeper water draws larger, fully-laden vessels with higher "
     "hotelling demand — strengthening the case for shore power. Berths concentrate in the ", False, False),
    ("Inner Harbor", True, False),
    (", with additional energy terminals along ", False, False),
    ("La Quinta/Ingleside", True, False),
    (".", False, False),
])
pic = doc.add_paragraph()
pic.alignment = WD_ALIGN_PARAGRAPH.CENTER
pic.paragraph_format.space_after = Pt(2)
pic.add_run().add_picture("map_for_docx.png", width=Inches(7.0))
cap = doc.add_paragraph()
cap.paragraph_format.space_after = Pt(4)
r = cap.add_run(
    "Figure 1 — Geographic Network Diagram (not to scale). Channel reaches Gulf-to-inland: Entrance/Jetty (3.9 mi), "
    "Lower Bay (8.6 mi), Upper Bay (9.6 mi), Inner Harbor (7.3 mi), with the La Quinta Channel (5.9 mi) branching "
    "north. Power assets and berth locations are approximate; a surveyed GIS alignment is to be developed during "
    "the feasibility study.")
r.font.size = Pt(8); r.font.color.rgb = MUTED; r.italic = True

# ---------- Page break to page 2 ----------
doc.add_page_break()

# ---------- Section 3: phasing ----------
heading("3. Phased Buildout — 2 Berths to 20 Berths")
p = doc.add_paragraph()
add_runs(p, [
    ("Shore power (cold ironing / high-voltage shore connection, HVSC) supplies vessels at berth at ", False, False),
    ("6.6 kV or 11 kV", True, False),
    (" per IEC/IEEE 80005-1, allowing main and auxiliary engines to shut down. Per-berth demand depends on vessel "
     "class; for the Corpus mix (tankers, bulk, dry cargo, occasional container) a planning figure of ", False, False),
    ("~5 MW/berth", True, False),
    (" is reasonable, with diversity reducing the coincident peak below the simple sum.", False, False),
])

rows = [
    ("Phase", "Horizon", "Berths", "Approx. connected load", "Delivery / interconnection"),
    ("Phase 1 — Pilot", "Yr 1–2", "2", "~8–12 MW", "Distribution tap off existing AEP Texas circuit"),
    ("Phase 2 — Expand", "Yr 2–4", "6", "~25–30 MW", "New distribution substation / express feeders (crosses 25 MW)"),
    ("Phase 3 — Scale", "Yr 4–7", "12", "~55–70 MW", "Begin dedicated 138 kV substation (nears 75 MW)"),
    ("Phase 4 — Full", "Yr 7–10", "20", "~90–120 MW", "Dedicated 138 kV port substation; full LLIS"),
]
tbl = doc.add_table(rows=len(rows), cols=5)
tbl.style = "Light Grid Accent 1"
widths = [Inches(1.25), Inches(0.8), Inches(0.65), Inches(1.6), Inches(2.7)]
for ri, row in enumerate(rows):
    for ci, val in enumerate(row):
        cell = tbl.rows[ri].cells[ci]
        cell.width = widths[ci]
        para = cell.paragraphs[0]
        para.paragraph_format.space_after = Pt(1)
        run = para.add_run(val)
        run.font.size = Pt(8.5)
        if ri == 0:
            run.bold = True
            run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            tcPr = cell._tc.get_or_add_tcPr()
            shd = OxmlElement("w:shd"); shd.set(qn("w:val"), "clear"); shd.set(qn("w:fill"), "0B5D8F"); tcPr.append(shd)
        elif ci == 0:
            run.bold = True

note = doc.add_paragraph()
note.paragraph_format.space_before = Pt(3)
add_runs(note, [
    ("Geographically, the pilot targets ", False, True),
    ("Inner Harbor", True, True),
    (" berths closest to existing AEP Texas feeders, expanding along the Inner Harbor and then to the ", False, True),
    ("La Quinta/Ingleside", True, True),
    (" energy terminals as a dedicated 138 kV substation comes online. This sequences the ERCOT studies so the "
     "substation is energized ahead of the berths that depend on it. Berth counts, loads, and horizons are the "
     "planning basis the study will refine against surveyed vessel data and AEP Texas hosting-capacity input.", False, True),
], size=8.5, color=MUTED)

# ---------- Section 4: ERCOT ----------
heading("4. ERCOT Interconnection for Loads of This Size")
p = doc.add_paragraph()
add_runs(p, [
    ("ERCOT formalized large-load interconnection through ", False, False),
    ("NPRR1234", True, False),
    (" and ", False, False),
    ("PGRR115", True, False),
    (" (approved by the ERCOT Board on ", False, False),
    ("April 8, 2025", True, False),
    ("; phased implementation from July 21, 2025, with key PGRR115 provisions effective Dec 15, 2025). Two "
     "thresholds govern this program:", False, False),
])
bullets([
    [("≥ 25 MW", True, False), (" — modeling standards apply; the load must be explicitly represented in ERCOT "
                                "planning cases. ", False, False), ("Reached around Phase 2.", False, True)],
    [("≥ 75 MW", True, False), (" aggregate at a single site behind common point(s) of interconnection — triggers "
                                "the full ", False, False), ("Large Load Interconnection Study (LLIS)", True, False),
     (". ", False, False), ("Reached at Phase 3–4.", False, True)],
])
p = doc.add_paragraph()
add_runs(p, [
    ("The LLIS is led by the interconnecting ", False, False),
    ("TSP (AEP Texas)", True, False),
    (" and includes ", False, False),
    ("steady-state, short-circuit, and dynamic/transient stability", True, False),
    (" analyses. A study fee of ", False, False),
    ("~$14,000 per LLIS request", True, False),
    (" applies. Large loads must clear ERCOT's ", False, False),
    ("Quarterly Stability Assessment (QSA)", True, False),
    (" before Initial Energization. Each project submits a step-by-step ramp-up schedule with milestone demands, "
     "and must demonstrate development milestones (land control, permits, study payments) to hold queue position.", False, False),
])
callout([
    ("Feasibility study deliverable: ", True, False),
    ("Because the program crosses both the 25 MW and 75 MW thresholds over time, our study will map the "
     "ERCOT/AEP Texas interconnection pathway and timeline — identifying when modeling submissions (Phase 2) and "
     "the LLIS (ahead of Phase 3/4) must start so transmission facilities land on the critical path, not behind "
     "it — and flag this coordination as a defined downstream deliverable for the implementation phase.", False, False),
])

# ---------- Page 3: reliability + resiliency ----------
doc.add_page_break()

heading("5. Transmission Reliability & the Harvey Benchmark")
p = doc.add_paragraph()
add_runs(p, [
    ("Under normal “blue-sky” conditions the 345 kV and 138 kV network is effectively always available: "
     "bulk-transmission availability routinely exceeds ", False, False),
    ("99.9%", True, False),
    (", and ", False, False),
    ("N-1", True, False),
    (" design ensures any single line or transformer can fail without dropping load. The correct planning "
     "assumption is therefore not that the grid ", False, False),
    ("never", False, True),
    (" fails, but that it is highly reliable ", False, False),
    ("except under a major hurricane", True, False),
    (" — the one scenario a Gulf-coast port must explicitly design for. ", False, False),
    ("Hurricane Harvey", True, False),
    (" (Category 4, landfall at Rockport/Port Aransas essentially at Corpus Christi, Aug 2017) is the governing "
     "benchmark and shows that even the bulk transmission system is not immune:", False, False),
])
lead = doc.add_paragraph()
lead.paragraph_format.space_after = Pt(1)
add_runs(lead, [("Harvey at a glance (AEP Texas / ERCOT South-Coastal):", True, False)], size=9.5, color=ACCENT)
bullets([
    [("Forced outages on ", False, False), ("six 345 kV lines", True, False), (" and ", False, False),
     ("200+ 69–138 kV lines", True, False), (" along the coast.", False, False)],
    [("~25% of AEP Texas’s ~1M customers", True, False), (" lost power; ~3,100+ distribution poles and "
     "~500 transmission structures damaged; ~712 miles of conductor replaced; 5,600 mutual-aid linemen.", False, False)],
    [("A Port Aransas substation was swamped by storm surge", True, False), (" — saltwater destroyed breakers, "
     "which had to be replaced.", False, False)],
    [("Corpus’s Inner Harbor recovered in days", True, False), (" (~12,000 peak outages); the hardest-hit "
     "coastal communities nearest the entrance and La Quinta/Ingleside were ", False, False),
     ("not fully restored for ~2 weeks", True, False), (".", False, False)],
])
# coastal storm-surge subsection
sub = doc.add_paragraph()
sub.paragraph_format.space_before = Pt(4)
sub.paragraph_format.space_after = Pt(1)
add_runs(sub, [("Coastal storm-surge exposure", True, False)], size=10, color=INK)
p = doc.add_paragraph()
add_runs(p, [
    ("Hurricane Harvey was a significant surge event, but by no means the worst that can be expected. SLOSH "
     "modeling by the National Weather Service (NWS) shows the “maximum of maximums” anticipated from storm surge; "
     "while it does not capture compound (rainfall/riverine) flooding, it clearly demonstrates the footprint where "
     "surge waters would propagate through the inner-harbor region. The NWS storm-surge inundation map for the "
     "100-year annual exceedance probability (Figure 2) illustrates this footprint across the Corpus Christi inner "
     "harbor. We recommend using the U.S. Army Corps of Engineers (USACE) ", False, False),
    ("Coastal Hazard System (CHS)", True, False),
    (" to conduct a desktop analysis of ", False, False),
    ("annual exceedance probabilities (AEPs)", True, False),
    (" to determine the required protective elevations for power infrastructure — substations, switchgear, and "
     "shore-power converters.", False, False),
])

# Figure 2 — surge map (embedded if present, else placeholder box)
import os
surge_img = "storm-surge-corpus.png"
fig2 = doc.add_paragraph()
fig2.alignment = WD_ALIGN_PARAGRAPH.CENTER
fig2.paragraph_format.space_after = Pt(2)
if os.path.exists(surge_img):
    fig2.add_run().add_picture(surge_img, width=Inches(6.4))
else:
    box = fig2.add_run("[ NWS storm-surge inundation map (100-yr annual exceedance probability), "
                       "Corpus Christi inner harbor — image to be embedded ]")
    box.italic = True
    box.font.size = Pt(9)
    box.font.color.rgb = MUTED
    shade(fig2, SHADE)
cap2 = doc.add_paragraph()
cap2.paragraph_format.space_after = Pt(4)
r = cap2.add_run(
    "Figure 2 — NWS storm-surge inundation map, 100-year annual exceedance probability, Corpus Christi inner "
    "harbor. Surge-depth bands (4–6 ft up to 18–25 ft) define the inundation footprint that governs siting and "
    "protective elevation of port power infrastructure. Source: National Weather Service.")
r.font.size = Pt(8); r.font.color.rgb = MUTED; r.italic = True

callout([
    ("Implication for backup power: ", True, False),
    ("shore power cannot assume grid availability during a Harvey-class event. For priority berths, "
     "backup/islanding should be sized to a ", False, False),
    ("multi-day to ~2-week restoration window", True, False),
    (" — favoring on-site/standby generation paired with BESS rather than batteries alone — and coastal substations "
     "and switchgear must be hardened against storm surge and saltwater intrusion (elevated pads, "
     "sealed/submersible-rated breakers) per the Port Aransas failure mode. Equipment platform elevations should be "
     "set from the USACE CHS / AEP analysis above. Because the entrance and La Quinta/Ingleside berths sit nearer "
     "the worst-hit zone than the Inner Harbor, backup duration and protective elevation should scale by berth "
     "location.", False, False),
], color="0F8A6A")

# ---------- Page 4: resiliency measures ----------
doc.add_page_break()
heading("6. Resiliency Measures & Backup Power")
bullets([
    [("N-1 redundancy & looped feeds: ", True, False), ("the dedicated port substation takes dual 138 kV sources "
        "from independent points on the ring, so a single line/transformer outage cannot de-energize the berths.", False, False)],
    [("In-zone generation buffer: ", True, False), ("proximity to Barney Davis, Nueces Bay, and Lon Hill (~1.5 GW) "
        "supports local voltage and resource adequacy during import constraints.", False, False)],
    [("BESS: ", True, False), ("peak-shaving, ride-through for momentary disturbances, and smoother load steps as "
        "vessels connect/disconnect.", False, False)],
    [("On-site / standby generation: ", True, False), ("for storm-duration islanding beyond battery economics, "
        "sized to priority-berth load over the expected restoration window.", False, False)],
    [("Microgrid & islanding: ", True, False), ("island critical berths on local generation/BESS during grid "
        "outages, with black-start capability for priority docks.", False, False)],
    [("Storm hardening: ", True, False), ("elevated/flood-rated pads, wind-rated structures, sealed/surge-rated "
        "switchgear, and corrosion protection for the marine/salt-air environment.", False, False)],
    [("Power quality & redundant conversion: ", True, False), ("frequency conversion (50/60 Hz vessels), harmonic "
        "mitigation, reactive support, and N+1 shore-power converters so one failed unit does not strand a berth.", False, False)],
])
callout([
    ("Resiliency target: ", True, False),
    ("priority berths ride through a single transmission contingency without interruption and can island for a "
     "defined storm-restoration window — protecting air-quality compliance and continuity of port operations "
     "through the next Harvey-class event.", False, False),
])

# closing
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(4)
add_runs(p, [
    ("What our feasibility study will deliver: ", True, False),
    ("(1) surveyed per-berth load profiles and coincident-demand diversity; (2) a costed Phase 1 pilot vs. "
     "Phase 4 138 kV substation comparison; (3) a mapped ERCOT/AEP Texas interconnection pathway with LLIS timing; "
     "(4) a recommended BESS/microgrid resiliency package with availability targets; and (5) a storm-resilience "
     "basis of design benchmarked to Hurricane Harvey, sizing backup/islanding to the expected restoration window "
     "by berth location — concluding with a go/no-go recommendation and a phased implementation roadmap.", False, False),
], size=9.5)

# sources
src = doc.add_paragraph()
src.paragraph_format.space_before = Pt(6)
pPr = src._p.get_or_add_pPr()
pbdr = OxmlElement("w:pBdr")
top = OxmlElement("w:top"); top.set(qn("w:val"), "single"); top.set(qn("w:sz"), "6"); top.set(qn("w:space"), "4"); top.set(qn("w:color"), "C9D2DD")
pbdr.append(top); pPr.append(pbdr)
r = src.add_run("Sources: USACE CCSC Channel Improvement Project (2019) & Coastal Hazard System; NWS SLOSH "
                "storm-surge inundation mapping; ERCOT NPRR1234 / PGRR115 & Harvey response; AEP Texas / ETT "
                "filings; U.S. DOE/EIA Hurricane Harvey event reports; CPS Energy / Talen; IEC/IEEE 80005-1.")
r.font.size = Pt(7.5); r.font.color.rgb = MUTED

out = "/home/user/trustclaw/docs/corpus-shore-power-rfp/corpus-area-power-infrastructure.docx"
doc.save(out)
print("saved", out)
