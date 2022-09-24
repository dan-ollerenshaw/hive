"""
Implementation of the slot machine game.
"""

import logging
import random

logger = logging.getLogger(__name__)

NUM_BLOCKS = 3
DEFAULT_CREDIT = 10


class SlotMachine:
    # symbol names and the associated credit gains for a win
    symbols = {
        "cherry": 10,
        "lemon": 20,
        "orange": 30,
        "watermelon": 40,
    }

    def __init__(self, credit=DEFAULT_CREDIT, cost_to_play=1):
        self.credit = credit
        self.cost_to_play = cost_to_play

    def play(self) -> list[str]:
        """
        Perform a roll and adjust credit accordingly.
        """
        roll = self._perform_roll()
        self.credit -= self.cost_to_play
        logger.debug(f"{self.cost_to_play} credit spent. Roll result: {roll}")
        if self._is_winning_roll(roll):
            credit_gain = self.symbols[roll[0]]
            self.credit += credit_gain
            logger.debug(f"You win! Credit gained: {credit_gain}.")
        else:
            logger.debug(f"You lose!")
        logger.debug(f"Credit: {self.credit}")
        return roll

    def _perform_roll(self) -> list[str]:
        """
        Perform a roll, but potentially reroll depending on the current credit.

        If 40 <= credit <= 60, give a 30% to reroll a winning roll
        If credit > 60, give a 60% to reroll a winning roll
        """
        roll = self._roll()
        if self.credit < 40:
            return roll

        p = 0.6 if self.credit > 60 else 0.3
        if self._is_winning_roll(roll) and self._should_reroll_round(p):
            logger.debug("[CHEAT] Rerolling winning role!")
            return self._roll()
        return roll

    def _roll(self) -> list[str]:
        return [self._choose_symbol() for _ in range(NUM_BLOCKS)]

    def _choose_symbol(self) -> str:
        return random.choice(list(self.symbols.keys()))

    def _is_winning_roll(self, roll) -> bool:
        return len(set(roll)) == 1

    def _should_reroll_round(self, p: float) -> bool:
        """
        Args:
            p: probability that round should be rerolled. Should be in the interval [0, 1]
        """
        return random.choices([True, False], weights=[p, 1 - p])[0]
    
    def __repr__(self):
        return f"<SlotMachine(credit={self.credit},cost_to_play={self.cost_to_play})>"
