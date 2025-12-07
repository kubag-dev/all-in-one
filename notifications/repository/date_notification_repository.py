from uuid import UUID
from datetime import date
from datetime import datetime
from datetime import time

from fastapi import Depends
from sqlmodel import select
from sqlmodel import Session

from core.database import get_session
from notifications import types
from notifications.exceptions import InstanceNotFoundError
from notifications.models.date_noficiation import DateNotification
from notifications.schemas.date_notification_update_schema import (
    DateNotificationUpdateSchema,
)


class DateNotificationRepository:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def fetch_notifications_by_module(self, *, module: types.Modules):
        return self.session.exec(
            select(DateNotification).where(
                DateNotification.attached_to_module == module
            )
        ).all()

    def fetch_notifications_by_item(self, *, item_id: UUID):
        return self.session.exec(
            select(DateNotification).where(DateNotification.attached_to_item == item_id)
        ).all()

    def fetch_on_day_notifications(self, *, on_date: date):
        return self.session.exec(
            select(DateNotification).where(
                DateNotification.reminder_at == datetime.combine(on_date, time())
            )
        ).all()

    def update_notification(
        self,
        *,
        date_notification_id: types.notificationId,
        date_notification_data: DateNotificationUpdateSchema
    ) -> DateNotification:
        notification = self.session.get(DateNotification, date_notification_id)
        if not notification:
            raise InstanceNotFoundError("Notification not found")

        update_data = date_notification_data.model_dump(exclude_unset=True)
        if update_data.get("reminder_at"):
            update_data["is_read"] = None

        for key, value in update_data.items():
            setattr(notification, key, value)

        self.session.add(notification)
        self.session.commit()
        return DateNotification()

    def delete_notification(self, *, date_notification_id: types.notificationId):
        notification = self.session.get(DateNotification, date_notification_id)
        if not notification:
            raise InstanceNotFoundError("Notification not found")

        self.session.delete(notification)
