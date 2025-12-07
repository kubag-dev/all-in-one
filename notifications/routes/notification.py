from datetime import date
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from notifications import types
from notifications.models.date_noficiation import DateNotification
from notifications.repository.date_notification_repository import (
    DateNotificationRepository,
)
from notifications.schemas.date_notification_update_schema import (
    DateNotificationUpdateSchema,
)

router = APIRouter(prefix="/notifications")


@router.get("/{module}", response_model=list[DateNotification])
def get_notifications_by_module(
    module: types.Modules,
    date_notification_repository: DateNotificationRepository = Depends(),
):
    return date_notification_repository.fetch_notifications_by_module(module=module)


@router.get("{item_id}", response_model=list[DateNotification])
def get_notifications_by_item(
    item_id: UUID, date_notification_repository: DateNotificationRepository = Depends()
):
    return date_notification_repository.fetch_notifications_by_item(item_id=item_id)


@router.get("/today", response_model=list[DateNotification])
def get_today_notifications(
    date_notification_repository: DateNotificationRepository = Depends(),
):
    on_date = date.today()
    return date_notification_repository.fetch_on_day_notifications(on_date=on_date)


@router.patch("/{notification_id}", response_model=DateNotification)
def patch_notification(
    date_notification_id: types.notificationId,
    date_notification_update_data: DateNotificationUpdateSchema,
    date_notification_repository: DateNotificationRepository = Depends(),
):
    return date_notification_repository.update_notification(
        date_notification_id=date_notification_id,
        date_notification_data=date_notification_update_data,
    )


@router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_notification(
    notification_id: types.notificationId,
    date_notification_repository: DateNotificationRepository = Depends(),
):
    return date_notification_repository.delete_notification(
        date_notification_id=notification_id
    )
