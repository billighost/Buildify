from flask_login import login_required, current_user
from datetime import datetime, timedelta
from app import db
from app.utils.structure_templates import get_house_type_template, STRUCTURE_TYPES, SUB_STRUCTURE_TYPES, MEASUREMENT_UNITS
from flask import render_template, redirect, url_for, flash, request, jsonify, Blueprint, send_file
import json
import csv
import io
from app.models import Project, ProjectShare, Team, TeamMember, ProjectCollaborator
from app.utils.reports import ReportGenerator, generate_comparison_report
from app.utils.reports import calculate_efficiency_score
from app.utils.calculator import BlockCalculator
from app.utils.notifications import NotificationManager
import base64
projects = Blueprint('projects', __name__)

# Update the dashboard route in projects/routes.py

@projects.route('/dashboard')
@login_required
def dashboard():
    # Get user's own projects
    user_projects = current_user.projects.order_by(Project.updated_at.desc()).all()
    
    # Get shared projects
    shared_projects = Project.query.join(ProjectCollaborator).filter(
        ProjectCollaborator.user_id == current_user.id
    ).order_by(Project.updated_at.desc()).all()
    
    
    
    # Get team projects
    team_projects = Project.query.join(Team).join(TeamMember).filter(
        TeamMember.user_id == current_user.id,
        Project.team_id.isnot(None)
    ).order_by(Project.updated_at.desc()).all()
    
    # Combine all projects (remove duplicates)
    all_projects = list({project.id: project for project in user_projects + shared_projects + team_projects}.values())
    all_projects.sort(key=lambda x: x.updated_at, reverse=True)
    
    # Calculate statistics
    total_blocks = sum(project.total_blocks or 0 for project in all_projects)

    house_types_count = len(set(project.house_type for project in all_projects))
    
    # Recent projects (last 30 days)
    one_month_ago = datetime.utcnow() - timedelta(days=30)
    recent_projects = sum(1 for project in all_projects if project.created_at >= one_month_ago)
 
    
    return render_template('projects/dashboard.html', 
                         title='Dashboard',
                         projects=all_projects,
                         total_blocks=total_blocks,
                     
                         house_types_count=house_types_count,
                         recent_projects=recent_projects,
                      )



@projects.route('/project/new', methods=['GET', 'POST'])
@login_required
def new_project():
    if request.method == 'POST':
        data = request.get_json()
        
        # Create new project
        project = Project(
            title=data.get('title', 'New Project'),
            house_type=data.get('house_type', 'custom'),
            structures_data=data.get('structures', {}),
            user_id=current_user.id,
            team_id=data.get('team_id')
        )
        
        # Set privacy settings
        privacy_level = data.get('privacy', 'private')
        project.set_privacy(privacy_level)
        
        # Calculate blocks immediately
        if data.get('structures', {}).get('structures'):
            project.calculate_blocks()
            
        
        
        db.session.add(project)
        db.session.commit()
        # Send project created notification - FIXED
        try:
            # Method 1: Using the NotificationManager if it exists
            from app.utils.notifications import NotificationManager
            NotificationManager.send_project_created_notification(current_user, project)
            print(f"DEBUG: Sent notification via NotificationManager for project: {project.title}")
        except Exception as e:
            # Method 2: Fallback to direct notification creation
            print(f"DEBUG: NotificationManager failed, using fallback: {e}")
            current_user.add_notification(
                title="Project Created Successfully!",
                message=f"Your project '{project.title}' has been created with {project.total_blocks} blocks calculated.",
                notification_type='success',
                action_url=url_for('projects.view_project', project_id=project.id),
                related_id=project.id,
                related_type='project'
            )
            db.session.commit()
            print(f"DEBUG: Created fallback notification for project: {project.title}")
        
        return jsonify({
            'success': True, 
            'project_id': project.id, 
            'total_blocks': project.total_blocks,
            'redirect_url': url_for('projects.view_project', project_id=project.id)
        })
    
    # Get team_id from query parameter if available
    team_id = request.args.get('team_id')
    
    # Load user preferences
    user_preferences = {
        'preferred_block_type': current_user.preferred_block_type,
        'preferred_waste_percentage': current_user.preferred_waste_percentage,
        'measurement_system': current_user.measurement_system
    }
    
    # Get house types and structure types
    from app.utils.structure_templates import (
        HOUSE_TYPE_TEMPLATES, STRUCTURE_TYPES, SUB_STRUCTURE_TYPES, MEASUREMENT_UNITS
    )
    
    # Create house types list with ALL templates
    house_types = [{'id': 'custom', 'name': 'Custom Design'}]
    for key, template in HOUSE_TYPE_TEMPLATES.items():
        house_types.append({
            'id': key,
            'name': template['name'],
            'category': template.get('category', 'residential'),
            'description': template.get('description', '')
        })
    
    structure_types = STRUCTURE_TYPES
    sub_structure_types = SUB_STRUCTURE_TYPES
    
    return render_template('projects/new_project.html', 
                         title='New Project',
                         house_types=house_types,
                         structure_types=structure_types,
                         sub_structure_types=sub_structure_types,
                         measurement_units=MEASUREMENT_UNITS,
                         team_id=team_id,
                         user_preferences=user_preferences)  # Add this line


