"""
StockIQ - AI-Powered Stock Intelligence Platform
Application factory and configuration
"""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name="default"):
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # ── Configuration ──────────────────────────────────────────────────────────
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key-change-in-prod")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "sqlite:///stockiq.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # FIX 1: removed sslmode — that's PostgreSQL only, crashes SQLite locally
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }

    # ── Extensions ─────────────────────────────────────────────────────────────
    db.init_app(app)
    migrate.init_app(app, db)

    # ── Template Helpers ───────────────────────────────────────────────────────
    from app.template_helpers import register_template_helpers
    register_template_helpers(app)

    # ── Blueprints ─────────────────────────────────────────────────────────────
    from app.routes.main import main_bp
    from app.routes.api import api_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    
    app.register_blueprint(admin_bp, url_prefix="/api/admin")

    return app