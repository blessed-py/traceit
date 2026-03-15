from functools import wraps
from flask import session, redirect, url_for, request, flash, g
from app.Database.database import DatabaseManager
from datetime import datetime

db_manager = DatabaseManager()

def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            # remember where user wanted to go
            next_url = request.path
            return redirect(url_for('auth.login', next=next_url))
        
        # Load current user and store in g
        g.current_user = db_manager.get_user_by_id(user_id)
        if not g.current_user:
            # if somehow the user_id is invalid, log out
            session.clear()
            return redirect(url_for('auth.login'))
        
        return view_func(*args, **kwargs)
    return wrapper


def roles_required(*roles):
    """Ensure the logged-in user has one of the required roles.
    Usage: @roles_required('Admin', 'SYSTEM MAINTAINER')
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            user = getattr(g, 'current_user', None)
            if not user:
                return redirect(url_for('auth.login'))

            user_role = user.get('user_role')
            if roles and user_role not in roles:
                flash('You are not authorized to access that resource.', 'danger')
                return redirect(url_for('dashboard.dashboard'))
            return view_func(*args, **kwargs)
        return wrapper
    return decorator

def time_ago(date_found, time_found=None):

    if time_found:
        dt = datetime.combine(date_found, time_found)
    else:
        dt = datetime.combine(date_found, datetime.min.time())

    now = datetime.now()
    diff = now - dt

    days = diff.days
    seconds = diff.seconds

    if days > 0:
        return f"{days} day{'s' if days > 1 else ''} ago"
    elif seconds >= 3600:
        hours = seconds // 3600
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    elif seconds >= 60:
        minutes = seconds // 60
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    else:
        return "Just now"