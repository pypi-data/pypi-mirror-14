def create_table_drop_query(table_name):
    return "DROP TABLE IF EXISTS {0} CASCADE;".format(table_name)


def query_function_drop_command(function_name):
    return "SELECT format('DROP FUNCTION %s(%s);', oid::regproc, pg_get_function_identity_arguments(oid)) " \
           "FROM   pg_proc " \
           "WHERE  proname = '{0}' " \
           "AND    pg_function_is_visible(oid);".format(function_name)


QUERY_LIST_FUNCTIONS = "SELECT routine_name " \
                       "FROM information_schema.routines " \
                       "WHERE routine_type='FUNCTION' " \
                       "AND specific_schema='public';"

QUERY_LIST_TABLES = "SELECT table_name " \
                    "FROM information_schema.tables " \
                    "WHERE table_schema = 'public';"

QUERY_CREATE_MIGRATION_TABLE = 'CREATE TABLE IF NOT EXISTS "version_migration" ' \
                               '(version INTEGER, migrated_at INTEGER DEFAULT EXTRACT(EPOCH FROM CURRENT_TIMESTAMP));'

QUERY_DROP_MIGRATION_TABLE = 'DROP TABLE IF EXISTS "version_migration";'

QUERY_DATABASE_MIGRATIONS_TABLE_EXISTS = "SELECT EXISTS (" \
                                             "SELECT 1 " \
                                             "FROM information_schema.tables " \
                                             "WHERE table_schema = 'public' AND table_name = 'version_migration'" \
                                         ");"
QUERY_DATABASE_CURRENT_VERSION = "SELECT MAX(version) FROM version_migration"

QUERY_DATABASE_INSERT_MIGRATION = "INSERT INTO version_migration(version) VALUES({0});"

QUERY_DATABASE_DELETE_MIGRATION = "DELETE FROM version_migration WHERE version = {0};"

QUERY_DATABASE_MIGRATION_VERSIONS = "SELECT * FROM version_migration;"

QUERY_RESET_DATABASE_MIGRATION_TABLE = create_table_drop_query("version_migration")
