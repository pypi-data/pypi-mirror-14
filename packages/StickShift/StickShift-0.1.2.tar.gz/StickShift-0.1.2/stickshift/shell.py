import click
from migration_repository import MigrationRepository
from database_manager import DatabaseManager


@click.command()
@click.argument("fn", nargs=1)
@click.argument("sub_fn", nargs=-1)
def shell(fn, sub_fn):
    if fn == "setup":
        setup()
    if fn == "clear":
        clear()
    elif fn == "new":
        new(sub_fn)
    elif fn == "alter":
        alter(sub_fn)
    elif fn == "db":
        database(sub_fn)


def setup():
    MigrationRepository.create_repository()


def clear():
    MigrationRepository.clear()


def new(sub_fn=None):
    if len(sub_fn) > 1:
        if MigrationRepository.is_repository_setup():
            new_type = sub_fn[0]
            new_name = sub_fn[1]
            if new_type is None:
                print("Invalid type")
                return
            if new_name is None:
                print("Invalid name")
                return
            if new_type == "table":
                MigrationRepository.create_new_table_migration(name=new_name)
            elif new_type == "procedure":
                MigrationRepository.create_new_procedure_migration(name=new_name)
        else:
            print("Migration is not setup")
    else:
        print("Invalid number of arguments")


def alter(sub_fn=None):
    if len(sub_fn) > 1:
        if MigrationRepository.is_repository_setup():
            table_name = sub_fn[0]
            table_change = sub_fn[1]
            migration_name = "{0}_{1}".format(table_name, table_change)
            MigrationRepository.create_new_table_alteration_migration(name=migration_name)
        else:
            print("Migration is not setup")
    else:
        print("Invalid number of arguments")


def database(sub_fn=None):
    if MigrationRepository.is_repository_setup():
        if sub_fn is not None:
            environment = None
            if len(sub_fn) == 2:
                environment = sub_fn[1]
            database_manager = DatabaseManager(MigrationRepository.database_config(environment))
            if database_manager.connection is not None:
                if sub_fn[0] == "provision":
                    database_manager.provision_database()
                elif sub_fn[0] == "deprovision":
                    database_manager.deprovision_database()
                elif sub_fn[0] == "version":
                    database_manager.list_database_current_version()
                elif sub_fn[0] == "versions":
                    database_manager.list_database_versions()
                elif sub_fn[0] == "procedures":
                    database_manager.list_procedures()
                elif sub_fn[0] == "tables":
                    database_manager.list_tables()
                elif sub_fn[0] == "upgrade" or sub_fn[0] == "migrate":
                    database_manager.upgrade()
                elif sub_fn[0] == "downgrade":
                    database_manager.downgrade()
                elif sub_fn[0] == "reset":
                    database_manager.reset()
                else:
                    print("invalid database command")
        else:
            print("invalid database command")
