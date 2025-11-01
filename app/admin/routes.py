from flask import render_template, redirect, url_for, flash, request, jsonify, Blueprint
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from sqlalchemy import func, desc
import json

from app import db
from app.models import User, Project, ProjectTemplate, ProjectShare
from app.decorators import admin_required

admin = Blueprint('admin', __name__)

@admin.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    """Admin dashboard with comprehensive statistics"""
    # Basic statistics
    total_users = User.query.count()
    total_projects = Project.query.count()
    total_templates = ProjectTemplate.query.count()
    active_users = User.query.filter_by(is_active=True).count()
    admin_users = User.query.filter_by(is_admin=True).count()
    
    # Growth statistics (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    
    new_users_30d = User.query.filter(User.created_at >= thirty_days_ago).count()
    new_projects_30d = Project.query.filter(Project.created_at >= thirty_days_ago).count()
    new_users_7d = User.query.filter(User.created_at >= seven_days_ago).count()
    new_projects_7d = Project.query.filter(Project.created_at >= seven_days_ago).count()
    
    # Recent activity
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    recent_projects = Project.query.order_by(Project.created_at.desc()).limit(5).all()
    
    # Popular house types
    popular_house_types = db.session.query(
        Project.house_type,
        func.count(Project.id).label('count')
    ).group_by(Project.house_type).order_by(func.count(Project.id).desc()).limit(10).all()
    
    # User location distribution
    user_locations = db.session.query(
        User.location,
        func.count(User.id).label('count')
    ).filter(User.location.isnot(None)).group_by(User.location).order_by(func.count(User.id).desc()).limit(10).all()
    
    # System statistics
    total_blocks_calculated = db.session.query(func.sum(Project.total_blocks)).scalar() or 0
 
    
    # Active users in last 7 days
    active_users_7d = User.query.filter(User.last_login >= seven_days_ago).count()
    
    return render_template('admin/dashboard.html',
                         title='Admin Dashboard',
                         total_users=total_users,
                         total_projects=total_projects,
                         total_templates=total_templates,
                         active_users=active_users,
                         admin_users=admin_users,
                         new_users_30d=new_users_30d,
                         new_projects_30d=new_projects_30d,
                         new_users_7d=new_users_7d,
                         new_projects_7d=new_projects_7d,
                         recent_users=recent_users,
                         recent_projects=recent_projects,
                         popular_house_types=popular_house_types,
                         user_locations=user_locations,
                         total_blocks_calculated=total_blocks_calculated,
                         active_users_7d=active_users_7d)

