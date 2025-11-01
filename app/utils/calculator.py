import math
from app.utils.structure_templates import NIGERIAN_BLOCK_STANDARDS, MEASUREMENT_UNITS

from datetime import datetime  # Add this import


class BlockCalculator:
    def __init__(self, structures_data, block_type='9_inch_hollow'):
        self.structures_data = structures_data
        self.block_type = block_type
        self.block_standard = NIGERIAN_BLOCK_STANDARDS[block_type]
        self.waste_percentage = structures_data.get('waste_percentage', 10)
        
    def calculate(self):
        """Main calculation method - UPDATED without price"""
        print("DEBUG: Starting calculation with structures:", self.structures_data)
        
        total_blocks = 0
        total_wall_area = 0
        total_net_area = 0
        structure_breakdown = []
        
        structures = self.structures_data.get('structures', [])
        print(f"DEBUG: Found {len(structures)} structures")
        
        for structure in structures:
            (structure_blocks, structure_area, 
            net_area, openings_area, structure_details) = self.calculate_structure_blocks(structure)
            
            total_blocks += structure_blocks
            total_wall_area += structure_area
            total_net_area += net_area
            
            structure_breakdown.append({
                'name': structure.get('name', 'Unnamed Structure'),
                'type': structure.get('type', 'unknown'),
                'total_area': structure_area,
                'openings_area': openings_area,
                'net_area': net_area,
                'blocks': structure_blocks,
                'details': structure_details
            })
        
        print(f"DEBUG: Total blocks before waste: {total_blocks}")
        
        # Add waste percentage (Nigerian standard practice)
        total_blocks_with_waste = math.ceil(total_blocks * (1 + self.waste_percentage/100))
        waste_blocks = total_blocks_with_waste - total_blocks
        
        # REMOVED all price calculations
        
        # Calculate additional materials (optional - keep if you want)
        cement_bags = self.calculate_cement_needed(total_blocks_with_waste)
        sand_trucks = self.calculate_sand_needed(total_blocks_with_waste)
        
        result = {
            'total_blocks': total_blocks_with_waste,
            'total_area': total_net_area,
            'waste_blocks': waste_blocks,
            'waste_percentage': self.waste_percentage,
            'block_type': self.block_type,
            'cement_bags': cement_bags,
            'sand_trucks': sand_trucks,
            'structure_breakdown': structure_breakdown,
            'calculation_time': datetime.utcnow().isoformat()
        }
        
        print("DEBUG: Final result:", result)
        return result
    
     # KEEP all the helper methods but remove price-related ones
    def calculate_structure_blocks(self, structure):
        """Calculate blocks for a single structure with detailed breakdown"""
        # Convert dimensions to meters
        length_m = self.convert_to_meters(structure['length'], structure['unit'])
        width_m = self.convert_to_meters(structure['width'], structure['unit']) 
        height_m = self.convert_to_meters(structure['height'], structure['unit'])
        
        # Calculate total wall area (all 4 walls)
        wall_area = self.calculate_wall_area(length_m, width_m, height_m)
        
        # Calculate openings from sub-structures
        openings_area, openings_breakdown = self.calculate_openings_area(structure.get('sub_structures', []))
        
        # Net wall area (area that needs blocks)
        net_wall_area = wall_area - openings_area
        
        if net_wall_area <= 0:
            return 0, wall_area, net_wall_area, openings_area, openings_breakdown
            
        # Calculate number of blocks needed
        block_area = self.calculate_block_area()
        blocks_needed = net_wall_area / block_area
        
        structure_details = {
            'dimensions': {
                'length': structure['length'],
                'width': structure['width'],
                'height': structure['height'],
                'unit': structure['unit']
            },
            'wall_area': wall_area,
            'openings_breakdown': openings_breakdown
        }
        
        return blocks_needed, wall_area, net_wall_area, openings_area, structure_details
    
    def calculate_wall_area(self, length, width, height):
        """Calculate total area of all walls"""
        return (2 * length * height) + (2 * width * height)
    
    def calculate_openings_area(self, sub_structures):
        """Calculate total area of all openings with detailed breakdown"""
        total_openings_area = 0
        openings_breakdown = []
        
        for sub_structure in sub_structures:
            if sub_structure['type'] in ['door', 'window', 'ac_unit', 'vent']:
                width_m = self.convert_to_meters(sub_structure['width'], sub_structure['unit'])
                height_m = self.convert_to_meters(sub_structure['height'], sub_structure['unit'])
                quantity = sub_structure.get('quantity', 1)
                
                opening_area = width_m * height_m * quantity
                total_openings_area += opening_area
                
                openings_breakdown.append({
                    'type': sub_structure['type'],
                    'width': sub_structure['width'],
                    'height': sub_structure['height'],
                    'unit': sub_structure['unit'],
                    'quantity': quantity,
                    'area': opening_area
                })
                
        return total_openings_area, openings_breakdown
    
    def calculate_block_area(self):
        """Calculate area covered by one block with robust fallbacks for different schemas."""
        try:
            # Try common keys and convert to cm where necessary
            length_cm = None
            height_cm = None

            if 'length_cm' in self.block_standard:
                length_cm = self.block_standard['length_cm']
            elif 'length_mm' in self.block_standard:
                length_cm = self.block_standard['length_mm'] / 10
            elif 'length_m' in self.block_standard:
                length_cm = self.block_standard['length_m'] * 100

            if 'height_cm' in self.block_standard:
                height_cm = self.block_standard['height_cm']
            elif 'height_mm' in self.block_standard:
                height_cm = self.block_standard['height_mm'] / 10
            elif 'height_m' in self.block_standard:
                height_cm = self.block_standard['height_m'] * 100

            # Support nested dimension dict if present
            dims = self.block_standard.get('dimensions') or {}
            if length_cm is None:
                if 'length_cm' in dims:
                    length_cm = dims.get('length_cm')
                elif 'length_mm' in dims:
                    length_cm = dims.get('length_mm') / 10
                elif 'length_m' in dims:
                    length_cm = dims.get('length_m') * 100

            if height_cm is None:
                if 'height_cm' in dims:
                    height_cm = dims.get('height_cm')
                elif 'height_mm' in dims:
                    height_cm = dims.get('height_mm') / 10
                elif 'height_m' in dims:
                    height_cm = dims.get('height_m') * 100

            # Final defaults if still missing (sensible typical block sizes in cm)
            if length_cm is None or height_cm is None:
                if '6_inch' in self.block_type:
                    length_cm = length_cm or 45.0
                    height_cm = height_cm or 15.0
                else:
                    # default to typical 9-inch hollow block footprint (approx 45cm x 22.5cm)
                    length_cm = length_cm or 45.0
                    height_cm = height_cm or 22.5

            # Ensure numeric values
            length_cm = float(length_cm)
            height_cm = float(height_cm)

            block_length_m = length_cm / 100.0
            block_height_m = height_cm / 100.0
            return block_length_m * block_height_m

        except Exception as e:
            # Fallback area in case of unexpected schema to avoid crashing the app
            print(f"DEBUG: calculate_block_area error: {e}")
            # default to 0.10125 m^2 (45cm x 22.5cm)
            return 0.10125
    
    def convert_to_meters(self, value, unit):
        """Convert any unit to meters"""
        for unit_info in MEASUREMENT_UNITS:
            if unit_info['id'] == unit:
                return value * unit_info['conversion_to_meters']
        return value
    
    
    def calculate_cement_needed(self, total_blocks):
        """Calculate cement bags needed (Nigerian standard: 1 bag per 70-80 blocks)"""
        return math.ceil(total_blocks / 75)
    
    def calculate_sand_needed(self, total_blocks):
        """Calculate sand needed in trucks (Nigerian standard)"""
        # Approximately 1 truck of sand for every 2000 blocks
        return math.ceil(total_blocks / 2000)

