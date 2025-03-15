# This allows tasks to be discovered by Celery
# but avoids circular imports during Django initialization
default_app_config = 'tasks.apps.TasksConfig'