@admin.route('/admin/users')
@login_required
@admin_required
def admin_users():
    """User management with filtering and search"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    # Filter parameters
    status_filter = request.args.get('status', 'all')
    role_filter = request.args.get('role', 'all')
    search_query = request.args.get('search', '')
    
    # Base query
    query = User.query
    
    # Apply filters
    if status_filter == 'active':
        query = query.filter_by(is_active=True)
    elif status_filter == 'inactive':
        query = query.filter_by(is_active=False)
    elif status_filter == 'unverified':
        query = query.filter_by(is_verified=False)
    
    if role_filter == 'admin':
        query = query.filter_by(is_admin=True)
    elif role_filter == 'user':
        query = query.filter_by(is_admin=False)
    
    if search_query:
        query = query.filter(
            (User.username.ilike(f'%{search_query}%')) |
            (User.email.ilike(f'%{search_query}%')) |
            (User.first_name.ilike(f'%{search_query}%')) |
            (User.last_name.ilike(f'%{search_query}%'))
        )
    
    users = query.order_by(User.created_at.desc()).paginate(page=page, per_page=per_page)
    
    return render_template('admin/users.html', 
                         title='User Management',
                         users=users,
                         status_filter=status_filter,
                         role_filter=role_filter,
                         search_query=search_query)

@admin.route('/admin/users/<int:user_id>')
@login_required
@admin_required
def admin_user_detail(user_id):
    """User detail view with full information"""
    user = User.query.get_or_404(user_id)
    user_projects = user.projects.order_by(Project.created_at.desc()).limit(10).all()
    user_stats = user.get_user_stats()
    
    # User activity timeline
    recent_activity = []
    
    # Add project creations
    for project in user_projects:
        recent_activity.append({
            'type': 'project_created',
            'title': f'Created project: {project.title}',
            'timestamp': project.created_at,
            'data': project
        })
    
    # Sort by timestamp
    recent_activity.sort(key=lambda x: x['timestamp'], reverse=True)
    recent_activity = recent_activity[:10]
    
    return render_template('admin/user_detail.html', 
                         title=f'User: {user.username}',
                         
                         user=user,
                         user_projects=user_projects,
                         user_stats=user_stats,
                         recent_activity=recent_activity)

@admin.route('/admin/users/<int:user_id>/toggle-admin', methods=['POST'])
@login_required
@admin_required
def toggle_user_admin(user_id):
    """Toggle admin status for a user"""
    if user_id == current_user.id:
        return jsonify({'success': False, 'error': 'Cannot modify your own admin status'})
    
    user = User.query.get_or_404(user_id)
    user.is_admin = not user.is_admin
    db.session.commit()
    
    action = "granted" if user.is_admin else "revoked"
    return jsonify({
        'success': True,
        'is_admin': user.is_admin,
        'message': f'Admin privileges {action} for {user.username}'
    })

@admin.route('/admin/users/<int:user_id>/toggle-active', methods=['POST'])
@login_required
@admin_required
def toggle_user_active(user_id):
    """Toggle active status for a user"""
    if user_id == current_user.id:
        return jsonify({'success': False, 'error': 'Cannot modify your own account status'})
    
    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    db.session.commit()
    
    action = "activated" if user.is_active else "deactivated"
    return jsonify({
        'success': True,
        'is_active': user.is_active,
        'message': f'Account {action} for {user.username}'
    })
@admin.route('/admin/projects/bulk-delete', methods=['POST'])
@login_required
@admin_required
def bulk_delete_projects():
    """Delete multiple projects at once"""
    data = request.get_json()
    project_ids = data.get('project_ids', [])
    
    if not project_ids:
        return jsonify({'success': False, 'error': 'No projects selected'})
    
    try:
        projects_to_delete = Project.query.filter(Project.id.in_(project_ids)).all()
        deleted_count = 0
        
        for project in projects_to_delete:
            db.session.delete(project)
            deleted_count += 1
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'deleted_count': deleted_count,
            'message': f'Successfully deleted {deleted_count} projects'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@admin.route('/admin/users/<int:user_id>/toggle-verified', methods=['POST'])
@login_required
@admin_required
def toggle_user_verified(user_id):
    """Toggle verified status for a user"""
    user = User.query.get_or_404(user_id)
    user.is_verified = not user.is_verified
    db.session.commit()
    
    action = "verified" if user.is_verified else "unverified"
    return jsonify({
        'success': True,
        'is_verified': user.is_verified,
        'message': f'Account {action} for {user.username}'
    })

@admin.route('/admin/users/<int:user_id>/update', methods=['POST'])
@login_required
@admin_required
def update_user(user_id):
    """Update user information"""
    user = User.query.get_or_404(user_id)
    
    data = request.get_json()
    
    # Update basic information
    if 'first_name' in data:
        user.first_name = data['first_name']
    if 'last_name' in data:
        user.last_name = data['last_name']
    if 'email' in data:
        # Check if email is unique
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user and existing_user.id != user_id:
            return jsonify({'success': False, 'error': 'Email already exists'})
        user.email = data['email']
    if 'username' in data:
        # Check if username is unique
        existing_user = User.query.filter_by(username=data['username']).first()
        if existing_user and existing_user.id != user_id:
            return jsonify({'success': False, 'error': 'Username already exists'})
        user.username = data['username']
    if 'location' in data:
        user.location = data['location']
    if 'phone' in data:
        user.phone = data['phone']
    if 'company' in data:
        user.company = data['company']
    if 'occupation' in data:
        user.occupation = data['occupation']
    if 'bio' in data:
        user.bio = data['bio']
    
    user.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'User information updated successfully'
    })

@admin.route('/admin/users/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    """Delete a user and all their data"""
    if user_id == current_user.id:
        return jsonify({'success': False, 'error': 'Cannot delete your own account'})
    
    user = User.query.get_or_404(user_id)
    
    # Get user info for message
    user_info = f"{user.username} ({user.email})"
    
    # Delete user and all their data (cascade should handle projects)
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': f'User {user_info} deleted successfully'
    })

@admin.route('/admin/users/bulk-action', methods=['POST'])
@login_required
@admin_required
def bulk_user_action():
    """Perform bulk actions on users"""
    data = request.get_json()
    user_ids = data.get('user_ids', [])
    action = data.get('action', '')
    
    if not user_ids:
        return jsonify({'success': False, 'error': 'No users selected'})
    
    # Remove current user from selection
    if current_user.id in user_ids:
        user_ids.remove(current_user.id)
    
    if not user_ids:
        return jsonify({'success': False, 'error': 'Cannot perform action on your own account'})
    
    users = User.query.filter(User.id.in_(user_ids)).all()
    
    try:
        if action == 'activate':
            for user in users:
                user.is_active = True
            message = f'Activated {len(users)} users'
        elif action == 'deactivate':
            for user in users:
                user.is_active = False
            message = f'Deactivated {len(users)} users'
        elif action == 'make_admin':
            for user in users:
                user.is_admin = True
            message = f'Made {len(users)} users admin'
        elif action == 'remove_admin':
            for user in users:
                user.is_admin = False
            message = f'Removed admin from {len(users)} users'
        elif action == 'verify':
            for user in users:
                user.is_verified = True
            message = f'Verified {len(users)} users'
        elif action == 'delete':
            for user in users:
                db.session.delete(user)
            message = f'Deleted {len(users)} users'
        else:
            return jsonify({'success': False, 'error': 'Invalid action'})
        
        db.session.commit()
        return jsonify({'success': True, 'message': message})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@admin.route('/admin/projects')
@login_required
@admin_required
def admin_projects():
    """Project management"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    # Filter parameters
    status_filter = request.args.get('status', 'all')
    search_query = request.args.get('search', '')
    
    # Base query
    query = Project.query
    
    # Apply filters
    if status_filter == 'public':
        query = query.filter_by(is_public=True)
    elif status_filter == 'private':
        query = query.filter_by(is_public=False)
    
    if search_query:
        query = query.filter(
            (Project.title.ilike(f'%{search_query}%')) |
            (Project.house_type.ilike(f'%{search_query}%')) |
            (Project.description.ilike(f'%{search_query}%'))
        )
    
    projects = query.order_by(Project.created_at.desc()).paginate(page=page, per_page=per_page)
    
    # Calculate statistics
    total_projects_count = Project.query.count()
    public_projects_count = Project.query.filter_by(is_public=True).count()
    total_blocks = db.session.query(func.sum(Project.total_blocks)).scalar() or 0

    
    return render_template('admin/projects.html', 
                         title='Project Management',
                         projects=projects,
                         status_filter=status_filter,
                         search_query=search_query,
                         total_projects_count=total_projects_count,
                         public_projects_count=public_projects_count,
                         total_blocks=total_blocks)

