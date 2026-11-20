import random
def generate_minute():
    minute = random.randint(30, 180)
    return minute
def calc_amount(machine_type,minutes):
    if machine_type =="A":
        cost=50.00
        rate = 30.00
    elif machine_type =="B":
        cost=62.50
        rate = 36.25
    elif machine_type =="C":
        cost=74.87
        rate =40.50
    else:
        cost=0.00
        rate=0.00


    hours = minutes/60
    amount_before_vat = cost +(rate*hours)
    return amount_before_vat

def calc_total_amount(amount):
        VAT = amount * 0.14
        total_amount = amount + VAT
        return total_amount, VAT

def display_summary(payments):
    num_customer = len(payments)
    #total_amount, VAT = calc_total_amount(payments)
    if num_customer==0:
        print("No customer payments processed")
        return
    combined_amount = sum(payments)
    ave_payment =combined_amount/num_customer
    highest_payment = max(payments)
    lowest_payment = min(payments)


    print("\n"+"="*20)
    print(" DAILY SUMMARY" )
    print("="*20)
    print (f"number of customers : {num_customer}")
    print (f"Combined amount : R{combined_amount:.2f}")
    print (f"Average payment per costumer : R{ave_payment:.2f}")
    print (f"Highest payment : R{highest_payment:.2f}")
    print (f"Lowest payment : R{lowest_payment:.2f}")
    print("=" * 20)


def process_payments():
    num_customer = int (input("Enter the number of customer to process: ?       "))
    payments = []
    for num in range(num_customer):
        customer_name = input("Enter the customer name: ?         ")
        machine_type = input("Enter the machine type (A,B or C ): ?").upper()
        minutes = generate_minute()
        amount_before_vat = calc_amount(machine_type,minutes)
        total_amount, VAT = calc_total_amount(amount_before_vat)
        payments.append(total_amount)


        print("\n"+"-"*20)
        print("   INVOICE")
        print("-"*20)
        print(f"Customers name : {customer_name}")
        print(f"Machine Type : {machine_type}")
        print(f"Minutes generated : {minutes}: mins")
        print(f"Amount before VAT R{amount_before_vat:.2f}")
        print(f"VAT amount (14%) : R{VAT:.2f}")
        print(f"Total payable amount : R{total_amount:.2f}")
        print("-" * 20)
        print("\n")

    display_summary(payments)

process_payments()


