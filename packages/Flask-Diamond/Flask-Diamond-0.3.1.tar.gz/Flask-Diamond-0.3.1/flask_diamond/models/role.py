# -*- coding: utf-8 -*-

from flask.ext.security import RoleMixin
from .. import db
from ..mixins.crud import CRUDMixin
from ..mixins.marshmallow import MarshmallowMixin


class Role(db.Model, RoleMixin, CRUDMixin, MarshmallowMixin):
    """
    For the purpose of access controls, Roles can be used to create
    collections of users and give them permissions as a group.
    """

    id = db.Column(db.Integer(), primary_key=True)
    "integer -- primary key"

    name = db.Column(db.String(80), unique=True)
    "string -- what the role is called"

    description = db.Column(db.String(255))
    "string -- a sentence describing the role"

    def __str__(self):
        return self.name
