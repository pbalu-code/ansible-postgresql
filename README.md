ansible-postgresql
===========
Ansible role to install postgresql server on Centos/Redhat 7 - 8 , ( Soon: Ubuntu 18.04 ).

Tested:
- Redhat7
- Redhat8
- Centos7
- Centos8 


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

This role requires Ansible 2.9+

Role Variables
--------------

### All variables are optional but... ###

- `postgresql_user_name`: System username to be used for PostgreSQL (default: `postgres`).

- `postgresql_version`: PostgreSQL version to install. On Debian-based platforms, the default is whatever version is
  pointed to by the `postgresql` metapackage). On RedHat-based platforms, the default is `10`.


- ___Soon:___ _`postgresql_flavor`: On Debian-based platforms, this specifies whether you want to use PostgreSQL packages from pgdg
  or the distribution's apt repositories. Possible values: `apt`, `pgdg` (default: `apt`)._ {: .gitlab-purple}
  
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
    - max_connections: 250
    - archive_mode: "off"
    - work_mem: "'8MB'"
    - listen_addresses: "'0.0.0.0'"
    - password_encryption: scram-sha-256
    - hot_standby: "on"
    - ssl: "on"
    - ssl_ca_file: "'{{ pg_ssl_ca }}'"
    - ssl_cert_file: "'{{ pg_ssl_cert }}'"
    - ssl_key_file: "'{{ pg_ssl_key }}'"
    - ssl_ciphers: "'HIGH:MEDIUM:+3DES:!aNULL'"
    - ssl_prefer_server_ciphers: "on"
    - ssl_min_protocol_version: 'TLSv1.1'
    - ssl_max_protocol_version: 'TLSv1.2'
  ```

  Becomes the following in `25ansible_postgresql.conf`:

  ```
  max_connections = 250
  archive_mode = off
  work_mem: '8MB'
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

- `installpostgis`: `true/false` Optional parameter if you want to install postgis extension, you can enable this option.
  
- `posgis_to_install`: `postgis24_10` Declace which version of postgis to be installed.

- `use_ssl`: boolean This option is turning on/off managing ssl keys transfer. 

- `pg_ssl_key`: [path/]pgstandby.key

- `pg_ssl_cert`: [path/]pgstandby.crt

- `pg_ssl_ca`: [path/]root.crt

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

Replication
---------------
Tested with PostgreSQL 12

This role is able to create asyncron streaming replication too.
Access rights and the config should be created by config options like postgresql_conf, postgresql_pg_hba_conf ect.  
The authentication is trust / IP based.

Replication related variables:

- `pg_standby_slot_name`: string, what should be the name of the replication stream. This is a host related variable. Use it in host variable! 
- `init_replication`: boolean Sync standby server to the master by pg_basebackup method. __If the standby.signal file is not present.__ 
- `replication_master`: ip/hostname. Will it use during pg_basebackup
 


Example Playbook
----------------

Standard install: Default `postgresql.conf`, `pg_hba.conf` and default version for the OS:

```yaml
---

- hosts: dbservers
  remote_user: root
  roles:
    - postgresql
```

Use the pgdg packages on a Debian-based host:

```yaml
---

- hosts: dbservers
  remote_user: root
  vars:
    postgresql_flavor: pgdg
  roles:
    - postgresql
```

Use the PostgreSQL 9.6 packages and set some `postgresql.conf` options and `pg_hba.conf` entries:

```yaml
---

- hosts: dbservers
  remote_user: root
  vars:
    postgresql_version: 9.6
    postgresql_conf:
      - listen_addresses: "''"    # disable network listening (listen on unix socket only)
      - max_connections: 50       # decrease connection limit
    postgresql_pg_hba_conf:
      - host     all    all    0.0.0.0/0    md5
  roles:
    - postgresql
```

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

