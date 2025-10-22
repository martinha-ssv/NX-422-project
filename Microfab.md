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

### Additional Remarks-chatgpt
- PDMS is not a high-quality hermetic barrier — it is permeable to water and gases. The paper demonstrates good short/mid-term performance but does not provide multi-month functional chronic stimulation data in a large animal with implanted electronics and a hermetic IPG feedthrough. For an implanted IPG you will need robust hermetic feedthroughs or additional thin-film / metallic barriers for the traces to prevent long-term corrosion/delamination.
- Connectorization to an implantable IPG: the paper uses FlexComb and microfabricated polyimide connectors to link to external stimulators. Integration with an implanted IPG (inductive power, NFMI/BLE communications, and magnet alignment) requires implantable-grade, mechanically robust, hermetic interconnects — the present connector approach will need redesign for a surgically implanted permanent feedthrough
- Insufficient chronic functional stimulation data: the only chronic data are 6-week passive implants with very small n. You need chronic, fully-functional implants (with continuous/periodic stimulation) in a large animal for ≥3–6 months to evaluate: electrode degradation, threshold drift, selectivity retention, FBR evolution, connector durability, and mechanical wear.
- Localized adverse effects linked to implantation orientation: the pilot chronic histology showed localized demyelination in one fascicle that the authors attribute to cuff locking/orientation and connector tethering. This highlights the sensitivity of outcomes to surgical handling and connector mechanics — a design for IPG integration must minimize tethering forces and provide strain-relief.
- For expected stimulation amplitudes (worst-case 300–400 µA, 100–300 µs) either:

        - increase electrode geometric area per contact, or

        -adopt a higher-CIC electrode coating (sputtered IrOx, electrodeposited IrOx / PEDOT formulations) so you have a safety margin above 60 µC/cm². (With the present Pt-PDMS composite, 400 µA / 300 µs on 0.8×0.25 mm² equals the CIC limit.)

## Validation plan
- Continuous charge-balanced pulsing at the intended worst-case settings (e.g., 300–400 µA, 300 µs, up to physiological frequency, e.g., 50–200 Hz) for an accelerated number of cycles (e.g., 10⁸–10⁹ pulses) while the devices are under cyclic mechanical strain representative of limb motion (10–20% strain) in PBS at elevated temperature. Monitor impedance, VTs, delamination. (The paper reports some cycling data in prior references but not at the full combined electrical/mechanical stress level needed for an IPG.)
- Implant cuff + an implant-grade IPG in a large animal (pig) with full implanted electronics (inductive power used as in your design) and run chronic stimulation protocol (daily stimulation at target frequencies and amplitudes) for ≥3–6 months. Outcome measures: stimulation thresholds over time, selectivity retention, histology (macrophages, fibroblasts, myelin, axon counts), connector integrity, and device electrochemistry. The paper’s acute pig results are promising but do not replace this.
- Create surgical workflows and cable management solutions to avoid the connector orientation/tension effects the authors observed (they saw localized demyelination possibly linked to connector pulling). Test multiple mounting/orientation variants and strain-relief designs.
- Use Finite Element Analysis (electric field + volume conductor models) to predict activation contours for your nerve targets (ulnar/radial/median) and to design electrode spacing/geometry before committing to a high-channel hardware iteration. The authors note FEA would help optimize configurations.

## [Polyimide substrate with iodine-etched gold and PEDOT:PSS coating](https://www.sciencedirect.com/science/article/pii/S0925400518314345)

### Quick schematic (stack & components)
- Substrate: Polyimide (flexible, ~20 µm total thickness)  
- Conductive layer: Electroplated gold (≈2.5 µm) over sputtered Ti/Au seed layer  
- Surface conditioning: Iodine etching (0.05 mol/L, 120 s) to increase Au roughness and adhesion  
- Electrode coating: Electropolymerized PEDOT:PSS (~1 µm thick)  
- Optional activation: Cyclic voltammetry (−0.9 to +0.6 V) to optimize doping state  
- Layout: Circular microelectrodes (585 µm diameter) in flexible arrays  

### Key specs & results
- **Impedance (EIS):**
  - 13.2 kΩ @ 1 Hz; 679 Ω @ 1 kHz (99% reduction vs. bare Au)  
- **Charge injection capacity (CIC):**
  - 2.0 mC/cm² — ~30× higher than uncoated Au (60 µC/cm² typical)  
- **Charge storage capacity (CSC):**
  - don't know but perhaps can be estimated from CV area
- **Polarization voltage reduction:**
  - ~30% drop after CV activation  
- **Electrochemical stability:**
  - 7 days continuous stimulation (5 mA biphasic pulses, 100 µs per phase, 604 million cycles) → no degradation or delamination  
- **Adhesion & mechanical robustness:**
  - 100% retention after ultrasonic stress test (11 min, 35 kHz, 300 W)  
- **In vivo validation:**
  - 36-day subcutaneous implantation — no delamination or impedance drift reported  

### Electrical / mechanical performance
- PEDOT:PSS film strongly anchored by iodine-etched gold surface microstructure → no delamination even under cyclic stimulation  
- Electrochemical performance maintained over billions of pulses at amplitudes exceeding those needed for peripheral nerve stimulation  
- Impedance stable under mechanical bending typical of flexible neural interfaces  
- Electrodes operate well below water window limits (−0.9 to +0.6 V), ensuring charge-balanced, safe stimulation  

