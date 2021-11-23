ansible-postgresql v2.1.4
===========
Ansible role to install postgresql server on Centos/Redhat 7 - 8 , Ubuntu 18-20

###Tested:
- Centos7
- Centos8 
- Ubuntu18
- Ubuntu20

###PostgreSQL:
- 9.6
- 10
- 11
- 12
- 13
- 14

###Replication tested:  
**Postgresql: 12, 13, 14**

### No pg_repack for centos for version 14 of postgresql 

###Test enivonment:
**molecule:**
- vagrant: (Centos7-8, Ubuntu18-20)
- docker: Centos8

Extra features
--------------
 - ssl
 - postgis  # broken 
 - pg_rman
 - pg_audit
 - replication


About
--------
An [Ansible][ansible] role for installing and managing [PostgreSQL][postgresql] servers. This role works with both
Debian and RedHat based systems.

On RedHat-based platforms, the [PostgreSQL Global Development Group (PGDG) packages][pgdg_yum] packages will be
installed. On Debian-based platforms, you can choose from the distribution's packages (from APT) or the [PGDG
packages][pgdg_apt].

[ansible]: http://www.ansible.com/
[postgresql]: http://www.postgresql.org/
[pgdg_yum]: http://yum.postgresql.org/
[pgdg_apt]: http://apt.postgresql.org/

**Changes that require a restart will not be applied unless you manually restart PostgreSQL.** This role will reload the
server for those configuration changes that can be updated with only a reload because reloading is a non-intrusive
operation, but options that require a full restart will not cause the server to restart.

Requirements
------------

- This role requires Ansible 2.9+

- The language settings should be correct, LANG, LC_* variables should be defined!!

Role tags
--------------
genlocales - Generate locales ( Ubuntu only )  



Role Variables
--------------

### All variables are optional but... ###

- `postgresql_user_name`: System username to be used for PostgreSQL (default: `postgres`).

- `postgresql_version`: PostgreSQL version to install.The default is `12`.
  
- `postgresql_conf`: A list of hashes (dictionaries) of `postgresql.conf` options (keys) and values. These options are
  not added to `postgresql.conf` directly - the role adds a `conf.d` subdirectory in the configuration directory and an
  include statement for that directory to `postgresql.conf`. Options set in `postgresql_conf` are then set in
  `conf.d/25ansible_postgresql.conf`. For legacy reasons, this can also be a single hash, but the list syntax is
  preferred because it preserves order.

  Due to YAML parsing, you must take care when defining values in
  `postgresql_conf` to ensure they are properly written to the config file. For
  example:

  ```yaml
  postgresql_conf:
      - listen_addresses: "'0.0.0.0'"
      - max_connections: '200'       # decrease connection limit
      - password_encryption: 'scram-sha-256'
      - max_wal_senders: 5
      - max_replication_slots: 5
      - ssl: "on"
      - ssl_ca_file: "'{{ postgresql_conf_dir }}/{{ postgresql_ssl_ca }}'"
      - ssl_cert_file: "'{{ postgresql_conf_dir }}/{{ postgresql_ssl_crt }}'"
      - ssl_key_file: "'{{ postgresql_conf_dir }}/{{ postgresql_ssl_key }}'"
      - ssl_ciphers: "'HIGH:MEDIUM:+3DES:!aNULL'"
      # ssl_dh_params_file - not exists in 9.6, 10(Centos)
      - ssl_dh_params_file: "'{{ postgresql_conf_dir }}/{{ postgresql_ssl_dh }}'"
      - ssl_prefer_server_ciphers: "on"
      - ssl_min_protocol_version: 'TLSv1.1'  # not exists in 9.6
      - ssl_max_protocol_version: 'TLSv1.2'  # not exists in 9.6
      - log_destination: "'syslog'"
      - log_filename: "'postgresql-%a.log'"
      - syslog_facility: "'LOCAL0'"
      - syslog_ident: "'postgres'"
      - syslog_sequence_numbers: on
      - syslog_split_messages: on
  ```

  Becomes the following in `25ansible_postgresql.conf`:

  ```
    
    listen_addresses = '0.0.0.0'
    max_connections = 200
    password_encryption = scram-sha-256
    max_wal_senders = 5
    max_replication_slots = 5
    ssl = on
    ssl_ca_file = '/var/lib/pgsql/13/data/root.crt'
    ssl_cert_file = '/var/lib/pgsql/13/data/postgres.crt'
    ssl_key_file = '/var/lib/pgsql/13/data/postgres.key'
    ssl_ciphers = 'HIGH:MEDIUM:+3DES:!aNULL'
    ssl_dh_params_file = '/var/lib/pgsql/13/data/postgres_dh.crt'
    ssl_prefer_server_ciphers = on
    ssl_min_protocol_version = TLSv1.1
    ssl_max_protocol_version = TLSv1.2
    log_destination = 'syslog'
    log_filename = 'postgresql-%a.log'
    syslog_facility = 'LOCAL0'
    syslog_ident = 'postgres'
    syslog_sequence_numbers = True
    syslog_split_messages = True


  ```

