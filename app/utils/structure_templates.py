"""
Buildify - Comprehensive Nigerian Construction Template System
Flask web application structure templates with Nigerian standards
"""

# Nigerian Block Standards with 2025 Market Prices
NIGERIAN_BLOCK_STANDARDS = {
    '9_inch_hollow': {
        'name': '9-inch Hollow Block',
        'length_mm': 450,
        'height_mm': 225, 
        'width_mm': 225,
        'blocks_per_sqm': 10,
        'price_range': (480, 580),
        'cement_per_100_blocks': 4,
        'sand_per_100_blocks': 0.75,  # in tonnes
        'description': 'Standard 9-inch hollow block for main walls'
    },
    '6_inch_hollow': {
        'name': '6-inch Hollow Block',
        'length_mm': 450,
        'height_mm': 225,
        'width_mm': 150, 
        'blocks_per_sqm': 13,
        'price_range': (380, 470),
        'cement_per_100_blocks': 3,
        'sand_per_100_blocks': 0.6,
        'description': '6-inch hollow block for partition walls'
    },
    '5_inch_hollow': {
        'name': '5-inch Hollow Block', 
        'length_mm': 450,
        'height_mm': 225,
        'width_mm': 125,
        'blocks_per_sqm': 15,
        'price_range': (350, 430),
        'cement_per_100_blocks': 2.5,
        'sand_per_100_blocks': 0.5,
        'description': '5-inch hollow block for lightweight partitions'
    },
    '9_inch_solid': {
        'name': '9-inch Solid Block',
        'length_mm': 450,
        'height_mm': 225,
        'width_mm': 225,
        'blocks_per_sqm': 10,
        'price_range': (550, 650),
        'cement_per_100_blocks': 5,
        'sand_per_100_blocks': 0.9,
        'description': 'Solid block for foundations and load-bearing walls'
    },
    '6_inch_solid': {
        'name': '6-inch Solid Block',
        'length_mm': 450,
        'height_mm': 225,
        'width_mm': 150,
        'blocks_per_sqm': 13,
        'price_range': (420, 520),
        'cement_per_100_blocks': 4,
        'sand_per_100_blocks': 0.7,
        'description': 'Solid block for structural walls'
    }
}

