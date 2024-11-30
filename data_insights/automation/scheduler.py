from celery import Celery
from data_insights.queries.insights_generator import run_daily_insights
from backend.config.settings import settings

# Celery Configuration
app = Celery('insights_tasks', 
             broker=settings.REDIS_URL, 
             backend=settings.REDIS_URL)

@app.task
def daily_search_insights():
    run_daily_insights(settings.DATABASE_URL)

# Configure periodic tasks
app.conf.beat_schedule = {
    'run-daily-insights': {
        'task': 'scheduler.daily_search_insights',
        'schedule': 86400.0,  # Run daily
    },
}