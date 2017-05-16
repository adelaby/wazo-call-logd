# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from marshmallow import fields
from marshmallow import post_load
from marshmallow import Schema
from marshmallow.validate import OneOf
from marshmallow.validate import Range


class CDRSchema(Schema):
    start = fields.DateTime(attribute='date')
    answer = fields.DateTime(attribute='date_answer')
    end = fields.DateTime()
    source_name = fields.String()
    source_extension = fields.String(attribute='source_exten')
    direction = fields.String()
    destination_name = fields.String()
    destination_extension = fields.String(attribute='destination_exten')
    duration = fields.TimeDelta()
    answered = fields.Boolean()


cdr_schema = CDRSchema()


class CDRListRequestSchema(Schema):
    from_ = fields.DateTime(load_from='from', missing=None)
    until = fields.DateTime(missing=None)
    direction = fields.String(validate=OneOf(['asc', 'desc']), missing='asc')
    order = fields.String(validate=OneOf(set(cdr_schema.fields) - {'end'}), missing='start')
    limit = fields.Integer(validate=Range(min=0), missing=None)
    offset = fields.Integer(validate=Range(min=0), missing=None)
    search = fields.String(missing=None)

    @post_load
    def map_order_field(self, in_data):
        mapped_order = cdr_schema.fields[in_data['order']].attribute
        if mapped_order:
            in_data['order'] = mapped_order


list_schema = CDRListRequestSchema(strict=True)
