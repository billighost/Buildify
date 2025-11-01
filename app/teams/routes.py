# app/teams/routes.py

from flask import render_template, redirect, url_for, flash, request, jsonify, Blueprint
from flask_login import login_required, current_user
from app import db
from app.models import Team, TeamMember, Project, ProjectInvitation, ProjectCollaborator, User
from app.utils.notifications import NotificationManager
from datetime import datetime, timedelta

teams = Blueprint('teams', __name__)

@teams.route('/')
@login_required
def teams_dashboard():
    """Main teams dashboard"""
    user_teams = Team.query.join(TeamMember).filter(
        TeamMember.user_id == current_user.id
    ).all()
    
    pending_invitations = ProjectInvitation.query.filter_by(
        invitee_id=current_user.id,
        status='pending'
    ).all()
    # Add ownership/admin info
    team_roles = {
        team.id: TeamMember.query.filter(
            TeamMember.team_id == team.id,
            TeamMember.user_id == current_user.id,
            TeamMember.role.in_(['owner', 'admin'])
        ).first()
        for team in user_teams
    }
    
    return render_template('teams/dashboard.html',
                         title='Teams & Collaboration',
                         user_teams=user_teams,
                         pending_invitations=pending_invitations,
                         team_roles=team_roles)

# Add these new routes to teams/routes.py

@teams.route('/<int:team_id>/delete', methods=['POST'])
@login_required
def delete_team(team_id):
    """Delete a team and all its associations"""
    team = Team.query.get_or_404(team_id)
    
    # Check if user is team owner
    membership = TeamMember.query.filter_by(
        team_id=team_id,
        user_id=current_user.id,
        role='owner'
    ).first()
    
    if not membership:
        return jsonify({'success': False, 'error': 'Only team owner can delete the team'})
    
    try:
        team_name = team.name
        
        # Use the safe delete method
        if team.delete_team():
            # Send notifications to former team members
            former_members = User.query.join(TeamMember).filter(
                TeamMember.team_id == team_id
            ).all()
            
            for member in former_members:
                if member.id != current_user.id:
                    member.add_notification(
                        title="Team Deleted",
                        message=f"The team '{team_name}' has been deleted by {current_user.first_name}",
                        notification_type='warning',
                        action_url='/teams',
                        related_type='team'
                    )
            
            return jsonify({
                'success': True,
                'message': f'Team "{team_name}" has been deleted successfully'
            })
        else:
            return jsonify({'success': False, 'error': 'Failed to delete team'})
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@teams.route('/<int:team_id>/projects')
@login_required
def team_projects(team_id):
    """Get all projects for a team with detailed information"""
    team = Team.query.get_or_404(team_id)
    
    # Check if user is a member of the team
    membership = TeamMember.query.filter_by(
        team_id=team_id,
        user_id=current_user.id
    ).first()
    
    if not membership:
        return jsonify({'success': False, 'error': 'Access denied'})
    
    projects = Project.query.filter_by(team_id=team_id).all()
    
    project_data = []
    for project in projects:
        project_data.append({
            'id': project.id,
            'title': project.title,
            'house_type': project.house_type,
            'total_blocks': project.total_blocks,
            'total_area': project.total_area,
            'created_at': project.created_at.isoformat(),
            'updated_at': project.updated_at.isoformat(),
            'author': {
                'id': project.author.id,
                'name': f"{project.author.first_name} {project.author.last_name}",
                'username': project.author.username
            },
            'privacy': project.get_privacy_status(),
            'last_updated_by': project.get_last_updated_by().to_dict() if project.get_last_updated_by() else None
        })
    
    return jsonify({
        'success': True,
        'projects': project_data,
        'team': team.to_dict()
    })

@teams.route('/<int:team_id>/update', methods=['POST'])
@login_required
def update_team(team_id):
    """Update team information"""
    team = Team.query.get_or_404(team_id)
    
    # Check if user is team admin/owner
    membership = TeamMember.query.filter_by(
        team_id=team_id,
        user_id=current_user.id
    ).first()
    
    if not membership or membership.role not in ['owner', 'admin']:
        return jsonify({'success': False, 'error': 'Insufficient permissions'})
    
    data = request.get_json()
    
    try:
        if 'name' in data:
            team.name = data['name']
        if 'description' in data:
            team.description = data['description']
        
        team.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Team updated successfully',
            'team': team.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})
    
# Add these new routes to teams/routes.py

