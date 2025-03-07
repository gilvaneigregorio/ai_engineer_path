import glob
import os
from typing import Dict

from sqlalchemy import text

from utils.logging import logger
from utils.relational_database import get_session


class Migration:
    def run(self):
        try:
            logger.info("Running migrations")
            self.db_session = next(get_session())

            migrations = self._get_migrations()

            current_version = self._get_current_version()
            logger.info(f"current_version: {current_version}")
            while True:
                next_version = self._get_next_version(current_version)

                if next_version not in migrations:
                    break

                migration = migrations[next_version]
                self._run_migration(migration)
                self._update_current_version(next_version)
                current_version = next_version

                self.db_session.commit()
            logger.info("Migration finished, database is up to date")
        except Exception as e:
            self.db_session.rollback()
            logger.error(f"Error running migrations: {e}")
            raise
        finally:
            self.db_session.close()

    def _get_migrations(self) -> Dict:
        version_folder = os.path.dirname(os.path.realpath(__file__))
        versions_folder = os.path.join(version_folder, "versions")

        files = glob.glob(os.path.join(versions_folder, "*"))
        # order files by name
        files.sort()

        result = {}
        for file in files:
            key = int(os.path.basename(file).split("_")[0])
            value = file
            result[key] = value
        logger.info(f"migrations found: {len(result)}")
        return result

    def _has_migration_version_table(self) -> bool:
        statement = text("SELECT * FROM migrations")
        try:
            self.db_session.execute(statement)
            return True
        except Exception as e:
            logger.error(f"Error checking migration version table: {e}")
            self.db_session.rollback()
            return False

    def _create_migration_version_table(self) -> None:
        statement = text("CREATE TABLE migrations (version_num VARCHAR(32) NOT NULL)")
        self.db_session.execute(statement)

        statement = text("INSERT INTO migrations (version_num) VALUES (:version_num)")
        self.db_session.execute(statement, {"version_num": 0})

    def _get_current_version(self) -> int:
        if not self._has_migration_version_table():
            self._create_migration_version_table()
            return 0

        statement = text("SELECT * FROM migrations")
        result = self.db_session.execute(statement).scalar_one_or_none()
        if not result:
            return 0
        return int(result)

    def _get_next_version(self, current_version) -> int:
        return current_version + 1

    def _run_migration(self, migration):
        logger.info(f"running migration: {migration}")
        with open(migration, "r") as f:
            sql_commands = f.read()
            self.db_session.execute(text(sql_commands))
        return True

    def _update_current_version(self, next_version):
        statement = text("UPDATE migrations SET version_num = :version_num")
        self.db_session.execute(statement, {"version_num": next_version})