@projects.route('/debug/templates')
@login_required
def debug_templates():
    """Debug endpoint to check template loading"""
    templates_info = {}
    
    for house_type in ['3_bedroom_bungalow', '4_bedroom_duplex', 'hotel_building']:
        template = get_house_type_template(house_type)
        templates_info[house_type] = {
            'name': template.get('name', 'Unknown'),
            'structure_count': len(template.get('structures', [])),
            'structures': template.get('structures', [])
        }
    
    return jsonify({
        'structure_types_count': len(STRUCTURE_TYPES),
        'sub_structure_types_count': len(SUB_STRUCTURE_TYPES),
        'templates': templates_info
    })

@projects.route('/project/<int:project_id>')
@login_required
def view_project(project_id):
    project = Project.query.get_or_404(project_id)
    
    # Check if user can view the project (owner, collaborator, or team member)
    if not project.can_view(current_user):
        flash('You do not have permission to view this project.', 'danger')
        return redirect(url_for('projects.dashboard'))
    
    # Recalculate if needed (in case calculation methods have updated)
    if not project.total_blocks and project.structures_data.get('structures'):
        project.calculate_blocks()
    
    # Get collaborators information
    collaborators = project.get_collaborators()
    
    return render_template('projects/view_project.html', 
                         title=project.title, 
                         project=project,
                         collaborators=collaborators,
                         can_edit=project.can_edit(current_user))



# Update the calculate_project route
@projects.route('/project/<int:project_id>/calculate', methods=['POST'])
@login_required
def calculate_project(project_id):
    """Calculate blocks without page reload - UPDATED without price"""
    project = Project.query.get_or_404(project_id)
    if project.author != current_user:
        return jsonify({'success': False, 'error': 'Permission denied'})
    
    data = request.get_json()
    
    # Update project data
    project.title = data.get('title', project.title)
    project.house_type = data.get('house_type', project.house_type)
    project.structures_data = data.get('structures', project.structures_data)
    project.updated_at = datetime.utcnow()
    
    # Calculate blocks
    total_blocks = project.calculate_blocks()
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'total_blocks': total_blocks  # REMOVE estimated_cost
    })


@projects.route('/project/<int:project_id>/update', methods=['POST'])
@login_required
def update_project(project_id):
    project = Project.query.get_or_404(project_id)
    if project.author != current_user:
        return jsonify({'success': False, 'error': 'Permission denied'})
    
    data = request.get_json()
    project.title = data.get('title', project.title)
    project.structures_data = data.get('structures', project.structures_data)
    project.updated_at = datetime.utcnow()
    
    db.session.commit()
    return jsonify({'success': True})

@projects.route('/project/<int:project_id>/delete', methods=['POST'])
@login_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    if project.author != current_user:
        flash('You do not have permission to delete this project.', 'danger')
        return redirect(url_for('projects.dashboard'))
    
    project_title = project.title
    
    # Use safe delete method
    if project.safe_delete():
        # Send project deleted notification
        NotificationManager.send_project_deleted_notification(current_user, project_title)
        flash('Project has been deleted.', 'success')
    else:
        flash('An error occurred while deleting the project.', 'danger')
    
    return redirect(url_for('projects.dashboard'))

# @projects.route('/project/<int:project_id>/settings', methods=['GET', 'POST'])
# @login_required
# def project_settings(project_id):
#     """Project settings and management"""
#     project = Project.query.get_or_404(project_id)
    
