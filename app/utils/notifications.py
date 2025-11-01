from app.models import Notification, User, Project
from app import db
from datetime import datetime

class NotificationManager:
    @staticmethod
    def send_welcome_notification(user):
        """Send welcome notification after registration"""
        user.add_notification(
            title="Welcome to Buildify! 🎉",
            message=f"Hello {user.first_name}! Welcome to Buildify. We're excited to help you build smarter. Start by creating your first project!",
            notification_type='success',
            action_url='/project/new',
            related_type='welcome'
        )
    
    @staticmethod
    def send_project_created_notification(user, project):
        """Send notification when a project is created - UPDATED without price"""
        user.add_notification(
            title="Project Created Successfully! 🏗️",
            message=f'Your project "{project.title}" has been created. We calculated you need {project.total_blocks} blocks.',
            notification_type='info',
            action_url=f'/project/{project.id}',
            related_id=project.id,
            related_type='project'
        )
        
    @staticmethod
    def send_project_deleted_notification(user, project_title):
        """Send notification when a project is deleted"""
        user.add_notification(
            title="Project Deleted",
            message=f'Your project "{project_title}" has been permanently deleted.',
            notification_type='warning',
            action_url='/projects/dashboard',
            related_type='project'
        )
    
    @staticmethod
    def send_bulk_delete_notification(user, count):
        """Send notification for bulk project deletion"""
        user.add_notification(
            title="Bulk Delete Completed",
            message=f'Successfully deleted {count} projects.',
            notification_type='warning',
            action_url='/projects/dashboard',
            related_type='project'
        )
    
    @staticmethod
    def send_profile_updated_notification(user):
        """Send notification when profile is updated"""
        user.add_notification(
            title="Profile Updated",
            message="Your profile information has been updated successfully.",
            notification_type='info',
            action_url='/account',
            related_type='profile'
        )
    
    @staticmethod
    def send_system_notification(user, title, message, notification_type='info'):
        """Send system notification"""
        user.add_notification(
            title=title,
            message=message,
            notification_type=notification_type,
            related_type='system'
        )

def create_welcome_notifications(user):
    """Create initial welcome notifications for new users"""
    # Welcome notification
    NotificationManager.send_welcome_notification(user)
    
    # Tips notification
    user.add_notification(
        title="Quick Tip 💡",
        message="Use our auto-fill templates to quickly get started with common house types in Nigeria.",
        notification_type='info',
        action_url='/project/new',
        related_type='tip'
    )