# -*- coding: utf-8 -*-

# Copyright (C) 2013 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

from hamcrest import assert_that, equal_to
from mock import Mock, patch
from unittest import TestCase

from xivo_call_logs.cel_interpretor import CELInterpretor
from xivo_dao.data_handler.cel.event_type import CELEventType
from xivo_dao.data_handler.call_log.model import CallLog


class TestCELInterpretor(TestCase):
    def setUp(self):
        self.cel_interpretor = CELInterpretor()

    def tearDown(self):
        pass

    def test_interpret_call(self):
        cels = [Mock(), Mock()]
        filtered_cels = [Mock()]
        expected_call_log = call_log = Mock(CallLog)
        self.cel_interpretor.filter_cels = Mock(return_value=filtered_cels)
        self.cel_interpretor.interpret_cels = Mock(return_value=call_log)

        result = self.cel_interpretor.interpret_call(cels)

        self.cel_interpretor.filter_cels.assert_called_once_with(cels)
        self.cel_interpretor.interpret_cels.assert_called_once_with(filtered_cels)
        assert_that(result, equal_to(expected_call_log))

    def test_filter_cels_no_cels(self):
        cels = []

        result = self.cel_interpretor.filter_cels(cels)

        assert_that(result, equal_to([]))

    def test_filter_cels(self):
        cels = [Mock(uniqueid=1), Mock(uniqueid=2), Mock(uniqueid=1), Mock(uniqueid=3)]
        expected = [cel for cel in cels if cel.uniqueid == 1]

        result = self.cel_interpretor.filter_cels(cels)

        assert_that(result, equal_to(expected))

    @patch('xivo_dao.data_handler.call_log.model.CallLog')
    def test_interpret_cels(self, mock_call_log):
        cels = cel_1, cel_2 = [Mock(), Mock()]
        call = Mock(CallLog, id=1)
        self.cel_interpretor.interpret_cel = Mock(return_value=call)
        mock_call_log.side_effect = [call, Mock(CallLog, id=2)]

        result = self.cel_interpretor.interpret_cels(cels)

        self.cel_interpretor.interpret_cel.assert_any_call(cel_1, call)
        self.cel_interpretor.interpret_cel.assert_any_call(cel_2, call)
        assert_that(self.cel_interpretor.interpret_cel.call_count, equal_to(2))
        assert_that(result, equal_to(call))