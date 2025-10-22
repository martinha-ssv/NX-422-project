## [PDMS substrate cuff with Pt/silicone composite coating](https://bioelecmed.biomedcentral.com/articles/10.1186/s42234-023-00137-y)

### Quick schematic (stack & components)
- Silicone substrate (200 µm, E ≈ 1 MPa)
- Stretchable conductive layer: microcracked gold tracks (35 nm Au over 5 nm Cr adhesion)
- Electrode surface: Pt / PDMS (platinum-elastomer) composite coating
- Mechanical closure: belt-like locking mechanism
- Multichannel layout: soft cuff with 16 sites (tested)

### Key specs & results
- Target nerve size: > 1.5 mm (tested on pig sciatic nerve, d = 4.5 mm)
- Electrode site area: 0.8 × 0.25 mm²
- Conductors: gold (nanowires / microcracked thin-film tracks)
  - Track thickness: 35 nm Au / 5 nm Cr
  - Minimum interconnect width reported: 150 µm
  - Note: kirigami-like stretchable interconnects can allow track widths down to ~30 µm (alternative)
- Substrate: 200 µm silicone (E ≈ 1 MPa)
- Coating: Platinum / PDMS composite
  - Lowers electrode/electrolyte impedance (proposed alternative to PEDOT)
  - Tensile modulus ≈ 10 MPa
  - Charge injection limit: 57 ± 9 µC/cm²
  - CSC: 47 ± 3 mC/cm²  (source: platinum-elastomer mesocomposite as neural electrode coating)

### Electrical / mechanical performance
- EIS under bending/strain: minimal functional impact
  - ≈2× impedance increase at 1 kHz with 45% applied strain
  - Track resistance not significantly affected by different folding conditions
- Contact: near-complete electrode contact on nerve surface
- Stimulation (voltage transient)
  - Biphasic pulse: 100 µA, PW = 300 µs → voltage drop < 4 V (mostly resistive)
  - IPG compliance = 12 V → stimulation current could be increased up to ~300 µA without hitting compliance limit

### Practical notes / trade-offs
- Pt/PDMS mesocomposite gives high charge capacity and lower impedance vs bare metal; stiffer than silicone but still compliant
- Minimum interconnect width (150 µm) sets routing density; in this configuration using micro-cracked gold technology, the minimum width of the interconnects is limited to 150 µm. Consequently, as the tracks are designed to travel along the sides of the central slits, the total width of the cuff can quickly become significant, especially when working with small animal models. Consider kirigami or other stretchable geometries for higher density (these can allow track widths down to ~30 µm)
- Device remains functional under large strains and folding — suitable for conformal nerve cuff applications

