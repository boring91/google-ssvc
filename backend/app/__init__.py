from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from markupsafe import escape

from app.utils import dataclass_to_camelcase_dict
from config import Config

load_dotenv('./.env.dev')


def create_app(config_class=Config):
    from database.db import Db
    from database.migration_manager import MigrationManager

    migration_manager = MigrationManager(Db(), 'database/migrations')
    migration_manager.migrate()

    app = Flask(__name__)
    app.config.from_object(config_class)

    CORS(app, resources={
        r"/*": {
            "origins": [
                "http://localhost:4300",
            ],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })

    @app.route('/query/<string:cve_id>')
    def query(cve_id: str):
        from ssvc.ssvc_score_evaluator import SsvcScoreEvaluator
        ssvc = SsvcScoreEvaluator()
        result = ssvc.evaluate(escape(cve_id))
        return {} if result is None else dataclass_to_camelcase_dict(result)

    return app
