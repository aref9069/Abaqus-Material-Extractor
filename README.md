# Abaqus-Material-Extractor
A Python tool to extract material properties from Abaqus .inp files and export them to JSON and CSV formats. Supports elastic, plastic, density, thermal, hyperelastic, and other material definitions commonly used in finite element analysis.


# Features

Material Parser: Automatically detects and parses *MATERIAL blocks (Elastic, Plastic, Damage, Density, etc.) from Abaqus input files, outputting clean JSON and CSV summaries.

Rate-Dependent Plasticity Tools: Supports both tabular rate data (*Plastic, rate=) and power-law viscoplastic formulations (*Rate Dependent with multiplier and exponent).

Unit Conversion: Converts between SI (m–kg–s–Pa) and engineering (mm–tonne–s–MPa) systems with automatic scaling for density, modulus, and displacement-based damage parameters.

Visualization: Optional scripts to plot stress–strain curves at different strain rates and visualize rate sensitivity or damage evolution curves.

Material Library Export: Generates ready-to-import Abaqus material keyword files (.inp) or a CAE material database for quick use in simulations.

# Supported Material Cards

- Elastic (isotropic, orthotropic, anisotropic)
  - Plastic (isotropic, kinematic hardening)
  - Density
  - Thermal conductivity
  - Specific heat
  - Thermal expansion
  - Damping
  - Hyperelastic (Mooney-Rivlin, Neo-Hooke, Ogden, etc.)
  - Viscoelastic
  - User-defined materials (UMAT)

# Dual export formats
- **JSON**: Preserves hierarchical structure
- **CSV**: Spreadsheet-friendly tabular format

# Extract materials
materials = extract_material_properties("your_model.inp")

# Export results
save_to_json(materials, "materials.json")
save_to_csv(materials, "materials.csv")


# Example Use Cases

Automate extraction of experimental material data from .inp models.

Convert Abaqus materials between unit systems (Pa ↔ MPa).

Build rate-sensitive metal plasticity models (e.g., steel, aluminum, copper).

Visualize and validate strain-rate effects before impact or forming simulations.
