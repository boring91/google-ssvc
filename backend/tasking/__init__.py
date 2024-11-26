import json
import os
import re
import uuid
from typing import Literal, List, Optional

from . import config

from celery import Celery
from celery.signals import *

from database.db import Db

app = Celery(broker=f'pyamqp://guest@{os.getenv("RABBITMQ_HOST")}')


def submit_task(
        task_type: Literal['ssvc_bulk_evaluation'],
        args: List,
        data: Optional[any] = None) -> str:
    with Db() as db:
        task_id = str(uuid.uuid4())
        db.execute("INSERT INTO tasks(id, type, data) VALUES(%s, %s, %s)",
                   (task_id, task_type, None if data is None else json.dumps(data)))

    if task_type == 'ssvc_bulk_evaluation':
        ssvc_bulk_evaluation.apply_async(args=args, task_id=task_id)

    return task_id


@task_prerun.connect
def handler(task_id, task, *args, **kwargs):
    with Db() as db:
        db.execute(
            'UPDATE tasks SET status = %s WHERE id = %s',
            ('running', task_id)
        )


@task_postrun.connect
def task_postrun_handler(task_id, task, *args, **kwargs):
    state = kwargs['state']
    with Db() as db:
        db.execute(
            'UPDATE tasks SET status = %s WHERE id = %s',
            ('succeeded' if state == 'SUCCESS' else 'failed', task_id)
        )


@app.task(bind=True)
def ssvc_bulk_evaluation(self, cve_list: List[str], reevaluate: bool = False):
    task_id: str = self.request.id

    from ssvc.ssvc_score_evaluator import SsvcScoreEvaluator
    ssvc = SsvcScoreEvaluator()

    for cve_id in cve_list:
        # check if the cve is evaluated for this task.
        with Db() as db:
            result = db.first('SELECT * FROM ssvc_result_task_links WHERE task_id=%s AND cve_id=%s',
                              (task_id, cve_id))
            if result is not None:
                continue

        # Check if valid cve:
        pattern = r'^(?:CVE|GO|HSEC|PYSEC)-\d{4}-\d{1,7}$'
        if not bool(re.match(pattern, cve_id)):
            with Db() as db:
                db.execute(
                    """
                    INSERT INTO ssvc_result_task_links(task_id, cve_id, notes)
                    VALUES(%s, %s, %s)
                    """,
                    (task_id, cve_id, 'Invalid cve id format.'))
                continue

        # Evaluate
        result = ssvc.evaluate(cve_id, reevaluate)

        if result is None:
            with Db() as db:
                db.execute(
                    """
                    INSERT INTO ssvc_result_task_links(task_id, cve_id, notes)
                    VALUES(%s, %s, %s)
                    """,
                    (task_id, cve_id, 'Could not evaluate the cve.'))
                continue

        with Db() as db:
            db.execute(
                """
                INSERT INTO ssvc_result_task_links(task_id, cve_id, result_id)
                VALUES(%s, %s, %s)
                """,
                (task_id, cve_id, result[0])
            )