#     # Check if user can edit the project
#     if not project.can_edit(current_user):
#         flash('You do not have permission to edit this project.', 'danger')
#         return redirect(url_for('projects.view_project', project_id=project_id))
    
#     if request.method == 'POST':
#         data = request.get_json()
        
#         # Update project data
#         project.title = data.get('title', project.title)
#         project.description = data.get('description', project.description)
#         project.house_type = data.get('house_type', project.house_type)
#         project.updated_at = datetime.utcnow()
        
#         # Update privacy settings
#         privacy_level = data.get('privacy', 'private')
#         project.set_privacy(privacy_level)
        
#         db.session.commit()
        
#         return jsonify({
#             'success': True,
#             'message': 'Project settings updated successfully'
#         })
    
#     # Get project statistics
#     collaborators = project.get_collaborators()
#     contribution_stats = project.get_contribution_stats()
    
#     return render_template('projects/project_settings.html',
#                          title=f'Settings - {project.title}',
#                          project=project,
#                          collaborators=collaborators,
#                          contribution_stats=contribution_stats)

@projects.route('/projects/bulk/delete', methods=['POST'])
@login_required
def bulk_delete_projects():
    """Delete multiple projects at once"""
    data = request.get_json()
    project_ids = data.get('project_ids', [])
    
    if not project_ids:
        return jsonify({'success': False, 'error': 'No projects selected'})
    
    try:
        # Get projects that belong to current user
        projects_to_delete = Project.query.filter(
            Project.id.in_(project_ids),
            Project.user_id == current_user.id
        ).all()
        
        deleted_count = 0
        for project in projects_to_delete:
            db.session.delete(project)
            deleted_count += 1
        
        db.session.commit()
        
        # Send bulk delete notification
        if deleted_count > 0:
            NotificationManager.send_bulk_delete_notification(current_user, deleted_count)
        
        flash(f'Successfully deleted {deleted_count} projects.', 'success')
        return jsonify({
            'success': True,
            'deleted_count': deleted_count,
            'message': f'Deleted {deleted_count} projects'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})
    
# Add new routes
@projects.route('/project/<int:project_id>/report/pdf')
@login_required
def generate_pdf_report(project_id):
    """Generate PDF report for project"""
    project = Project.query.get_or_404(project_id)
    if project.author != current_user:
        flash('Permission denied.', 'danger')
        return redirect(url_for('projects.dashboard'))
    
    try:
        report_generator = ReportGenerator(project)
        pdf_data = report_generator.generate_pdf_report()
        
        response = send_file(
            io.BytesIO(pdf_data),
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'{project.title}-report-{datetime.utcnow().strftime("%Y%m%d")}.pdf'
        )
        
        return response
        
    except Exception as e:
        flash(f'Error generating PDF report: {str(e)}', 'danger')
        return redirect(url_for('projects.view_project', project_id=project_id))

@projects.route('/project/<int:project_id>/report/materials')
@login_required
def generate_materials_report(project_id):
    """Generate materials list report"""
    project = Project.query.get_or_404(project_id)
    if project.author != current_user:
        return jsonify({'success': False, 'error': 'Permission denied'})
    
    report_generator = ReportGenerator(project)
    materials = report_generator.generate_materials_list()
    
    
    return jsonify({
        'success': True,
        'materials': materials
    
    })



@projects.route('/projects/comparison')
@login_required
def projects_comparison():
    """Compare multiple projects"""
    try:
        # Get user's own projects
        user_projects = current_user.projects.order_by(Project.updated_at.desc()).all()
        
        # Get shared projects
        shared_projects = Project.query.join(ProjectCollaborator).filter(
            ProjectCollaborator.user_id == current_user.id
        ).order_by(Project.updated_at.desc()).all()
        
        # Get team projects
        team_projects = Project.query.join(Team).join(TeamMember).filter(
            TeamMember.user_id == current_user.id,
            Project.team_id.isnot(None)
        ).order_by(Project.updated_at.desc()).all()
        
        # Combine all projects (remove duplicates)
        all_projects = list({project.id: project for project in user_projects + shared_projects + team_projects}.values())
        all_projects.sort(key=lambda x: x.updated_at, reverse=True)
        
        print(f"DEBUG: Found {len(all_projects)} projects for comparison")  # Debug
        
        if len(all_projects) < 2:
            if len(all_projects) == 1:
                flash('You need at least 2 projects to use the comparison feature. Create another project to compare.', 'info')
            else:
                flash('No projects available for comparison.', 'info')
            return redirect(url_for('projects.dashboard'))
        
        comparison_data = generate_comparison_report(all_projects)
        
        return render_template('projects/comparison.html',
                             title='Project Comparison',
                             comparison_data=comparison_data,
                             projects=all_projects)
    
    except Exception as e:
        print(f"Error in projects_comparison: {str(e)}")  # Debug
        import traceback
        traceback.print_exc()
        flash('An error occurred while generating the comparison.', 'error')
        return redirect(url_for('projects.dashboard'))
