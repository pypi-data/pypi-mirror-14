#!/usr/bin/env python

#
# This file is part of MAD.
#
# MAD is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# MAD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with MAD.  If not, see <http://www.gnu.org/licenses/>.
#

from unittest import TestCase
from mock import MagicMock

from mad.ast import *
from mad.evaluation import Evaluation


class ExpressionTest(TestCase):

    def test_concatenation(self):
        actual = Think(1) + Think(2)
        self.assertEqual(Sequence(Think(1), Think(2)), actual)

    def test_concatenation_with_sequence(self):
        actual = Think(1) + Sequence(Think(2), Think(3))
        self.assertEqual(Sequence(Think(1), Think(2), Think(3)), actual)


class ThinkTest(TestCase):

    def test_equality(self):
        exp1 = Think(5)
        exp2 = Think(6)
        exp3 = Think(5)

        self.assertNotEqual(exp1, exp2)
        self.assertEqual(exp1, exp3)


class QueryTests(TestCase):

    def test_equality(self):
        queries = [ Query("S1", "Op1"),
                    Query("S1", "Op2"),
                    Query("S2", "Op1"),
                    Query("S2", "Op2"),
                    Query("S1", "Op1")]

        self.assertNotEqual(queries[0], queries[1])
        self.assertNotEqual(queries[0], queries[2])
        self.assertNotEqual(queries[0], queries[3])
        self.assertEqual(queries[0], queries[4])


class SequenceTests(TestCase):

    def test_equality(self):
        seq1 = Sequence(Think(5), Think(6))
        seq2 = Sequence(Think(5), Think(6))

        self.assertEqual(seq1, seq2)

    def test_concatenation_between_sequence(self):
        seq1 = Sequence(Think(1), Think(2))
        seq2 = Sequence(Think(3), Think(4))

        actual = seq1 + seq2
        expected = Sequence(Think(1), Think(2), Think(3), Think(4))
        self.assertEqual(expected, actual)

    def test_concatenation_with_an_expression(self):
        seq = Sequence(Think(1), Think(2))

        actual = seq + Think(3)

        expected = Sequence(Think(1), Think(2), Think(3))
        self.assertEqual(expected, actual)


class SettingsTest(TestCase):

    def test_default_queue_settings_is_fifo(self):
        settings = Settings()
        self.assertIsInstance(settings.queue, FIFO)

    def test_setting_queue(self):
        settings = Settings(queue=LIFO())
        self.assertIsInstance(settings.queue, LIFO)

    def test_accept(self):
        settings = Settings()
        evaluation = MagicMock(Evaluation)
        settings._accepts(evaluation)

        evaluation.of_settings.assert_called_once_with(settings)

    def test_equality(self):
         self.assertEqual(Settings(queue=FIFO()), Settings(queue=FIFO()))


class AutoscalingSettingsTest(TestCase):

    def test_reject_invalid_limits(self):
        with self.assertRaises(ValueError):
            Autoscaling(period=10, limits=23)

    def test_reject_invalid_period(self):
        with self.assertRaises(ValueError):
            Autoscaling(period="wrong", limits=23)

    def test_evaluation(self):
        settings = Autoscaling()
        evaluation = MagicMock(Evaluation)
        settings._accepts(evaluation)

        evaluation.of_autoscaling.assert_called_once_with(settings)


class FIFOTests(TestCase):

     def test_accept(self):
        queue = FIFO()
        evaluation = MagicMock(Evaluation)
        queue._accepts(evaluation)

        evaluation.of_fifo.assert_called_once_with(queue)

     def test_equality(self):
         self.assertEqual(FIFO(), FIFO())


class LIFOTests(TestCase):

     def test_accept(self):
        queue = LIFO()
        evaluation = MagicMock(Evaluation)
        queue._accepts(evaluation)

        evaluation.of_lifo.assert_called_once_with(queue)

     def test_equality(self):
         self.assertEqual(FIFO(), FIFO())