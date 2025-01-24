from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import RUser, Role, Product
import logging




@receiver(post_save, sender=[RUser, Role, Product])  # List of models
def log_model_save(sender, instance, created, **kwargs):
    model_name = instance._meta.model_name
    action = "Created" if created else "Updated"
    print(f"{action} {model_name}: {instance}")

@receiver(post_delete, sender=[RUser, Role, Product])
def log_model_delete(sender, instance, **kwargs):
    model_name = instance._meta.model_name
    print(f"Deleted {model_name}: {instance}")


logger = logging.getLogger(__name__)
def some_crud_operation():
    try:
        # Perform operation
        logger.info("CRUD operation performed successfully.")
    except Exception as e:
        logger.error(f"Error during CRUD operation: {e}")