@teams.route('/<int:team_id>/settings', methods=['GET', 'POST'])
@login_required
def team_settings(team_id):
    """Team settings and management"""
    team = Team.query.get_or_404(team_id)
    user_teams = Team.query.join(TeamMember).filter(
        TeamMember.user_id == current_user.id
    ).all()
    
    # Check if user is team admin/owner
    membership = TeamMember.query.filter_by(
        team_id=team_id,
        user_id=current_user.id
    ).first()
    
    if not membership or membership.role not in ['owner', 'admin']:
        flash('You do not have permission to access team settings.', 'danger')
        return redirect(url_for('teams.team_detail', team_id=team_id))
    
    if request.method == 'POST':
        data = request.get_json()
        
        try:
            # Update basic team info
            if 'name' in data:
                team.name = data['name']
            if 'description' in data:
                team.description = data['description']
            
            # Update team settings
            if 'settings' in data:
                team.update_settings(data['settings'])
            
            team.updated_at = datetime.utcnow()
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Team settings updated successfully',
                'team': team.to_dict()
            })
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)})
    
    # Get team statistics for settings page
    members = TeamMember.query.filter_by(team_id=team_id).all()
    projects = Project.query.filter_by(team_id=team_id).all()
    
    team_stats = {
        'total_members': len(members),
        'total_projects': len(projects),
        'total_blocks': sum(project.total_blocks or 0 for project in projects),
        'active_members': len([m for m in members if m.user.last_login and (datetime.utcnow() - m.user.last_login).days < 30]),
        'project_types': {},
        'member_roles': {
            'owner': len([m for m in members if m.role == 'owner']),
            'admin': len([m for m in members if m.role == 'admin']),
            'member': len([m for m in members if m.role == 'member'])
        }
    }
    # Add ownership/admin info
    team_roles = {
        team.id: TeamMember.query.filter(
            TeamMember.team_id == team.id,
            TeamMember.user_id == current_user.id,
            TeamMember.role.in_(['owner', 'admin'])
        ).first()
        for team in user_teams
    }
    
    
    # Count projects by type
    for project in projects:
        project_type = project.house_type
        team_stats['project_types'][project_type] = team_stats['project_types'].get(project_type, 0) + 1
    
    return render_template('teams/team_settings.html',
                         title=f'Settings - {team.name}',
                         team=team,
                         members=members,
                         team_stats=team_stats,
                         team_roles=team_roles,
                         user_membership=membership)

@teams.route('/<int:team_id>/settings/members', methods=['POST'])
@login_required
def update_team_member_role(team_id):
    """Update team member role"""
    team = Team.query.get_or_404(team_id)
    
    # Check if user is team admin/owner
    membership = TeamMember.query.filter_by(
        team_id=team_id,
        user_id=current_user.id
    ).first()
    
    if not membership or membership.role not in ['owner', 'admin']:
        return jsonify({'success': False, 'error': 'Insufficient permissions'})
    
    data = request.get_json()
    member_id = data.get('member_id')
    new_role = data.get('role')
    
    if not member_id or not new_role:
        return jsonify({'success': False, 'error': 'Member ID and role are required'})
    
    # Find the member to update
    member_to_update = TeamMember.query.filter_by(
        team_id=team_id,
        id=member_id
    ).first()
    
    if not member_to_update:
        return jsonify({'success': False, 'error': 'Member not found'})
    
    # Prevent self-demotion if you're the only owner
    if member_to_update.user_id == current_user.id and member_to_update.role == 'owner':
        owner_count = TeamMember.query.filter_by(team_id=team_id, role='owner').count()
        if owner_count <= 1 and new_role != 'owner':
            return jsonify({'success': False, 'error': 'Cannot remove yourself as the only owner'})
    
    success, message = member_to_update.update_role(new_role, current_user.id)
    
    if success:
        return jsonify({
            'success': True,
            'message': message,
            'member': member_to_update.to_dict()
        })
    else:
        return jsonify({'success': False, 'error': message})

