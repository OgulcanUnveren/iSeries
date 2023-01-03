# Gunicorn-django settings
bind = ["0.0.0.0:8888"]
name = "iseries"
python_path = "/app/sandbox/"

# Run
graceful_timeout = 90
timeout = 90
workers = 3

# Logging
# Using '-' for the access log file makes gunicorn log accesses to stdout
accesslog = "-"
# Using '-' for the error log file makes gunicorn log errors to stderr
errorlog = "-"
loglevel = "debug"