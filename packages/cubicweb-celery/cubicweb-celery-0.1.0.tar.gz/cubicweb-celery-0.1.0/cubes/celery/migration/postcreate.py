import os

if config.system_source_config['db-driver'] == 'postgres':
    d = os.path.dirname(__file__)

    sql(open(os.path.join(d, 'table.sql'), 'r').read())
    sql(open(os.path.join(d, 'ddl.sql'), 'r').read())