@teams.route('/<int:team_id>/stats/detailed')
@login_required
def get_detailed_team_stats(team_id):
    """Get detailed team statistics"""
    team = Team.query.get_or_404(team_id)
    
    # Check if user is a member of the team
    membership = TeamMember.query.filter_by(
        team_id=team_id,
        user_id=current_user.id
    ).first()
    
    if not membership:
        return jsonify({'success': False, 'error': 'Access denied'})
    
    # Get all team projects
    projects = Project.query.filter_by(team_id=team_id).all()
    
    # Calculate detailed statistics
    total_blocks = sum(project.total_blocks or 0 for project in projects)
    total_area = sum(project.total_area or 0 for project in projects)
    
    # Member contributions
    member_contributions = []
    members = TeamMember.query.filter_by(team_id=team_id).all()
    
    for member in members:
        user_projects = Project.query.filter_by(
            team_id=team_id,
            user_id=member.user_id
        ).all()
        
        user_blocks = sum(project.total_blocks or 0 for project in user_projects)
        user_area = sum(project.total_area or 0 for project in user_projects)
        
        contribution_percentage = (user_blocks / total_blocks * 100) if total_blocks > 0 else 0
        
        member_contributions.append({
            'user': member.user.to_dict(),
            'role': member.role,
            'projects_count': len(user_projects),
            'blocks_contributed': user_blocks,
            'area_contributed': user_area,
            'contribution_percentage': round(contribution_percentage, 1),
            'joined_at': member.joined_at.isoformat(),
            'last_active': member.user.last_login.isoformat() if member.user.last_login else None
        })
    
    # Project type distribution
    project_types = {}
    for project in projects:
        project_type = project.house_type
        if project_type not in project_types:
            project_types[project_type] = {
                'count': 0,
                'total_blocks': 0,
                'total_area': 0
            }
        
        project_types[project_type]['count'] += 1
        project_types[project_type]['total_blocks'] += project.total_blocks or 0
        project_types[project_type]['total_area'] += project.total_area or 0
    
    # Monthly activity
    monthly_activity = {}
    for project in projects:
        month_key = project.created_at.strftime('%Y-%m')
        if month_key not in monthly_activity:
            monthly_activity[month_key] = 0
        monthly_activity[month_key] += 1
    
    return jsonify({
        'success': True,
        'stats': {
            'total_projects': len(projects),
            'total_blocks': total_blocks,
            'total_area': total_area,
            'member_count': len(members),
            'average_blocks_per_project': total_blocks / len(projects) if projects else 0,
            'member_contributions': member_contributions,
            'project_types': project_types,
            'monthly_activity': monthly_activity,
            'team_created': team.created_at.isoformat(),
            'last_updated': team.updated_at.isoformat()
        }
    })

@teams.route('/create', methods=['POST'])
@login_required
def create_team():
    """Create a new team"""
    data = request.get_json()
    
    if not data or not data.get('name'):
        return jsonify({'success': False, 'error': 'Team name is required'})
    
    try:
        team = Team(
            name=data.get('name'),
            description=data.get('description'),
            created_by=current_user.id
        )
        
        db.session.add(team)
        db.session.flush()  # Get team ID without committing
        
        # Add creator as team owner
        owner_member = TeamMember(
            team_id=team.id,
            user_id=current_user.id,
            role='owner'
        )
        db.session.add(owner_member)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'team': team.to_dict(),
            'message': 'Team created successfully!'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@teams.route('/<int:team_id>/invite', methods=['POST'])
@login_required
def invite_to_team(team_id):
    """Invite users to a team"""
    team = Team.query.get_or_404(team_id)
    
    # Check if user is team admin/owner
    membership = TeamMember.query.filter_by(
        team_id=team_id,
        user_id=current_user.id
    ).first()
    
    if not membership or membership.role not in ['owner', 'admin']:
        return jsonify({'success': False, 'error': 'Insufficient permissions'})
    
    data = request.get_json()
    usernames = data.get('usernames', [])
    
    invited_users = []
    for username in usernames:
        user = User.query.filter_by(username=username).first()
        if user and user.id != current_user.id:
            # Check if user is already in team
            existing_member = TeamMember.query.filter_by(
                team_id=team_id,
                user_id=user.id
            ).first()
            
            if not existing_member:
                team_member = TeamMember(
                    team_id=team_id,
                    user_id=user.id,
                    role='member'
                )
                db.session.add(team_member)
                
                # Send notification
                user.add_notification(
                    title="Team Invitation",
                    message=f"You've been invited to join the team '{team.name}' by {current_user.first_name}",
                    notification_type='info',
                    action_url='/teams',
                    related_id=team_id,
                    related_type='team'
                )
                
                invited_users.append(user.username)
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'invited_users': invited_users,
        'message': f'Invited {len(invited_users)} users to the team'
    })

