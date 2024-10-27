import os
import hashlib
from typing import List, Dict
import logging

import pandas as pd

from app.ssvc.database.db import Db
from app.ssvc.database.sql_parser import SQLParser

logging.basicConfig(level=logging.INFO)


class MigrationManager:
    def __init__(self, db: Db, migrations_dir: str):
        """
        Initialize the migration manager.

        Args:
            db: Database connection class instance
            migrations_dir: Directory containing migration files
        """
        self._db = db
        self._migrations_dir = migrations_dir
        self._ensure_migrations_table()

    def _ensure_migrations_table(self):
        """Create migrations table if it doesn't exist."""
        with self._db as db:
            db.execute("""
                CREATE TABLE IF NOT EXISTS migrations (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    hash VARCHAR(64) NOT NULL,
                    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def _get_applied_migrations(self) -> Dict[str, str]:
        """Get all applied migrations and their hashes."""
        with self._db as db:
            df = db.query(
                "SELECT name, hash FROM migrations ORDER BY applied_at",
                index_column=None
            )
            if len(df) == 0:
                return dict()
            return dict(zip(df['name'], df['hash']))

    def _get_migration_files(self) -> List[str]:
        """Get all migration files from migrations directory."""
        if not os.path.exists(self._migrations_dir):
            os.makedirs(self._migrations_dir)

        files = []
        for file in os.listdir(self._migrations_dir):
            if file.endswith('.sql'):
                files.append(file)
        return sorted(files)

    def _calculate_file_hash(self, filename: str) -> str:
        """Calculate SHA-256 hash of migration file."""
        filepath = os.path.join(self._migrations_dir, filename)
        with open(filepath, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()

    def _apply_migration(self, filename: str):
        """Apply a single migration file."""
        filepath = os.path.join(self._migrations_dir, filename)
        file_hash = self._calculate_file_hash(filename)

        with open(filepath, 'r') as f:
            sql = f.read()

        with self._db as db:
            try:
                # Start transaction
                db.begin()

                # Execute migration
                parser = SQLParser(sql)
                for statement in parser.parse_statements():
                    if statement.strip():
                        print('=====')
                        print(statement)
                        print('=====')
                        db.execute(statement)

                # Record migration
                db.execute(
                    "INSERT INTO migrations (name, hash) VALUES (%s, %s)",
                    (filename, file_hash)
                )

                # Commit transaction
                db.commit()
                logging.info(f"Applied migration: {filename}")

            except Exception as e:
                db.rollback()
                logging.error(f"Error applying migration {filename}: {str(e)}")
                raise

    def migrate(self):
        """Apply all pending migrations."""
        applied_migrations = self._get_applied_migrations()
        migration_files = self._get_migration_files()

        for filename in migration_files:
            if filename not in applied_migrations:
                self._apply_migration(filename)
            else:
                # Verify hash of applied migration hasn't changed
                current_hash = self._calculate_file_hash(filename)
                if current_hash != applied_migrations[filename]:
                    raise ValueError(
                        f"Migration {filename} has been modified after being applied"
                    )

        logging.info("All migrations applied successfully")

    def get_migration_status(self) -> pd.DataFrame:
        """Get status of all migrations."""
        with self._db as db:
            applied = db.query("""
                SELECT 
                    name,
                    hash,
                    applied_at
                FROM migrations 
                ORDER BY id
            """, index_column=None)

            all_files = pd.DataFrame({
                'name': self._get_migration_files()
            })

            # Merge to get status of all files
            if len(applied) == 0:
                status = all_files.copy()
                status['hash'] = None
                status['applied_at'] = None
            else:
                status = all_files.merge(
                    applied,
                    on='name',
                    how='left'
                )

            # Add current hash and status columns
            status['current_hash'] = status['name'].apply(self._calculate_file_hash)
            status['status'] = status.apply(
                lambda x: 'modified' if pd.notna(x['hash']) and x['hash'] != x['current_hash']
                else 'pending' if pd.isna(x['hash'])
                else 'applied',
                axis=1
            )

            return status
