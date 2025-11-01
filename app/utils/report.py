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
    """Generate comparison report for multiple projects"""
    comparison_data = []
    
    for project in projects:
        calculator = BlockCalculator(project.structures_data)
        calculation = calculator.calculate()
        
        comparison_data.append({
            'project': project,
            'calculation': calculation,
     
            'efficiency_score': calculate_efficiency_score(calculation)
        })
    
    # Sort by efficiency (cost per block)

    
    return comparison_data

def calculate_efficiency_score(calculation):
    """Calculate building efficiency score (0-100)"""
    # Factors: waste percentage, cost efficiency, material usage
    waste_score = max(0, 100 - (calculation['waste_percentage'] * 5))
   
    area_score = min(100, (calculation['total_area'] / calculation['total_blocks']) * 1000)
    
    return (waste_score + area_score) / 3