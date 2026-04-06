import os
from datetime import date

import pandas as pd
from dateutil.relativedelta import relativedelta

file_path = "loan.xlsx"
is_found = False

# Test file existence
if os.path.exists(file_path):
    df = pd.read_excel(file_path, sheet_name="active")
    loan = df.to_dict(orient="records")
    is_found = True

    try:
        df1 = pd.read_excel(file_path, sheet_name="finished")
        finished_loan = df1.to_dict(orient="records")
    except FileNotFoundError:
        finished_loan = []

else:
    loan = []
    finished_loan = []

# Blank list for new data updates
new_loan_data = []
new_finished_loan = []


# Function to create new loan entry
def new_loan(name, amount, duration):
    # Loan informations save to dictionary
    loan_dict = {}
    interest_rate = 0.05  # 5% interest rate
    loan_dict["name"] = name
    loan_dict["amount"] = amount
    loan_dict["duration"] = duration
    loan_dict["start_date"] = date.today()

    # Adds total duration of loan (months) to the start date of loan application
    loan_dict["end_date"] = date.today() + relativedelta(months=duration)

    # Loan total computation (amount + total interest)
    loan_dict["total_credit"] = amount + (amount * interest_rate * duration)

    # Loan computation for monthly payment
    loan_dict["monthly_payment"] = (
        amount + (amount * interest_rate * duration)
    ) / duration

    loan_dict["total_payment"] = 0

    # Validate if loan excel file exists if True will create new list to be added to existing excel file
    if is_found:
        new_loan_data.append(loan_dict)
    else:
        loan.append(loan_dict)


# Function to view loan information
def view_loan(name):
    is_found = False
    if new_loan_data:
        for i in range(len(new_loan_data)):
            if name.lower() == new_loan_data[i]["name"]:
                is_found = True
                for key, value in new_loan_data[i].items():
                    print(f"{key}: {value}")

    for i in range(len(loan)):
        if name.lower() == loan[i]["name"]:
            is_found = True
            for key, value in loan[i].items():
                print(f"{key}: {value}")

    if not is_found:
        print(f"No active loan for {name} found!")


# Function for payment updates
def payment(name, amount):
    is_found = False
    # If loan record is empty
    if loan == []:
        print("No active loans!")

    # Finds loan name from the records and make computation for payment
    for i in range(len(loan)):
        if name.lower() in loan[i]["name"]:
            is_found = True
            loan[i]["total_payment"] += amount
            loan[i]["balance"] = loan[i]["total_credit"] - loan[i]["total_payment"]

            # Once loan is finished it will transfer to a new list for record purposes
            if loan[i]["balance"] == 0:
                new_finished_loan.append(loan[i])
                loan.pop(i)
                print("Thank you for completing your loan payments!")
                break
            else:
                print(
                    f"Remaining balance as of {date.today().strftime('%b %d, %Y')} : {loan[i]['balance']:,.2f} "
                )

    # If name of loan not found
    if not is_found:
        print(f"No active loan for {name} found!")


# Function to clear screen
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


# Main Function that will take user input for data requirement
def main():
    # Prints choices for user into new screen until user choose to exit
    while True:
        clear_screen()
        print("--- Loaning App ---")
        print("\n1. Apply for new loan")
        print("2. View loan information")
        print("3. Make payments")
        print("4. Exit")

        # Takes user input for chosen transaction
        ch = input("\nPlease enter number for your transaction: ")

        if ch == "1":
            name = input("Please enter loan name: ").strip()
            amount = input("Please enter amount to loan: ").strip()
            duration = input("Please enter duration of loan (months): ").strip()

            # Loop for checking a valid number input
            while not amount.isdigit() and not duration.isdigit():
                print("Please enter a valid number!")
                amount = input("Please enter amount to loan: ").strip()
                duration = input("Please enter duration of loan (months): ").strip()

            # Run if data input is complete
            if name and amount and duration:
                new_loan(name, int(amount), int(duration))
                input("\nPress enter to continue...")

        elif ch == "2":
            if new_loan_data == [] and loan == []:
                print("No active loans!")
                input("\nPress enter to continue...")
            else:
                name = input("Please enter name of loan: ").strip()
                if name:
                    view_loan(name)
                    input("\nPress enter to continue...")

        elif ch == "3":
            name = input("Please enter loan name: ").strip()
            amount = input("Please enter amount to pay: ").strip()

            # Loop for checking a valid number input
            while not amount.isdigit():
                print("Please enter a valid number!")
                amount = input("Please enter amount to pay: ").strip()

            # Run if data input is complete
            if name and amount:
                payment(name, int(amount))
                input("\nPress enter to continue...")

        # Program exit and saves updates to Excel file
        elif ch == "4":
            print("Thank you for using my app! Goodbye!")

            # If existing Excel file found update file
            if is_found:
                # Updates active loan
                df_new_loan = pd.DataFrame(new_loan_data)
                df_old = pd.DataFrame(loan)
                df_final_loan = pd.concat([df_old, df_new_loan], ignore_index=True)

                # Updates finished loan
                df_new_fin_loan = pd.DataFrame(new_finished_loan)
                df_old_fin_loan = pd.DataFrame(finished_loan)
                df_final_fin_loan = pd.concat(
                    [df_old_fin_loan, df_new_fin_loan], ignore_index=True
                )

                # Saves updates
                with pd.ExcelWriter("loan.xlsx", engine="xlsxwriter") as writer:
                    df_final_loan.to_excel(writer, sheet_name="active", index=False)
                    df_final_fin_loan.to_excel(
                        writer, sheet_name="finished", index=False
                    )

            # If no existing Excel file found create new file
            else:
                df = pd.DataFrame(loan)
                df1 = pd.DataFrame(finished_loan)
                with pd.ExcelWriter("loan.xlsx", engine="xlsxwriter") as writer:
                    df.to_excel(writer, sheet_name="active", index=False)
                    df1.to_excel(writer, sheet_name="finished", index=False)
            break

        else:
            print("Invalid input!")
            input("\nPress enter to continue...")


# Main program start
if __name__ == "__main__":
    main()
