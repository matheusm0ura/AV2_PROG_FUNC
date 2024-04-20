import threading
from q1_MatheusLima import *


def test_cash_flow_with_sufficient_balance():
    authenticated = lambda: authenticate_user("alice123", "p")
    assert authenticated() == authenticate_user("alice123", "p")
    # Test cash flow with sufficient balance
    check_balance_action(authenticated, "alice123", 900, "cash")
    assert user_accounts["alice123"]["balance"] == 100


def test_auth_user():
    authenticated = lambda: authenticate_user("alice123", "p")
    assert authenticated() == authenticate_user("alice12", "p")


def test_debit():
    user_accounts = lambda: user_accounts_dict()
    initial_balance_alice = user_accounts()["alice123"]["balance"]

    debit("alice123", 500, "cash")

    assert user_accounts()["alice123"]["balance"] == initial_balance_alice - 500


def stress_test():
    threads = []

    add_and_start_threads = lambda num_threads, threads: [
        (thread := threading.Thread(target=authenticate_user, args=("alice123", "p"))) and (
                threads.append(thread) or thread.start()) for _ in range(num_threads)
    ]

    add_and_start_threads(10000, [])

    join_threads = lambda threads: [thread.join() for thread in threads]
    return join_threads(threads)


stress_test()