@projects.route('/project/<int:project_id>/privacy', methods=['POST'])
@login_required
def change_project_privacy(project_id):
    """Change project privacy settings"""
    project = Project.query.get_or_404(project_id)
    
    # Only project owner can change privacy
    if project.author != current_user:
        return jsonify({'success': False, 'error': 'Only project owner can change privacy settings'})
    
    data = request.get_json()
    privacy_level = data.get('privacy', 'private')
    
    project.set_privacy(privacy_level)
    
    return jsonify({
        'success': True,
        'message': f'Project privacy updated to {privacy_level}',
        'privacy_status': project.get_privacy_status()
    })
    
@projects.route('/project/<int:project_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    """Edit an existing project"""
    project = Project.query.get_or_404(project_id)
    
    # Check if user can edit the project
    if not project.can_edit(current_user):
        flash('You do not have permission to edit this project.', 'danger')
        return redirect(url_for('projects.dashboard'))
    
    if request.method == 'POST':
        data = request.get_json()
        
         # Update project data
        project.title = data.get('title', project.title)
        project.description = data.get('description', project.description)
        project.house_type = data.get('house_type', project.house_type)
        project.structures_data = data.get('structures', project.structures_data)
        project.updated_at = datetime.utcnow()
        
        # Update privacy settings
        privacy_level = data.get('privacy', 'private')
        project.set_privacy(privacy_level)
        
        # Recalculate blocks
        if data.get('structures', {}).get('structures'):
            project.calculate_blocks()
        
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'project_id': project.id, 
            'total_blocks': project.total_blocks,
            'redirect_url': url_for('projects.view_project', project_id=project.id)
        })
    
    # **FIX: Get ALL house types for edit page too**
    from app.utils.structure_templates import (
        HOUSE_TYPE_TEMPLATES, STRUCTURE_TYPES, SUB_STRUCTURE_TYPES, MEASUREMENT_UNITS
    )
    
    # Create house types list with ALL templates
    house_types = [{'id': 'custom', 'name': 'Custom Design'}]
    for key, template in HOUSE_TYPE_TEMPLATES.items():
        house_types.append({
            'id': key,
            'name': template['name'],
            'category': template.get('category', 'residential'),
            'description': template.get('description', '')
        })
    
    structure_types = STRUCTURE_TYPES
    sub_structure_types = SUB_STRUCTURE_TYPES
    
    return render_template('projects/edit_project.html', 
                         title=f'Edit {project.title}',
                         project=project,
                         house_types=house_types,
                         structure_types=structure_types,
                         sub_structure_types=sub_structure_types,
                         measurement_units=MEASUREMENT_UNITS)

    
@projects.route('/api/project/<int:project_id>/efficiency')
@login_required
def get_project_efficiency(project_id):
    """Get project efficiency metrics"""
    project = Project.query.get_or_404(project_id)
    if project.author != current_user:
        return jsonify({'success': False, 'error': 'Permission denied'})
    
    calculator = BlockCalculator(project.structures_data)
    calculation = calculator.calculate()
    
    efficiency_score = calculate_efficiency_score(calculation)
    
    return jsonify({
        'success': True,
        'efficiency_score': efficiency_score,
     
        'blocks_per_area': calculation['total_blocks'] / calculation['total_area'],
        'waste_percentage': calculation['waste_percentage']
    })

