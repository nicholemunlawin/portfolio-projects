import os
from datetime import date

import pandas as pd
from dateutil.relativedelta import relativedelta

file_path = "loan.xlsx"
is_found = False

# Test file existence
if os.path.exists(file_path):
    df = pd.read_excel(file_path, sheet_name="active")
    try:
        df1 = pd.read_excel(file_path, sheet_name="finished")
        finished_loan = df1.to_dict(orient="records")
    except:
        finished_loan = []
    finally:
        loan = df.to_dict(orient="records")
        new_loan_data = []
        new_finished_loan = []
        is_found = True
else:
    print("File does not exists!")
    loan = []
    finished_loan = []


# Function to create new loan entry
def new_loan(name, amount, duration):
    # Loan informations save to dictionary
    loan_dict = {}
    interest_rate = 0.05  # 5% interest rate
    loan_dict["name"] = name
    loan_dict["amount"] = amount
    loan_dict["duration"] = duration
    loan_dict["start_date"] = date.today()
    loan_dict["end_date"] = date.today() + relativedelta(months=duration)
    loan_dict["total_credit"] = amount + (amount * interest_rate * duration)
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
    if loan == []:
        print("No active loans!")
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
    if loan == []:
        print("No active loans!")
    for i in range(len(loan)):
        if name.lower() in loan[i]["name"]:
            is_found = True
            loan[i]["total_payment"] += amount
            loan[i]["balance"] = loan[i]["total_credit"] - loan[i]["total_payment"]
            if loan[i]["balance"] == 0:
                # Once loan is finished it will transfer to a new list for record purposes
                finished_loan.append(loan[i])
                loan.pop(i)
                print("Thank you for comleting your loan payments!")
                break
            else:
                print(
                    f"Remaining balance as of {date.today().strftime('%b %d, %Y')} : {loan[i]['balance']:,.2f} "
                )
    if not is_found:
        print(f"No active loan for {name} found!")


# Function to clear screen
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


# Main Function that will take user input for data requirement
def main():
    while True:
        # Run program until user choose to exit
        clear_screen()
        print("--- Loaning App ---")
        print("\n1. Apply for new loan")
        print("2. View loan information")
        print("3. Make payments")
        print("4. Exit")
        ch = input("\nPlease enter number for your transaction: ")
        if ch == "1":
            name = input("Please enter loan name: ").strip()
            amount = input("Please enter amount to loan: ").strip()
            duration = input("Please enter duration of loan (months): ").strip()
            while not amount.isdigit() and not duration.isdigit():
                print("Please enter a valid number!")
                amount = input("Please enter amount to loan: ").strip()
                duration = input("Please enter duration of loan (months): ").strip()
            if name and amount and duration:
                new_loan(name, int(amount), int(duration))
                input("\nPress enter to continue...")
        elif ch == "2":
            name = input("Please enter name of loan: ").strip()
            if name:
                view_loan(name)
                input("\nPress enter to continue...")
        elif ch == "3":
            name = input("Please enter loan name: ").strip()
            amount = input("Please enter amount to loan: ").strip()
            while not amount.isdigit():
                print("Please enter a valid number!")
                amount = input("Please enter amount to loan: ").strip()
            if name and amount:
                payment(name, int(amount))
                input("\nPress enter to continue...")
        elif ch == "4":
            print("Thank you for using my app! Goodbye!")
            if is_found:
                df_new_loan = pd.DataFrame(new_loan_data)
                df_old = pd.read_excel(file_path, sheet_name="active")
                df_final_loan = pd.concat([df_old, df_new_loan], ignore_index=True)
                df_final_loan.to_excel("loan.xlsx", sheet_name="active", index=False)
                if finished_loan:
                    df_new_fin_loan = pd.DataFrame(new_finished_loan)
                    df_old_fin_loan = pd.read_excel(file_path, sheet_name="finished")
                    df_final_fin_loan = pd.concat(
                        [df_old_fin_loan, df_new_fin_loan], ignore_index=True
                    )
                    df_final_fin_loan.to_excel(
                        "loan.xlsx", sheet_name="finished", index=False
                    )
            else:
                df = pd.DataFrame(loan)
                if finished_loan:
                    df1 = pd.DataFrame(finished_loan)
                with pd.ExcelWriter("loan.xlsx", engine="xlsxwriter") as writer:
                    df.to_excel(writer, sheet_name="active", index=False)
                    df1.to_excel(writer, sheet_name="finished", index=False)
            break
        else:
            print("Invalid input!")
            input("\nPress enter to continue...")


if __name__ == "__main__":
    main()
