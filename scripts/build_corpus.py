"""Rebuild the sample corpus from the prose, charts and speech scripts below.

Writes data/core and data/corpus. Only run when the corpus changes: PDF metadata carries a
timestamp, so a rebuild shows as a diff even when nothing else did. Needs requirements-dev.txt
and the espeak-ng binary on PATH.
"""
import subprocess
import textwrap
from pathlib import Path
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Wedge
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak

ROOT = str(Path(__file__).resolve().parent.parent / "data")
def md(path, text): open(path, "w").write(textwrap.dedent(text).strip() + "\n")

# ---------------- core tier: short, stable, held in context ----------------
md(f"{ROOT}/core/overview.md", """
# The Solar System in brief

The Solar System is the Sun together with everything bound to it by gravity: eight planets,
their moons, five recognised dwarf planets, and countless asteroids, comets and other small bodies.
It formed about 4.6 billion years ago from a collapsing cloud of gas and dust.

The eight planets, in order of increasing distance from the Sun, are Mercury, Venus, Earth, Mars,
Jupiter, Saturn, Uranus and Neptune. The first four are the inner or terrestrial planets: small,
dense and rocky, with solid surfaces. The outer four are giants. Jupiter and Saturn are gas giants
made mostly of hydrogen and helium; Uranus and Neptune are ice giants with more water, ammonia and
methane in their interiors.

Between Mars and Jupiter lies the asteroid belt. Beyond Neptune lies the Kuiper belt, a ring of icy
bodies that includes Pluto. All eight planets orbit the Sun in the same direction and in nearly the
same plane, called the ecliptic.
""")
md(f"{ROOT}/core/glossary.md", """
# Glossary

- Astronomical unit (AU): the average distance from Earth to the Sun, about 150 million kilometres.
  Distances inside the Solar System are usually quoted in AU.
- Orbit: the path a body follows around a more massive body. A planet's orbital period is its year.
- Rotation: a body spinning on its own axis. A planet's rotation period is its day.
- Axial tilt: the angle between a planet's rotation axis and the line perpendicular to its orbit.
  Tilt is what produces seasons.
- Terrestrial planet: a rocky planet with a solid surface. Mercury, Venus, Earth and Mars.
- Gas giant: a large planet made mostly of hydrogen and helium with no solid surface. Jupiter and Saturn.
- Ice giant: a large planet whose interior is dominated by water, ammonia and methane. Uranus and Neptune.
- Dwarf planet: a body that orbits the Sun and is round under its own gravity but has not cleared
  the neighbourhood of its orbit.
- Moon (natural satellite): a body that orbits a planet or dwarf planet rather than the Sun directly.
- Retrograde: motion in the direction opposite to the usual one. Most planets rotate in the same
  direction they orbit; a retrograde rotation goes the other way.
""")
md(f"{ROOT}/core/planets_at_a_glance.md", """
# Planets at a glance

| Planet  | Order | Type        | Rings | Known moons (approx.) |
|---------|-------|-------------|-------|-----------------------|
| Mercury | 1     | terrestrial | no    | 0                     |
| Venus   | 2     | terrestrial | no    | 0                     |
| Earth   | 3     | terrestrial | no    | 1                     |
| Mars    | 4     | terrestrial | no    | 2                     |
| Jupiter | 5     | gas giant   | faint | 90+                   |
| Saturn  | 6     | gas giant   | yes   | 140+                  |
| Uranus  | 7     | ice giant   | faint | 27                    |
| Neptune | 8     | ice giant   | faint | 16                    |

Moon counts change as new small moons are confirmed, so the numbers above are rounded.
Only the four giant planets have ring systems; Saturn's is the only one easily visible from Earth.
""")