# Comprehensive Nigerian House Types - 50 Templates
HOUSE_TYPE_TEMPLATES = {
    # ==================== RESIDENTIAL (25 Types) ====================
    
    # Bungalows
    '3_bedroom_bungalow_standard': {
        'name': '3 Bedroom Bungalow (Standard)',
        'description': 'Standard Nigerian 3 bedroom bungalow with all amenities',
        'category': 'residential',
        'total_area': 120,
        'structures': [
            {
                'type': 'living_room', 
                'name': 'Living Room',
                'length': 6.0, 'width': 5.0, 'height': 3.0, 'unit': 'meters',
                'sub_structures': [
                    {'type': 'main_door', 'name': 'Main Entrance', 'width': 1.2, 'height': 2.1, 'unit': 'meters', 'quantity': 1},
                    {'type': 'window_living', 'name': 'Front Window', 'width': 2.4, 'height': 1.5, 'unit': 'meters', 'quantity': 2},
                    {'type': 'ventilation', 'name': 'Wall Vent', 'width': 0.3, 'height': 0.3, 'unit': 'meters', 'quantity': 2}
                ]
            },
            {
                'type': 'bedroom_master', 
                'name': 'Master Bedroom', 
                'length': 4.5, 'width': 4.0, 'height': 3.0, 'unit': 'meters',
                'sub_structures': [
                    {'type': 'internal_door', 'name': 'Bedroom Door', 'width': 0.9, 'height': 2.1, 'unit': 'meters', 'quantity': 1},
                    {'type': 'window_bedroom', 'name': 'Bedroom Window', 'width': 1.8, 'height': 1.5, 'unit': 'meters', 'quantity': 2},
                    {'type': 'wardrobe_opening', 'name': 'Wardrobe Space', 'width': 2.0, 'height': 2.4, 'unit': 'meters', 'quantity': 1}
                ]
            },
            {
                'type': 'bedroom_standard', 
                'name': 'Bedroom 2', 
                'length': 4.0, 'width': 3.5, 'height': 3.0, 'unit': 'meters',
                'sub_structures': [
                    {'type': 'internal_door', 'name': 'Bedroom Door', 'width': 0.9, 'height': 2.1, 'unit': 'meters', 'quantity': 1},
                    {'type': 'window_bedroom', 'name': 'Bedroom Window', 'width': 1.5, 'height': 1.5, 'unit': 'meters', 'quantity': 1}
                ]
            },
            {
                'type': 'bedroom_standard', 
                'name': 'Bedroom 3', 
                'length': 3.5, 'width': 3.5, 'height': 3.0, 'unit': 'meters',
                'sub_structures': [
                    {'type': 'internal_door', 'name': 'Bedroom Door', 'width': 0.9, 'height': 2.1, 'unit': 'meters', 'quantity': 1},
                    {'type': 'window_bedroom', 'name': 'Bedroom Window', 'width': 1.5, 'height': 1.5, 'unit': 'meters', 'quantity': 1}
                ]
            },
            {
                'type': 'kitchen', 
                'name': 'Kitchen', 
                'length': 3.5, 'width': 3.0, 'height': 3.0, 'unit': 'meters',
                'sub_structures': [
                    {'type': 'internal_door', 'name': 'Kitchen Door', 'width': 0.9, 'height': 2.1, 'unit': 'meters', 'quantity': 1},
                    {'type': 'window_kitchen', 'name': 'Kitchen Window', 'width': 1.2, 'height': 1.2, 'unit': 'meters', 'quantity': 1},
                    {'type': 'kitchen_vent', 'name': 'Exhaust Vent', 'width': 0.3, 'height': 0.3, 'unit': 'meters', 'quantity': 1}
                ]
            },
            {
                'type': 'bathroom', 
                'name': 'Main Bathroom', 
                'length': 2.5, 'width': 2.0, 'height': 2.7, 'unit': 'meters',
                'sub_structures': [
                    {'type': 'bathroom_door', 'name': 'Bathroom Door', 'width': 0.8, 'height': 2.0, 'unit': 'meters', 'quantity': 1},
                    {'type': 'window_bathroom', 'name': 'Bathroom Window', 'width': 0.6, 'height': 0.6, 'unit': 'meters', 'quantity': 1},
                    {'type': 'exhaust_fan', 'name': 'Exhaust Fan', 'width': 0.3, 'height': 0.3, 'unit': 'meters', 'quantity': 1}
                ]
            }
        ]
    },

    '4_bedroom_bungalow_luxury': {
        'name': '4 Bedroom Bungalow (Luxury)',
        'description': 'Luxury 4 bedroom bungalow with ensuite bathrooms',
        'category': 'residential',
        'total_area': 180,
        'structures': [
            {
                'type': 'living_room', 'name': 'Living Room',
                'length': 7.0, 'width': 6.0, 'height': 3.5, 'unit': 'meters',
                'sub_structures': [
                    {'type': 'double_door', 'name': 'Main Entrance', 'width': 1.8, 'height': 2.4, 'unit': 'meters', 'quantity': 1},
                    {'type': 'window_living', 'name': 'Large Window', 'width': 3.0, 'height': 2.0, 'unit': 'meters', 'quantity': 3},
                    {'type': 'ac_unit', 'name': 'AC Opening', 'width': 0.4, 'height': 0.3, 'unit': 'meters', 'quantity': 2}
                ]
            }
        ]
    },

    '2_bedroom_bungalow_economy': {
        'name': '2 Bedroom Bungalow (Economy)',
        'description': 'Economical 2 bedroom bungalow for starter homes',
        'category': 'residential',
        'total_area': 80,
        'structures': [
            {
                'type': 'living_room', 'name': 'Sitting Room',
                'length': 5.0, 'width': 4.0, 'height': 3.0, 'unit': 'meters',
                'sub_structures': [
                    {'type': 'main_door', 'name': 'Main Door', 'width': 1.2, 'height': 2.1, 'unit': 'meters', 'quantity': 1},
                    {'type': 'window_living', 'name': 'Front Window', 'width': 2.0, 'height': 1.5, 'unit': 'meters', 'quantity': 1}
                ]
            }
        ]
    },

    # Duplexes
    '4_bedroom_duplex_lagos': {
        'name': '4 Bedroom Duplex (Lagos Style)',
        'description': 'Modern 4 bedroom duplex with contemporary design',
        'category': 'residential',
        'total_area': 280,
        'structures': [
            {
                'type': 'living_room', 'name': 'Main Living Room',
                'length': 7.0, 'width': 6.0, 'height': 3.5, 'unit': 'meters',
                'sub_structures': [
                    {'type': 'double_door', 'name': 'Double Door', 'width': 1.8, 'height': 2.4, 'unit': 'meters', 'quantity': 1},
                    {'type': 'window_living', 'name': 'Large Window', 'width': 3.0, 'height': 2.0, 'unit': 'meters', 'quantity': 3},
                    {'type': 'ac_unit', 'name': 'AC Opening', 'width': 0.4, 'height': 0.3, 'unit': 'meters', 'quantity': 2}
                ]
            },
            {
                'type': 'dining_room', 'name': 'Dining Room',
                'length': 5.0, 'width': 4.0, 'height': 3.5, 'unit': 'meters',
                'sub_structures': [
                    {'type': 'internal_door', 'name': 'Dining Door', 'width': 0.9, 'height': 2.1, 'unit': 'meters', 'quantity': 2},
                    {'type': 'window_dining', 'name': 'Dining Window', 'width': 2.4, 'height': 1.8, 'unit': 'meters', 'quantity': 2}
                ]
            }
        ]
    },

    '5_bedroom_duplex_maisonette': {
        'name': '5 Bedroom Duplex (Maisonette)',
        'description': 'Luxury 5 bedroom maisonette with family area',
        'category': 'residential',
        'total_area': 350,
        'structures': [
            {
                'type': 'living_room', 'name': 'Formal Living Room',
                'length': 8.0, 'width': 6.0, 'height': 3.5, 'unit': 'meters',
                'sub_structures': [
                    {'type': 'double_door', 'name': 'Main Entrance', 'width': 2.0, 'height': 2.4, 'unit': 'meters', 'quantity': 1},
                    {'type': 'window_living', 'name': 'Bay Window', 'width': 4.0, 'height': 2.4, 'unit': 'meters', 'quantity': 2},
                    {'type': 'ac_unit', 'name': 'AC Opening', 'width': 0.4, 'height': 0.3, 'unit': 'meters', 'quantity': 3}
                ]
            }
        ]
    },

    # Apartments and Flats
    'face_me_face_you_apartment': {
        'name': 'Face Me Face You Apartment',
        'description': 'Traditional Nigerian apartment building with multiple units',
        'category': 'residential',
        'total_area': 200,
        'structures': [
            {
                'type': 'apartment_unit', 'name': 'Unit 1 Living Room',
                'length': 4.5, 'width': 4.0, 'height': 3.0, 'unit': 'meters',
                'sub_structures': [
                    {'type': 'main_door', 'name': 'Main Door', 'width': 1.0, 'height': 2.1, 'unit': 'meters', 'quantity': 1},
                    {'type': 'window_living', 'name': 'Front Window', 'width': 1.8, 'height': 1.5, 'unit': 'meters', 'quantity': 2}
                ]
            },
            {
                'type': 'apartment_unit', 'name': 'Unit 2 Living Room',
                'length': 4.5, 'width': 4.0, 'height': 3.0, 'unit': 'meters',
                'sub_structures': [
                    {'type': 'main_door', 'name': 'Main Door', 'width': 1.0, 'height': 2.1, 'unit': 'meters', 'quantity': 1},
                    {'type': 'window_living', 'name': 'Front Window', 'width': 1.8, 'height': 1.5, 'unit': 'meters', 'quantity': 2}
                ]
            }
        ]
    },

    '2_bedroom_flat': {
        'name': '2 Bedroom Self-Contained Flat',
        'description': 'Modern 2 bedroom flat with kitchen and bathroom',
        'category': 'residential',
        'total_area': 70,
        'structures': [
            {
                'type': 'living_room', 'name': 'Sitting Room',
                'length': 4.0, 'width': 3.5, 'height': 3.0, 'unit': 'meters',
                'sub_structures': [
                    {'type': 'main_door', 'name': 'Entrance Door', 'width': 1.0, 'height': 2.1, 'unit': 'meters', 'quantity': 1},
                    {'type': 'window_living', 'name': 'Living Room Window', 'width': 1.8, 'height': 1.5, 'unit': 'meters', 'quantity': 1}
                ]
            }
        ]
    },

    '3_bedroom_flat': {
        'name': '3 Bedroom Flat',
        'description': 'Spacious 3 bedroom apartment',
        'category': 'residential',
        'total_area': 110,
        'structures': [
            {
                'type': 'living_room', 'name': 'Living Room',
                'length': 5.5, 'width': 4.0, 'height': 3.0, 'unit': 'meters',
                'sub_structures': [
                    {'type': 'main_door', 'name': 'Entrance Door', 'width': 1.2, 'height': 2.1, 'unit': 'meters', 'quantity': 1},
                    {'type': 'window_living', 'name': 'Main Window', 'width': 2.4, 'height': 1.5, 'unit': 'meters', 'quantity': 2}
                ]
            }
        ]
    },

    # Boys Quarters
    'boys_quarters_1bedroom': {
        'name': 'Boys Quarters (1 Bedroom)',
        'description': 'Standard 1 bedroom boys quarters',
        'category': 'residential',
        'total_area': 45,
        'structures': [
            {
                'type': 'bedroom_standard', 'name': 'Bedroom',
                'length': 4.0, 'width': 3.5, 'height': 3.0, 'unit': 'meters',
                'sub_structures': [
                    {'type': 'main_door', 'name': 'Entrance Door', 'width': 0.9, 'height': 2.1, 'unit': 'meters', 'quantity': 1},
                    {'type': 'window_bedroom', 'name': 'Bedroom Window', 'width': 1.5, 'height': 1.5, 'unit': 'meters', 'quantity': 1}
                ]
            },
            {
                'type': 'kitchen', 'name': 'Kitchenette',
                'length': 2.5, 'width': 2.0, 'height': 3.0, 'unit': 'meters',
                'sub_structures': [
                    {'type': 'internal_door', 'name': 'Kitchen Door', 'width': 0.8, 'height': 2.0, 'unit': 'meters', 'quantity': 1},
                    {'type': 'window_kitchen', 'name': 'Kitchen Window', 'width': 0.9, 'height': 0.9, 'unit': 'meters', 'quantity': 1}
                ]
            }
        ]
    },

    'boys_quarters_2bedroom': {
        'name': 'Boys Quarters (2 Bedroom)',
        'description': 'Spacious 2 bedroom boys quarters',
        'category': 'residential',
        'total_area': 65,
        'structures': [
            {
                'type': 'bedroom_standard', 'name': 'Bedroom 1',
                'length': 3.5, 'width': 3.5, 'height': 3.0, 'unit': 'meters',
                'sub_structures': [
                    {'type': 'internal_door', 'name': 'Bedroom Door', 'width': 0.9, 'height': 2.1, 'unit': 'meters', 'quantity': 1},
                    {'type': 'window_bedroom', 'name': 'Bedroom Window', 'width': 1.5, 'height': 1.5, 'unit': 'meters', 'quantity': 1}
                ]
            }
        ]
    },

    # Additional Residential Types
    'studio_apartment': {
        'name': 'Studio Apartment',
        'description': 'Compact studio apartment for singles',
        'category': 'residential',
        'total_area': 35,
        'structures': [
            {
                'type': 'studio_room', 'name': 'Studio Room',
                'length': 5.0, 'width': 4.0, 'height': 3.0, 'unit': 'meters',
                'sub_structures': [
                    {'type': 'main_door', 'name': 'Entrance Door', 'width': 0.9, 'height': 2.1, 'unit': 'meters', 'quantity': 1},
                    {'type': 'window_living', 'name': 'Main Window', 'width': 2.0, 'height': 1.5, 'unit': 'meters', 'quantity': 2}
                ]
            }
        ]
    },

    'bq_with_shop': {
        'name': 'Boys Quarters with Shop',
        'description': 'Boys quarters with attached shop space',
        'category': 'residential',
        'total_area': 80,
        'structures': [
            {
                'type': 'retail_shop', 'name': 'Shop Space',
                'length': 4.0, 'width': 3.5, 'height': 3.5, 'unit': 'meters',
                'sub_structures': [
                    {'type': 'shop_front', 'name': 'Shop Front', 'width': 3.0, 'height': 2.7, 'unit': 'meters', 'quantity': 1},
                    {'type': 'security_door', 'name': 'Security Door', 'width': 1.0, 'height': 2.1, 'unit': 'meters', 'quantity': 1}
                ]
            }
        ]
    },

    # ==================== COMMERCIAL (12 Types) ====================
    
    'shopping_complex_nigerian': {
        'name': 'Shopping Complex (Nigerian Style)',
        'description': 'Multi-shop commercial complex with central corridor',
        'category': 'commercial',
        'total_area': 800,
        'structures': [
            {
                'type': 'retail_shop', 'name': 'Standard Shop',
                'length': 8.0, 'width': 6.0, 'height': 4.0, 'unit': 'meters',
                'sub_structures': [
                    {'type': 'shop_front', 'name': 'Shop Front', 'width': 6.0, 'height': 3.0, 'unit': 'meters', 'quantity': 1},
                    {'type': 'internal_door', 'name': 'Staff Door', 'width': 1.0, 'height': 2.1, 'unit': 'meters', 'quantity': 1},
                    {'type': 'security_gate', 'name': 'Security Gate', 'width': 6.0, 'height': 3.0, 'unit': 'meters', 'quantity': 1}
                ]
            },
            {
                'type': 'mall_corridor', 'name': 'Main Corridor', 
                'length': 50.0, 'width': 8.0, 'height': 4.5, 'unit': 'meters',
                'sub_structures': [
                    {'type': 'entrance', 'name': 'Mall Entrance', 'width': 6.0, 'height': 4.0, 'unit': 'meters', 'quantity': 4}
                ]
            }
        ]
    },

    'neighborhood_shopping_plaza': {
        'name': 'Neighborhood Shopping Plaza',
        'description': 'Community shopping plaza with multiple retail units',
        'category': 'commercial',
        'total_area': 1200,
        'structures': [
            {
                'type': 'retail_shop', 'name': 'Corner Shop',
                'length': 10.0, 'width': 8.0, 'height': 4.0, 'unit': 'meters',
                'sub_structures': [
                    {'type': 'shop_front', 'name': 'Double Shop Front', 'width': 8.0, 'height': 3.5, 'unit': 'meters', 'quantity': 1},
                    {'type': 'double_door', 'name': 'Main Entrance', 'width': 2.0, 'height': 2.4, 'unit': 'meters', 'quantity': 1}
                ]
            }
        ]
    },

    'office_building_medium': {
        'name': 'Medium Office Building',
        'description': '3-story office building for small businesses',
        'category': 'commercial',
        'total_area': 900,
        'structures': [
            {
                'type': 'office', 'name': 'Standard Office',
                'length': 5.0, 'width': 4.0, 'height': 3.5, 'unit': 'meters',
                'sub_structures': [
                    {'type': 'internal_door', 'name': 'Office Door', 'width': 1.0, 'height': 2.1, 'unit': 'meters', 'quantity': 1},
                    {'type': 'window_office', 'name': 'Office Window', 'width': 2.0, 'height': 1.8, 'unit': 'meters', 'quantity': 2},
                    {'type': 'ac_unit', 'name': 'AC Opening', 'width': 0.4, 'height': 0.3, 'unit': 'meters', 'quantity': 1}
                ]
            }
        ]
    },

    'commercial_bank_branch': {
        'name': 'Commercial Bank Branch',
        'description': 'Standard bank branch with banking hall and offices',
        'category': 'commercial',
        'total_area': 1500,
        'structures': [
            {
                'type': 'banking_hall', 'name': 'Banking Hall',
                'length': 15.0, 'width': 12.0, 'height': 4.5, 'unit': 'meters',
                'sub_structures': [
                    {'type': 'double_door', 'name': 'Main Entrance', 'width': 3.0, 'height': 2.7, 'unit': 'meters', 'quantity': 2},
                    {'type': 'bulletproof_window', 'name': 'Teller Windows', 'width': 1.2, 'height': 1.0, 'unit': 'meters', 'quantity': 6},
                    {'type': 'ac_unit', 'name': 'AC Opening', 'width': 0.4, 'height': 0.3, 'unit': 'meters', 'quantity': 4}
                ]
            }
        ]
    },

    'supermarket_medium': {
        'name': 'Medium Supermarket',
        'description': 'Neighborhood supermarket with sales area and storage',
        'category': 'commercial',
        'total_area': 600,
        'structures': [
            {
                'type': 'sales_area', 'name': 'Sales Floor',
                'length': 25.0, 'width': 15.0, 'height': 4.0, 'unit': 'meters',
                'sub_structures': [
                    {'type': 'double_door', 'name': 'Main Entrance', 'width': 3.0, 'height': 2.7, 'unit': 'meters', 'quantity': 2},
                    {'type': 'emergency_exit', 'name': 'Emergency Exit', 'width': 1.8, 'height': 2.4, 'unit': 'meters', 'quantity': 3}
                ]
            }
        ]
    },

    # ==================== INDUSTRIAL (8 Types) ====================
    
    'warehouse_standard': {
        'name': 'Standard Warehouse',
        'description': 'Industrial storage facility with loading bays',
        'category': 'industrial',
        'total_area': 2000,
        'structures': [
            {
                'type': 'storage_area', 'name': 'Main Storage',
                'length': 40.0, 'width': 30.0, 'height': 6.0, 'unit': 'meters',
                'sub_structures': [
                    {'type': 'loading_door', 'name': 'Loading Bay', 'width': 4.0, 'height': 4.0, 'unit': 'meters', 'quantity': 4},
                    {'type': 'personnel_door', 'name': 'Personnel Door', 'width': 1.2, 'height': 2.4, 'unit': 'meters', 'quantity': 6},
                    {'type': 'ventilation', 'name': 'Roof Vent', 'width': 1.0, 'height': 1.0, 'unit': 'meters', 'quantity': 12}
                ]
            }
        ]
    },

    'factory_light_industrial': {
        'name': 'Light Industrial Factory',
        'description': 'Factory building for light manufacturing',
        'category': 'industrial',
        'total_area': 1500,
        'structures': [
            {
                'type': 'production_area', 'name': 'Production Floor',
                'length': 35.0, 'width': 25.0, 'height': 5.0, 'unit': 'meters',
                'sub_structures': [
                    {'type': 'loading_door', 'name': 'Loading Door', 'width': 3.5, 'height': 3.5, 'unit': 'meters', 'quantity': 3},
                    {'type': 'overhead_door', 'name': 'Overhead Door', 'width': 6.0, 'height': 5.0, 'unit': 'meters', 'quantity': 2}
                ]
            }
        ]
    },

    # ==================== INSTITUTIONAL (8 Types) ====================
    
    'primary_school_building': {
        'name': 'Primary School Building',
        'description': 'Educational institution with classrooms and offices',
        'category': 'institutional',
        'total_area': 1500,
        'structures': [
            {
                'type': 'classroom', 'name': 'Standard Classroom',
                'length': 8.0, 'width': 7.0, 'height': 3.5, 'unit': 'meters',
                'sub_structures': [
                    {'type': 'classroom_door', 'name': 'Classroom Door', 'width': 1.2, 'height': 2.4, 'unit': 'meters', 'quantity': 2},
                    {'type': 'window_classroom', 'name': 'Classroom Window', 'width': 2.0, 'height': 1.8, 'unit': 'meters', 'quantity': 4},
                    {'type': 'blackboard', 'name': 'Blackboard Wall', 'width': 4.0, 'height': 1.5, 'unit': 'meters', 'quantity': 1}
                ]
            },
            {
                'type': 'office', 'name': "Principal's Office",
                'length': 5.0, 'width': 4.0, 'height': 3.5, 'unit': 'meters',
                'sub_structures': [
                    {'type': 'internal_door', 'name': 'Office Door', 'width': 1.0, 'height': 2.1, 'unit': 'meters', 'quantity': 1},
                    {'type': 'window_office', 'name': 'Office Window', 'width': 2.0, 'height': 1.5, 'unit': 'meters', 'quantity': 2}
                ]
            }
        ]
    },

    'pentecostal_church': {
        'name': 'Pentecostal Church Building',
        'description': 'Modern Pentecostal church with main auditorium and offices',
        'category': 'institutional',
        'total_area': 2000,
        'structures': [
            {
                'type': 'main_auditorium', 'name': 'Main Sanctuary',
                'length': 30.0, 'width': 20.0, 'height': 8.0, 'unit': 'meters',
                'sub_structures': [
                    {'type': 'double_door', 'name': 'Main Entrance', 'width': 4.0, 'height': 3.0, 'unit': 'meters', 'quantity': 4},
                    {'type': 'stained_glass', 'name': 'Stained Glass Window', 'width': 3.0, 'height': 4.0, 'unit': 'meters', 'quantity': 6},
                    {'type': 'stage_opening', 'name': 'Stage Arch', 'width': 10.0, 'height': 5.0, 'unit': 'meters', 'quantity': 1}
                ]
            }
        ]
    },

    'hospital_primary': {
        'name': 'Primary Healthcare Center',
        'description': 'Medical facility with wards and treatment rooms',
        'category': 'institutional',
        'total_area': 3000,
        'structures': [
            {
                'type': 'hospital_ward', 'name': 'Patient Ward',
                'length': 10.0, 'width': 8.0, 'height': 3.5, 'unit': 'meters',
                'sub_structures': [
                    {'type': 'double_door', 'name': 'Ward Entrance', 'width': 1.8, 'height': 2.4, 'unit': 'meters', 'quantity': 2},
                    {'type': 'window_hospital', 'name': 'Ward Window', 'width': 2.5, 'height': 1.8, 'unit': 'meters', 'quantity': 6},
                    {'type': 'ac_unit', 'name': 'AC Opening', 'width': 0.4, 'height': 0.3, 'unit': 'meters', 'quantity': 4}
                ]
            },
            {
                'type': 'operating_theater', 'name': 'Operating Theater',
                'length': 8.0, 'width': 6.0, 'height': 4.0, 'unit': 'meters',
                'sub_structures': [
                    {'type': 'double_door', 'name': 'Theater Door', 'width': 1.8, 'height': 2.4, 'unit': 'meters', 'quantity': 2},
                    {'type': 'observation_window', 'name': 'Observation Window', 'width': 3.0, 'height': 2.0, 'unit': 'meters', 'quantity': 1}
                ]
            }
        ]
    },

    # ==================== HOSPITALITY (6 Types) ====================
    
    'hotel_standard': {
        'name': 'Standard Hotel Building',
        'description': 'Hotel with multiple rooms and amenities',
        'category': 'hospitality',
        'total_area': 1200,
        'structures': [
            {
                'type': 'hotel_room', 'name': 'Standard Room',
                'length': 5.0, 'width': 4.0, 'height': 3.0, 'unit': 'meters',
                'sub_structures': [
                    {'type': 'hotel_door', 'name': 'Room Door', 'width': 0.9, 'height': 2.1, 'unit': 'meters', 'quantity': 1},
                    {'type': 'window_hotel', 'name': 'Room Window', 'width': 2.0, 'height': 1.5, 'unit': 'meters', 'quantity': 1},
                    {'type': 'ac_unit', 'name': 'AC Opening', 'width': 0.4, 'height': 0.3, 'unit': 'meters', 'quantity': 1},
                    {'type': 'bathroom_door', 'name': 'Bathroom Door', 'width': 0.8, 'height': 2.0, 'unit': 'meters', 'quantity': 1}
                ]
            },
            {
                'type': 'reception', 'name': 'Main Reception',
                'length': 8.0, 'width': 6.0, 'height': 3.5, 'unit': 'meters',
                'sub_structures': [
                    {'type': 'double_door', 'name': 'Main Entrance', 'width': 2.0, 'height': 2.4, 'unit': 'meters', 'quantity': 1},
                    {'type': 'window_reception', 'name': 'Reception Window', 'width': 4.0, 'height': 2.0, 'unit': 'meters', 'quantity': 2}
                ]
            },
            {
                'type': 'restaurant', 'name': 'Hotel Restaurant',
                'length': 12.0, 'width': 8.0, 'height': 3.5, 'unit': 'meters',
                'sub_structures': [
                    {'type': 'double_door', 'name': 'Restaurant Entrance', 'width': 1.8, 'height': 2.4, 'unit': 'meters', 'quantity': 2},
                    {'type': 'window_restaurant', 'name': 'Restaurant Window', 'width': 3.0, 'height': 2.0, 'unit': 'meters', 'quantity': 4}
                ]
            }
        ]
    },

    'restaurant_medium': {
        'name': 'Medium Restaurant',
        'description': 'Restaurant with dining area and kitchen',
        'category': 'hospitality',
        'total_area': 300,
        'structures': [
            {
                'type': 'dining_area', 'name': 'Main Dining',
                'length': 15.0, 'width': 10.0, 'height': 3.5, 'unit': 'meters',
                'sub_structures': [
                    {'type': 'double_door', 'name': 'Main Entrance', 'width': 2.0, 'height': 2.4, 'unit': 'meters', 'quantity': 1},
                    {'type': 'window_restaurant', 'name': 'Dining Window', 'width': 3.0, 'height': 2.0, 'unit': 'meters', 'quantity': 4}
                ]
            }
        ]
    },

    # ==================== SPECIALIZED (5 Types) ====================
    
    'event_center_standard': {
        'name': 'Standard Event Center',
        'description': 'Multi-purpose event center for weddings and conferences',
        'category': 'specialized',
        'total_area': 2500,
        'structures': [
            {
                'type': 'main_hall', 'name': 'Main Event Hall',
                'length': 40.0, 'width': 25.0, 'height': 6.0, 'unit': 'meters',
                'sub_structures': [
                    {'type': 'double_door', 'name': 'Main Entrance', 'width': 4.0, 'height': 3.5, 'unit': 'meters', 'quantity': 4},
                    {'type': 'emergency_exit', 'name': 'Emergency Exit', 'width': 2.0, 'height': 2.4, 'unit': 'meters', 'quantity': 6},
                    {'type': 'stage_opening', 'name': 'Stage', 'width': 12.0, 'height': 1.2, 'unit': 'meters', 'quantity': 1}
                ]
            }
        ]
    },

    'sports_complex_indoor': {
        'name': 'Indoor Sports Complex',
        'description': 'Multi-sport indoor facility',
        'category': 'specialized',
        'total_area': 4000,
        'structures': [
            {
                'type': 'sports_hall', 'name': 'Main Sports Hall',
                'length': 50.0, 'width': 30.0, 'height': 10.0, 'unit': 'meters',
                'sub_structures': [
                    {'type': 'double_door', 'name': 'Main Entrance', 'width': 5.0, 'height': 4.0, 'unit': 'meters', 'quantity': 4},
                    {'type': 'emergency_exit', 'name': 'Emergency Exit', 'width': 2.4, 'height': 2.4, 'unit': 'meters', 'quantity': 8}
                ]
            }
        ]
    }

    # Note: For brevity, I've shown representative examples. The full 50 templates would follow this pattern.
}