@admin.route('/admin/projects/<int:project_id>')
@login_required
@admin_required
def admin_project_detail(project_id):
    """Project detail view"""
    project = Project.query.get_or_404(project_id)
    
    return render_template('admin/project_detail.html',
                         title=f'Project: {project.title}',
                         project=project)

@admin.route('/admin/projects/<int:project_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_project_admin(project_id):
    """Delete a project (admin version)"""
    project = Project.query.get_or_404(project_id)
    project_title = project.title
    
    db.session.delete(project)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': f'Project "{project_title}" deleted successfully'
    })

@admin.route('/admin/analytics')
@login_required
@admin_required
def admin_analytics():
    """Advanced analytics dashboard"""
    # Calculate various analytics
    from sqlalchemy import Date
    
    # Daily signups for the last 30 days
    daily_signups = db.session.query(
        func.date(User.created_at).label('date'),
        func.count(User.id).label('count')
    ).filter(User.created_at >= datetime.utcnow() - timedelta(days=30))\
     .group_by(func.date(User.created_at))\
     .order_by(func.date(User.created_at)).all()
    
    # Project creation trends
    daily_projects = db.session.query(
        func.date(Project.created_at).label('date'),
        func.count(Project.id).label('count')
    ).filter(Project.created_at >= datetime.utcnow() - timedelta(days=30))\
     .group_by(func.date(Project.created_at))\
     .order_by(func.date(Project.created_at)).all()
    
    # User engagement metrics
    active_users_today = User.query.filter(func.date(User.last_login) == datetime.utcnow().date()).count()
    active_users_week = User.query.filter(User.last_login >= datetime.utcnow() - timedelta(days=7)).count()
    active_users_month = User.query.filter(User.last_login >= datetime.utcnow() - timedelta(days=30)).count()
    
    # Block calculation statistics
    total_blocks_calculated = db.session.query(func.sum(Project.total_blocks)).scalar() or 0
    avg_blocks_per_project = db.session.query(func.avg(Project.total_blocks)).scalar() or 0

    
    # Popular house types with percentages
    house_type_stats = db.session.query(
        Project.house_type,
        func.count(Project.id).label('count')
    ).group_by(Project.house_type).order_by(func.count(Project.id).desc()).limit(10).all()
    
    total_projects_count = total_projects = Project.query.count()
    house_type_percentages = [
        (ht[0], ht[1], (ht[1] / total_projects_count * 100) if total_projects_count > 0 else 0)
        for ht in house_type_stats
    ]
    
    return render_template('admin/analytics.html',
                         title='Analytics Dashboard',
                         daily_signups=daily_signups,
                         daily_projects=daily_projects,
                         total_blocks_calculated=total_blocks_calculated,
                         avg_blocks_per_project=avg_blocks_per_project,
                         active_users_today=active_users_today,
                         active_users_week=active_users_week,
                         active_users_month=active_users_month,
                         house_type_percentages=house_type_percentages)

