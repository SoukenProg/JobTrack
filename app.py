import os
from pathlib import Path
from flask import Flask, render_template
from models import db

from routes.dashboard import bp as dashboard_bp
from routes.companies import bp as company_bp

def create_app():
    app = Flask(__name__)
    database_path = Path(app.instance_path) / "JobTracker.db"
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-change-me"),
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{database_path}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    db.init_app(app)

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(company_bp)
    with app.app_context():
        db.create_all()
    return app
if __name__ == '__main__':
    app = create_app()