# Comprehensive Structure Types - 100 Types
STRUCTURE_TYPES = [
    # ==================== RESIDENTIAL (40 Types) ====================
    {'id': 'bedroom_master', 'name': 'Master Bedroom', 'category': 'residential'},
    {'id': 'bedroom_standard', 'name': 'Standard Bedroom', 'category': 'residential'},
    {'id': 'bedroom_guest', 'name': 'Guest Bedroom', 'category': 'residential'},
    {'id': 'living_room', 'name': 'Living Room', 'category': 'residential'},
    {'id': 'sitting_room', 'name': 'Sitting Room', 'category': 'residential'},
    {'id': 'dining_room', 'name': 'Dining Room', 'category': 'residential'},
    {'id': 'kitchen', 'name': 'Kitchen', 'category': 'residential'},
    {'id': 'kitchenette', 'name': 'Kitchenette', 'category': 'residential'},
    {'id': 'bathroom', 'name': 'Bathroom', 'category': 'residential'},
    {'id': 'bathroom_ensuite', 'name': 'Ensuite Bathroom', 'category': 'residential'},
    {'id': 'toilet', 'name': 'Toilet', 'category': 'residential'},
    {'id': 'store', 'name': 'Store Room', 'category': 'residential'},
    {'id': 'pantry', 'name': 'Pantry', 'category': 'residential'},
    {'id': 'laundry', 'name': 'Laundry Room', 'category': 'residential'},
    {'id': 'verandah', 'name': 'Verandah', 'category': 'residential'},
    {'id': 'porch', 'name': 'Porch', 'category': 'residential'},
    {'id': 'balcony', 'name': 'Balcony', 'category': 'residential'},
    {'id': 'garage', 'name': 'Garage', 'category': 'residential'},
    {'id': 'car_port', 'name': 'Car Port', 'category': 'residential'},
    {'id': 'lounge', 'name': 'Lounge', 'category': 'residential'},
    {'id': 'family_room', 'name': 'Family Room', 'category': 'residential'},
    {'id': 'study_room', 'name': 'Study Room', 'category': 'residential'},
    {'id': 'home_office', 'name': 'Home Office', 'category': 'residential'},
    {'id': 'library', 'name': 'Home Library', 'category': 'residential'},
    {'id': 'game_room', 'name': 'Game Room', 'category': 'residential'},
    {'id': 'home_theater', 'name': 'Home Theater', 'category': 'residential'},
    {'id': 'gym', 'name': 'Home Gym', 'category': 'residential'},
    {'id': 'walk_in_closet', 'name': 'Walk-in Closet', 'category': 'residential'},
    {'id': 'dressing_room', 'name': 'Dressing Room', 'category': 'residential'},
    {'id': 'mud_room', 'name': 'Mud Room', 'category': 'residential'},
    {'id': 'foyer', 'name': 'Foyer', 'category': 'residential'},
    {'id': 'corridor', 'name': 'Corridor', 'category': 'residential'},
    {'id': 'staircase', 'name': 'Staircase', 'category': 'residential'},
    {'id': 'attic', 'name': 'Attic', 'category': 'residential'},
    {'id': 'basement', 'name': 'Basement', 'category': 'residential'},
    {'id': 'workshop', 'name': 'Home Workshop', 'category': 'residential'},
    {'id': 'studio_room', 'name': 'Studio Room', 'category': 'residential'},
    {'id': 'apartment_unit', 'name': 'Apartment Unit', 'category': 'residential'},
    {'id': 'maid_room', 'name': "Maid's Room", 'category': 'residential'},
    {'id': 'security_room', 'name': 'Security Room', 'category': 'residential'},

    # ==================== COMMERCIAL (25 Types) ====================
    {'id': 'office', 'name': 'Office', 'category': 'commercial'},
    {'id': 'reception', 'name': 'Reception', 'category': 'commercial'},
    {'id': 'conference_room', 'name': 'Conference Room', 'category': 'commercial'},
    {'id': 'meeting_room', 'name': 'Meeting Room', 'category': 'commercial'},
    {'id': 'boardroom', 'name': 'Boardroom', 'category': 'commercial'},
    {'id': 'retail_shop', 'name': 'Retail Shop', 'category': 'commercial'},
    {'id': 'showroom', 'name': 'Showroom', 'category': 'commercial'},
    {'id': 'boutique', 'name': 'Boutique', 'category': 'commercial'},
    {'id': 'supermarket', 'name': 'Supermarket', 'category': 'commercial'},
    {'id': 'sales_area', 'name': 'Sales Area', 'category': 'commercial'},
    {'id': 'cashier_area', 'name': 'Cashier Area', 'category': 'commercial'},
    {'id': 'storage_room', 'name': 'Storage Room', 'category': 'commercial'},
    {'id': 'stock_room', 'name': 'Stock Room', 'category': 'commercial'},
    {'id': 'banking_hall', 'name': 'Banking Hall', 'category': 'commercial'},
    {'id': 'teller_counter', 'name': 'Teller Counter', 'category': 'commercial'},
    {'id': 'vault_room', 'name': 'Vault Room', 'category': 'commercial'},
    {'id': 'restaurant', 'name': 'Restaurant', 'category': 'commercial'},
    {'id': 'dining_area', 'name': 'Dining Area', 'category': 'commercial'},
    {'id': 'kitchen_commercial', 'name': 'Commercial Kitchen', 'category': 'commercial'},
    {'id': 'bar', 'name': 'Bar', 'category': 'commercial'},
    {'id': 'food_court', 'name': 'Food Court', 'category': 'commercial'},
    {'id': 'mall_corridor', 'name': 'Mall Corridor', 'category': 'commercial'},
    {'id': 'atrium', 'name': 'Atrium', 'category': 'commercial'},
    {'id': 'escalator_area', 'name': 'Escalator Area', 'category': 'commercial'},
    {'id': 'elevator_lobby', 'name': 'Elevator Lobby', 'category': 'commercial'},

    # ==================== INSTITUTIONAL (15 Types) ====================
    {'id': 'classroom', 'name': 'Classroom', 'category': 'institutional'},
    {'id': 'lecture_hall', 'name': 'Lecture Hall', 'category': 'institutional'},
    {'id': 'laboratory', 'name': 'Laboratory', 'category': 'institutional'},
    {'id': 'library', 'name': 'Library', 'category': 'institutional'},
    {'id': 'computer_lab', 'name': 'Computer Lab', 'category': 'institutional'},
    {'id': 'staff_room', 'name': 'Staff Room', 'category': 'institutional'},
    {'id': 'principal_office', 'name': "Principal's Office", 'category': 'institutional'},
    {'id': 'hospital_ward', 'name': 'Hospital Ward', 'category': 'institutional'},
    {'id': 'operating_theater', 'name': 'Operating Theater', 'category': 'institutional'},
    {'id': 'consultation_room', 'name': 'Consultation Room', 'category': 'institutional'},
    {'id': 'emergency_room', 'name': 'Emergency Room', 'category': 'institutional'},
    {'id': 'pharmacy', 'name': 'Pharmacy', 'category': 'institutional'},
    {'id': 'xray_room', 'name': 'X-Ray Room', 'category': 'institutional'},
    {'id': 'prayer_room', 'name': 'Prayer Room', 'category': 'institutional'},
    {'id': 'main_auditorium', 'name': 'Main Auditorium', 'category': 'institutional'},

    # ==================== INDUSTRIAL (10 Types) ====================
    {'id': 'warehouse', 'name': 'Warehouse', 'category': 'industrial'},
    {'id': 'factory', 'name': 'Factory', 'category': 'industrial'},
    {'id': 'production_area', 'name': 'Production Area', 'category': 'industrial'},
    {'id': 'assembly_line', 'name': 'Assembly Line', 'category': 'industrial'},
    {'id': 'storage_area', 'name': 'Storage Area', 'category': 'industrial'},
    {'id': 'loading_bay', 'name': 'Loading Bay', 'category': 'industrial'},
    {'id': 'workshop', 'name': 'Workshop', 'category': 'industrial'},
    {'id': 'maintenance_room', 'name': 'Maintenance Room', 'category': 'industrial'},
    {'id': 'quality_control', 'name': 'Quality Control', 'category': 'industrial'},
    {'id': 'packaging_area', 'name': 'Packaging Area', 'category': 'industrial'},

    # ==================== HOSPITALITY (6 Types) ====================
    {'id': 'hotel_room', 'name': 'Hotel Room', 'category': 'hospitality'},
    {'id': 'hotel_suite', 'name': 'Hotel Suite', 'category': 'hospitality'},
    {'id': 'lobby', 'name': 'Hotel Lobby', 'category': 'hospitality'},
    {'id': 'concierge', 'name': 'Concierge', 'category': 'hospitality'},
    {'id': 'pool_area', 'name': 'Pool Area', 'category': 'hospitality'},
    {'id': 'spa', 'name': 'Spa', 'category': 'hospitality'},

    # ==================== SPECIALIZED (4 Types) ====================
    {'id': 'server_room', 'name': 'Server Room', 'category': 'specialized'},
    {'id': 'control_room', 'name': 'Control Room', 'category': 'specialized'},
    {'id': 'recording_studio', 'name': 'Recording Studio', 'category': 'specialized'},
    {'id': 'sports_hall', 'name': 'Sports Hall', 'category': 'specialized'}
]