# ---------------- retrieved tier: markdown ----------------
md(f"{ROOT}/corpus/mercury.md", """
# Mercury

Mercury is the smallest planet in the Solar System and the closest to the Sun, with an equatorial
diameter of about 4,879 kilometres. It has no moons and almost no atmosphere, only a thin exosphere
of atoms knocked off its surface by the solar wind.

Because there is no atmosphere to hold heat, the temperature swings more than on any other planet:
roughly 430 degrees Celsius on the day side and minus 180 degrees Celsius at night. Despite being
closest to the Sun it is not the hottest planet; that title belongs to Venus.

Mercury completes an orbit in 88 Earth days but rotates slowly, once every 59 Earth days. The
combination means a single solar day on Mercury, from one sunrise to the next, lasts about 176
Earth days. Its surface is heavily cratered and looks much like the Moon. The largest impact
feature is the Caloris Basin, about 1,550 kilometres across.

Two spacecraft have studied Mercury closely: Mariner 10 flew past three times in 1974 and 1975, and
MESSENGER orbited it from 2011 until 2015, mapping the entire surface and confirming water ice in
permanently shadowed craters near the poles.
""")
md(f"{ROOT}/corpus/venus.md", """
# Venus

Venus is the second planet from the Sun and the hottest, with an average surface temperature of
about 465 degrees Celsius. The heat comes from a dense carbon dioxide atmosphere that traps
infrared radiation in a runaway greenhouse effect. Surface pressure is about 92 times that of
Earth at sea level, and the clouds are made of sulphuric acid droplets.

Venus is often called Earth's twin because the two are nearly the same size: Venus has a diameter
of about 12,104 kilometres against Earth's 12,756. The similarity ends there. Venus rotates
backwards, or retrograde, so the Sun rises in the west, and it rotates very slowly. One rotation
takes 243 Earth days, longer than its 225-day year.

The surface is mostly volcanic plains with some highland regions. The highest mountain, Maxwell
Montes, rises about 11 kilometres. Venus has no moons and no rings.

The Soviet Venera programme landed several probes on the surface in the 1970s and 1980s; the
longest survived about two hours before the heat and pressure destroyed it. NASA's Magellan
orbiter mapped the surface with radar between 1990 and 1994.
""")
md(f"{ROOT}/corpus/earth.md", """
# Earth

Earth is the third planet from the Sun and the only body known to support life. About 71 percent
of its surface is covered by liquid water. The atmosphere is roughly 78 percent nitrogen and 21
percent oxygen, with the remainder mostly argon and a small but climatically important amount of
carbon dioxide.

Earth's rotation axis is tilted about 23.4 degrees relative to its orbit. This tilt, not the
changing distance from the Sun, is what causes the seasons: the hemisphere tilted towards the Sun
receives more direct sunlight and longer days.

The planet rotates once every 23 hours and 56 minutes relative to the stars, and orbits the Sun
once every 365.25 days, which is why a leap day is added every four years. Earth has a molten
outer core of iron and nickel whose motion generates a magnetic field. That field deflects most of
the solar wind and is responsible for the aurorae near the poles.

Earth is the densest planet in the Solar System and the largest of the four terrestrial planets.
Its outer shell is broken into tectonic plates whose slow movement builds mountains, opens ocean
basins and causes earthquakes.
""")
md(f"{ROOT}/corpus/mars.md", """
# Mars

Mars is the fourth planet from the Sun and about half the diameter of Earth, at 6,792 kilometres.
Iron oxide dust gives the surface its rusty colour. The atmosphere is thin, about 0.6 percent of
Earth's surface pressure, and is mostly carbon dioxide. Average surface temperature is around
minus 60 degrees Celsius.

Mars has the largest volcano in the Solar System, Olympus Mons, which rises about 22 kilometres
above the surrounding plains, and the largest canyon system, Valles Marineris, which stretches
roughly 4,000 kilometres. Both polar caps contain water ice covered by a seasonal layer of frozen
carbon dioxide.

A Martian day, called a sol, lasts 24 hours and 37 minutes, close to an Earth day. The Martian year
is 687 Earth days. Mars has two small moons, which are described in a separate recording.

Several rovers have operated on the surface. Curiosity landed in Gale Crater in 2012 and
Perseverance landed in Jezero Crater in 2021, where it collects rock samples intended for a future
return to Earth. Evidence from orbiters and rovers shows that liquid water flowed on Mars in the
distant past.
""")
md(f"{ROOT}/corpus/jupiter.md", """
# Jupiter

Jupiter is the fifth planet from the Sun and by far the largest, with an equatorial diameter of
about 142,984 kilometres, eleven times that of Earth. It contains more than twice the mass of all
the other planets combined, about 318 Earth masses. It is a gas giant made mostly of hydrogen and
helium with no solid surface.

Jupiter rotates faster than any other planet, once every ten hours, which flattens it noticeably at
the poles. Its banded appearance comes from alternating jet streams. The Great Red Spot is a storm
larger than Earth that has been observed for at least 190 years, although it has been shrinking.

Jupiter has more than ninety known moons. The four largest, discovered by Galileo in 1610, are
covered in a separate recording. It also has a faint ring system made of dust, discovered by
Voyager 1 in 1979.

The planet's strong magnetic field traps charged particles in intense radiation belts. NASA's Juno
spacecraft has orbited Jupiter since 2016, studying its interior, atmosphere and magnetosphere.
""")
md(f"{ROOT}/corpus/saturn.md", """
# Saturn

Saturn is the sixth planet from the Sun and the second largest, with an equatorial diameter of
about 120,536 kilometres. Like Jupiter it is a gas giant made mostly of hydrogen and helium. Its
average density is less than that of water, the lowest of any planet.

Saturn's rings are its most recognisable feature. They are made mostly of water ice, in pieces
ranging from dust grains to boulders several metres across. The main rings span about 280,000
kilometres from edge to edge but are typically only tens of metres thick. They are labelled with
letters in order of discovery, so the bright A and B rings are separated by the Cassini Division.

A persistent hexagonal jet stream surrounds Saturn's north pole, a pattern not seen on any other
planet. Saturn has more than 140 known moons; the two most studied, Titan and Enceladus, are
covered in a separate recording.

The Cassini spacecraft orbited Saturn from 2004 until 2017, when it was deliberately flown into
the atmosphere to avoid contaminating any of the moons.
""")
md(f"{ROOT}/corpus/small_bodies.md", """
# Asteroids, comets and meteors

The asteroid belt lies between the orbits of Mars and Jupiter. Despite containing millions of
objects, its total mass is only about three percent of the Moon's, and the objects are so spread
out that spacecraft pass through it without difficulty. Jupiter's gravity prevented the material
from ever forming a planet.

Comets are bodies of ice and dust, typically a few kilometres across, on long elliptical orbits.
When a comet approaches the Sun, its ices sublimate and release gas and dust that form a glowing
coma and one or more tails. The tails always point away from the Sun, pushed by sunlight and the
solar wind, so a comet moving away from the Sun travels tail first. Halley's Comet returns about
every 76 years and was last seen in 1986.

The terms meteoroid, meteor and meteorite describe the same kind of object at different stages: a
meteoroid is a small rock in space, a meteor is the streak of light it makes when burning up in
the atmosphere, and a meteorite is any piece that reaches the ground.

Long-period comets are thought to come from the Oort cloud, a hypothesised spherical shell of icy
bodies far beyond the Kuiper belt, out to perhaps 100,000 astronomical units.
""")

