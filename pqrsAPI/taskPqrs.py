import time
import threading
from datetime import datetime, timedelta


def check_expiration():
    from .models import PqrsMain, PqrsNotifify
    # Your code logic here
    print("Running check_expiration")

    today = datetime.today().date()
    ten_days_later = today + timedelta(days=10)
    
    instances_to_notify = PqrsMain.objects.filter(
        expiration_date__gt=today,
        expiration_date__lte=ten_days_later
    )
    
    for instance in instances_to_notify:
        notification_msg = f"NÚMERO DE PROCESO '{instance.process_num}' está a punto de caducar en 10 días y date {instance.finish_date - timedelta(days=10)}"
        print("Baba Test", notification_msg)

        # Check if a notification with the same message already exists
        existing_notification = PqrsNotifify.objects.filter(msg=notification_msg).first()
        
        if existing_notification:
            # Notification already exists, skip creating a new one
            print("Notification already exists for:", notification_msg)
        else:
            # Create a new notification if it doesn't exist
            PqrsNotifify.objects.create(msg=notification_msg)



def run_check_expiration_daily():
    while True:
        # Get the current time
        now = datetime.now()
        
        # Set the target time for 11:20 AM
        target_time = now.replace(hour=11, minute=20, second=0, microsecond=0)
        
        # If the target time is in the past, set it to 11:20 AM tomorrow
        if now > target_time:
            target_time += timedelta(days=1)
        
        # Calculate the time until the next 9 PM
        time_until_next_run = (target_time - now).total_seconds()
        
        # Sleep until the next run
        time.sleep(time_until_next_run)
        
        # Call the function
        check_expiration()

# Start the thread
thread = threading.Thread(target=run_check_expiration_daily)
thread.daemon = True
thread.start()