- `postgresql_pg_hba_conf`: A list of lines to add to `pg_hba.conf`

- `postgresql_pg_hba_local_postgres_user`: If set to `false`, this will remove the `postgres` user's entry from
  `pg_hba.conf` that is preconfigured on Debian-based PostgreSQL installations. You probably do not want to do this
  unless you know what you're doing.

- `postgresql_pg_hba_local_socket`: If set to `false`, this will remove the `local` entry from `pg_hba.conf` that is
  preconfigured by the PostgreSQL package.

- `postgresql_pg_hba_local_ipv4`: If set to `false`, this will remove the `host ... 127.0.0.1/32` entry from
  `pg_hba.conf` that is preconfigured by the PostgreSQL package.

- `postgresql_pg_hba_local_ipv6`: If set to `false`, this will remove the `host ... ::1/128` entry from `pg_hba.conf`
  that is preconfigured by the PostgreSQL package.

- `postgresql_listen_on_all_ip`: `false` If set `true` this will add `host    all   all   0.0.0.0/0   md5` entry to  `pg_hba.conf`

- `postgresql_network_password_mode`: `md5` Encryption method for networked connections.  
  Values: 
  - trust
  - reject
  - md5
  - password
  - scram-sha-256
  - gss
  - sspi
  - ident
  - peer
  - pam
  - ldap
  - radius
  - cert  

   Note that "password" sends passwords in clear text; "md5" or scram-sha-256" are preferred since they send encrypted passwords.

- `postgresql_install_postgis`: `true/false` Optional parameter if you want to install postgis extension, you can enable this option.  