# ---------------- retrieved tier: PDFs ----------------
def pdf(path, title, pages):
    doc = SimpleDocTemplate(path, pagesize=A4, title=title)
    st = getSampleStyleSheet(); flow = [Paragraph(title, st["Title"]), Spacer(1, 12)]
    for i, paras in enumerate(pages):
        if i: flow.append(PageBreak())
        for p in paras: flow += [Paragraph(p, st["BodyText"]), Spacer(1, 8)]
    doc.build(flow)

pdf(f"{ROOT}/corpus/sun.pdf", "The Sun", [[
 "The Sun is a G-type main-sequence star, an ordinary yellow dwarf, and holds about 99.8 percent of the mass of the Solar System. It is about 4.6 billion years old and roughly halfway through its life on the main sequence. Its diameter is about 1.39 million kilometres, 109 times that of Earth, and about 1.3 million Earths would fit inside it.",
 "Energy comes from nuclear fusion in the core, where hydrogen nuclei combine to form helium at a temperature of about 15 million degrees Celsius. The energy takes tens of thousands of years to work its way out to the visible surface, the photosphere, which is much cooler at about 5,500 degrees Celsius.",
 "Light from the Sun takes about 8 minutes and 20 seconds to reach Earth. The Sun rotates faster at its equator, about 25 days per rotation, than near its poles, about 35 days, because it is not a solid body.",
], [
 "Sunspots are darker, cooler regions of the photosphere where strong magnetic fields suppress convection. Their number rises and falls in a cycle of about 11 years. Solar flares and coronal mass ejections are often associated with sunspot groups and can disrupt satellites and power grids on Earth.",
 "The corona is the Sun's outer atmosphere, visible during a total solar eclipse as a pale halo. It is surprisingly hot, over a million degrees, far hotter than the surface beneath it, and why remains an active research question. The corona continuously streams charged particles outward as the solar wind, which fills the whole Solar System.",
 "In about five billion years the Sun will exhaust the hydrogen in its core, expand into a red giant large enough to engulf Mercury and Venus, and finally shed its outer layers, leaving a dense white dwarf behind.",
]])
pdf(f"{ROOT}/corpus/uranus.pdf", "Uranus", [[
 "Uranus is the seventh planet from the Sun and the first to be discovered with a telescope, by William Herschel in 1781. It is an ice giant with an equatorial diameter of about 51,118 kilometres, four times that of Earth. Methane in the upper atmosphere absorbs red light and gives the planet its pale blue-green colour.",
 "The most unusual thing about Uranus is its axial tilt of about 98 degrees. The planet effectively rotates on its side, so during its 84-year orbit each pole spends about 42 years in continuous sunlight followed by 42 years of darkness. The cause is unknown but a giant collision early in its history is the usual explanation.",
], [
 "Uranus has the coldest atmosphere of any planet, with a minimum recorded temperature of about minus 224 degrees Celsius, even though Neptune is farther from the Sun. It has 13 known faint, dark rings, discovered in 1977 when the planet passed in front of a star.",
 "Its 27 known moons are named after characters from the works of William Shakespeare and Alexander Pope, including Titania, Oberon, Umbriel, Ariel and Miranda. Miranda has one of the most varied surfaces known, with cliffs up to 20 kilometres high. Voyager 2 remains the only spacecraft to have visited Uranus, flying past in January 1986.",
]])
pdf(f"{ROOT}/corpus/neptune.pdf", "Neptune", [[
 "Neptune is the eighth and most distant planet from the Sun, orbiting at about 30 astronomical units and taking 165 Earth years to complete one orbit. It was the first planet found by mathematical prediction rather than observation: Urbain Le Verrier calculated its position from irregularities in the orbit of Uranus, and Johann Galle observed it in 1846 within a degree of the predicted spot.",
 "Neptune is an ice giant slightly smaller than Uranus, with an equatorial diameter of about 49,528 kilometres, but more massive. Its deep blue colour also comes from methane. Neptune has the strongest sustained winds in the Solar System, measured at around 2,000 kilometres per hour.",
], [
 "When Voyager 2 flew past in August 1989 it photographed a large storm called the Great Dark Spot, comparable in size to Earth. When the Hubble Space Telescope looked in 1994 the spot had vanished, and other dark spots have appeared and disappeared since.",
 "Neptune has 16 known moons. The largest, Triton, orbits in the retrograde direction, opposite to Neptune's rotation, which strongly suggests it is a captured Kuiper belt object rather than a moon that formed in place. Voyager 2 saw active geysers of nitrogen on Triton's surface, making it one of the few geologically active bodies in the outer Solar System.",
]])
pdf(f"{ROOT}/corpus/dwarf_planets.pdf", "Dwarf planets", [[
 "In 2006 the International Astronomical Union defined a planet as a body that orbits the Sun, is round under its own gravity, and has cleared the neighbourhood around its orbit. A body that meets the first two conditions but not the third is a dwarf planet. Pluto, which shares its region with many Kuiper belt objects, was reclassified under this definition.",
 "Five bodies are officially recognised as dwarf planets: Ceres, Pluto, Haumea, Makemake and Eris. Ceres is the largest object in the asteroid belt, about 940 kilometres across, and the only dwarf planet in the inner Solar System. The Dawn spacecraft orbited it from 2015 to 2018 and found bright deposits of salt on its surface.",
], [
 "Pluto has a diameter of about 2,377 kilometres, smaller than Earth's Moon. Its largest moon, Charon, is about half its size, so the two orbit a point in space between them. The New Horizons spacecraft flew past Pluto in July 2015 and revealed a young, heart-shaped plain of nitrogen ice called Sputnik Planitia, mountains of water ice, and a thin nitrogen atmosphere.",
 "Eris, discovered in 2005, is slightly smaller than Pluto but about 27 percent more massive, and its discovery was the immediate trigger for the 2006 definition. Haumea is unusual for its elongated shape, the result of a rotation period of under four hours. Makemake is a reddish body a little smaller than Pluto with one known moon.",
]])