@teams.route('/projects/<int:project_id>/invite', methods=['POST'])
@login_required
def invite_to_project(project_id):
    """Invite users to collaborate on a project"""
    project = Project.query.get_or_404(project_id)
    
    # Check if user owns the project or is admin collaborator
    if project.author != current_user:
        collaborator = ProjectCollaborator.query.filter_by(
            project_id=project_id,
            user_id=current_user.id,
            role='collaborator'
        ).first()
        if not collaborator:
            return jsonify({'success': False, 'error': 'Insufficient permissions'})
    
    data = request.get_json()
    usernames = data.get('usernames', [])
    message = data.get('message', '')
    
    invited_users = []
    for username in usernames:
        user = User.query.filter_by(username=username).first()
        if user and user.id != current_user.id:
            # Check if invitation already exists
            existing_invitation = ProjectInvitation.query.filter_by(
                project_id=project_id,
                invitee_id=user.id,
                status='pending'
            ).first()
            
            if not existing_invitation:
                invitation = ProjectInvitation(
                    project_id=project_id,
                    inviter_id=current_user.id,
                    invitee_id=user.id,
                    message=message
                )
                db.session.add(invitation)
                
                # Send notification
                user.add_notification(
                    title="Project Collaboration Invitation",
                    message=f"{current_user.first_name} has invited you to collaborate on '{project.title}'",
                    notification_type='info',
                    action_url='/teams',
                    related_id=project_id,
                    related_type='project'
                )
                
                invited_users.append(user.username)
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'invited_users': invited_users,
        'message': f'Sent invitations to {len(invited_users)} users'
    })

@teams.route('/invitations/<int:invitation_id>/accept', methods=['POST'])
@login_required
def accept_invitation(invitation_id):
    """Accept a project invitation"""
    invitation = ProjectInvitation.query.filter_by(
        id=invitation_id,
        invitee_id=current_user.id,
        status='pending'
    ).first_or_404()
    
    try:
        invitation.accept()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Invitation accepted! You can now access the project.',
            'project_id': invitation.project_id
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@teams.route('/invitations/<int:invitation_id>/decline', methods=['POST'])
@login_required
def decline_invitation(invitation_id):
    """Decline a project invitation"""
    invitation = ProjectInvitation.query.filter_by(
        id=invitation_id,
        invitee_id=current_user.id,
        status='pending'
    ).first_or_404()
    
    try:
        invitation.decline()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Invitation declined'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@teams.route('/projects/<int:project_id>/collaborators')
@login_required
def get_project_collaborators(project_id):
    """Get project collaborators"""
    project = Project.query.get_or_404(project_id)
    
    if not project.can_view(current_user):
        return jsonify({'success': False, 'error': 'Access denied'})
    
    return jsonify({
        'success': True,
        'collaborators': project.get_collaborators()
    })

@teams.route('/projects/<int:project_id>/remove-collaborator/<int:user_id>', methods=['POST'])
@login_required
def remove_collaborator(project_id, user_id):
    """Remove collaborator from project"""
    project = Project.query.get_or_404(project_id)
    
    # Only project owner can remove collaborators
    if project.author != current_user:
        return jsonify({'success': False, 'error': 'Only project owner can remove collaborators'})
    
    collaborator = ProjectCollaborator.query.filter_by(
        project_id=project_id,
        user_id=user_id
    ).first()
    
    if collaborator:
        db.session.delete(collaborator)
        db.session.commit()
        
        # Send notification
        User.query.get(user_id).add_notification(
            title="Removed from Project",
            message=f"You've been removed from the project '{project.title}'",
            notification_type='warning',
            action_url='/projects/dashboard',
            related_type='project'
        )
    
    return jsonify({'success': True, 'message': 'Collaborator removed'})

