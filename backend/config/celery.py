"""
Celery Configuration for NexusCore v4.0
Task queue with high, default, and low priority queues
"""
import os

from celery import Celery
from kombu import Queue

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

app = Celery('nexuscore')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# =============================================================================
# Queue Configuration (PRD-d-3 compliant)
# =============================================================================
app.conf.task_queues = (
    Queue('high', routing_key='high'),
    Queue('default', routing_key='default'),
    Queue('low', routing_key='low'),
)

app.conf.task_default_queue = 'default'
app.conf.task_default_exchange = 'tasks'
app.conf.task_default_routing_key = 'default'

# =============================================================================
# Task Routes
# =============================================================================
app.conf.task_routes = {
    # High priority - webhooks and payments
    'apps.webhooks.tasks.*': {'queue': 'high'},
    'apps.billing.tasks.process_*': {'queue': 'high'},
    'apps.subscriptions.tasks.process_*': {'queue': 'high'},
    
    # Default priority - emails and notifications
    'apps.users.tasks.*': {'queue': 'default'},
    'apps.billing.tasks.send_*': {'queue': 'default'},
    'apps.billing.tasks.generate_*': {'queue': 'default'},
    
    # Low priority - reports and DSAR
    'apps.privacy.tasks.*': {'queue': 'low'},
    'apps.events.tasks.*': {'queue': 'low'},
}

# =============================================================================
# Timezone Configuration (Singapore)
# =============================================================================
app.conf.timezone = 'Asia/Singapore'
app.conf.enable_utc = True

# =============================================================================
# Task Execution Settings
# =============================================================================
app.conf.task_acks_late = True
app.conf.task_reject_on_worker_lost = True
app.conf.worker_prefetch_multiplier = 1

# =============================================================================
# Result Backend Settings
# =============================================================================
app.conf.result_expires = 3600  # 1 hour

# =============================================================================
# Beat Scheduler (for periodic tasks)
# =============================================================================
app.conf.beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Debug task for testing Celery configuration."""
    print(f'Request: {self.request!r}')
