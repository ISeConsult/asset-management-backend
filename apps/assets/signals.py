from django.dispatch import receiver
from django.db.models.signals import post_save
from apps.assets.models import (
    AssetRequest,
    AssetCheckIn,
    AssetCheckOut,
    AssetReturn,
    AssetMaintenanceRequest,
    AssetsHistory,
    AssetAudit,
    ComponentHistory,
    ComponentCheckIn,
    ComponentCheckOut,
    ComponentRequest,
)
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)


# Utility function to create asset history
def create_asset_history(action, instance, user):
    try:
        AssetsHistory.objects.create(
            asset=getattr(instance, "asset", None),
            user=user,
            action=action,
        )
    except Exception as e:
        logger.warning(f"Failed to create asset history: {str(e)}")


# Generic signal handler
@receiver(post_save, sender=AssetCheckIn)
@receiver(post_save, sender=AssetCheckOut)
@receiver(post_save, sender=AssetReturn)
@receiver(post_save, sender=AssetMaintenanceRequest)
@receiver(post_save, sender=AssetRequest)
@receiver(post_save, sender=AssetAudit)
def asset_save_handler(sender, instance, created, **kwargs):
    try:
        action_mapping = {
            AssetCheckIn: "check_in",
            AssetCheckOut: "check_out",
            AssetReturn: "return",
            AssetMaintenanceRequest: "maintenance_request",
            AssetRequest: "request",
            AssetAudit: "audit",
        }

        action = action_mapping.get(sender)
        if not action:
            logger.warning(f"No action mapped for sender: {sender}")
            return

        user = getattr(
            instance, "user", None
        )  # Ensure the instance has a `user` attribute
        if not user:
            logger.warning(f"No user associated with instance: {instance}")
            return

        if created:  # Log only for newly created instances
            create_asset_history(action, instance, user)
    except Exception as e:
        logger.warning(f"Error in asset_save_handler: {str(e)}")


def create_component_history(action, instance, user):
    try:
        ComponentHistory.objects.create(
            component=getattr(instance, "component", None), user=user, action=action
        )
    except Exception as e:
        logger.warning(f"Failed to create component history: {str(e)}")


@receiver(post_save, sender=ComponentCheckIn)
@receiver(post_save, sender=ComponentCheckOut)
@receiver(post_save, sender=ComponentRequest)
def component_save_handler(sender, instance, created, **kwargs):
    try:
        action_mapping = {
            ComponentCheckIn: "check_in",
            ComponentCheckOut: "check_out",
            ComponentRequest: "request",
        }
        action = action_mapping.get(sender)
        if not action:
            logger.warning(f"No action mapped for sender: {sender}")
            return
        user = getattr(instance, "user", None)
        if not user:
            logger.warning(f"No user associated with instance: {instance}")
            return
        if created:  # Log only for newly created instances
            create_component_history(action, instance, user)

    except Exception as e:
        logger.warning(f"Failed to create component history: {str(e)}")
