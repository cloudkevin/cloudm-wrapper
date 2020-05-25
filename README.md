# CloudM-API_Wrapper

This was written to allow easier implementation of the CloudM API when using Python.

## Installation

Download this repo and run ```python3 setup.py install```

## Usage

Import the library:
```
from cloudm import CloudM
```

Create a new object and pass in the server ip address with port, CloudM username, and password.

```
from cloudm import CloudM  
migration = CloudM('192.168.1.1:5250', 'username@domain.com', 'userPassword')
```

## Supported Functions

```list_migrations()```

```get_migration_details(migration_id)```

```get_migration_history(migration_id)```

```start_migration(migration_id)```

```stop_migration(migration_id)```

```get_total_stats(migration_id)```

```get_item_stats(migration_id, [query_state])```

```get_progress_totals(migration_id)```

```delete_project(project_id)```

```list_projects()```

```update_ip_address(new_ip_address)```

```update_login(new_login, new_password)```

### Requirements

* requests