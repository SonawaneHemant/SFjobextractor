from apscheduler.schedulers.background import BackgroundScheduler
from salesforce_monitor_backend.Agent.limit_guard_agent import LimitGuardAgent

scheduler = BackgroundScheduler()


def start_scheduler():

    agent = LimitGuardAgent()

    # Run the agent every 5 minutes
    scheduler.add_job(
        agent.run,
        'interval',
        minutes=5,
        id="limit_guard_agent_job",
        replace_existing=True
    )

    scheduler.start()

    print("Scheduler started: Limit Guard Agent running every 5 minutes")