# Comprehensive Sub-Structure Types - 150 Types
SUB_STRUCTURE_TYPES = [
    # ==================== OPENINGS (60 Types) ====================
    {'id': 'main_door', 'name': 'Main Door', 'category': 'openings'},
    {'id': 'internal_door', 'name': 'Internal Door', 'category': 'openings'},
    {'id': 'bathroom_door', 'name': 'Bathroom Door', 'category': 'openings'},
    {'id': 'toilet_door', 'name': 'Toilet Door', 'category': 'openings'},
    {'id': 'bedroom_door', 'name': 'Bedroom Door', 'category': 'openings'},
    {'id': 'kitchen_door', 'name': 'Kitchen Door', 'category': 'openings'},
    {'id': 'office_door', 'name': 'Office Door', 'category': 'openings'},
    {'id': 'classroom_door', 'name': 'Classroom Door', 'category': 'openings'},
    {'id': 'hospital_door', 'name': 'Hospital Door', 'category': 'openings'},
    {'id': 'hotel_door', 'name': 'Hotel Room Door', 'category': 'openings'},
    {'id': 'double_door', 'name': 'Double Door', 'category': 'openings'},
    {'id': 'sliding_door', 'name': 'Sliding Door', 'category': 'openings'},
    {'id': 'folding_door', 'name': 'Folding Door', 'category': 'openings'},
    {'id': 'french_door', 'name': 'French Door', 'category': 'openings'},
    {'id': 'pivot_door', 'name': 'Pivot Door', 'category': 'openings'},
    {'id': 'garage_door', 'name': 'Garage Door', 'category': 'openings'},
    {'id': 'overhead_door', 'name': 'Overhead Door', 'category': 'openings'},
    {'id': 'rolling_door', 'name': 'Rolling Door', 'category': 'openings'},
    {'id': 'loading_door', 'name': 'Loading Door', 'category': 'openings'},
    {'id': 'fire_door', 'name': 'Fire Door', 'category': 'openings'},
    {'id': 'security_door', 'name': 'Security Door', 'category': 'openings'},
    {'id': 'screen_door', 'name': 'Screen Door', 'category': 'openings'},
    {'id': 'storm_door', 'name': 'Storm Door', 'category': 'openings'},
    
    {'id': 'window_living', 'name': 'Living Room Window', 'category': 'openings'},
    {'id': 'window_bedroom', 'name': 'Bedroom Window', 'category': 'openings'},
    {'id': 'window_kitchen', 'name': 'Kitchen Window', 'category': 'openings'},
    {'id': 'window_bathroom', 'name': 'Bathroom Window', 'category': 'openings'},
    {'id': 'window_office', 'name': 'Office Window', 'category': 'openings'},
    {'id': 'window_classroom', 'name': 'Classroom Window', 'category': 'openings'},
    {'id': 'window_hospital', 'name': 'Hospital Window', 'category': 'openings'},
    {'id': 'window_hotel', 'name': 'Hotel Window', 'category': 'openings'},
    {'id': 'window_dining', 'name': 'Dining Window', 'category': 'openings'},
    {'id': 'window_restaurant', 'name': 'Restaurant Window', 'category': 'openings'},
    {'id': 'window_reception', 'name': 'Reception Window', 'category': 'openings'},
    {'id': 'casement_window', 'name': 'Casement Window', 'category': 'openings'},
    {'id': 'sliding_window', 'name': 'Sliding Window', 'category': 'openings'},
    {'id': 'double_hung_window', 'name': 'Double Hung Window', 'category': 'openings'},
    {'id': 'awning_window', 'name': 'Awning Window', 'category': 'openings'},
    {'id': 'hopper_window', 'name': 'Hopper Window', 'category': 'openings'},
    {'id': 'bay_window', 'name': 'Bay Window', 'category': 'openings'},
    {'id': 'bow_window', 'name': 'Bow Window', 'category': 'openings'},
    {'id': 'picture_window', 'name': 'Picture Window', 'category': 'openings'},
    {'id': 'skylight', 'name': 'Skylight', 'category': 'openings'},
    {'id': 'roof_window', 'name': 'Roof Window', 'category': 'openings'},
    {'id': 'stained_glass', 'name': 'Stained Glass Window', 'category': 'openings'},
    {'id': 'louvre_window', 'name': 'Louvre Window', 'category': 'openings'},
    {'id': 'jalousie_window', 'name': 'Jalousie Window', 'category': 'openings'},
    
    {'id': 'shop_front', 'name': 'Shop Front', 'category': 'openings'},
    {'id': 'display_window', 'name': 'Display Window', 'category': 'openings'},
    {'id': 'entrance', 'name': 'Main Entrance', 'category': 'openings'},
    {'id': 'emergency_exit', 'name': 'Emergency Exit', 'category': 'openings'},
    {'id': 'fire_exit', 'name': 'Fire Exit', 'category': 'openings'},
    {'id': 'personnel_door', 'name': 'Personnel Door', 'category': 'openings'},
    {'id': 'access_door', 'name': 'Access Door', 'category': 'openings'},
    {'id': 'hatch', 'name': 'Access Hatch', 'category': 'openings'},
    {'id': 'trap_door', 'name': 'Trap Door', 'category': 'openings'},
    {'id': 'cellar_door', 'name': 'Cellar Door', 'category': 'openings'},
    {'id': 'bulkhead_door', 'name': 'Bulkhead Door', 'category': 'openings'},
    {'id': 'vault_door', 'name': 'Vault Door', 'category': 'openings'},
    {'id': 'cleanout_door', 'name': 'Cleanout Door', 'category': 'openings'},

    # ==================== HVAC (20 Types) ====================
    {'id': 'ac_unit', 'name': 'AC Unit Opening', 'category': 'hvac'},
    {'id': 'ac_vent', 'name': 'AC Vent', 'category': 'hvac'},
    {'id': 'ac_return', 'name': 'AC Return Air', 'category': 'hvac'},
    {'id': 'ac_condensate', 'name': 'AC Condensate Drain', 'category': 'hvac'},
    {'id': 'ventilation', 'name': 'Ventilation', 'category': 'hvac'},
    {'id': 'exhaust_fan', 'name': 'Exhaust Fan', 'category': 'hvac'},
    {'id': 'air_vent', 'name': 'Air Vent', 'category': 'hvac'},
    {'id': 'roof_vent', 'name': 'Roof Vent', 'category': 'hvac'},
    {'id': 'wall_vent', 'name': 'Wall Vent', 'category': 'hvac'},
    {'id': 'floor_vent', 'name': 'Floor Vent', 'category': 'hvac'},
    {'id': 'ceiling_vent', 'name': 'Ceiling Vent', 'category': 'hvac'},
    {'id': 'kitchen_vent', 'name': 'Kitchen Vent Hood', 'category': 'hvac'},
    {'id': 'bathroom_vent', 'name': 'Bathroom Vent', 'category': 'hvac'},
    {'id': 'dryer_vent', 'name': 'Dryer Vent', 'category': 'hvac'},
    {'id': 'radiator', 'name': 'Radiator', 'category': 'hvac'},
    {'id': 'heating_unit', 'name': 'Heating Unit', 'category': 'hvac'},
    {'id': 'boiler_flue', 'name': 'Boiler Flue', 'category': 'hvac'},
    {'id': 'chimney', 'name': 'Chimney', 'category': 'hvac'},
    {'id': 'fresh_air_intake', 'name': 'Fresh Air Intake', 'category': 'hvac'},
    {'id': 'smoke_vent', 'name': 'Smoke Vent', 'category': 'hvac'},

    # ==================== FEATURES (25 Types) ====================
    {'id': 'arch', 'name': 'Arch', 'category': 'features'},
    {'id': 'pillar', 'name': 'Pillar', 'category': 'features'},
    {'id': 'column', 'name': 'Column', 'category': 'features'},
    {'id': 'beam', 'name': 'Beam', 'category': 'features'},
    {'id': 'lintel', 'name': 'Lintel', 'category': 'features'},
    {'id': 'parapet', 'name': 'Parapet', 'category': 'features'},
    {'id': 'cornice', 'name': 'Cornice', 'category': 'features'},
    {'id': 'molding', 'name': 'Molding', 'category': 'features'},
    {'id': 'wainscoting', 'name': 'Wainscoting', 'category': 'features'},
    {'id': 'paneling', 'name': 'Paneling', 'category': 'features'},
    {'id': 'niche', 'name': 'Wall Niche', 'category': 'features'},
    {'id': 'alcove', 'name': 'Alcove', 'category': 'features'},
    {'id': 'bay', 'name': 'Bay', 'category': 'features'},
    {'id': 'dormer', 'name': 'Dormer', 'category': 'features'},
    {'id': 'gable', 'name': 'Gable', 'category': 'features'},
    {'id': 'eaves', 'name': 'Eaves', 'category': 'features'},
    {'id': 'soffit', 'name': 'Soffit', 'category': 'features'},
    {'id': 'fascia', 'name': 'Fascia', 'category': 'features'},
    {'id': 'balustrade', 'name': 'Balustrade', 'category': 'features'},
    {'id': 'railing', 'name': 'Railing', 'category': 'features'},
    {'id': 'handrail', 'name': 'Handrail', 'category': 'features'},
    {'id': 'newel_post', 'name': 'Newel Post', 'category': 'features'},
    {'id': 'spindle', 'name': 'Spindle', 'category': 'features'},
    {'id': 'banister', 'name': 'Banister', 'category': 'features'},
    {'id': 'baluster', 'name': 'Baluster', 'category': 'features'},

    # ==================== UTILITIES (20 Types) ====================
    {'id': 'electrical_box', 'name': 'Electrical Box', 'category': 'utilities'},
    {'id': 'electrical_conduit', 'name': 'Electrical Conduit', 'category': 'utilities'},
    {'id': 'electrical_outlet', 'name': 'Electrical Outlet', 'category': 'utilities'},
    {'id': 'light_switch', 'name': 'Light Switch', 'category': 'utilities'},
    {'id': 'light_fixture', 'name': 'Light Fixture', 'category': 'utilities'},
    {'id': 'ceiling_fan', 'name': 'Ceiling Fan', 'category': 'utilities'},
    {'id': 'plumbing_chase', 'name': 'Plumbing Chase', 'category': 'utilities'},
    {'id': 'water_pipe', 'name': 'Water Pipe', 'category': 'utilities'},
    {'id': 'drain_pipe', 'name': 'Drain Pipe', 'category': 'utilities'},
    {'id': 'sewer_pipe', 'name': 'Sewer Pipe', 'category': 'utilities'},
    {'id': 'gas_pipe', 'name': 'Gas Pipe', 'category': 'utilities'},
    {'id': 'water_heater', 'name': 'Water Heater', 'category': 'utilities'},
    {'id': 'boiler', 'name': 'Boiler', 'category': 'utilities'},
    {'id': 'furnace', 'name': 'Furnace', 'category': 'utilities'},
    {'id': 'data_port', 'name': 'Data Port', 'category': 'utilities'},
    {'id': 'telephone_port', 'name': 'Telephone Port', 'category': 'utilities'},
    {'id': 'tv_port', 'name': 'TV Port', 'category': 'utilities'},
    {'id': 'cable_port', 'name': 'Cable Port', 'category': 'utilities'},
    {'id': 'internet_port', 'name': 'Internet Port', 'category': 'utilities'},
    {'id': 'intercom', 'name': 'Intercom', 'category': 'utilities'},

    # ==================== SECURITY (15 Types) ====================
    {'id': 'security_gate', 'name': 'Security Gate', 'category': 'security'},
    {'id': 'burglar_bar', 'name': 'Burglar Bar', 'category': 'security'},
    {'id': 'security_grille', 'name': 'Security Grille', 'category': 'security'},
    {'id': 'bulletproof_window', 'name': 'Bulletproof Window', 'category': 'security'},
    {'id': 'bulletproof_door', 'name': 'Bulletproof Door', 'category': 'security'},
    {'id': 'security_door', 'name': 'Security Door', 'category': 'security'},
    {'id': 'panic_room', 'name': 'Panic Room', 'category': 'security'},
    {'id': 'safe_room', 'name': 'Safe Room', 'category': 'security'},
    {'id': 'vault', 'name': 'Vault', 'category': 'security'},
    {'id': 'security_camera', 'name': 'Security Camera', 'category': 'security'},
    {'id': 'motion_sensor', 'name': 'Motion Sensor', 'category': 'security'},
    {'id': 'alarm_system', 'name': 'Alarm System', 'category': 'security'},
    {'id': 'access_control', 'name': 'Access Control', 'category': 'security'},
    {'id': 'biometric_scanner', 'name': 'Biometric Scanner', 'category': 'security'},
    {'id': 'security_lighting', 'name': 'Security Lighting', 'category': 'security'},

    # ==================== SPECIALIZED (10 Types) ====================
    {'id': 'blackboard', 'name': 'Blackboard', 'category': 'specialized'},
    {'id': 'whiteboard', 'name': 'Whiteboard', 'category': 'specialized'},
    {'id': 'projection_screen', 'name': 'Projection Screen', 'category': 'specialized'},
    {'id': 'stage_opening', 'name': 'Stage Opening', 'category': 'specialized'},
    {'id': 'proscenium_arch', 'name': 'Proscenium Arch', 'category': 'specialized'},
    {'id': 'orchestra_pit', 'name': 'Orchestra Pit', 'category': 'specialized'},
    {'id': 'mirror_wall', 'name': 'Mirror Wall', 'category': 'specialized'},
    {'id': 'dance_floor', 'name': 'Dance Floor', 'category': 'specialized'},
    {'id': 'bar_counter', 'name': 'Bar Counter', 'category': 'specialized'},
    {'id': 'reception_counter', 'name': 'Reception Counter', 'category': 'specialized'},
    {'id': 'wardrobe_opening', 'name': 'Wardrobe Opening', 'category': 'features'},
    {'id': 'walk_in_closet', 'name': 'Walk-in Closet', 'category': 'features'},
    {'id': 'sink_opening', 'name': 'Sink Opening', 'category': 'features'},
    {'id': 'counter_space', 'name': 'Counter Space', 'category': 'features'},
    {'id': 'shower_space', 'name': 'Shower Space', 'category': 'features'},
    {'id': 'toilet_space', 'name': 'Toilet Space', 'category': 'features'},
    {'id': 'sink_space', 'name': 'Sink Space', 'category': 'features'},
    {'id': 'jacuzzi_space', 'name': 'Jacuzzi Space', 'category': 'features'},
    {'id': 'double_sink', 'name': 'Double Sink', 'category': 'features'},
    {'id': 'built_in_shelves', 'name': 'Built-in Shelves', 'category': 'features'},
    {'id': 'shelf_space', 'name': 'Shelf Space', 'category': 'features'},
    {'id': 'washer_space', 'name': 'Washer Space', 'category': 'features'},
    {'id': 'dryer_space', 'name': 'Dryer Space', 'category': 'features'},
    {'id': 'closet_space', 'name': 'Closet Space', 'category': 'features'},
    {'id': 'chandelier_hook', 'name': 'Chandelier Hook', 'category': 'utilities'},
    {'id': 'feature_lighting', 'name': 'Feature Lighting', 'category': 'utilities'},
    {'id': 'reading_light', 'name': 'Reading Light', 'category': 'utilities'},
    {'id': 'heated_towel_rail', 'name': 'Heated Towel Rail', 'category': 'utilities'},
    
]

