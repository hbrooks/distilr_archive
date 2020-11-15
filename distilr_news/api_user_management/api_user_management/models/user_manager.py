from datetime import datetime
from uuid import uuid4
import logging

from .user import User
from .db_models import UsersRow
from ..exceptions.user import UserNotFound
from ..exceptions.user import AccountCreationNotAuthorized
from ..exceptions.user import LoginDisallowed


LOG = logging.getLogger(__name__)


class UserManager:

    def __init__(self, event_manager):
        self.events = event_manager

    def create_standard_user(self, session, email, password):
        try:
            return self._get_by_email(session, email)
        except UserNotFound:
            new_users_row = UsersRow(
                id=str(uuid4()),
                address=None,
                email=email,
                password=password,
                created_at=datetime.now(),
                type='standard',
            )
            return self._create(session, new_users_row)

    def _create(self, session, row):
        session.add(row)
        user = self._assemble_user(row)
        self.events.create_user(session, user, datetime.now())
        return user

    def create_anonymous_user(self, session, address):
        try:
            return self._get_by_address(session, address)
        except UserNotFound:
            new_users_row = UsersRow(
                id=str(uuid4()),
                address=address,
                email=None,
                password=None,
                created_at=datetime.now(),
                type='anonymous',
            )
            return self._create(session, new_users_row)

    def _assemble_user(self, users_row):
        return User(
            users_row.id,
            users_row.email,
            users_row.type
        )

    def _get_by_address(self, session, address):
        row = session.query(UsersRow).filter(UsersRow.address == address).first()
        if row == None:
            raise UserNotFound('address', address)
        return self._assemble_user(row)

    def _get_by_email(self, session, email):
        row = session.query(UsersRow).filter(UsersRow.email == email).first()
        if row == None:
            raise UserNotFound('email', email)
        return self._assemble_user(row)

    def get_by_user_id(self, session, user_id):
        row = session.query(UsersRow).filter(UsersRow.id == user_id).first()
        if row == None:
            raise UserNotFound('userId', user_id)
        return self._assemble_user(row)

    def attempt_login(self, session, email, password):
        row = session.query(UsersRow).filter(UsersRow.email == email).first()
        if row == None:
            raise UserNotFound('email', email)
        user = self._assemble_user(row)
        if row.password != password:
            LOG.error(row.password)
            LOG.error(password)
            # TODO: Log event?
            raise LoginDisallowed(email)
        return user
