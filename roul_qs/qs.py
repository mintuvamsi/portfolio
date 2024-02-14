# qs.py
import random

def french_roulette_payout(bet_type, amount):
    """
    Calculate the payout for a given bet in French roulette.

    Parameters:
        bet_type (str): Type of bet, should be one of 'straight', 'split', 'street', 'corner', 'six_line',
                        'dozen', 'column', 'even_odd', 'red_black', 'high_low'.
        amount (float): Amount of money bet on the given type.

    Returns:
        float: Payout amount for the given bet.
    """

    payouts = {
        'straight': 35,  # Betting on a single number
        'split': 17,     # Betting on two adjacent numbers
        'street': 11,    # Betting on three numbers in a row
        'corner': 8,     # Betting on four numbers that form a square
        'six_line': 5    # Betting on six numbers from two adjacent rows
    }

    if bet_type in payouts:
        return payouts[bet_type] * amount
    else:
        return None  # Return None for unsupported bet types


payouts = {
    'straight': 35,  # Betting on a single number
    'split': 17,     # Betting on two adjacent numbers
    'street': 11,    # Betting on three numbers in a row
    'corner': 8,     # Betting on four numbers that form a square
    'six_line': 5,   # Betting on six numbers from two adjacent rows
}


def generate_question(num_questions=5):
    questions = []
    for _ in range(num_questions):
        bet_type = random.choice(list(payouts.keys()))
        amount = random.randint(1, 20)
        correct_answer = french_roulette_payout(bet_type, amount)
        questions.append((bet_type, amount, correct_answer))
    return questions
