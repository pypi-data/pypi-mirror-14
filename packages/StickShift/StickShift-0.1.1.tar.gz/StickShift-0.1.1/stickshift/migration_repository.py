import os
import sys
import shutil
from natsort import natsorted

python_version = sys.version_info.major
if python_version == 3:
    from configparser import ConfigParser, NoOptionError, NoSectionError
else:
    from ConfigParser import ConfigParser, NoOptionError, NoSectionError

DB_DIR = "db"
DB_CONFIG_PATH = "db/database.ini"
DB_CONFIG_FILE_CONTENTS = "[DATABASE]" \
                          "\nhost: DB_HOST" \
                          "\nport: DB_PORT" \
                          "\nusername: DB_USERNAME" \
                          "\npassword: DB_PASSWORD" \
                          "\ndatabase: DB_NAME\n"
DB_UPGRADE_DIR = "db/upgrade"
DB_DOWNGRADE_DIR = "db/downgrade"


def parse_environment_variable(text):
    import re
    matches = re.findall(r'\[(.*?)\]', text)
    return matches


class MigrationRepository(object):

    @staticmethod
    def is_repository_setup():
        return os.path.exists(DB_DIR)

    @staticmethod
    def clear():
        if MigrationRepository.is_repository_setup():
            shutil.rmtree(DB_DIR)
            print("Migration Repository cleared")
            return True
        else:
            print("Migration Repository not setup")
            return False

    @staticmethod
    def create_repository():
        if not MigrationRepository.is_repository_setup():
            os.mkdir(DB_DIR)
            os.mkdir(DB_UPGRADE_DIR)
            os.mkdir(DB_DOWNGRADE_DIR)
            config_file = open(DB_CONFIG_PATH, 'a')
            config_file.write(DB_CONFIG_FILE_CONTENTS)
            config_file.close()
            print("Migration Repository created")
            return True
        else:
            print("Migration Repository already setup")
            return False

    @staticmethod
    def database_config(environment=None):
        config = ConfigParser()
        config.read(DB_CONFIG_PATH)
        if environment is None:
            return None
        database_map = config.options(environment)
        dict_map = {}
        for option in database_map:
            try:
                config_value = config.get(environment, option)
                environment_values = parse_environment_variable(config_value)
                if len(environment_values) > 0:
                    config_value = os.environ[environment_values[0]]
                dict_map[option] = config_value
            except NoSectionError as sectionError:
                print("exception:{0} on {1}".format(sectionError, option))
                dict_map[option] = None
            except NoOptionError as optionError:
                print("exception:{0} on {1}".format(optionError, option))
                dict_map[option] = None
        return dict_map

    @staticmethod
    def current_migration_count():
        return len(MigrationRepository.current_migrations_list())

    @staticmethod
    def current_downgrade_count():
        return len(MigrationRepository.current_downgrade_list())

    @staticmethod
    def current_migrations_list():
        return natsorted(os.listdir(DB_UPGRADE_DIR))

    @staticmethod
    def current_downgrade_list():
        return natsorted(os.listdir(DB_DOWNGRADE_DIR))

    @staticmethod
    def create_new_table_migration(name=None):
        if name:
            migration_count = MigrationRepository.current_migration_count()
            MigrationRepository.create_migration(name="create_table_{0}".format(name),
                                                 contents="CREATE TABLE IF NOT EXISTS {0} ()".format(name),
                                                 migration_index=migration_count)
            MigrationRepository.create_migration(name="drop_table_{0}".format(name),
                                                 contents="DROP TABLE IF EXISTS {0} CASCADE;".format(name),
                                                 directory=DB_DOWNGRADE_DIR,
                                                 migration_index=migration_count)

    @staticmethod
    def create_new_table_alteration_migration(name=None):
        if name:
            migration_count = MigrationRepository.current_migration_count()
            MigrationRepository.create_migration(name="alter_table_{0}".format(name),
                                                 contents="/* Insert Table Alter statements here*/",
                                                 migration_index=migration_count)
            MigrationRepository.create_migration(name="undo_alter_table_{0}".format(name),
                                                 directory=DB_DOWNGRADE_DIR,
                                                 migration_index=migration_count)

    @staticmethod
    def create_new_procedure_migration(name=None):
        if name:
            migration_count = MigrationRepository.current_migration_count()
            MigrationRepository.create_migration(name="create_sp_{0}".format(name),
                                                 contents="CREATE OR REPLACE FUNCTION sp_{0} \n(\n\n) \n\nRETURNS RETURN_TYPE \n(\n) AS $$ "
                                                          "\n\nBEGIN \n\nEND; $$ LANGUAGE plpgsql;".format(name),
                                                 migration_index=migration_count)
            MigrationRepository.create_migration(name="drop_sp_{0}".format(name),
                                                 contents="DROP FUNCTION IF EXISTS sp_{0};".format(name),
                                                 directory=DB_DOWNGRADE_DIR,
                                                 migration_index=migration_count)

    @staticmethod
    def create_migration(name=None,
                         contents=None,
                         directory=DB_UPGRADE_DIR,
                         migration_index=0):
        if migration_index< 10:
            migration_prefix = "V0{0}__".format(migration_index)
        else:
            migration_prefix = "V{0}__".format(migration_index)

        migration_file_name = migration_prefix + name + ".sql"
        migration_path = directory + "/" + migration_file_name
        print("Created migration:{0}".format(migration_path))
        migration_file = open(migration_path, 'a')
        if contents is not None:
            migration_file.write(contents)
        migration_file.close()
