# Definição da função user_accounts
user_accounts = lambda: {
        "alice123": {
            "balance": 1000,
            "login": "Alice",
            "password": "p",
            "CC": "9090"
        },
        "bob423": {
            "balance": 1500,
            "login": "Bob",
            "password": "password456",
            "CC": "1212"
        },
        "charlie421": {
            "balance": 2000,
            "login": "Charlie",
            "password": "password789",
            "CC": "2222"
        }
    }

create_transaction = lambda: print("Creating transaction...")

# Completando transação
complete_transaction = lambda: print("Completing transaction...")

# Funções que representam cada etapa do fluxo de "Cash"
receive_cash = lambda: print("Receiving cash...")
print_payment_receipt = lambda: print("Printing payment receipt...")
return_payment_receipt = lambda: print("Returning payment receipt...")

# Funções que representam cada etapa do fluxo de "Credit"
request_credit_account_details = lambda: print("Requesting credit account details...")
request_payment_from_bank = lambda: print("Requesting payment from bank...")
cancel_transaction = lambda: print("Canceling transaction...")
close_transaction = lambda: print("Closing transaction...")
confirm_payment = lambda: print("Confirming payment...")

# Funções que representam cada etapa do fluxo de "Fund Transfer"
fund_trasnfer = lambda: print("Transferring fund...")
bank_details = lambda: print("Providing bank deposit details...")

# Funções de fluxo
confirm_payment_approval_from_bank = lambda: input("Was the operation canceled? (Yes/No): ")

confirm_amount = lambda: input("Amount: ")

decision = lambda: (confirm_payment(), credit_activities.append(complete_transaction)) and \
                   fund_cash_activities.append(complete_transaction) if \
                   confirm_payment_approval_from_bank().lower() == "no" \
                   else (cancel_transaction(), close_transaction())

# Lista de atividades para o fluxo "Credit"
credit_activities = [
    create_transaction,
    request_credit_account_details,
    request_payment_from_bank,
    decision
]

# Lista de atividades para o fluxo "Cash"
cash_activities = lambda: [
    create_transaction,
    receive_cash,
    print_payment_receipt,
    return_payment_receipt,
    complete_transaction
]

fund_cash_activities = [
    create_transaction,
    fund_trasnfer,
    bank_details,
    decision
]

# Função para verificar as credenciais do usuário com base no login
authenticate_user = lambda login, password: any(login == user and
                                                info["password"] == password
                                                for user, info in user_accounts().items())

# Função lambda para verificar saldo suficiente
check_balance = lambda user, amount: user_accounts().get(user, {}).get("balance", 0) > amount if \
                type(amount) is int or type(amount) is float else None

authenticate_and_check = lambda login, password: \
                        confirm_amount() if authenticate_user(login, password) \
                        else (False, None)

check_balance_and_check = lambda login, amount: (True, print("The user has sufficient balance...")) if \
                        check_balance(login, amount) else (False, print("The user does NOT have sufficient balance..."))

debit = lambda user, amount, flow: {**user_accounts(), **{user: {**user_accounts()[user],
                                                           "balance": user_accounts()[user]["balance"] - amount}}} if \
                                                            check_balance(user, amount)  else None

# Função para executar o fluxo de atividades
execute_activities = lambda activities: [activity() for activity in activities if activity]

# Função para escolher o fluxo com base na entrada do usuário e executar as atividades correspondentes
choose_flow = lambda flow_type: execute_activities(cash_activities) if flow_type == "cash" \
            else execute_activities(credit_activities) if flow_type == "credit" \
            else execute_activities(fund_cash_activities) if flow_type == "fund" \
            else print("Invalid flow type")
# Teste
authenticated, amount = authenticate_and_check("alice123", "p")
authenticated_action = lambda auth, login, amount: check_balance_and_check(login, amount) \
                        if auth else print("Credenciais inválidas.")

authenticated_action(authenticated, "alice123", amount)
check_balance_action = lambda auth, login, amount, flow: choose_flow(flow) and debit(login, amount, flow) \
                        if check_balance(login, amount) and auth else None
check_balance_action(authenticated, "alice123", amount, "cash")
print(user_accounts())
user_accounts = debit("alice123", 100, "cash")
print(user_accounts)
