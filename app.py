"""
Main user interface.

Database top row: phone_number, surname, name, date_of_registration, total_expenses, bonus_card.

Description of bonus cards:
standard - every customer
bronze - total expenses > 1 000 rubles
silver - total expenses > 5 000 rubles
gold - total expenses > 10 000 rubles
"""
import sqlite3
from datetime import date
import database
print("There is your cafe customers app.")
database.create_table()


def _menu():
    user_choice = input("""
        You can:
        'a' - add a customer.
        'd' - delete a customer.
        'q' - check the list of available queries.
        'ae' - add expenses for a customer.
        'e' - exit app.
        
        Your choice: 
        """)

    if user_choice in [command for command in commands]:
        commands[user_choice]()
    else:
        print(f"Sorry, but {user_choice} is invalid command.")
    _menu()


def _get_phone_number():
    phone_number = input("Phone number: +7/8 ")
    try:
        int(phone_number)
    except ValueError("You should enter a number."):
        pass
    else:
        if len(phone_number) != 10:
            print("Not valid phone number. It should have 10 digits.")
        else:
            return int(phone_number)


def add_customer():
    phone_number = _get_phone_number()
    name = input("Name: ")
    surname = input("Surname: ")
    date_of_registration = date.today().strftime('%y/%m/%d')  # format 21/11/04

    try:
        database.add_customer(phone_number, surname.title(), name.title(), date_of_registration)
        print("Customer is successfully added.")
    except sqlite3.Error:
        print("A customer with that phone number already exists.")


def delete_customer():
    phone_number = _get_phone_number()

    try:
        customer = database.get_certain_customer(phone_number)  # returns a dictionary with data
        proceed = input(f"""
        You want to delete the following customer: {customer['surname']} {customer['name']},
        registered: {_convert_date(customer['date_of_registration'])}, phone number: {customer['phone_number']},
        total expenses: {customer['total_expenses']}
        Proceed? (yes/no)""")
        if proceed == 'yes':
            database.delete_customer(phone_number)
            print("Customer is successfully deleted.")
        else:
            print("Customer is not deleted.")
    except sqlite3.Error:
        print("There is no such customer.")


def _list_queries():
    user_choice = input("""
    You can do several queries for data:
    'top' - get top or bottom X customers by parameter.
    'get' - extract info about certain customer by phone number.
    'bonus' - get info about people with certain bonus card type.
    'list' - list all customers.
    
    Your choice: 
    """)
    if user_choice in [query for query in queries]:
        queries[user_choice]()
    else:
        print(f"Sorry, but {user_choice} is not valid command.")


def _update_bonus_card(total_expenses, new_expenses):
    expenses = total_expenses + new_expenses
    if expenses > 10000:
        return 'gold'
    elif 5000 < expenses <= 10000:
        return 'silver'
    elif 1000 < expenses <= 5000:
        return 'bronze'
    else:
        return 'standard'


def add_expenses():
    phone_number = _get_phone_number()
    customer = database.get_certain_customer(phone_number)
    user_choice = input(f"""
          {customer['surname']} {customer['name']},
          registered: {_convert_date(customer['date_of_registration'])},
          phone number: {customer['phone_number']},
          total expenses: {customer['total_expenses']}
          Proceed? (yes/no)""")
    if user_choice == 'yes':
        expenses = input(f"This sum will be added to {customer['surname']} {customer['name']} total expenses: ")
        try:
            expenses = float(expenses)
            update = _update_bonus_card(customer['total_expenses'], expenses)
            database.add_expenses(phone_number, expenses, update)
            print("Expenses successfully updated.")
        except ValueError:
            print("You should enter a number.")


commands = {
    'a': add_customer,
    'd': delete_customer,
    'q': _list_queries,
    'ae': add_expenses,
    'e': exit
}


def list_customers():
    customers = database.get_customers()  # returns a list (of dictionaries) of customers
    for count, customer in enumerate(customers):
        print(f"{count + 1}, {customer['phone_number']}, {customer['surname']} {customer['name']}, date registered: "
              f"{_convert_date(customer['date_of_registration'])}, total expenses:"
              f"{customer['total_expenses']}, bonus card: {customer['bonus_card']}")


def _convert_date(registration_date):
    x = [int(digit) for digit in str(registration_date)]
    return f"20{x[0]}{x[1]}/{x[2]}{x[3]}/{x[4]}{x[5]}"


def get_certain_customer():
    phone_number = _get_phone_number()
    customer = database.get_certain_customer(phone_number)
    print(f"{customer['phone_number']}, {customer['surname']} {customer['name']}, date registered: "
          f"{_convert_date(customer['date_of_registration'])}, total expenses: {customer['total_expenses']},"
          f"bonus card: {customer['bonus_card']}")


def get_bonus_info():
    card_types = {
        1: 'standard',
        2: 'bronze',
        3: 'silver',
        4: 'gold'
    }
    bonus_card = input("""
    1 - standard card - 0%
    2 - bronze card - 15%
    3 - silver card - 10%
    4 - gold card - 20%
    
    Enter the type of card you want to get info about: 
    """)
    try:
        int(bonus_card)
        if int(bonus_card) in [1, 2, 3, 4]:
            bonus_card_customers = database.get_bonus_info(card_types[int(bonus_card)])
            print(f"There is {len(bonus_card_customers)} with {bonus_card} level of card: ")
            for count, customer in enumerate(bonus_card_customers):
                print(f"{count + 1}, {customer['phone_number']}, {customer['surname']} {customer['name']},"
                      f"date registered: {_convert_date(customer['date_of_registration'])}, total expenses: "
                      f"{customer['total_expenses']}, bonus card: {customer['bonus_card']}")

        else:
            print("Invalid card type. Enter 1,2,3, or 4")
    except ValueError:
        print("You should enter a number from 1 to 4.")


def top_bottom_customers():
    orders = {
        1: 'ASC',  # A to Z (smallest to largest/ 0 to 9)
        2: 'DESC'  # Z to A (largest to smallest/ 9 to 0)
    }

    number = input("Enter top # of customers you want to see: ")
    order = input(f"""
        You can choose {number} customers from top or bottom.
        1 - bottom {number} customers.
        2 - top {number} customers.
        """)
    criteria = input(f"""
        Which criteria you want to use?
        1 - {order} {number} customers by date of registration.
        2 - {order} {number} customers by total expenses.
        """)
    try:
        number = int(number)
        order = int(order)
        criteria = int(criteria)
        if criteria in [1, 2] and order in [1, 2]:
            order = orders[order]
            customers = database.top_bottom_customers(number, order, criteria)
            for count, customer in enumerate(customers):
                print(
                    f"{count + 1}, {customer['phone_number']}, {customer['surname']} {customer['name']}, date registered: "
                    f"{_convert_date(customer['date_of_registration'])}, total expenses: {customer['total_expenses']}, bonus card: "
                    f"{customer['bonus_card']}")
        else:
            print("You should enter 1 or 2.")
    except ValueError:
        print("You should enter a number.")


queries = {
    'list': list_customers,
    'get': get_certain_customer,
    'bonus': get_bonus_info,
    'top': top_bottom_customers
}


_menu()