@projects.route('/projects/bulk/duplicate', methods=['POST'])
@login_required
def bulk_duplicate_projects():
    """Duplicate multiple projects at once"""
    data = request.get_json()
    project_ids = data.get('project_ids', [])
    
    if not project_ids:
        return jsonify({'success': False, 'error': 'No projects selected'})
    
    try:
        # Get projects that belong to current user
        projects_to_duplicate = Project.query.filter(
            Project.id.in_(project_ids),
            Project.user_id == current_user.id
        ).all()
        
        duplicated_count = 0
        new_project_ids = []
        
        for project in projects_to_duplicate:
            new_project = Project(
                title=f"{project.title} (Copy)",
                description=project.description,
                house_type=project.house_type,
                structures_data=project.structures_data.copy(),
                user_id=current_user.id
            )
            
            # Recalculate for the new project
            if new_project.structures_data.get('structures'):
                new_project.calculate_blocks()
            
            db.session.add(new_project)
            duplicated_count += 1
            new_project_ids.append(new_project.id)
        
        db.session.commit()
        
        flash(f'Successfully duplicated {duplicated_count} projects.', 'success')
        return jsonify({
            'success': True,
            'duplicated_count': duplicated_count,
            'new_project_ids': new_project_ids,
            'message': f'Duplicated {duplicated_count} projects'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@projects.route('/projects/bulk/export', methods=['POST'])
@login_required
def bulk_export_projects():
    """Export multiple projects as ZIP"""
    data = request.get_json()
    project_ids = data.get('project_ids', [])
    
    if not project_ids:
        return jsonify({'success': False, 'error': 'No projects selected'})
    
    try:
        import zipfile
        import io
        
        # Get projects that belong to current user
        projects_to_export = Project.query.filter(
            Project.id.in_(project_ids),
            Project.user_id == current_user.id
        ).all()
        
        if not projects_to_export:
            return jsonify({'success': False, 'error': 'No projects found'})
        
        # Create ZIP file in memory
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            for project in projects_to_export:
                # Add JSON file for each project
                project_data = json.dumps(project.to_dict(), indent=2)
                zip_file.writestr(f"{project.title}.json", project_data)
                
                # Add CSV summary
                csv_output = io.StringIO()
                csv_writer = csv.writer(csv_output)
                
                # Write CSV header
                csv_writer.writerow(['Project:', project.title])
                csv_writer.writerow(['House Type:', project.house_type])
                csv_writer.writerow(['Total Blocks:', project.total_blocks])
            
                csv_writer.writerow(['Total Area:', f"{project.total_area:.2f} m²"])
                csv_writer.writerow([])
                csv_writer.writerow(['Structures'])
                csv_writer.writerow(['Name', 'Type', 'Length', 'Width', 'Height', 'Unit'])
                
                for structure in project.structures_data.get('structures', []):
                    csv_writer.writerow([
                        structure.get('name', ''),
                        structure.get('type', ''),
                        structure.get('length', ''),
                        structure.get('width', ''),
                        structure.get('height', ''),
                        structure.get('unit', '')
                    ])
                
                zip_file.writestr(f"{project.title}.csv", csv_output.getvalue())
        
        zip_buffer.seek(0)
        
        response = send_file(
            zip_buffer,
            mimetype='application/zip',
            as_attachment=True,
            download_name=f'buildify-projects-export-{datetime.utcnow().strftime("%Y%m%d")}.zip'
        )
        
        return response
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    
@projects.route('/api/house-type-template/<house_type>')
@login_required
def get_house_type_template_api(house_type):
    """API endpoint to get auto-fill template"""
    try:
        template = get_house_type_template(house_type)
        print(f"DEBUG: Loading template for {house_type}: {template}")  # Debug
        return jsonify(template)
    except Exception as e:
        print(f"DEBUG: Error loading template: {e}")  # Debug
        return jsonify({'error': str(e)}), 500

# Update the calculate_preview route
@projects.route('/api/calculate-preview', methods=['POST'])
@login_required
def calculate_preview():
    """Calculate blocks for preview without saving - UPDATED without price"""
    data = request.get_json()
    structures_data = data.get('structures', {})
    
    print(f"DEBUG: Starting calculation with structures: {structures_data}")
    
    from app.utils.calculator import BlockCalculator
    calculator = BlockCalculator(structures_data)
    result = calculator.calculate()
    
    print(f"DEBUG: Calculation result: {result}")
    
    return jsonify({
        'success': True,
        'total_blocks': result['total_blocks'],
        'total_area': result['total_area'],
        'cement_bags': result.get('cement_bags', 0),
        'sand_trucks': result.get('sand_trucks', 0)
    })
# Add API endpoint for structured data
@projects.route('/api/structure-categories')
@login_required
def get_structure_categories():
    """Get all structure types organized by category"""
    from app.utils.structure_templates import (
        get_structured_structure_types, 
        get_structured_sub_structure_types
    )
    
    return jsonify({
        'success': True,
        'structure_categories': get_structured_structure_types(),
        'sub_structure_categories': get_structured_sub_structure_types()
    })
    
@projects.route('/project/<int:project_id>/share', methods=['POST'])
@login_required
def share_project(project_id):
    """Make project publicly shareable"""
    project = Project.query.get_or_404(project_id)
    if project.author != current_user:
        return jsonify({'success': False, 'error': 'Permission denied'})
    
    project.is_public = True
    share_url = project.get_share_url()
    
    db.session.commit()
    
    return jsonify({
        'success': True, 
        'share_url': share_url,
        'message': 'Project is now publicly shareable'
    })

@projects.route('/project/<int:project_id>/unshare', methods=['POST'])
@login_required
def unshare_project(project_id):
    """Make project private"""
    project = Project.query.get_or_404(project_id)
    if project.author != current_user:
        return jsonify({'success': False, 'error': 'Permission denied'})
    
    project.is_public = False
    db.session.commit()
    
    return jsonify({
        'success': True, 
        'message': 'Project is now private'
    })

@projects.route('/project/shared/<token>')
def shared_project(token):
    """View a shared project without login"""
    project = Project.query.filter_by(share_token=token, is_public=True).first_or_404()
    
    return render_template('projects/shared_project.html', 
                         title=f"Shared: {project.title}",
                         project=project)

@projects.route('/project/<int:project_id>/export/json')
@login_required
def export_project_json(project_id):
    """Export project as JSON"""
    project = Project.query.get_or_404(project_id)
    if project.author != current_user:
        flash('Permission denied.', 'danger')
        return redirect(url_for('projects.dashboard'))
    
    project_data = project.to_dict()
    
    # Create JSON response
    response = jsonify(project_data)
    response.headers['Content-Type'] = 'application/json'
    response.headers['Content-Disposition'] = f'attachment; filename={project.title}.json'
    
    return response


@projects.route('/project/<int:project_id>/export/csv')
@login_required
def export_project_csv(project_id):
    """Export project as CSV"""
    project = Project.query.get_or_404(project_id)
    if project.author != current_user:
        flash('Permission denied.', 'danger')
        return redirect(url_for('projects.dashboard'))
    
    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['Project:', project.title])
    writer.writerow(['House Type:', project.house_type])
    writer.writerow(['Total Blocks:', project.total_blocks])

    writer.writerow(['Total Area:', f"{project.total_area:.2f} m²"])
    writer.writerow([])
    
    # Write structures
    writer.writerow(['Structures'])
    writer.writerow(['Name', 'Type', 'Length', 'Width', 'Height', 'Unit'])
    
    for structure in project.structures_data.get('structures', []):
        writer.writerow([
            structure.get('name', ''),
            structure.get('type', ''),
            structure.get('length', ''),
            structure.get('width', ''),
            structure.get('height', ''),
            structure.get('unit', '')
        ])
    
    # Convert to bytes for response
    output.seek(0)
    response = send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'{project.title}.csv'
    )
    
    return response

@projects.route('/project/<int:project_id>/duplicate', methods=['POST'])
@login_required
def duplicate_project(project_id):
    """Duplicate an existing project"""
    original_project = Project.query.get_or_404(project_id)
    if original_project.author != current_user:
        return jsonify({'success': False, 'error': 'Permission denied'})
    
    # Create new project with copied data
    new_project = Project(
        title=f"{original_project.title} (Copy)",
        description=original_project.description,
        house_type=original_project.house_type,
        structures_data=original_project.structures_data.copy(),
        user_id=current_user.id
    )
    
    # Recalculate for the new project
    if new_project.structures_data.get('structures'):
        new_project.calculate_blocks()
    
    db.session.add(new_project)
    db.session.commit()
    
    flash('Project duplicated successfully!', 'success')
    return jsonify({
        'success': True,
        'project_id': new_project.id,
        'redirect_url': url_for('projects.view_project', project_id=new_project.id)
    })