from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

import pandas as pd

from database.db import Db
from ssvc.ssvc_score_evaluator import SsvcEvaluationResult
from ssvc.utils import from_json
from tasking import submit_task


@dataclass
class TaskResult:
    created_time: datetime
    cve_id: str
    notes: str
    result: Optional[SsvcEvaluationResult]


@dataclass
class Task:
    id: str
    created_time: datetime
    modified_time: datetime
    status: str
    data: Optional[dict]
    results: List[TaskResult]

    @classmethod
    def from_dataframe(cls, df):
        # First row for task data
        first = df.iloc[0]

        # Check if result columns exist in the dataframe
        required_result_columns = {'result_created_time', 'cve_id', 'notes', 'result'}
        has_result_columns = all(col in df.columns for col in required_result_columns)

        results = []
        if has_result_columns:
            results = [
                TaskResult(r['result_created_time'], r['cve_id'], r['notes'],
                           None if r['result'] is None else from_json(r['result'], SsvcEvaluationResult))
                for _, r in df.iterrows() if r['result_created_time'] is not None
            ]

        return cls(
            first['id'], first['created_time'], first['modified_time'],
            first['status'], None if 'data' not in first else first['data'], results
        )

    @classmethod
    def from_tasks_dataframe(cls, df: pd.DataFrame) -> List['Task']:
        """
        Convert a dataframe containing multiple tasks into a list of Task instances.
        Each task and its associated results are grouped by task ID.

        Args:
            df: DataFrame containing one or more tasks with their results

        Returns:
            List[Task]: List of Task instances
        """
        return [
            cls.from_dataframe(group_df)
            for _, group_df in df.groupby('id')
        ]


class SsvcTaskService:
    def list(self) -> List[Task]:
        with Db() as db:
            data = db.query(
                """
               SELECT t.id,
                       t.created_time,
                       t.modified_time,
                       t.status
                FROM tasks t
                WHERE t.type = 'ssvc_bulk_evaluation'
                """,
                index_column=None
            )

        if len(data) == 0:
            return []

        return Task.from_tasks_dataframe(data)

    def get(self, task_id: str) -> Optional[Task]:
        with Db() as db:
            data = db.query(
                """
               SELECT t.id,
                       t.created_time,
                       t.modified_time,
                       t.status,
                       t.data,
                       srtl.created_time AS result_created_time,
                       srtl.cve_id       AS cve_id,
                       srtl.notes        AS notes,
                       sr.result         AS result
                FROM tasks t
                         LEFT JOIN ssvc_result_task_links srtl ON t.id = srtl.task_id
                         LEFT JOIN ssvc_results sr ON srtl.result_id = sr.id
                WHERE t.id = %s
                  AND t.type = 'ssvc_bulk_evaluation'
                """,
                data=(task_id,),
                index_column=None
            )

        if len(data) == 0:
            return None

        return Task.from_tasks_dataframe(data)[0]

    def submit(self, df: pd.DataFrame, reevaluate: bool = False):
        cve_list = list(set(x.strip().upper() for x in df.values[:, 0]))
        return submit_task('ssvc_bulk_evaluation', [cve_list, reevaluate], data=cve_list)
