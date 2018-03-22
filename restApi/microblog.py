from app import app, db
from app.models import User, Post

#for manking "flask shell" work from venv, working with db easier
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}