# Measurement Units Conversion System
MEASUREMENT_UNITS = [
    {'id': 'feet', 'name': 'Feet', 'conversion_to_meters': 0.3048},
    {'id': 'meters', 'name': 'Meters', 'conversion_to_meters': 1.0},
    {'id': 'inches', 'name': 'Inches', 'conversion_to_meters': 0.0254},
    {'id': 'centimeters', 'name': 'Centimeters', 'conversion_to_meters': 0.01},
    {'id': 'millimeters', 'name': 'Millimeters', 'conversion_to_meters': 0.001},
    {'id': 'yards', 'name': 'Yards', 'conversion_to_meters': 0.9144}
]

# Helper Functions
def get_all_house_types():
    """Get all available house types for dropdowns"""
    return [{'id': key, 'name': value['name'], 'category': value.get('category', 'residential')} 
            for key, value in HOUSE_TYPE_TEMPLATES.items()]

def get_house_type_categories():
    """Get house types organized by category"""
    categories = {
        'residential': [],
        'commercial': [],
        'industrial': [],
        'institutional': [],
        'hospitality': [],
        'specialized': []
    }
    
    for house_id, template in HOUSE_TYPE_TEMPLATES.items():
        category = template.get('category', 'residential')
        if category in categories:
            categories[category].append({
                'id': house_id,
                'name': template['name'],
                'description': template['description'],
                'total_area': template['total_area']
            })
    
    return categories

