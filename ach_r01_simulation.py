import random
import time

class Account:
    def __init__(self, account_number, initial_balance):
        self.account_number = account_number
        self.balance = initial_balance

    def __str__(self):
        return f"Account {self.account_number}: Balance ${self.balance:.2f}"

def process_ach_payment(sender_account, receiver_account, amount):
    """Simulates an ACH payment attempt and handles R01 return code."""
    print(f"Attempting to send ${amount:.2f} from {sender_account.account_number} to {receiver_account.account_number}...")

    # Simulate insufficient funds check
    if sender_account.balance < amount:
        print(f"ACH Return Code R01: Insufficient Funds detected for account {sender_account.account_number}.")
        return False # Payment failed

    # Simulate successful transaction
    sender_account.balance -= amount
    receiver_account.balance += amount
    print(f"Payment successful. {sender_account} | {receiver_account}")
    return True # Payment succeeded

def smart_retry_strategy(sender_account, receiver_account, amount, max_retries=3):
    """Implements a smart retry strategy for failed ACH payments (R01)."""
    print(f"\nInitiating smart retry strategy for ${amount:.2f} to {receiver_account.account_number}. Max retries: {max_retries}")
    retries = 0
    while retries < max_retries:
        # Simulate a delay before retrying (e.g., wait for funds to be deposited)
        delay = random.randint(2, 8) # Random delay between 2 and 8 seconds
        print(f"Waiting {delay} seconds before retry {retries + 1}/{max_retries}...")
        time.sleep(delay)

        # Attempt to process payment again
        if process_ach_payment(sender_account, receiver_account, amount):
            print("Retry successful!")
            return True # Payment succeeded on retry
        else:
            retries += 1

    print(f"\nSmart retry strategy failed after {max_retries} retries. Payment of ${amount:.2f} could not be completed.")
    return False # Payment failed after all retries

if __name__ == "__main__":
    # Setup accounts
    account_a = Account("123456789", 100.00) # Sender with low balance
    account_b = Account("987654321", 500.00) # Receiver

    print("--- Initial State ---")
    print(account_a)
    print(account_b)

    payment_amount = 150.00 # Amount that will cause R01

    print("\n--- First Payment Attempt ---")
    success = process_ach_payment(account_a, account_b, payment_amount)

    if not success:
        # If the first attempt failed due to R01, initiate smart retry
        smart_retry_strategy(account_a, account_b, payment_amount)

    print("\n--- Final State ---")
    print(account_a)
    print(account_b)

    # Example of a successful payment
    print("\n--- Successful Payment Example ---")
    account_c = Account("111222333", 300.00)
    account_d = Account("444555666", 200.00)
    print(account_c)
    print(account_d)
    process_ach_payment(account_c, account_d, 50.00)
    print(account_c)
    print(account_d)
