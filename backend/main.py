from flask import Flask
from flask_cors import CORS
from markupsafe import escape
from dotenv import load_dotenv

from database.db import Db
from database.migration_manager import MigrationManager
from ssvc_score_evaluator import SsvcScoreEvaluator
from utils import dataclass_to_camelcase_dict

load_dotenv()

# Apply database migrations
migration_manager = MigrationManager(Db(), 'database/migrations')
migration_manager.migrate()

app = Flask(__name__)

cors = CORS(app, resources={
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
    ssvc = SsvcScoreEvaluator()
    result = ssvc.evaluate(escape(cve_id))
    return dataclass_to_camelcase_dict(result)