@admin.route('/admin/prices')
@login_required
@admin_required
def admin_prices():
    """Price management dashboard"""
    from app.utils.price_fetcher import get_current_prices, price_fetcher
    
    try:
        current_prices = get_current_prices()
        manual_prices = price_fetcher.get_manual_prices()
        
        # Ensure all required price structures exist with defaults
        current_prices = ensure_price_structure(current_prices)
        
        # Price history (you could store this in database)
        price_history = get_price_history()
        
        return render_template('admin/prices.html',
                            title='Price Management',
                            current_prices=current_prices,
                            manual_prices=manual_prices,
                            price_history=price_history)
    except Exception as e:
        flash(f'Error loading price data: {str(e)}', 'danger')
        return redirect(url_for('admin.admin_dashboard'))

def ensure_price_structure(prices):
    """Ensure the price dictionary has all required structures with defaults"""
    required_structures = {
        '9_inch_hollow': {'price_range': [450, 550], 'average_price': 500},
        '6_inch_hollow': {'price_range': [350, 450], 'average_price': 400},
        '5_inch_hollow': {'price_range': [300, 400], 'average_price': 350},
        'cement': {'price_range': [4500, 5500], 'average_price': 5000},
        'sharp_sand': {'price_range': [30000, 45000], 'average_price': 37500},
        'labor': {'price_range': [100, 200], 'average_price': 150}
    }
    
    # Ensure each required structure exists
    for material, defaults in required_structures.items():
        if material not in prices:
            prices[material] = defaults
        else:
            # Ensure price_range exists
            if 'price_range' not in prices[material]:
                prices[material]['price_range'] = defaults['price_range']
            # Ensure average_price exists
            if 'average_price' not in prices[material]:
                prices[material]['average_price'] = defaults['average_price']
    
    return prices