- `postgresql_posgis_to_install`: `postgis25_12` Declare which version of postgis to be installed.
- `postgresql_posgis_to_install_ubuntu` (string or list): `postgresql-12-postgis-2.5, postgresql-12-postgis-scripts`  Declare which version of postgis to be installed under Ubuntu.
  [Compatibility matrix](https://trac.osgeo.org/postgis/wiki/UsersWikiPostgreSQLPostGIS)

- `postgresql_use_ssl`: boolean This option is turning on/off managing ssl keys transfer. 
    __SSL keys and certs must be placed in inventory_dir/files__  
    For example ..../staging/files/  
  [PostgreSQL SSL runtme configuration](https://www.postgresql.org/docs/12/runtime-config-connection.html#RUNTIME-CONFIG-CONNECTION-SSL)
  
- `postgresql_ssl_curve` (string): `secp384r1` Type of the curve for ssl key generation  
- `postgresql_ssl_size` (number): `4096` SSL Key size (selfsigned)  
- `postgresql_ssl_type` (string): `RSA` SSL key algorithm  # DSA  ECC  Ed25519  Ed448  RSA   X25519  X448  
- `postgresql_ssl_key` (string): **`postgresql-key.pem`**  SSL key file's name. This file will be generated or will be copied from the files folder under the inventory's path if it exists. 
- `postgresql_ssl_ca` (string): `postgresql-CA.pem` SSL CA file's name. This file will be generated or will be copied from the files folder under the inventory's path if it exists.
- **`postgresql_ssl_crt`** (string): **`postgresql-ssl.pem`**  SSL cert's name. This file will be generated or will be copied from the files folder under the inventory's path, if it exists. **In this case the selfsigned key and certificate generation will be skipped and the external files will be copied.**
- `postgresql_ssl_common_name` (string): `"pgsql.local"` Common name for SSL cert. (Defalt: invetory_hostname)  
- `postgresql_ssl_alt_name` (list): See the modul's manual "subject alt name" for self signe SSL cert. 
- `postgresql_ssl_organization_name` (string): `"The Big One Organisation Ltd."` Organisation name for SSL cert. 
- `postgresql_ssl_organization_unit_name` (string):`"IT - Who else"` SSL cert - Organisation Unit's name. 
- `postgresql_ssl_DH_size` (number): `2048`  Optional - The size of the Diffie-Hellman Parameters (Default: 4096)
- `postgresql_pgdata`: Only set this if you have changed the `$PGDATA` directory from the package default. Note this
  does not configure PostgreSQL to actually use a different directory, you will need to do that yourself, it just allows
  the role to properly locate the directory.

- `postgresql_conf_dir`: As with `postgresql_pgdata` except for the configuration directory.

- `postgresql_dbs`:  Create databases with these parameters.
    - `name`: database name
    - `password`: (optional) User's password to connect the database
    - `user`: User to connect the current database
    - `priv`: Slash-separated PostgreSQL privileges string: priv1/priv2, where privileges can be defined for database ( allowed options - 'CREATE', 'CONNECT', 'TEMPORARY', 'TEMP', 'ALL'. For example CONNECT ) or for table ( allowed options - 'SELECT', 'INSERT', 'UPDATE', 'DELETE', 'TRUNCATE', 'REFERENCES', 'TRIGGER', 'ALL'. For example table:SELECT ). Mixed example of this string: CONNECT/CREATE/table1:SELECT/table2:INSERT.
    - `ssl_mode`: __Optional__ Determines whether or with what priority a secure SSL TCP/IP connection will be negotiated with the server.
See https://www.postgresql.org/docs/current/static/libpq-ssl.html for more information on the modes.
Default of prefer matches libpq default.  
Choices:
        - allow
        - disable   
        - prefer ← (default)
        - require
        - verify-ca
        - verify-full
    - `encoding`: UTF-8
    - `locale`: en_US.UTF-8
    - `template`: 'template0'  # __optional!!!__ template0 is the default value
    - `lc_collate`: en_US.UTF-8  # __optional!!!__ The default is the `locale` parameter from above. Collation order (LC_COLLATE) to use in the database. Must match collation order of template database unless template0 is used as template.
    - `lc_ctype`: en_US.UTF-8  # __optional!!!__ The default is the `locale` parameter from above.
    - `tablespace`: [Path] # Default: omit The tablespace to set for the database https://www.postgresql.org/docs/current/sql-alterdatabase.html.
If you want to move the database back to the default tablespace, explicitly set this to pg_default. 

- `postgresql_global_users`: __Optional__ Create non database specific users with special rights  
    - `name`: User's login name
    - `password`: (optional) User's password  
    - `role_attr_flags`: PostgreSQL user attributes string in the format: CREATEDB,CREATEROLE,SUPERUSER.  Choices:  
         - [NO]SUPERUSER  
         - [NO]CREATEROLE
         - [NO]CREATEDB
         - [NO]INHERIT
         - [NO]LOGIN
         - [NO]REPLICATION
         - [NO]BYPASSRLS
    - ssl_mode: __Optional__ see before...

- `postgresql_locales`: (list)  - en_US.UTF-8  Ubuntu/Debian only. Generate locales. 
- `postgresql_extra_packages`: (list or string ) - Install optional packages.


Replication
---------------
Tested with PostgreSQL 12, 13

This role is able to create asyncron streaming replication too.
Access rights and the config should be created by config options like postgresql_conf, postgresql_pg_hba_conf ect.  
The authentication is trust / IP based.

Replication related variables:

- `postgresql_standby_slot_name`: string, what should be the name of the replication stream. This is a host related variable. Use it in host variable! 
- `postgresql_init_replication`: boolean Sync standby server to the master by pg_basebackup method. __If the standby.signal file is not present.__ 
- `postgresql_replication_master`: ip/hostname. Will it use during pg_basebackup
 
pg_rman
----------------
_https://github.com/ossc-db/pg_rman_

Variables:
 - `postgresql_install_pg_rman`: `False/True` Turn on pg_rman installation (RPM source, Centos / Rhel 7-8 only)
 - `postgresql_pg_rman_install_from_source`: `True/False` pg_rman is available in rpm and in source from github. `False: rpm will be installed.`, `True: The source will be cloned from the github and compiled.` In this case, all necessary devel packages git, make, zlib, ect. will be installed too.
 - `postgresql_pg_rman_git_repo`: `https://github.com/ossc-db/pg_rman.git` pg_rman source repo. There should be branches like: REL9_3_STABLE, 
REL_12_STABLE, ect.
 - `postgresql_pg_rman_postgres_conf`: `[list]` pg_rman specific postgres config parameters. These are go into `conf.d/26ansible_pg_rman.conf` 
 - `postgresql_pg_rman_ini`: `{dict}`  Configuration parameters for pg_rman.ini "- {option: COMPRESS_DATA, value: 'True'}"

Backups will be saved under postgres home folder/postgresql-version/backups ( {{ postgresql_home }}/{{ postgresql_version }}/backups" )  

For example: `/var/lib/pgsql/12/backups` Under Centos/RedHat  

pg_audit
----------------
_https://www.pgaudit.org/_

Variables:
 - `postgresql_install_pg_audit`: `True/False`
 - `postgresql_pg_audit_postgres_conf`: `[list]` pg_rman specific postgres config parameters. These are go into `conf.d/28ansible_pg_audit.conf` 

The role does install pgaudit packages.

Example Playbook
----------------

Standard install: Default `postgresql.conf`, `pg_hba.conf` and default version for the OS:

```yaml
---
- hosts: dbservers
  remote_user: root
  roles:
    - ansible-postgresql
```


Use the PostgreSQL 13 packages and set some `postgresql.conf` options and `pg_hba.conf` entries:

```yaml
---
- hosts: dbservers
  remote_user: root
  vars:
    postgresql_version: 13
    postgresql_use_ssl: true
    postgresql_ssl_key: postgres.key
    postgresql_ssl_crt: postgres.crt
    postgresql_ssl_dh: postgres_dh.crt  # not exists in 9.6
    postgresql_ssl_ca: root.crt
    postgresql_ssl_DH_size: 2048
    postgresql_network_password_mode: 'scram-sha-256'
    postgresql_conf:
      - listen_addresses: "'0.0.0.0'"
      - max_connections: '200'       # decrease connection limit
      - password_encryption: 'scram-sha-256'
      - max_wal_senders: 5
      - max_replication_slots: 5
      - ssl: "on"
      - ssl_ca_file: "'{{ postgresql_conf_dir }}/{{ postgresql_ssl_ca }}'"
      - ssl_cert_file: "'{{ postgresql_conf_dir }}/{{ postgresql_ssl_crt }}'"
      - ssl_key_file: "'{{ postgresql_conf_dir }}/{{ postgresql_ssl_key }}'"
      - ssl_ciphers: "'HIGH:MEDIUM:+3DES:!aNULL'"
      # ssl_dh_params_file - not exists in 9.6, 10(Centos)
      - ssl_dh_params_file: "'{{ postgresql_conf_dir }}/{{ postgresql_ssl_dh }}'"
      - ssl_prefer_server_ciphers: "on"
      - ssl_min_protocol_version: 'TLSv1.1'  # not exists in 9.6
      - ssl_max_protocol_version: 'TLSv1.2'  # not exists in 9.6
      - log_destination: "'syslog'"
      - log_filename: "'postgresql-%a.log'"
      - syslog_facility: "'LOCAL0'"
      - syslog_ident: "'postgres'"
      - syslog_sequence_numbers: on
      - syslog_split_messages: on
    postgresql_pg_hba_conf:
      - host     all    all    0.0.0.0/0    md5
  roles:
    - postgresql
```

###pg_hba.conf
https://www.postgresql.org/docs/13/auth-pg-hba-conf.html 

local  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;    database &nbsp;&nbsp;&nbsp;&nbsp; user &nbsp;&nbsp;&nbsp;&nbsp; auth-method &nbsp;&nbsp;&nbsp;&nbsp; [auth-options]  
host  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;     database &nbsp;&nbsp;&nbsp;&nbsp; user &nbsp;&nbsp;&nbsp;&nbsp; address &nbsp;&nbsp;&nbsp;&nbsp; auth-method &nbsp;&nbsp;&nbsp;&nbsp; [auth-options]  
hostssl &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;   database &nbsp;&nbsp;&nbsp;&nbsp; user &nbsp;&nbsp;&nbsp;&nbsp; address &nbsp;&nbsp;&nbsp;&nbsp; auth-method &nbsp;&nbsp;&nbsp;&nbsp; [auth-options]  
hostnossl &nbsp;&nbsp;&nbsp;&nbsp; database &nbsp;&nbsp;&nbsp;&nbsp; user &nbsp;&nbsp;&nbsp;&nbsp; address &nbsp;&nbsp;&nbsp;&nbsp; auth-method &nbsp;&nbsp;&nbsp;&nbsp; [auth-options]  
host   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;    database &nbsp;&nbsp;&nbsp;&nbsp; user &nbsp;&nbsp;&nbsp;&nbsp; IP-address &nbsp;&nbsp;&nbsp;&nbsp; IP-mask  auth-method &nbsp;&nbsp;&nbsp;&nbsp; [auth-options]  
hostssl  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  database &nbsp;&nbsp;&nbsp;&nbsp; user &nbsp;&nbsp;&nbsp;&nbsp; IP-address &nbsp;&nbsp;&nbsp;&nbsp; IP-mask  auth-method &nbsp;&nbsp;&nbsp;&nbsp; [auth-options]  
hostnossl  &nbsp;&nbsp;&nbsp;&nbsp;database &nbsp;&nbsp;&nbsp;&nbsp; user &nbsp;&nbsp;&nbsp;&nbsp; IP-address &nbsp;&nbsp;&nbsp;&nbsp; IP-mask  auth-method &nbsp;&nbsp;&nbsp;&nbsp; [auth-options]  
.....

There are a lot new option in version 13: hostnossl, hostgsenc, ect.

Create database (__Recommended to set__)

```yaml
postgresql_dbs:
  - name: database1
    password: password123
    user: pguser
    priv: ALL
    ssl_mode: prefer
    encoding: UTF-8
    locale: en_US.UTF-8
```
Create global users

```yaml
postgresql_global_users:
  - user: "replicator"
    ssl_mode: require
    role_attr_flags: "NOSUPERUSER,NOCREATEROLE,NOCREATEDB,LOGIN,REPLICATION"
```

pg_rman config

```yaml
postgresql_pg_rman_postgres_conf:
  - wal_init_zero: on
  - wal_level: replica
  - archive_mode: on
  - archive_command: "'test ! -f {{ postgresql_home }}/{{ postgresql_version }}/arclog/%f \
      && cp %p {{ postgresql_home }}/{{ postgresql_version }}/arclog/%f'"
```
pg_rman.ini (default configuration.) It is extendable. 
```yaml
postgresql_pg_rman_ini:
  - option: COMPRESS_DATA
    value: "True"
```

pg_audit

```yaml
postgresql_pg_audit_postgres_conf:
  - pgaudit.log: "'role, misc_set'"
  - pgaudit.log_level: "'error'"
```