# ---------------- retrieved tier: images ----------------
names = ["Mercury","Venus","Earth","Mars","Jupiter","Saturn","Uranus","Neptune"]
diam = [4879,12104,12756,6792,142984,120536,51118,49528]
au = [0.39,0.72,1.0,1.52,5.2,9.58,19.2,30.05]
fig, ax = plt.subplots(figsize=(10,3.2)); ax.set_aspect("equal"); ax.axis("off"); x = 0
for n, d in zip(names, diam):
    r = (d/142984)**0.5 * 1.0; x += r + 0.35
    ax.add_patch(plt.Circle((x, 0), r, color="#c9a66b")); ax.text(x, -1.3, n, ha="center", fontsize=9); x += r
ax.set_xlim(0, x + 0.3); ax.set_ylim(-1.6, 1.2); ax.set_title("Relative sizes of the eight planets (area scaled to diameter)")
fig.savefig(f"{ROOT}/corpus/planet_sizes.png", dpi=90, bbox_inches="tight"); plt.close(fig)

fig, ax = plt.subplots(figsize=(9,4)); ax.barh(names[::-1], au[::-1], color="#5b7fa6")
ax.set_xlabel("Average distance from the Sun (astronomical units)"); ax.set_title("Orbital distances of the planets")
for i, v in enumerate(au[::-1]): ax.text(v + 0.3, i, f"{v} AU", va="center", fontsize=8)
fig.tight_layout(); fig.savefig(f"{ROOT}/corpus/orbital_distances.png", dpi=90); plt.close(fig)