@teams.route('/<int:team_id>/remove-member/<int:user_id>', methods=['POST'])
@login_required
def remove_team_member(team_id, user_id):
    """Remove member from team"""
    team = Team.query.get_or_404(team_id)
    
    # Check permissions
    membership = TeamMember.query.filter_by(
        team_id=team_id,
        user_id=current_user.id
    ).first()
    
    if not membership or membership.role not in ['owner', 'admin']:
        return jsonify({'success': False, 'error': 'Insufficient permissions'})
    
    # Cannot remove yourself if you're the only owner
    if user_id == current_user.id:
        owner_count = TeamMember.query.filter_by(
            team_id=team_id,
            role='owner'
        ).count()
        if owner_count <= 1:
            return jsonify({'success': False, 'error': 'Cannot remove the only team owner'})
    
    member = TeamMember.query.filter_by(
        team_id=team_id,
        user_id=user_id
    ).first()
    
    if member:
        db.session.delete(member)
        db.session.commit()
        
        # Send notification
        User.query.get(user_id).add_notification(
            title="Removed from Team",
            message=f"You've been removed from the team '{team.name}'",
            notification_type='warning',
            action_url='/teams',
            related_type='team'
        )
    
    return jsonify({'success': True, 'message': 'Team member removed'})

@teams.route('/<int:team_id>/stats')
@login_required
def get_team_stats(team_id):
    """Get team statistics and analytics"""
    team = Team.query.get_or_404(team_id)
    
    if not TeamMember.query.filter_by(team_id=team_id, user_id=current_user.id).first():
        return jsonify({'success': False, 'error': 'Access denied'})
    
    # Team statistics
    total_projects = team.projects.count()
    total_blocks = sum(project.total_blocks or 0 for project in team.projects.all())

    
    # Member activity
    members = TeamMember.query.filter_by(team_id=team_id).all()
    member_stats = []
    
    for member in members:
        user_projects = Project.query.filter_by(
            team_id=team_id,
            user_id=member.user_id
        ).count()
        
        member_stats.append({
            'user': member.user.to_dict(),
            'role': member.role,
            'project_count': user_projects,
            'joined_at': member.joined_at.isoformat()
        })
    
    # Project distribution by type
    from sqlalchemy import func
    project_types = db.session.query(
        Project.house_type,
        func.count(Project.id)
    ).filter_by(team_id=team_id).group_by(Project.house_type).all()
    
    return jsonify({
        'success': True,
        'stats': {
            'total_projects': total_projects,
            'total_blocks': total_blocks,
     
            'member_count': len(members),
            'project_types': [{'type': pt[0], 'count': pt[1]} for pt in project_types],
            'member_stats': member_stats
        }
    })

@teams.route('/users/search')
@login_required
def search_users():
    """Search users by username for invitations"""
    query = request.args.get('q', '')
    
    if len(query) < 2:
        return jsonify({'success': True, 'users': []})
    
    users = User.query.filter(
        User.username.ilike(f'%{query}%') |
        User.first_name.ilike(f'%{query}%') |
        User.last_name.ilike(f'%{query}%')
    ).filter(User.id != current_user.id).limit(10).all()
    
    return jsonify({
        'success': True,
        'users': [{
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        } for user in users]
    })
@teams.route('/<int:team_id>')
@login_required
def team_detail(team_id):
    """Team detail page with statistics and member management"""
    team = Team.query.get_or_404(team_id)
    user_teams = Team.query.join(TeamMember).filter(
        TeamMember.user_id == current_user.id
    ).all()
    
    # Check if user is a member of the team
    membership = TeamMember.query.filter_by(
        team_id=team_id,
        user_id=current_user.id
    ).first()
    
    if not membership:
        flash('You are not a member of this team.', 'danger')
        return redirect(url_for('teams.teams_dashboard'))
    
    # Get team members with their roles
    members = TeamMember.query.filter_by(team_id=team_id).all()
    
    # Get team projects
    projects = Project.query.filter_by(team_id=team_id).all()
    
    # Calculate team statistics
    total_projects = len(projects)
    total_blocks = sum(project.total_blocks or 0 for project in projects)

    
    # Project type distribution
    from collections import Counter
    project_types = Counter(project.house_type for project in projects)
    
    # Member activity (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    active_members = set()
    for project in projects:
        if project.updated_at >= thirty_days_ago:
            active_members.add(project.user_id)
            
    # Add ownership/admin info
    team_roles = {
        team.id: TeamMember.query.filter(
            TeamMember.team_id == team.id,
            TeamMember.user_id == current_user.id,
            TeamMember.role.in_(['owner', 'admin'])
        ).first()
        for team in user_teams
    }
    
    return render_template('teams/team_detail.html',
                         title=f'Team: {team.name}',
                         team=team,
                         members=members,
                         projects=projects,
                         total_projects=total_projects,
                         total_blocks=total_blocks,
                         team_roles=team_roles,
                         project_types=dict(project_types),
                         active_members_count=len(active_members),
                         user_membership=membership)