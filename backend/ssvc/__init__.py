from ssvc.database.db import Db
from ssvc.database.migration_manager import MigrationManager

migration_manager = MigrationManager(Db(), 'ssvc/database/migrations')
migration_manager.migrate()