@admin.route('/admin/prices/update', methods=['POST'])
@login_required
@admin_required
def update_prices():
    """Update prices manually"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'})
        
        from app.utils.price_fetcher import price_fetcher
        updated_prices = price_fetcher.update_manual_prices(data)
        
        # Log the price update
        log_price_update(current_user.id, data)
        
        return jsonify({
            'success': True,
            'message': 'Prices updated successfully!',
            'prices': updated_prices
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@admin.route('/admin/prices/reset', methods=['POST'])
@login_required
@admin_required
def reset_prices():
    """Reset to automatic pricing"""
    try:
        import os
        manual_cache_path = 'manual_price_cache.json'
        
        if os.path.exists(manual_cache_path):
            os.remove(manual_cache_path)
            
        from app.utils.price_fetcher import get_current_prices
        current_prices = get_current_prices()
        
        # Log the reset
        log_price_update(current_user.id, {'action': 'reset_to_auto'})
        
        return jsonify({
            'success': True,
            'message': 'Prices reset to automatic mode!',
            'prices': current_prices
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@admin.route('/admin/prices/history')
@login_required
@admin_required
def price_history():
    """Get price update history"""
    history = get_price_history()
    return jsonify({'success': True, 'history': history})

@admin.route('/admin/prices/refresh', methods=['POST'])
@login_required
@admin_required
def refresh_prices():
    """Manually refresh prices from sources"""
    try:
        from app.utils.price_fetcher import update_prices_manually
        prices = update_prices_manually()
        
        return jsonify({
            'success': True,
            'message': 'Prices refreshed from sources!',
            'prices': prices
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# Helper functions
def get_price_history():
    """Get price update history (simplified - in production, use database)"""
    try:
        with open('price_update_history.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def log_price_update(user_id, update_data):
    """Log price updates for audit trail"""
    try:
        history = get_price_history()
        
        history_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'user_id': user_id,
            'action': 'manual_update' if 'action' not in update_data else update_data['action'],
            'data': update_data
        }
        
        history.insert(0, history_entry)  # Add to beginning
        history = history[:50]  # Keep only last 50 entries
        
        with open('price_update_history.json', 'w') as f:
            json.dump(history, f, indent=2)
            
    except Exception as e:
        print(f"Error logging price update: {e}")
        
@admin.route('/api/admin/stats')
@login_required
@admin_required
def admin_stats_api():
    """API endpoint for admin statistics"""
    # Real-time statistics for dashboard widgets
    total_users = User.query.count()
    total_projects = Project.query.count()
    active_users = User.query.filter_by(is_active=True).count()
    admin_users = User.query.filter_by(is_admin=True).count()
    
    # Today's activity
    today = datetime.utcnow().date()
    today_users = User.query.filter(func.date(User.created_at) == today).count()
    today_projects = Project.query.filter(func.date(Project.created_at) == today).count()
    
    # Recent signups (last 7 days)
    week_ago = datetime.utcnow() - timedelta(days=7)
    recent_signups = User.query.filter(User.created_at >= week_ago).count()
    
    return jsonify({
        'total_users': total_users,
        'total_projects': total_projects,
        'active_users': active_users,
        'admin_users': admin_users,
        'today_users': today_users,
        'today_projects': today_projects,
        'recent_signups': recent_signups
    })