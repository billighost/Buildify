from flask import render_template, Blueprint, redirect, url_for
from flask_login import current_user
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    # # If user is logged in, redirect to dashboard
    # if current_user.is_authenticated:
    #     return redirect(url_for('projects.dashboard'))
    return render_template('main/home.html', title='Home')

@main.route('/features')
def features():
    return render_template('main/features.html', title='Features')

@main.route('/pricing')
def pricing():
    return render_template('main/pricing.html', title='Pricing')

@main.route('/about')
def about():
    return render_template('main/about.html', title='About')

@main.route('/contact')
def contact():
    return render_template('main/contact.html', title='Contact')

@main.route('/privacy')
def privacy():
    return render_template('main/privacy.html', title='Privacy Policy')


@main.route('/terms')
def terms():
    return render_template('main/terms.html', title='Terms of Service', current_date=datetime.utcnow())