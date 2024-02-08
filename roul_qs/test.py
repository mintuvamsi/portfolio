import random

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
        'six_line': 5,   # Betting on six numbers from two adjacent rows
        'dozen': 2,      # Betting on one of the three dozen (1-12, 13-24, 25-36)
        'column': 2,     # Betting on one of the three columns
        'even_odd': 1,   # Betting on even or odd numbers
        'red_black': 1,  # Betting on red or black numbers
        'high_low': 1    # Betting on high (19-36) or low (1-18) numbers
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


def generate_question():
    bet_type = random.choice(list(payouts.keys()))  # Accessing the keys of the payouts dictionary
    amount = random.randint(1, 20)
    return bet_type, amount

print("Welcome to the Roulette Quiz!")
# while True:
#     bet_type, amount = generate_question()
#     correct_answer = french_roulette_payout(bet_type, amount)
#     print(f"What is the payout for a {bet_type} bet of {amount} chips?")
#     user_input = input(f"What is the payout for a {bet_type} bet of {amount} chips?")
    
#     if user_input.lower() == 'exit':
#         print("Thanks for playing!")
#         break
    
#     try:
#         user_answer = float(user_input)
#         if user_answer == correct_answer:
#             print("Correct! Well done!")
#         else:
#             print(f"Sorry, the correct answer was ${correct_answer}. Try again!")
#     except ValueError:
#         print("Invalid input. Please enter a number or 'exit' to quit.")


def main():
    print("Welcome to the French Roulette Quiz!")
    while True:
        bet_type, amount = generate_question()
        correct_answer = french_roulette_payout(bet_type, amount)
        print(f"What is the payout for a {bet_type} bet of ${amount}?")
        user_input = input("Enter your answer (or type 'exit' to quit): ")
        
        if user_input.lower() == 'exit':
            print("Thanks for playing!")
            break
        
        try:
            user_answer = float(user_input)
            if user_answer == correct_answer:
                print("Correct! Well done!")
            else:
                print(f"Sorry, the correct answer was ${correct_answer}. Try again!")
        except ValueError:
            print("Invalid input. Please enter a number or 'exit' to quit.")

if __name__ == "__main__":
    main()