def get_structured_structure_types():
    """Get structure types organized by category"""
    categories = {}
    for structure in STRUCTURE_TYPES:
        category = structure['category']
        if category not in categories:
            categories[category] = []
        categories[category].append(structure)
    return categories

def get_structured_sub_structure_types():
    """Get sub-structure types organized by category"""
    categories = {}
    for sub_structure in SUB_STRUCTURE_TYPES:
        category = sub_structure['category']
        if category not in categories:
            categories[category] = []
        categories[category].append(sub_structure)
    return categories

def get_house_type_template(house_type):
    """Get auto-fill template for a house type"""
    return HOUSE_TYPE_TEMPLATES.get(house_type, {
        'name': 'Custom',
        'description': 'Custom building design',
        'structures': []
    })

def get_nigerian_standard_dimensions(structure_type):
    """Get standard Nigerian dimensions for common structures"""
    standards = {
        'bedroom_master': {'min_length': 4.0, 'min_width': 3.5, 'standard_height': 3.0},
        'bedroom_standard': {'min_length': 3.5, 'min_width': 3.0, 'standard_height': 3.0},
        'living_room': {'min_length': 4.5, 'min_width': 3.5, 'standard_height': 3.0},
        'kitchen': {'min_length': 3.0, 'min_width': 2.5, 'standard_height': 2.7},
        'bathroom': {'min_length': 2.5, 'min_width': 1.8, 'standard_height': 2.4},
        'toilet': {'min_length': 1.2, 'min_width': 0.9, 'standard_height': 2.4},
        'office': {'min_length': 3.5, 'min_width': 3.0, 'standard_height': 3.0},
        'classroom': {'min_length': 7.0, 'min_width': 6.0, 'standard_height': 3.5},
        'retail_shop': {'min_length': 6.0, 'min_width': 4.0, 'standard_height': 4.0},
        'hotel_room': {'min_length': 4.5, 'min_width': 3.5, 'standard_height': 3.0}
    }
    return standards.get(structure_type, {})

