"""Executable observation helpers for the 旅とも human-choice boundary.

This module deliberately contains no Runtime policy change. It only provides a
small, explicit representation of the interaction boundary for tests.
"""


def character_can_offer_without_deciding(character_response, options, traveler_choice):
    return (
        character_response not in options
        and traveler_choice in options
        and traveler_choice != character_response
    )
