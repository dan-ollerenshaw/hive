"""
Tests for SlotMachine class.
"""

import unittest
from unittest.mock import MagicMock


from backend.slot_machine import SlotMachine, NUM_BLOCKS


class TestFoo(unittest.TestCase):
    def setUp(self):
        slot = SlotMachine()
        self.symbols = list(slot.symbols.keys())

    def test_credit_deduction(self):
        """Test that credit is deducted correctly when a game is played."""
        slot = SlotMachine(credit=10, cost_to_play=1)
        slot._is_winning_roll = MagicMock(return_value=False)
        slot.play()
        self.assertEqual(slot.credit, 9)

    def test_credit_addition(self):
        """Test the credit is added correctly for a winning game."""
        slot = SlotMachine(credit=10, cost_to_play=1)
        starting_credit = slot.credit
        symbol = self.symbols[0]
        expected_gain = slot.symbols[symbol]
        slot._roll = MagicMock(return_value=[symbol] * NUM_BLOCKS)
        slot.play()
        expected_credit = starting_credit - slot.cost_to_play + expected_gain
        self.assertEqual(slot.credit, expected_credit)

    def test_cheating_case_1(self):
        """
        Test for credit < 40. _roll() should be called once
        """
        slot = SlotMachine(credit=10, cost_to_play=1)
        symbol = self.symbols[0]
        slot._roll = MagicMock(return_value=[symbol] * NUM_BLOCKS)
        slot.play()
        self.assertEqual(slot._roll.call_count, 1)

    def test_cheating_case_2(self):
        """
        Test for credit >= 40
        _roll() may be called once or twice
        """
        symbol = self.symbols[0]
        # test cases where 40 <= credit <= 60 and credit > 60
        credit_values = [50, 1000]

        for credit in credit_values:
            # case where _roll() should be called once
            slot = SlotMachine(credit=credit, cost_to_play=1)
            slot._should_reroll_round = MagicMock(return_value=False)
            slot._roll = MagicMock(return_value=[symbol] * NUM_BLOCKS)
            slot.play()
            self.assertEqual(slot._roll.call_count, 1)

            # case where _roll() should be called twice
            slot = SlotMachine(credit=credit, cost_to_play=1)
            slot._should_reroll_round = MagicMock(return_value=True)
            slot._is_winning_roll = MagicMock(return_value=True)
            slot._roll = MagicMock(return_value=[symbol] * NUM_BLOCKS)
            slot.play()
            self.assertEqual(slot._roll.call_count, 2)
