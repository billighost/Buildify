import json
import io
from datetime import datetime, timedelta  # Add timedelta
from flask import render_template
from weasyprint import HTML
from app.utils.calculator import BlockCalculator

class ReportGenerator:
    def __init__(self, project):
        self.project = project
        self.calculator = BlockCalculator(project.structures_data)
    
    def generate_pdf_report(self):
        """Generate a comprehensive PDF report"""
        # Calculate detailed breakdown
        calculation_result = self.calculator.calculate()
        
        # Generate HTML content
        html_content = render_template(
            'reports/project_report.html',
            project=self.project,
            calculation=calculation_result,
            generated_date=datetime.utcnow().strftime('%B %d, %Y at %H:%M'),
            company_info=self.get_company_info()
        )
        
        # Generate PDF
        pdf_file = HTML(string=html_content).write_pdf()
        
        return pdf_file
    
    def generate_materials_list(self):
        """Generate detailed materials list"""
        calculation = self.calculator.calculate()
        
        materials = {
            'blocks': {
                'type': self.project.structures_data.get('block_type', '9_inch_hollow'),
                'quantity': calculation['total_blocks'],
                'waste_allowance': calculation['waste_percentage'],
             
            },
            'cement': {
                'quantity': calculation['cement_bags'],
                'purpose': 'Block laying and plastering'
            },
            'sand': {
                'quantity': calculation['sand_trucks'],

                'purpose': 'Mortar and plaster'
            },
            'additional_materials': self.get_additional_materials(calculation)
        }
        
        return materials
    
    def get_additional_materials(self, calculation):
        """Calculate additional construction materials"""
        return [
            {
                'name': 'Binding Wire',
                'quantity': f"{calculation['total_blocks'] / 100:.1f} rolls",
                'purpose': 'Block reinforcement'
            },
            {
                'name': 'Water',
                'quantity': f"{calculation['cement_bags'] * 50} liters",
                'purpose': 'Mixing and curing'
            },
            {
                'name': 'Labor',
                'quantity': f"{calculation['total_blocks'] / 80:.1f} person-days",
                'purpose': 'Block laying'
            }
        ]
    
    def get_company_info(self):
        """Get company information for reports"""
        return {
            'name': 'Buildify Nigeria',
            'slogan': 'Build Smarter One Block at a Time',
            'contact': 'support@buildify.ng',
            'website': 'www.buildify.ng',
            'address': 'Lagos, Nigeria'
        }
    
