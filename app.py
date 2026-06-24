import os
from pathlib import Path
from flask import Flask, render_template
from models import db


app = Flask(__name__)
database_path = Path(app.instance_path) / "JobTracker.db"
app.config.from_mapping(
    SECRET_KEY=os.environ.get("SECRET_KEY", "dev-change-me"),
    SQLALCHEMY_DATABASE_URI=f"sqlite:///{database_path}",
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)
Path(app.instance_path).mkdir(parents=True, exist_ok=True)
db.init_app(app)

# モックデータ
stats ={
    "companies": 0,
    "active": 0,
    "interview":0,
    "success":0,
}
@app.route('/')
def top():
    return render_template('index.html',stats=stats)

if __name__ == '__main__':
    app.run()
