import re

from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.utils import dataclass_to_camelcase_dict

load_dotenv('./.env.dev')


def create_app() -> FastAPI:
    # Apply db migrations.
    from database.db import Db
    from database.migration_manager import MigrationManager

    migration_manager = MigrationManager(Db(), 'database/migrations')
    migration_manager.migrate()

    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:4300"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Create the endpoints.
    @app.get('/query/{cve_id}')
    def query(cve_id: str, reevaluate: bool = False):
        # Ensure that we have a valid cve_id:
        cve_id = cve_id.upper().strip()
        pattern = r'^(?:CVE|GO|HSEC|PYSEC)-\d{4}-\d{1,7}$'
        if not bool(re.match(pattern, cve_id)):
            raise HTTPException(400, detail='Invalid cve id format.')

        from ssvc.ssvc_score_evaluator import SsvcScoreEvaluator
        ssvc = SsvcScoreEvaluator()
        result = ssvc.evaluate(cve_id, reevaluate)

        if result is None:
            raise HTTPException(400, detail='Could not evaluate the cve.')

        return dataclass_to_camelcase_dict(result[1])

    return app
