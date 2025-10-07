"""
Abaqus Material Property Extractor
===================================
A Python tool to extract material properties from Abaqus .inp files 
and export them to JSON and CSV formats.

Author: Aref Aasi

"""

import re
import json
import csv
from typing import Dict, List, Any


def extract_material_properties(inp_file_path: str) -> Dict[str, Dict[str, Any]]:
    """
    Extract material properties from an Abaqus .inp file.
    
    This function parses Abaqus input files and extracts all material definitions
    including elastic, plastic, density, thermal, and other properties.
    
    Args:
        inp_file_path (str): Path to the Abaqus .inp file
        
    Returns:
        Dict[str, Dict[str, Any]]: Nested dictionary with structure:
            {
                'MaterialName': {
                    'PropertyType': [[value1, value2, ...], ...],
                    'PropertyType_Attribute': 'value',
                    ...
                },
                ...
            }
    
    Example:
        >>> materials = extract_material_properties('model.inp')
        >>> steel_elastic = materials['Steel']['Elastic']
        >>> print(steel_elastic)  # [[210000.0, 0.3]]
    """
    
    # Initialize storage for all materials
    materials = {}
    
    # Track current parsing state
    current_material = None      # Name of material being processed
    current_property = None      # Property type being read (e.g., 'Elastic')
    reading_data = False         # Flag to indicate if we're reading property values
    
    # Read the entire input file with error handling for encoding issues
    with open(inp_file_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    
    # Process file line by line
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # =====================================================================
        # STEP 1: Handle empty lines and comments
        # =====================================================================
        
        # Skip completely empty lines
        if not line:
            i += 1
            continue
        
        # Skip comment-only lines (lines starting with **)
        if line.startswith('**'):
            i += 1
            continue
            
        # Remove inline comments from data lines
        if '**' in line:
            line = line.split('**')[0].strip()
            if not line:  # If nothing left after removing comment
                i += 1
                continue
        
        # =====================================================================
        # STEP 2: Detect material definition
        # =====================================================================
        
        if line.upper().startswith('*MATERIAL'):
            # Extract material name using regex (case insensitive)
            match = re.search(r'name\s*=\s*([^\s,]+)', line, re.IGNORECASE)
            
            if match:
                current_material = match.group(1)
                materials[current_material] = {}  # Initialize new material
                current_property = None
                reading_data = False
                print(f"Found material: {current_material}")
        
        # =====================================================================
        # STEP 3: Detect and process material property keywords
        # =====================================================================
        
        elif current_material and line.startswith('*'):
            reading_data = False  # Reset data reading flag
            line_upper = line.upper()
            
            # -----------------------------------------------------------------
            # Elastic Properties
            # -----------------------------------------------------------------
            if line_upper.startswith('*ELASTIC'):
                current_property = 'Elastic'
                materials[current_material][current_property] = []
                reading_data = True
                
                # Check for elastic type (e.g., ISOTROPIC, ORTHOTROPIC)
                type_match = re.search(r'type\s*=\s*([^\s,]+)', line, re.IGNORECASE)
                if type_match:
                    materials[current_material]['Elastic_Type'] = type_match.group(1)
            
            # -----------------------------------------------------------------
            # Plastic Properties
            # -----------------------------------------------------------------
            elif line_upper.startswith('*PLASTIC'):
                current_property = 'Plastic'
                materials[current_material][current_property] = []
                reading_data = True
                
                # Check for hardening type (e.g., ISOTROPIC, KINEMATIC)
                hard_match = re.search(r'hardening\s*=\s*([^\s,]+)', line, re.IGNORECASE)
                if hard_match:
                    materials[current_material]['Plastic_Hardening'] = hard_match.group(1)
            
            # -----------------------------------------------------------------
            # Density
            # -----------------------------------------------------------------
            elif line_upper.startswith('*DENSITY'):
                current_property = 'Density'
                materials[current_material][current_property] = []
                reading_data = True
            
            # -----------------------------------------------------------------
            # Thermal Conductivity
            # -----------------------------------------------------------------
            elif line_upper.startswith('*CONDUCTIVITY'):
                current_property = 'Conductivity'
                materials[current_material][current_property] = []
                reading_data = True
            
            # -----------------------------------------------------------------
            # Specific Heat
            # -----------------------------------------------------------------
            elif line_upper.startswith('*SPECIFIC HEAT'):
                current_property = 'Specific_Heat'
                materials[current_material][current_property] = []
                reading_data = True
            
            # -----------------------------------------------------------------
            # Thermal Expansion
            # -----------------------------------------------------------------
            elif line_upper.startswith('*EXPANSION'):
                current_property = 'Expansion'
                materials[current_material][current_property] = []
                reading_data = True
                
                # Check for expansion type (e.g., ISO, ORTHO)
                type_match = re.search(r'type\s*=\s*([^\s,]+)', line, re.IGNORECASE)
                if type_match:
                    materials[current_material]['Expansion_Type'] = type_match.group(1)
            
            # -----------------------------------------------------------------
            # Damping
            # -----------------------------------------------------------------
            elif line_upper.startswith('*DAMPING'):
                current_property = 'Damping'
                materials[current_material][current_property] = []
                reading_data = True
            
            # -----------------------------------------------------------------
            # Hyperelastic Materials
            # -----------------------------------------------------------------
            elif line_upper.startswith('*HYPERELASTIC'):
                current_property = 'Hyperelastic'
                materials[current_material][current_property] = []
                reading_data = True
                
                # Detect hyperelastic model type
                models = ['mooney-rivlin', 'neo hooke', 'ogden', 'polynomial', 'yeoh']
                for model in models:
                    if model.replace(' ', '') in line.lower().replace(' ', ''):
                        materials[current_material]['Hyperelastic_Model'] = model.title()
                        break
            
            # -----------------------------------------------------------------
            # Viscoelastic Materials
            # -----------------------------------------------------------------
            elif line_upper.startswith('*VISCOELASTIC'):
                current_property = 'Viscoelastic'
                materials[current_material][current_property] = []
                reading_data = True
            
            # -----------------------------------------------------------------
            # User-Defined Materials (UMAT)
            # -----------------------------------------------------------------
            elif line_upper.startswith('*USER MATERIAL'):
                current_property = 'User_Material'
                materials[current_material][current_property] = []
                reading_data = True
                
                # Extract number of constants
                const_match = re.search(r'constants\s*=\s*(\d+)', line, re.IGNORECASE)
                if const_match:
                    materials[current_material]['User_Material_Constants'] = int(const_match.group(1))
            
            # -----------------------------------------------------------------
            # Dependent Variables (DEPVAR)
            # -----------------------------------------------------------------
            elif line_upper.startswith('*DEPVAR'):
                const_match = re.search(r'(\d+)', line)
                if const_match:
                    materials[current_material]['Depvar'] = int(const_match.group(1))
                reading_data = False
            
            # -----------------------------------------------------------------
            # Other Keywords (may indicate end of material section)
            # -----------------------------------------------------------------
            else:
                reading_data = False
                
                # Check if we're leaving the material definition section
                non_material_keywords = [
                    '*STEP', '*PART', '*ASSEMBLY', '*ELEMENT', '*NODE',
                    '*SECTION', '*SOLID SECTION', '*SHELL SECTION', 
                    '*BEAM SECTION', '*BOUNDARY', '*ELSET', '*NSET'
                ]
                
                if any(line_upper.startswith(kw) for kw in non_material_keywords):
                    current_material = None
                    current_property = None
        
        # =====================================================================
        # STEP 4: Read property data values
        # =====================================================================
        
        elif current_material and reading_data and current_property and not line.startswith('*'):
            # Parse comma-separated values from data line
            values = [v.strip() for v in line.split(',') if v.strip()]
            
            if values:
                try:
                    # Attempt to convert all values to floats
                    numeric_values = [float(v) for v in values]
                    materials[current_material][current_property].append(numeric_values)
                    print(f"  {current_property}: {numeric_values}")
                    
                except ValueError:
                    # If conversion fails, store as strings
                    materials[current_material][current_property].append(values)
                    print(f"  {current_property}: {values}")
        
        # Move to next line
        i += 1
    
    return materials


def save_to_json(materials: Dict[str, Dict[str, Any]], 
                 output_file: str = "material_properties.json") -> None:
    """
    Save extracted material properties to a JSON file.
    
    The JSON format preserves the complete hierarchical structure of materials
    and their properties, making it ideal for programmatic access.
    
    Args:
        materials (Dict[str, Dict[str, Any]]): Material properties dictionary
        output_file (str): Path for output JSON file (default: material_properties.json)
    
    Example JSON structure:
        {
            "Steel": {
                "Elastic": [[210000.0, 0.3]],
                "Density": [[7850.0]],
                "Plastic": [[250.0, 0.0], [300.0, 0.1]]
            }
        }
    """
    
    with open(output_file, 'w') as f:
        json.dump(materials, f, indent=4)
    
    print(f"\n✓ Material properties saved to: {output_file}")


def save_to_csv(materials: Dict[str, Dict[str, Any]], 
                output_file: str = "material_properties.csv") -> None:
    """
    Save extracted material properties to a CSV file.
    
    The nested dictionary structure is flattened into a table format suitable
    for spreadsheet applications like Excel. Each row represents a single
    data entry for a material property.
    
    Args:
        materials (Dict[str, Dict[str, Any]]): Material properties dictionary
        output_file (str): Path for output CSV file (default: material_properties.csv)
    
    CSV columns:
        - Material: Name of the material
        - Property: Type of property (e.g., Elastic, Plastic)
        - Row_Index: Index for multiple data rows of same property
        - Values: String representation of all values
        - Value_1, Value_2, ...: Individual numeric values
    """
    
    rows = []
    
    # Flatten the nested dictionary structure
    for mat_name, properties in materials.items():
        for prop_name, prop_value in properties.items():
            
            # Handle list properties (most common case)
            if isinstance(prop_value, list):
                for idx, values in enumerate(prop_value):
                    row = {
                        'Material': mat_name,
                        'Property': prop_name,
                        'Row_Index': idx,
                        'Values': str(values)
                    }
                    
                    # Add individual value columns for numeric data
                    if isinstance(values, list):
                        for i, val in enumerate(values):
                            row[f'Value_{i+1}'] = val
                    
                    rows.append(row)
            
            # Handle single value properties (like material types)
            else:
                row = {
                    'Material': mat_name,
                    'Property': prop_name,
                    'Row_Index': 0,
                    'Values': str(prop_value)
                }
                rows.append(row)
    
    # Write to CSV if we have data
    if rows:
        # Determine all column names needed
        fieldnames = ['Material', 'Property', 'Row_Index', 'Values']
        
        # Find maximum number of value columns needed
        max_values = 0
        for row in rows:
            value_cols = [k for k in row.keys() if k.startswith('Value_')]
            if len(value_cols) > max_values:
                max_values = len(value_cols)
        
        # Add Value_N columns to fieldnames
        for i in range(1, max_values + 1):
            fieldnames.append(f'Value_{i}')
        
        # Write CSV file
        with open(output_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        
        print(f"✓ Material properties saved to: {output_file}")
    else:
        print("⚠ No data to write to CSV")


def print_material_properties(materials: Dict[str, Dict[str, Any]]) -> None:
    """
    Print extracted material properties in a readable format to console.
    
    Args:
        materials (Dict[str, Dict[str, Any]]): Material properties dictionary
    """
    
    for mat_name, properties in materials.items():
        print(f"\n{'='*60}")
        print(f"Material: {mat_name}")
        print(f"{'='*60}")
        
        if not properties:
            print("  (No properties found)")
        else:
            for prop_name, prop_value in properties.items():
                print(f"\n{prop_name}:")
                
                if isinstance(prop_value, list):
                    for i, values in enumerate(prop_value):
                        print(f"  {values}")
                else:
                    print(f"  {prop_value}")


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    
    # -------------------------------------------------------------------------
    # Configuration
    # -------------------------------------------------------------------------
    
    # Input file path - CHANGE THIS to your .inp file
    inp_file = "your_model.inp"
    
    # Output file paths
    json_output = "material_properties.json"
    csv_output = "material_properties.csv"
    
    # -------------------------------------------------------------------------
    # Processing
    # -------------------------------------------------------------------------
    
    try:
        print(f"{'='*60}")
        print(f"Abaqus Material Property Extractor")
        print(f"{'='*60}")
        print(f"\nReading material properties from: {inp_file}\n")
        
        # Extract materials from .inp file
        materials = extract_material_properties(inp_file)
        
        if materials:
            # Print summary to console
            print("\n" + "="*60)
            print("EXTRACTION SUMMARY")
            print("="*60)
            print_material_properties(materials)
            
            # Save to JSON format
            save_to_json(materials, json_output)
            
            # Save to CSV format
            save_to_csv(materials, csv_output)
            
            # Final summary
            print(f"\n{'='*60}")
            print(f"✓ Processing complete!")
            print(f"✓ Found {len(materials)} material(s)")
            print(f"{'='*60}\n")
            
        else:
            print("\n⚠ Warning: No materials found in the .inp file")
            print("   Check if the file contains *Material definitions\n")
        
    except FileNotFoundError:
        print(f"\n✗ Error: File '{inp_file}' not found.")
        print("   Please check the file path and try again.\n")
        
    except Exception as e:
        print(f"\n✗ Error: {e}\n")
        import traceback

        traceback.print_exc()