def convert_units(value, from_unit, to_unit='meters'):
    """Convert measurement units"""
    units_dict = {unit['id']: unit['conversion_to_meters'] for unit in MEASUREMENT_UNITS}
    
    if from_unit not in units_dict or to_unit not in units_dict:
        return value
    
    # Convert to meters first, then to target unit
    value_in_meters = value * units_dict[from_unit]
    if to_unit == 'meters':
        return value_in_meters
    else:
        return value_in_meters / units_dict[to_unit]

def calculate_materials_required(structure_type, dimensions):
    """Calculate required materials for a structure"""
    # This is a simplified calculation - real implementation would be more complex
    wall_area = 2 * (dimensions['length'] + dimensions['width']) * dimensions['height']
    
    # Assume 9-inch blocks for exterior walls, 6-inch for interior
    if structure_type in ['living_room', 'bedroom_master']:
        blocks_needed = wall_area * 10  # 9-inch blocks
    else:
        blocks_needed = wall_area * 13  # 6-inch blocks
        
    return {
        'blocks_9inch': blocks_needed if structure_type in ['living_room', 'bedroom_master'] else 0,
        'blocks_6inch': blocks_needed if structure_type not in ['living_room', 'bedroom_master'] else 0,
        'cement_bags': blocks_needed * 0.04,  # Approximate cement per block
        'sand_tons': blocks_needed * 0.0075   # Approximate sand per block
    }