fig, ax = plt.subplots(figsize=(7,5)); ax.set_aspect("equal"); ax.axis("off"); ax.set_facecolor("black"); fig.patch.set_facecolor("black")
for w, c in [(6.4,"#d9c9a3"),(5.6,"#2b2b2b"),(5.0,"#e8dcbf"),(4.2,"#000000")]:
    ax.add_patch(Ellipse((0,0), w, w*0.32, color=c))
ax.add_patch(plt.Circle((0,0), 1.4, color="#e6c98a"))
ax.add_patch(Ellipse((0,-0.05), 6.4, 6.4*0.32, color="#d9c9a3", clip_on=True))
ax.add_patch(Ellipse((0,-0.05), 5.6, 5.6*0.32, color="#2b2b2b"))
ax.add_patch(Ellipse((0,-0.05), 5.0, 5.0*0.32, color="#e8dcbf"))
ax.add_patch(Ellipse((0,-0.05), 4.2, 4.2*0.32, color="#000000"))
ax.add_patch(Wedge((0,0), 1.4, 0, 180, color="#e6c98a"))
ax.text(0, 2.3, "Saturn and its main rings, A ring outermost", color="white", ha="center")
ax.set_xlim(-3.6,3.6); ax.set_ylim(-2.6,2.8)
fig.savefig(f"{ROOT}/corpus/saturn_rings.png", dpi=90, facecolor="black"); plt.close(fig)

