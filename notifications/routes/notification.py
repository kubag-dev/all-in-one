from uuid import UUID

from fastapi import APIRouter
from fastapi import status

from notifications.models.date_noficiation import DateNotification
from notifications import types


router = APIRouter(prefix="/notifications")


@router.get("/{module}", response_model=list[DateNotification])
def get_notifications_by_type(module: types.Modules):
    pass
    # fetch filtered data


@router.get("{item_id}", response_model=list[DateNotification])
def get_notifications_by_item(item_id: UUID):
    pass


@router.get("/today", response_model=list[DateNotification])
def get_today_notifications():
    pass


@router.patch("/{notification_id}", response_model=DateNotification)
def patch_notification(notification: DateNotification):
    pass


@router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_notification(notification_id: types.notificationId):
    pass
