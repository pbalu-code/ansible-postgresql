import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_pgsql_is_listening(host):
    pgsql = host.socket('tcp://0.0.0.0:5432')
    assert pgsql.is_listening


def test_pgsql_db(host):
    psql_cmd1 = host.run(
        "PGPASSWORD=secret123 psql -U bull -h 127.0.0.1 \
        -p 5432 -w -d postgres -c 'SELECT * FROM pg_catalog.pg_tables;'"
    )
    psql_cmd2 = host.run(
        "PGPASSWORD=secret123 psql -U bull -h 127.0.0.1 \
        -p 5432 -w -d demo -c 'SELECT datcollate AS collation FROM \
        pg_database WHERE datname = current_database();'"
    )
    #psql_cmd2 = host.run(
    #    "PGPASSWORD=secret123 psql -U bull -h 127.0.0.1 \
    #    -p 5432 -w -d demo -c 'CREATE TABLE accounts \
    #    (user_id serial PRIMARY KEY, username VARCHAR \
	#     ( 50 ) UNIQUE NOT NULL, password VARCHAR ( 50 ) NOT NULL, \
	#        email VARCHAR ( 255 ) UNIQUE NOT NULL);'"
    #)
    #psql_cmd3 = host.run(
    #    "PGPASSWORD=secret123 psql -U bull -h 127.0.0.1 \
    #    -p 5432 -w -d demo -c \"INSERT into accounts(username, password, email) \
    #    VALUES ('bull01', 'secret01', 'bull01@local.net');\""
    #)
    #psql_cmd3 = host.run(
    #    "PGPASSWORD=secret123 psql -U bull -h 127.0.0.1 \
    #    -p 5432 -w -d demo -c 'DROP TABLE IF EXISTS accounts;'"
    #)
    assert psql_cmd1.rc == 0
    assert psql_cmd2.rc == 0
    #assert psql_cmd3.rc == 0

#def test_replication_pass_removed(host):
#    exists = host.file('/var/lib/pgsql/.pgpass').exists
#    if exists:
#        contains = host.file('/var/lib/pgsql/.pgpass').contains('heslojakcyp')
#    else:
#        contains = False
#    assert not contains


#def test_pgsql_extensions(host):
#    psql_cmd = host.run(
#        "PGPASSWORD=secret123 psql -U bull -d prematch "
#        "-h 127.0.0.1 -p 5432 -w -c '\dx'"
#    )
#    assert psql_cmd.rc == 0
#    assert 'dblink' in psql_cmd.stdout
#    assert 'file_fdw' in psql_cmd.stdout