def generate_comparison_report(projects):
    """Generate comprehensive comparison report for multiple projects"""
    try:
        if not projects:
            return None
        
        comparison_data = {
            'projects': [],
            'total_blocks': 0,
            'total_area': 0,
            'house_types_count': 0,
            'average_age': 0,
            'average_efficiency': 0,
            'average_blocks_per_area': 0,
            'most_efficient': None,
            'largest_project': None,
            'recently_updated': None,
            'best_value': None,
            'fastest_build': {'days': 0},
            'slowest_build': {'days': 0},
            'improvement_areas': [],
            'potential_savings': {'blocks': 0, 'percentage': 0}
        }
        
        house_types = set()
        total_efficiency = 0
        total_blocks_per_area = 0
        now = datetime.utcnow()
        
        for project in projects:
            # Ensure project has calculated values
            if not project.total_blocks and project.structures_data.get('structures'):
                project.calculate_blocks()
            
            calculator = BlockCalculator(project.structures_data)
            calculation = calculator.calculate()
            
            # Calculate project metrics
            efficiency_score = calculate_efficiency_score(calculation)
            space_utilization = min(100, (calculation.get('total_area', 0) / max(1, len(project.structures_data.get('structures', []))) * 10))
            material_utilization = max(0, 100 - calculation.get('waste_percentage', 10))
            complexity_score = min(10, len(project.structures_data.get('structures', [])) * 0.5 + 
                                  sum(len(s.get('sub_structures', [])) for s in project.structures_data.get('structures', [])) * 0.2)
            
            # Calculate project age in days
            project_age = (now - project.created_at).days
            
            # Prepare project data for comparison
            project_data = {
                'id': project.id,
                'title': project.title,
                'house_type': project.house_type,
                'total_blocks': project.total_blocks or 0,
                'total_area': project.total_area or 0,
                'structures_data': project.structures_data,
                'created_at': project.created_at,
                'updated_at': project.updated_at,
                'is_public': project.is_public,
                'is_private': project.is_private,
                'team_id': project.team_id,
                'efficiency_score': efficiency_score,
                'space_utilization': space_utilization,
                'material_utilization': material_utilization,
                'complexity_score': complexity_score,
                'project_age': project_age
            }
            
            comparison_data['projects'].append(project_data)
            
            # Update aggregate data
            comparison_data['total_blocks'] += project.total_blocks or 0
            comparison_data['total_area'] += project.total_area or 0
            house_types.add(project.house_type)
            total_efficiency += efficiency_score
            if project.total_area and project.total_area > 0:
                total_blocks_per_area += (project.total_blocks or 0) / project.total_area
            
            # Update best/worst metrics
            if not comparison_data['most_efficient'] or efficiency_score > comparison_data['most_efficient']['efficiency_score']:
                comparison_data['most_efficient'] = project_data
            
            if not comparison_data['largest_project'] or (project.total_blocks or 0) > comparison_data['largest_project']['total_blocks']:
                comparison_data['largest_project'] = project_data
            
            if not comparison_data['recently_updated'] or project.updated_at > comparison_data['recently_updated']['updated_at']:
                comparison_data['recently_updated'] = project_data
        
        # Calculate averages
        num_projects = len(comparison_data['projects'])
        if num_projects > 0:
            comparison_data['house_types_count'] = len(house_types)
            comparison_data['average_age'] = sum(p['project_age'] for p in comparison_data['projects']) // num_projects
            comparison_data['average_efficiency'] = total_efficiency / num_projects
            comparison_data['average_blocks_per_area'] = total_blocks_per_area / num_projects if total_blocks_per_area > 0 else 0
            
            # Determine best value (balance of efficiency and cost)
            if comparison_data['projects']:
                comparison_data['best_value'] = max(comparison_data['projects'], 
                                               key=lambda p: p['efficiency_score'] * 0.7 + (100 - p['complexity_score'] * 10) * 0.3)
            
            # Calculate build timelines
            if comparison_data['projects']:
                fastest = min(comparison_data['projects'], key=lambda p: p['total_blocks'])
                slowest = max(comparison_data['projects'], key=lambda p: p['total_blocks'])
                comparison_data['fastest_build'] = {'project': fastest, 'days': max(7, fastest['total_blocks'] // 100)}
                comparison_data['slowest_build'] = {'project': slowest, 'days': max(14, slowest['total_blocks'] // 80)}
            
            # Generate improvement areas
            if comparison_data['projects']:
                least_efficient = min(comparison_data['projects'], key=lambda p: p['efficiency_score'])
                comparison_data['improvement_areas'] = [
                    f"Optimize waste percentage in '{least_efficient['title']}' (currently {least_efficient['structures_data'].get('waste_percentage', 10)}%)",
                    f"Consider 6-inch blocks for non-load bearing walls in larger projects",
                    f"Review opening sizes in '{least_efficient['title']}' to reduce block usage"
                ]
            
            # Calculate potential savings
            if num_projects >= 2:
                max_blocks = max(p['total_blocks'] for p in comparison_data['projects'])
                min_blocks = min(p['total_blocks'] for p in comparison_data['projects'])
                comparison_data['potential_savings']['blocks'] = max_blocks - min_blocks
                comparison_data['potential_savings']['percentage'] = round(((max_blocks - min_blocks) / max_blocks) * 100, 1) if max_blocks > 0 else 0
        
        return comparison_data
    
    except Exception as e:
        print(f"Error in generate_comparison_report: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def calculate_efficiency_score(calculation):
    """Calculate building efficiency score (0-100) safely"""
    total_blocks = calculation.get('total_blocks', 0)
    total_area = calculation.get('total_area', 0)
    waste_percentage = calculation.get('waste_percentage', 0)

    # Waste score (penalizes higher waste)
    waste_score = max(0, 100 - (waste_percentage * 5))

    # Avoid division by zero
    if total_blocks <= 0:
        area_score = 0
    else:
        area_score = min(100, (total_area / total_blocks) * 1000)

    # Combine scores (weight can be adjusted)
    efficiency_score = (waste_score + area_score) / 2  # changed to /2 since only 2 metrics now
    
    return round(efficiency_score, 2)
