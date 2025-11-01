import uuid
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256))
    profile_pic = db.Column(db.String(120), default='default.jpg')
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    phone = db.Column(db.String(20))
    location = db.Column(db.String(100), default='Lagos')
    company = db.Column(db.String(100))
    occupation = db.Column(db.String(100))
    bio = db.Column(db.Text)
    
    # Admin fields
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    
    # User preferences
    preferred_block_type = db.Column(db.String(20), default='9_inch_hollow')
    preferred_waste_percentage = db.Column(db.Integer, default=10)
    measurement_system = db.Column(db.String(10), default='feet')  # feet or meters
    email_notifications = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    projects = db.relationship('Project', backref='author', lazy='dynamic', cascade='all, delete-orphan')
    shared_projects = db.relationship('ProjectShare', backref='user', lazy='dynamic', foreign_keys='ProjectShare.user_id')
    
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        # Make first user admin automatically
        if User.query.count() == 0:
            self.is_admin = True
            self.is_verified = True
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def update_last_login(self):
        self.last_login = datetime.utcnow()
        db.session.commit()
    def add_notification(self, title, message, notification_type='info', action_url=None, related_id=None, related_type=None):
        """Add a new notification for the user"""
        notification = Notification(
            user_id=self.id,
            title=title,
            message=message,
            notification_type=notification_type,
            action_url=action_url,
            related_id=related_id,
            related_type=related_type
        )
        db.session.add(notification)
        db.session.commit()
        return notification
    
    def get_unread_notifications(self, limit=None):
        """Get unread notifications"""
        query = Notification.query.filter_by(
            user_id=self.id, 
            is_read=False
        ).order_by(Notification.created_at.desc())
        
        if limit:
            return query.limit(limit).all()
        return query.all()
    
    def get_recent_notifications(self, limit=10):
        """Get recent notifications (both read and unread)"""
        return Notification.query.filter_by(
            user_id=self.id
        ).order_by(Notification.created_at.desc()).limit(limit).all()
    
    def get_notification_count(self):
        """Get count of unread notifications"""
        return Notification.query.filter_by(
            user_id=self.id, 
            is_read=False
        ).count()
    
    def mark_all_notifications_read(self):
        """Mark all notifications as read"""
        notifications = Notification.query.filter_by(
            user_id=self.id, 
            is_read=False
        ).all()
        
        for notification in notifications:
            notification.mark_as_read()
        
        return len(notifications)
    
    def get_user_stats(self):
        """Get user statistics for dashboard"""
        total_projects = self.projects.count()
        total_blocks = sum(project.total_blocks or 0 for project in self.projects.all())
        favorite_house_type = db.session.query(
            Project.house_type,
            db.func.count(Project.id)
        ).filter_by(user_id=self.id).group_by(Project.house_type).order_by(db.func.count(Project.id).desc()).first()
        
        return {
            'total_projects': total_projects,
            'total_blocks': total_blocks,
            'favorite_house_type': favorite_house_type[0] if favorite_house_type else 'Custom',
            'member_since': self.created_at.strftime('%B %Y')
        }
    def get_accessible_projects(self):
        """Get all projects the user can access (own, shared, or team projects)"""
        # Get user's own projects
        own_projects = self.projects.all()
        
        # Get projects shared with user
        shared_projects = Project.query.join(ProjectCollaborator).filter(
            ProjectCollaborator.user_id == self.id
        ).all()
        
        # Get team projects
        team_projects = Project.query.join(Team).join(TeamMember).filter(
            TeamMember.user_id == self.id,
            Project.team_id.isnot(None)
        ).all()
        
        # Combine and remove duplicates
        all_projects = list({project.id: project for project in own_projects + shared_projects + team_projects}.values())
        return sorted(all_projects, key=lambda x: x.updated_at, reverse=True)
    
    def can_login(self):
        """Check if user can login (active and verified)"""
        return self.is_active and self.is_verified
    
    def to_dict(self):
        """Convert user to dictionary for JSON response"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_admin': self.is_admin,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'location': self.location,
            'created_at': self.created_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'project_count': self.projects.count(),
            'total_blocks': sum(project.total_blocks or 0 for project in self.projects.all())
        }
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def __repr__(self):
        return f'<User {self.username}>'

class Project(db.Model):
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    house_type = db.Column(db.String(50), nullable=False, default='custom')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Project data
    structures_data = db.Column(db.JSON, default=lambda: {
        'structures': [],
        'block_type': '9_inch_hollow',
        'waste_percentage': 10
    })
    
    # Calculated results - REMOVE estimated_cost
    total_blocks = db.Column(db.Integer, default=0)
    total_area = db.Column(db.Float, default=0.0)
    
    # Privacy settings
    is_public = db.Column(db.Boolean, default=False)
    is_private = db.Column(db.Boolean, default=False)
    share_token = db.Column(db.String(32), unique=True, index=True)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=True)
    
    # Relationships
    shares = db.relationship('ProjectShare', backref='project', lazy='dynamic', cascade='all, delete-orphan')
    collaborators = db.relationship('ProjectCollaborator', backref='project', lazy='dynamic', cascade='all, delete-orphan')
    
    def get_collaborators(self):
        """Get all collaborators including owner"""
        collaborators = []
        
        # Add owner
        collaborators.append({
            'user': self.author.to_dict(),
            'role': 'owner',
            'joined_at': self.created_at.isoformat()
        })
        
        # Add collaborators
        for collab in self.collaborators:
            collaborators.append({
                'user': collab.user.to_dict(),
                'role': collab.role,
                'joined_at': collab.joined_at.isoformat()
            })
        
        return collaborators
    
    def can_view(self, user):
        """Check if user can view this project"""
        # Project owner can always view
        if user.id == self.user_id:
            return True
        
        # If project is private, only owner can view
        if self.is_private:
            return False
        
        # Check if user is collaborator
        collaborator = ProjectCollaborator.query.filter_by(
            project_id=self.id, 
            user_id=user.id
        ).first()
        if collaborator:
            return True
        
        # Check if project is in user's team and not private
        if self.team_id and not self.is_private:
            team_member = TeamMember.query.filter_by(
                team_id=self.team_id, 
                user_id=user.id
            ).first()
            if team_member:
                return True
        
        return False
    
    def can_edit(self, user):
        """Check if user can edit this project"""
        # Project owner can always edit
        if user.id == self.user_id:
            return True
        
        # If project is private, only owner can edit
        if self.is_private:
            return False
        
        # Check if user is collaborator with edit rights
        collaborator = ProjectCollaborator.query.filter_by(
            project_id=self.id, 
            user_id=user.id
        ).first()
        if collaborator and collaborator.role in ['owner', 'collaborator']:
            return True
        
        # Check if user is team admin/owner for team projects
        if self.team_id and not self.is_private:
            team_member = TeamMember.query.filter_by(
                team_id=self.team_id, 
                user_id=user.id
            ).first()
            if team_member and team_member.role in ['owner', 'admin']:
                return True
        
        return False
    
    def get_privacy_status(self):
        """Get human-readable privacy status"""
        if self.is_private:
            return "Private (Only you)"
        elif self.is_public:
            return "Public (Anyone with link)"
        elif self.team_id:
            return "Team (Team members)"
        else:
            return "Private (Only you)"
    
    def set_privacy(self, privacy_level):
        """Set project privacy level"""
        self.is_private = False
        self.is_public = False
        
        if privacy_level == 'private':
            self.is_private = True
        elif privacy_level == 'public':
            self.is_public = True
        elif privacy_level == 'team':
            # Team privacy is implied by having team_id
            pass
        
        db.session.commit()
    
    def calculate_blocks(self):
        """Calculate total blocks needed for this project - UPDATED without price"""
        try:
            from app.utils.calculator import BlockCalculator
            
            calculator = BlockCalculator(
                self.structures_data,
                block_type=self.structures_data.get('block_type', '9_inch_hollow')
            )
            
            result = calculator.calculate()
            
            self.total_blocks = result['total_blocks']
            self.total_area = result['total_area']
            
            return self.total_blocks
            
        except Exception as e:
            print(f"Error calculating blocks: {e}")
            self.total_blocks = 0
            self.total_area = 0
            return 0
    
    def generate_share_token(self):
        """Generate a unique share token for public access"""
        import secrets
        self.share_token = secrets.token_urlsafe(16)
        db.session.commit()
        return self.share_token
    
    def get_share_url(self):
        """Get the public share URL"""
        if not self.share_token:
            self.generate_share_token()
        return f"/project/shared/{self.share_token}"
    def assign_to_team(self, team_id):
        """Assign project to a team"""
        self.team_id = team_id
        db.session.commit()
    
    @classmethod
    def create_with_team(cls, title, house_type, structures_data, user_id, team_id=None):
        """Create a new project optionally assigned to a team"""
        project = cls(
            title=title,
            house_type=house_type,
            structures_data=structures_data,
            user_id=user_id,
            team_id=team_id
        )
        
        if structures_data.get('structures'):
            project.calculate_blocks()
        
        db.session.add(project)
        db.session.commit()
        return project
    def safe_delete(self):
        """Safely delete project by removing all related data first"""
        try:
            # Remove collaborators
            ProjectCollaborator.query.filter_by(project_id=self.id).delete()
            
            # Remove invitations
            ProjectInvitation.query.filter_by(project_id=self.id).delete()
            
            # Remove shares
            ProjectShare.query.filter_by(project_id=self.id).delete()
            
            # Remove notifications related to this project
            Notification.query.filter_by(
                related_id=self.id, 
                related_type='project'
            ).delete()
            
            # Now delete the project
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting project: {e}")
            return False
    
    def get_last_updated_by(self):
        """Get information about who last updated the project"""
        # This would need to be implemented based on your audit trail
        # For now, return the author
        return self.author
    
    def get_contribution_stats(self):
        """Get contribution statistics for team projects"""
        if not self.team_id:
            return None
            
        collaborators = ProjectCollaborator.query.filter_by(
            project_id=self.id
        ).all()
        
        stats = {
            'author_contribution': 100,  # Base percentage
            'collaborators': []
        }
        
        # In a real implementation, you'd track actual contributions
        for collab in collaborators:
            stats['collaborators'].append({
                'user': collab.user.to_dict(),
                'role': collab.role,
                'contribution_percentage': 0  # Placeholder
            })
        
        return stats
    
    def to_dict(self):
        """Convert project to dictionary for JSON response"""
        return {
            'id': self.id,
            'title': self.title,
            'house_type': self.house_type,
            'structures_data': self.structures_data,
            'total_blocks': self.total_blocks,
            'total_area': self.total_area,
            'is_public': self.is_public,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'author': {
                'username': self.author.username,
                'first_name': self.author.first_name,
                'last_name': self.author.last_name
            }
        }
    def __init__(self, **kwargs):
        super(Project, self).__init__(**kwargs)
        self.share_token = str(uuid.uuid4().hex)
    
    def __repr__(self):
        return f'<Project {self.title}>'

class ProjectShare(db.Model):
    __tablename__ = 'project_shares'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    shared_at = db.Column(db.DateTime, default=datetime.utcnow)
    can_edit = db.Column(db.Boolean, default=False)
    
    # Unique constraint to prevent duplicate shares
    __table_args__ = (db.UniqueConstraint('user_id', 'project_id', name='unique_user_project_share'),)
    
class ProjectTemplate(db.Model):
    __tablename__ = 'project_templates'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50), default='residential')  # residential, commercial, industrial
    house_type = db.Column(db.String(50), nullable=False)
    structures_data = db.Column(db.JSON, nullable=False)
    thumbnail = db.Column(db.String(200))
    is_public = db.Column(db.Boolean, default=True)
    usage_count = db.Column(db.Integer, default=0)
    rating = db.Column(db.Float, default=0.0)
    
    # Foreign keys
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    author = db.relationship('User', backref='templates')
    reviews = db.relationship('TemplateReview', backref='template', lazy='dynamic', cascade='all, delete-orphan')
    
    def increment_usage(self):
        self.usage_count += 1
        db.session.commit()
    
    def update_rating(self):
        reviews = self.reviews.all()
        if reviews:
            self.rating = sum(review.rating for review in reviews) / len(reviews)
            db.session.commit()
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'house_type': self.house_type,
            'structures_data': self.structures_data,
            'thumbnail': self.thumbnail,
            'is_public': self.is_public,
            'usage_count': self.usage_count,
            'rating': self.rating,
            'created_by': self.created_by,
            'author_name': f"{self.author.first_name} {self.author.last_name}",
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<ProjectTemplate {self.name}>'

class TemplateReview(db.Model):
    __tablename__ = 'template_reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    comment = db.Column(db.Text)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    template_id = db.Column(db.Integer, db.ForeignKey('project_templates.id'), nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='template_reviews')
    
    __table_args__ = (db.UniqueConstraint('user_id', 'template_id', name='unique_user_template_review'),)
    
    def __repr__(self):
        return f'<TemplateReview {self.rating} stars by {self.user.username}>'

class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    notification_type = db.Column(db.String(50), nullable=False)  # 'info', 'success', 'warning', 'danger', 'system'
    is_read = db.Column(db.Boolean, default=False)
    action_url = db.Column(db.String(500))  # URL for the notification action
    related_id = db.Column(db.Integer)  # ID of related object (project, user, etc)
    related_type = db.Column(db.String(50))  # Type of related object ('project', 'user', 'system')
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    read_at = db.Column(db.DateTime)
    
    # Relationships
    user = db.relationship('User', backref='notifications')
    
    def mark_as_read(self):
        self.is_read = True
        self.read_at = datetime.utcnow()
        db.session.commit()
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'message': self.message,
            'type': self.notification_type,
            'is_read': self.is_read,
            'action_url': self.action_url,
            'created_at': self.created_at.isoformat(),
            'read_at': self.read_at.isoformat() if self.read_at else None,
            'time_ago': self.get_time_ago()
        }
    
    def get_time_ago(self):
        """Get human-readable time difference"""
        now = datetime.utcnow()
        diff = now - self.created_at
        
        if diff.days > 0:
            return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
        elif diff.seconds >= 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif diff.seconds >= 60:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            return "Just now"
    
    def __repr__(self):
        return f'<Notification {self.title} for User {self.user_id}>'
    
class Team(db.Model):
    __tablename__ = 'teams'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Team Settings
    allow_member_invites = db.Column(db.Boolean, default=False)
    default_project_privacy = db.Column(db.String(20), default='team')  # private, team, public
    allow_project_deletion = db.Column(db.Boolean, default=False)
    team_color = db.Column(db.String(7), default='#0d6efd')  # Brand color for team
    
    # Foreign keys
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    members = db.relationship('TeamMember', backref='team', lazy='dynamic', cascade='all, delete-orphan')
    projects = db.relationship('Project', backref='team', lazy='dynamic')
    
    def get_team_settings(self):
        """Get all team settings"""
        return {
            'allow_member_invites': self.allow_member_invites,
            'default_project_privacy': self.default_project_privacy,
            'allow_project_deletion': self.allow_project_deletion,
            'team_color': self.team_color
        }
    
    def update_settings(self, settings):
        """Update team settings"""
        if 'allow_member_invites' in settings:
            self.allow_member_invites = settings['allow_member_invites']
        if 'default_project_privacy' in settings:
            self.default_project_privacy = settings['default_project_privacy']
        if 'allow_project_deletion' in settings:
            self.allow_project_deletion = settings['allow_project_deletion']
        if 'team_color' in settings:
            self.team_color = settings['team_color']
        
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def get_member_permissions(self, user_id):
        """Get permissions for a specific member"""
        member = TeamMember.query.filter_by(
            team_id=self.id,
            user_id=user_id
        ).first()
        
        if not member:
            return None
            
        permissions = {
            'can_invite': member.role in ['owner', 'admin'] or self.allow_member_invites,
            'can_edit_team': member.role in ['owner', 'admin'],
            'can_delete_team': member.role == 'owner',
            'can_remove_members': member.role in ['owner', 'admin'],
            'can_create_projects': True,
            'can_delete_projects': member.role in ['owner', 'admin'] or self.allow_project_deletion,
            'role': member.role
        }
        
        return permissions
    
    def delete_team(self):
        """Safely delete a team and handle all related data"""
        try:
            # Get all member IDs for notifications
            member_ids = [member.user_id for member in self.members]
            
            # Remove team members first
            TeamMember.query.filter_by(team_id=self.id).delete()
            
            # Remove team from projects (set team_id to None)
            Project.query.filter_by(team_id=self.id).update({'team_id': None})
            
            # Delete the team
            db.session.delete(self)
            db.session.commit()
            
            # Send notifications to former team members
            for user_id in member_ids:
                user = User.query.get(user_id)
                if user:
                    user.add_notification(
                        title="Team Deleted",
                        message=f"The team '{self.name}' has been deleted",
                        notification_type='warning',
                        action_url='/teams',
                        related_type='team'
                    )
            
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting team: {e}")
            return False
    def get_team_projects(self):
        """Get all projects associated with this team"""
        return Project.query.filter_by(team_id=self.id).all()
    
    def get_member_stats(self):
        """Get detailed statistics for each team member"""
        members = TeamMember.query.filter_by(team_id=self.id).all()
        member_stats = []
        
        for member in members:
            user_projects = Project.query.filter_by(
                team_id=self.id, 
                user_id=member.user_id
            ).all()
            
            total_blocks = sum(project.total_blocks or 0 for project in user_projects)
            total_area = sum(project.total_area or 0 for project in user_projects)
            
            member_stats.append({
                'user': member.user.to_dict(),
                'role': member.role,
                'project_count': len(user_projects),
                'total_blocks': total_blocks,
                'total_area': total_area,
                'joined_at': member.joined_at
            })
        
        return member_stats

class TeamMember(db.Model):
    __tablename__ = 'team_members'
    
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(20), default='member')  # owner, admin, member
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Additional member settings
    can_create_projects = db.Column(db.Boolean, default=True)
    can_invite_members = db.Column(db.Boolean, default=False)
    
    # Foreign keys
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    user = db.relationship('User', backref='team_memberships')
    
    __table_args__ = (db.UniqueConstraint('team_id', 'user_id', name='unique_team_member'),)
    
    def update_role(self, new_role, changed_by_id):
        """Update member role with permission checking"""
        if new_role not in ['owner', 'admin', 'member']:
            return False, 'Invalid role'
        
        # Get the user who is making the change
        changer = TeamMember.query.filter_by(
            team_id=self.team_id,
            user_id=changed_by_id
        ).first()
        
        if not changer or changer.role not in ['owner', 'admin']:
            return False, 'Insufficient permissions'
        
        # Special handling for owner role changes
        if new_role == 'owner':
            # Find current owner and demote them
            current_owner = TeamMember.query.filter_by(
                team_id=self.team_id,
                role='owner'
            ).first()
            
            if current_owner:
                current_owner.role = 'admin'
        
        self.role = new_role
        db.session.commit()
        
        # Send notification to the member
        self.user.add_notification(
            title="Team Role Updated",
            message=f"Your role in team '{self.team.name}' has been changed to {new_role}",
            notification_type='info',
            action_url=f"/teams/{self.team_id}",
            related_id=self.team_id,
            related_type='team'
        )
        
        return True, 'Role updated successfully'

class ProjectInvitation(db.Model):
    __tablename__ = 'project_invitations'
    
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20), default='pending')  # pending, accepted, declined
    message = db.Column(db.Text)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    responded_at = db.Column(db.DateTime)
    
    # Foreign keys
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    inviter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    invitee_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    project = db.relationship('Project', backref='invitations')
    inviter = db.relationship('User', foreign_keys=[inviter_id], backref='sent_invitations')
    invitee = db.relationship('User', foreign_keys=[invitee_id], backref='received_invitations')
    
    def accept(self):
        self.status = 'accepted'
        self.responded_at = datetime.utcnow()
        
        # Add user to project collaborators
        collaborator = ProjectCollaborator(
            project_id=self.project_id,
            user_id=self.invitee_id,
            role='collaborator'
        )
        db.session.add(collaborator)
        
        # Send notification to inviter
        self.inviter.add_notification(
            title="Project Invitation Accepted",
            message=f"{self.invitee.first_name} has accepted your invitation to collaborate on '{self.project.title}'",
            notification_type='success',
            action_url=f"/project/{self.project_id}",
            related_id=self.project_id,
            related_type='project'
        )
    
    def decline(self):
        self.status = 'declined'
        self.responded_at = datetime.utcnow()
        
        # Send notification to inviter
        self.inviter.add_notification(
            title="Project Invitation Declined",
            message=f"{self.invitee.first_name} has declined your invitation to collaborate on '{self.project.title}'",
            notification_type='warning',
            action_url=f"/project/{self.project_id}",
            related_id=self.project_id,
            related_type='project'
        )
    
    def to_dict(self):
        return {
            'id': self.id,
            'status': self.status,
            'message': self.message,
            'sent_at': self.sent_at.isoformat(),
            'project': {
                'id': self.project.id,
                'title': self.project.title,
                'house_type': self.project.house_type
            },
            'inviter': {
                'id': self.inviter.id,
                'username': self.inviter.username,
                'first_name': self.inviter.first_name,
                'last_name': self.inviter.last_name
            },
            'invitee': {
                'id': self.invitee.id,
                'username': self.invitee.username,
                'first_name': self.invitee.first_name,
                'last_name': self.invitee.last_name
            }
        }

class ProjectCollaborator(db.Model):
    __tablename__ = 'project_collaborators'
    
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(20), default='collaborator')  # owner, collaborator, viewer
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign keys
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    user = db.relationship('User', backref='project_collaborations')
    
    __table_args__ = (db.UniqueConstraint('project_id', 'user_id', name='unique_project_collaborator'),)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))