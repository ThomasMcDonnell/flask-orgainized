from app import app, db
from app.models import User, Todo


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, user=User, todo=Todo) 
