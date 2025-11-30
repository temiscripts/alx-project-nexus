from celery import shared_task
import time

@shared_task
def send_comment_notification(user_email, post_id, comment_text):
    """
    Simulates sending an email notification when a user comments on a post.
    """
    print(f"Sending notification to {user_email} for post {post_id}...")
    time.sleep(2) 
    print(f"Notification sent: '{comment_text}'")
    return f"Email sent to {user_email}"
