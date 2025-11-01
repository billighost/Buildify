from flask import render_template, redirect, url_for, flash, request, Blueprint, jsonify, current_app
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
import os
import uuid
from PIL import Image
from app import db
from app.utils.notifications import create_welcome_notifications
from app.models import User, Project, Notification
from app.auth.forms import (LoginForm, RegistrationForm, UpdateAccountForm, 
                           UserPreferencesForm, ChangePasswordForm, ProfilePictureForm)

auth = Blueprint('auth', __name__)

def save_profile_picture(form_picture):
    """Save profile picture with resizing and return filename"""
    # Generate unique filename
    random_hex = uuid.uuid4().hex
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static', 'profile_pics', picture_fn)
    
    # Resize image
    output_size = (300, 300)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    
    # Save image
    i.save(picture_path)
    
    return picture_fn

def delete_old_profile_picture(picture_fn):
    """Delete old profile picture if it's not the default"""
    if picture_fn != 'default.jpg':
        old_picture_path = os.path.join(current_app.root_path, 'static', 'profile_pics', picture_fn)
        if os.path.exists(old_picture_path):
            os.remove(old_picture_path)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('projects.dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            location=form.location.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        # Create welcome notifications
        create_welcome_notifications(user)
        
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', title='Register', form=form)

@auth.route('/notifications')
@login_required
def notifications():
    """Notifications page"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    notifications = Notification.query.filter_by(
        user_id=current_user.id
    ).order_by(Notification.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('auth/notifications.html', 
                         title='Notifications',
                         notifications=notifications)

@auth.route('/api/notifications')
@login_required
def get_notifications_api():
    """API endpoint to get notifications (for dropdown)"""
    limit = request.args.get('limit', 5, type=int)
    unread_only = request.args.get('unread_only', False, type=bool)
    
    query = Notification.query.filter_by(user_id=current_user.id)
    
    if unread_only:
        query = query.filter_by(is_read=False)
    
    notifications = query.order_by(Notification.created_at.desc()).limit(limit).all()
    
    return jsonify({
        'success': True,
        'notifications': [n.to_dict() for n in notifications],
        'unread_count': current_user.get_notification_count()
    })

@auth.route('/api/notifications/<int:notification_id>/read', methods=['POST'])
@login_required
def mark_notification_read(notification_id):
    """Mark a notification as read"""
    notification = Notification.query.get_or_404(notification_id)
    
    if notification.user_id != current_user.id:
        return jsonify({'success': False, 'error': 'Permission denied'})
    
    notification.mark_as_read()
    
    return jsonify({'success': True})

@auth.route('/api/notifications/read-all', methods=['POST'])
@login_required
def mark_all_notifications_read():
    """Mark all notifications as read"""
    count = current_user.mark_all_notifications_read()
    
    return jsonify({
        'success': True,
        'message': f'Marked {count} notifications as read',
        'count': count
    })

@auth.route('/api/notifications/<int:notification_id>/delete', methods=['DELETE'])
@login_required
def delete_notification(notification_id):
    """Delete a single notification"""
    notification = Notification.query.get_or_404(notification_id)
    
    if notification.user_id != current_user.id:
        return jsonify({'success': False, 'error': 'Permission denied'})
    
    db.session.delete(notification)
    db.session.commit()
    
    return jsonify({'success': True})

@auth.route('/api/notifications/bulk-delete', methods=['POST'])
@login_required
def bulk_delete_notifications():
    """Bulk delete notifications"""
    data = request.get_json()
    notification_ids = data.get('notification_ids', [])
    
    if not notification_ids:
        return jsonify({'success': False, 'error': 'No notifications selected'})
    
    try:
        # Get notifications that belong to current user
        notifications_to_delete = Notification.query.filter(
            Notification.id.in_(notification_ids),
            Notification.user_id == current_user.id
        ).all()
        
        deleted_count = 0
        for notification in notifications_to_delete:
            db.session.delete(notification)
            deleted_count += 1
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'deleted_count': deleted_count,
            'message': f'Deleted {deleted_count} notifications'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('projects.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user:
            # Check if account is active
            if not user.is_active:
                flash('Your account has been disabled. Please contact support.', 'danger')
                return render_template('auth/login.html', title='Login', form=form)
            
            # # Check if account is verified (if you implement email verification)
            # if not user.is_verified:
            #     flash('Please verify your email address before logging in.', 'warning')
            #     return render_template('auth/login.html', title='Login', form=form)
            
            if user.check_password(form.password.data):
                login_user(user, remember=form.remember.data)
                user.update_last_login()
                
                next_page = request.args.get('next')
                flash('Login successful!', 'success')
                return redirect(next_page) if next_page else redirect(url_for('projects.dashboard'))
        
        flash('Login unsuccessful. Please check email and password.', 'danger')
    
    return render_template('auth/login.html', title='Login', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

@auth.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    profile_form = UpdateAccountForm()
    picture_form = ProfilePictureForm()
    
    recent_projects = (
        Project.query
        .filter_by(user_id=current_user.id)
        .order_by(Project.updated_at.desc())
        .limit(5)
        .all()
    )
    
    if profile_form.validate_on_submit():
        # Update user profile data
        current_user.username = profile_form.username.data
        current_user.email = profile_form.email.data
        current_user.first_name = profile_form.first_name.data
        current_user.last_name = profile_form.last_name.data
        current_user.phone = profile_form.phone.data
        current_user.location = profile_form.location.data
        current_user.company = profile_form.company.data
        current_user.occupation = profile_form.occupation.data
        current_user.bio = profile_form.bio.data
        
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('auth.account'))
    
    elif request.method == 'GET':
        # Populate form with current user data
        profile_form.username.data = current_user.username
        profile_form.email.data = current_user.email
        profile_form.first_name.data = current_user.first_name
        profile_form.last_name.data = current_user.last_name
        profile_form.phone.data = current_user.phone
        profile_form.location.data = current_user.location
        profile_form.company.data = current_user.company
        profile_form.occupation.data = current_user.occupation
        profile_form.bio.data = current_user.bio
    
    user_stats = current_user.get_user_stats()
    return render_template('auth/account.html', 
                         title='Account Settings',
                         profile_form=profile_form,
                         picture_form=picture_form,
                         user_stats=user_stats,
                         recent_projects=recent_projects
                         )

@auth.route('/account/update-picture', methods=['POST'])
@login_required
def update_profile_picture():
    form = ProfilePictureForm()
    if form.validate_on_submit():
        if form.picture.data:
            # Delete old picture if it exists
            if current_user.profile_pic != 'default.jpg':
                delete_old_profile_picture(current_user.profile_pic)
            
            # Save new picture
            picture_file = save_profile_picture(form.picture.data)
            current_user.profile_pic = picture_file
            db.session.commit()
            flash('Your profile picture has been updated!', 'success')
        else:
            flash('No picture selected.', 'warning')
    else:
        flash('Please select a valid image file.', 'danger')
    
    return redirect(url_for('auth.account'))

@auth.route('/account/remove-picture', methods=['POST'])
@login_required
def remove_profile_picture():
    if current_user.profile_pic != 'default.jpg':
        delete_old_profile_picture(current_user.profile_pic)
        current_user.profile_pic = 'default.jpg'
        db.session.commit()
        flash('Profile picture removed successfully!', 'success')
    else:
        flash('No custom profile picture to remove.', 'info')
    
    return redirect(url_for('auth.account'))

@auth.route('/account/preferences', methods=['GET', 'POST'])
@login_required
def account_preferences():
    form = UserPreferencesForm()
    if form.validate_on_submit():
        current_user.preferred_block_type = form.preferred_block_type.data
        current_user.preferred_waste_percentage = int(form.preferred_waste_percentage.data)
        current_user.measurement_system = form.measurement_system.data
    
        current_user.email_notifications = form.email_notifications.data
        current_user.sms_notifications = form.sms_notifications.data
        current_user.marketing_emails = form.marketing_emails.data
        
        db.session.commit()
        flash('Your preferences have been updated!', 'success')
        return redirect(url_for('auth.account_preferences'))
    
    elif request.method == 'GET':
        form.preferred_block_type.data = current_user.preferred_block_type
        form.preferred_waste_percentage.data = str(current_user.preferred_waste_percentage)
        form.measurement_system.data = current_user.measurement_system
        form.email_notifications.data = current_user.email_notifications
        form.sms_notifications.data = getattr(current_user, 'sms_notifications', False)
        form.marketing_emails.data = getattr(current_user, 'marketing_emails', False)
    
    return render_template('auth/preferences.html', title='Preferences', form=form)

@auth.route('/account/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.current_password.data):
            current_user.set_password(form.new_password.data)
            db.session.commit()
            
            # Log the user out and redirect to login page
            logout_user()
            flash('Your password has been updated! Please log in again.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Current password is incorrect.', 'danger')
    
    return render_template('auth/change_password.html', title='Change Password', form=form)

@auth.route('/account/delete', methods=['GET', 'POST'])
@login_required
def delete_account():
    if request.method == 'POST':
        # Verify password
        password = request.form.get('password')
        if not current_user.check_password(password):
            flash('Incorrect password. Account deletion failed.', 'danger')
            return redirect(url_for('auth.delete_account'))
        
        # Delete user account
        username = current_user.username
        db.session.delete(current_user)
        db.session.commit()
        
        logout_user()
        flash(f'Account "{username}" has been permanently deleted.', 'success')
        return redirect(url_for('main.home'))
    
    return render_template('auth/delete_account.html', title='Delete Account')

@auth.route('/api/user/stats')
@login_required
def user_stats_api():
    """API endpoint to get user statistics"""
    stats = current_user.get_user_stats()
    return jsonify(stats)

@auth.route('/api/user/update-location', methods=['POST'])
@login_required
def update_user_location():
    """Update user location via API"""
    data = request.get_json()
    location = data.get('location')
    
    if location:
        current_user.location = location
        db.session.commit()
        return jsonify({'success': True, 'message': 'Location updated successfully'})
    
    return jsonify({'success': False, 'error': 'Invalid location'})