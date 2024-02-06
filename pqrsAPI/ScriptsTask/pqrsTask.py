import time
from datetime import datetime, timedelta


def schedule_task():
	print("Performing system checks...")
	print("Is working Succesfully")
	
def check_expiration():
    from ..models import PqrsMain, PqrsNotifify, StatusType
    # Your code logic here
    print("Performing system check_expiration....")

    today = datetime.today().date()
    ten_days_later = today + timedelta(days=5)
    
    instances_to_notify = PqrsMain.objects.filter(
        expiration_date__gt=today,
        expiration_date__lte=ten_days_later
    )
    
    for instance in instances_to_notify:
        notification_msg = f'El expediente NÚMERO {instance.file_num} está a punto de caducar'
        # print("Baba Test", notification_msg)

        # Check if a notification with the same message already exists
        existing_notification = PqrsNotifify.objects.filter(msg=notification_msg).first()
        st = StatusType.objects.get(id=2)
        if existing_notification:
            # Notification already exists, skip creating a new one
            print("Notification already exists for:", instance.file_num)
            
        else:
            # Create a new notification if it doesn't exist
            PqrsNotifify.objects.create(msg=notification_msg)
            
            if not instance.status_of_the_response.name == 'CERRADO' or not instance.status_of_the_response.name == 'REPARTO':
                instance.status_of_the_response = st
                instance.save()
                 

