from functools import wraps
from flask import flash, redirect, url_for, request, jsonify
from flask_login import current_user
import json

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        
        if not current_user.is_admin:
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('projects.dashboard'))
        
        return f(*args, **kwargs)
    return decorated_function

def admin_required_api(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({'success': False, 'error': 'Authentication required'}), 401
        
        if not current_user.is_admin:
            return jsonify({'success': False, 'error': 'Admin privileges required'}), 403
        
        return f(*args, **kwargs)
    return decorated_function