### Additional Remarks-chatgpt
- Polyimide substrate provides flexibility but limited hermeticity — will require additional encapsulation (e.g., PDMS or Parylene-C) for long-term implantation  
- Excellent electrochemical safety margin (CIC 2 mC/cm² vs. typical required <100 µC/cm²) allows use in high-density cuff systems with smaller contact areas  
- Process scalable with standard MEMS tools; iodine etching adds a simple, low-cost adhesion step  
- Surface roughness and electrochemical activation critical to reproducibility; requires careful control during scale-up  
- Long-term (>6 months) in vivo performance not yet established — further testing needed under physiological loading and motion  

- This PEDOT:PSS–on–iodine-etched Au system offers extremely high charge injection capability, excellent stability under mechanical and electrochemical stress, and strong adhesion — addressing key limitations of conventional PEDOT coatings.  
- For integration into an I2CS-based nerve cuff, the method is promising: flexible, low-impedance electrodes compatible with multi-site arrays.  
- Future work should adapt the process to PDMS or hybrid PDMS/polyimide substrates for full conformal cuffs and confirm chronic stability beyond 3–6 months under cyclic strain and stimulation.  
- Given its CIC margin, electrode size can be reduced significantly (to ~100–200 µm diameter) without exceeding safe charge limits.  

### Validation plan
- **Benchtop accelerated aging:** Apply continuous biphasic pulses (100 µs, 1–5 mA, 50–200 Hz) for 10⁸–10⁹ cycles in PBS under cyclic bending. Monitor impedance, polarization, and surface integrity.  
- **Long-term in vivo test:** Implant coated electrodes in a large-animal peripheral nerve model for ≥6 months under chronic stimulation. Measure impedance, selectivity, and histology post-explant.  
- **Process translation:** Reproduce iodine-etch + PEDOT:PSS deposition on PDMS-backed or fully stretchable interconnects. Assess mechanical reliability under strain (10–20%) and cyclic flexion.  
- **FEA modeling:** Use to correlate electric field distribution and safe current limits for scaled-down electrode geometries in human-sized nerves (ulnar, radial, median).  

## [Parylene-C encapsulated Pt microelectrodes with PEDOT:PSS coating](https://pubs.aip.org/aip/apb/article/7/3/046117/2896714)
This one was chat, didnt have time to read

### Quick schematic (stack & components)
- Substrate: Glass wafer (rigid)
- Conductive layer: 10 nm Ti / 120 nm Pt (e-beam evaporated, 8 × 15 nm steps)
- Insulation: 2 µm Parylene-C (A-174 silane adhesion promoter)
- Patterning: Photolithography + liftoff
- PEDOT:PSS coating: Spin-coated Clevios PH1000 + glycerol + DBSA + GOPS mixture  
  (four layers baked at 110 °C × 1 min each, final thickness ≈ 550 nm)
- Sacrificial Parylene-C lift-off defines electrode openings
- Final bake: 140 °C for 1 h + DI-water rinse (1 h)

### Key specs & results
- **Electrode geometry:** 100 µm diameter (7.85 × 10⁻⁵ cm²)  
- **Pulse parameters:** Biphasic, symmetric, 100 µs/phase, 130 Hz, 50–200 µA
- **Charge densities:** 64 – 255 µC/cm² per phase
- **Stimulation duration:** 2 h (9.36 × 10⁵ pulses) in PBS (200 µL)
- **Bare Pt:** Visible corrosion ≥ 191 µC/cm²; complete failure at 255 µC/cm²  
- **PEDOT:PSS-coated Pt:** No visible damage, no Pt dissolution detectable by ICP-MS up to 255 µC/cm²
- **Electrochemical tests:** EIS (1–10⁵ Hz, 25 mV), voltage transient recording confirmed stable delivery  
- **Composition analysis:** EDX showed no change after stimulation for PEDOT:PSS coatings  
- **Cell viability:** Neural cells maintained >90 % survival after 2 h × 3 days stimulation (191 µC/cm²)

### Electrical / mechanical performance
- PEDOT:PSS coating prevented Pt corrosion and maintained electrochemical integrity
- Biphasic stimulation (≤255 µC/cm² per phase) produced no delamination or potential excursion issues
- Coating thickness (≈550 nm) and GOPS crosslinking provided robust adhesion and hydration stability
- Performance remained stable throughout pulsing period and EIS tests

### Practical notes / trade-offs
- Demonstrates significant improvement in metal electrode durability for thin-film devices
- PEDOT:PSS film acts as a protective and capacitive interface, suppressing Pt dissolution
- Fabrication is compatible with MEMS processing and transferable to flexible substrates (polyimide or PDMS)
- Long-term (>weeks) stimulation and mechanical cycling studies still needed for implant reliability

### Validation plan
- **Benchtop:** Replicate biphasic pulsing (100 µA, 100 µs, 130 Hz) for ≥10⁷ cycles in PBS at 37 °C; monitor impedance and Pt leaching  
- **In vivo:** Evaluate chronic (≥3–6 months) stimulation on nerve targets to assess mechanical and electrochemical stability  
- **Integration:** Translate PEDOT:PSS/Parylene-C/Pt stack onto flexible PDMS/polyimide substrates for nerve cuffs
