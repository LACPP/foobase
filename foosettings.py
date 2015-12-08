"""FOOBASE Settings

"""

# Default (Host, Port)
(default_host, default_port) = ('localhost', 10001)
default_storage_file = "data_store/data.dat"
default_backlog = 1
# Logging management
LOG_FILE = "logging.log"


init_query_stats = {
    'CREATE': {'total':0, 'OK': 0, 'KO': 0},
    'READ'  : {'total':0, 'OK': 0, 'KO': 0},
    'UPDATE': {'total':0, 'OK': 0, 'KO': 0},
    'DELETE': {'total':0, 'OK': 0, 'KO': 0},
    'ALL'   : {'total':0, 'OK': 0, 'KO': 0}
    }    