# ---------------- retrieved tier: audio ----------------
audio = {
"mars_moons": "Mars has two small moons, Phobos and Deimos, both discovered by Asaph Hall in 1877. Their names come from the Greek words for fear and dread. Phobos is the larger of the two, about 22 kilometres across, and orbits so close to Mars that it circles the planet in under eight hours, faster than Mars itself rotates. Seen from the surface it rises in the west and sets in the east. Phobos is slowly spiralling inward and is expected to break apart or crash into Mars in roughly fifty million years. Deimos is smaller, about 12 kilometres across, and orbits farther out, taking about thirty hours to go around Mars. Both moons are dark, irregular lumps, and many astronomers think they are asteroids captured from the nearby belt, although a giant impact on Mars is another possible origin.",
"jupiter_moons": "The four largest moons of Jupiter were discovered by Galileo in January 1610 and are called the Galilean moons. Io is the innermost and the most volcanically active body in the Solar System. Tidal squeezing from Jupiter and the other moons heats its interior, and hundreds of volcanoes spray sulphur across its surface. Europa is covered by a smooth shell of water ice, and beneath it lies a salty ocean holding more water than all of Earth's oceans combined, which makes it one of the leading candidates for life beyond Earth. NASA's Europa Clipper spacecraft was launched in 2024 to study it. Ganymede is the largest moon in the Solar System, bigger than the planet Mercury, and the only moon known to generate its own magnetic field. Callisto is the outermost of the four and has an ancient, heavily cratered surface that has changed little in billions of years.",
"earth_moon": "The Moon is Earth's only natural satellite. It is about 3,474 kilometres across, roughly a quarter of Earth's diameter, and orbits at an average distance of about 384,400 kilometres. It is tidally locked, so the same side always faces Earth. The phases of the Moon are caused by the changing angle between the Sun, Earth and Moon as it orbits, not by Earth's shadow. The Moon's gravity raises the ocean tides. The leading explanation for its origin is the giant impact hypothesis, in which a Mars-sized body named Theia struck the young Earth and the debris gathered into the Moon. The dark patches visible from Earth are maria, ancient plains of solidified basalt lava. Apollo 11 made the first crewed landing in July 1969. Laser reflectors left by the Apollo missions show that the Moon is receding from Earth by about 3.8 centimetres each year.",
"saturn_moons": "Saturn's two best studied moons are Titan and Enceladus. Titan is the second largest moon in the Solar System and the only moon with a thick atmosphere, made mostly of nitrogen with some methane. Its surface pressure is about one and a half times Earth's. Titan has lakes and seas of liquid methane and ethane near its poles, the only stable surface liquids known beyond Earth. The Huygens probe, carried by Cassini, parachuted onto Titan in January 2005 and returned images of a landscape shaped by liquid. Enceladus is much smaller, about 500 kilometres across, and covered in bright clean ice. Cassini discovered geysers of water vapour and ice grains erupting from long fractures near its south pole, nicknamed the tiger stripes. The plumes come from a global ocean beneath the ice and are the main source of Saturn's faint E ring.",
}
for name, text in audio.items():
    subprocess.run(["espeak-ng", "-v", "en-us", "-s", "165", "-w", f"{ROOT}/corpus/{name}.wav", text], check=True)
print("done")
