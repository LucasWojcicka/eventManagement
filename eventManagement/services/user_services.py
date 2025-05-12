import reflex as rx

from eventManagement.models.user import User
from typing import Optional, List

class UserService:
    @staticmethod
    def make_user():
        print("make user")
