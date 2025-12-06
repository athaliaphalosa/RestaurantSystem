__author__ = "8515942, Phalosa, 8499763, El Marini"

import csv
from datetime import datetime

# For all item Food in the mneu
class Food:
    def __init__(self, name, typ, categorie, price):
        self.name = name
        self.typ = typ
        self.categorie = categorie
        self.price = float(price)
    
    # The form to show the menu card
    def show_item(self):
        print(f"Name: {self.name}   -   Categorie: {self.categorie}   -   Price: {self.price}")

# For the customer make the order
class Order:
    def __init__(self, table_number):
        self.table_number = table_number
        self.items = []
        self.special_wish = []
        self.not_paid = True
        self.total_price = 0
        
    # To customer add their order
    def add_foods(self, foods, special_request =" "):
        if self.not_paid:
            item = {"foods": foods, "special_request": special_request}
            self.items.append(item)
            self.total_price += foods.price

            # To add special request or add additional
            if special_request:
                self.special_wish.append(special_request)
                if "extra" in special_request or "more" in special_request:
                    # Will be charged 1 EUR
                    self.total_price += 1
                    print(f"{foods.name} with special request {special_request} (1 EUR added to the price!)")
                else:
                    print(f"{foods.name} with special request {special_request}")

        # When bill allready paid cannot add any more item
        else:
            print("Cannot add more item, the bill already succesfully paid!")
        
    # If customer want to changer their order before payment
    def remove_foods(self, food_name):
        if self.not_paid:
            for item in self.items:
                if item["foods"].name.lower() == food_name.lower():
                    self.items.remove(item)
                    self.total_price -= item["foods"].price
                    if "extra" in item["special_request"] or "more" in item["special_request"]:
                        self.total_price -= 1
                    print("~ ~" * 68)
                    print(f"{food_name} removed from your order. New total: {self.total_price} EUR")
                    print("~ ~" * 68)
                    return
            print("~ ~" * 68)
            print(f"{food_name} is not in the order!")
            print("Check again, maybe you made a typing mistake :)")
            print("~ ~" * 68)

        # When bill allready paid cannot remove any item that allready added
        else:
            print("Cannot remove items, the bill has already succesfully paid!")

    # If bill allready paid
    def mark_paid(self):
        self.not_paid = False
        print("~ ~" * 68)
        print(f"Bill for table {self.table_number} has been marked as paid!")
        print("You cannot change anything anymore")
        print("~ ~" * 68)

    # To make the invoice
    def invoice(self):
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("\n* Invoice *")
        print(f"Invoice Time: {time_now}")
        print(f"\nInvoice for table {self.table_number}")
        for item in self.items:
            print(f'\n{item["foods"].name} - {item["foods"].price} EUR')
            if item["special_request"]:
                print(f'Special request: {item["special_request"]}') 
        print(f"\nTotal price: {self.total_price} EUR")
        
    # To save the invoice in txt. file
    def save_invoice(self, filename = "rechnung.txt"):
        with open(filename, "w") as bill:
            order = [f"\nINVOICE TABLE {self.table_number}\n"]
            time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            order.append(f"INVOICE TIME: {time_now}\n")

            for item in self.items:
                order.append(f'\n{item["foods"].name} - {item["foods"].price} EUR\n')
                if item["special_request"]:
                    order.append(f'Self request: {item["special_request"]}\n')

            order.append(f"\nTotal price: {self.total_price} EUR")
            bill.writelines(order)
        
        print(f"\nInvoice saved to {filename}")

# To show the menu in file csv
class MenuReader:
    def __init__(self, filename = "food.csv"):
        self.filename = filename

    def reading_menu(self):
        menu = []
        with open(self.filename, "r") as card:
            read_menu = csv.reader(card, delimiter = ';' )
            next(read_menu)
            for row in read_menu:
                if len(row) == 4:
                        price = row[3].replace(",", ".")
                        food_item = Food(name=row[0], typ=row[1], categorie=row[2], price=float(price))
                        menu.append(food_item)
        return menu

# To run the programm
def main():
    
    print("\n" + ("<<") * 44 +  " Welcome to ABC Restaurant!! " + (">>" * 43))

    # to show the menu
    menu_reader = MenuReader("food.csv")
    menu = menu_reader.reading_menu()
    print("\n" + ("* *" * 68))
    print("\n" + ("  ") * 44 + "MENU / SPEISE KARTE:\n" + ("  " * 43))
    num = 1
    for food_item in menu:
        print(("  ") * 30 + f"{num}. Name: {food_item.name} - Typ: {food_item.typ} - Categorie: {food_item.categorie} - Price: {food_item.price} EUR" + ("  " * 43))
        num +=1
    print("\n" + ("* *" * 68))
    
    # To input number table
    while True:
        try:
            table_number = int(input("\nEnter your table number: "))
            break
        except ValueError:
            print("Invalid number! Please enter a valid number for your table")
    order = Order(table_number)

    # To order food with or without additional
    while True:
        print("- -" * 68)
        print("\nNow you can order food, remove food, or mark the bill as paid!")
        print("\nIf you choose '1', type 'exit' when you allready done choose your food!\n")
        print("1. Order food")
        print("2. Remove food from order")
        print("3. Mark Bill as paid")
        print("4. If you haved done order!")

        choice = input("Enter your choice between 1 - 4: ")

        # Order food
        if choice == "1":

            while True:
                print("\n" + ("! !" * 25) + " Type 'exit' when you allready done choose your food " + ("! !" * 24) + "\n")
                choose_food = input("Enter the menu number you would like to order: ")

                # Done ordering
                if choose_food.lower() == "exit":
                    break

                if choose_food.isdigit():
                    choose_food = int(choose_food)
                    if 1 <= choose_food <= len(menu):
                            print("- -" * 68)
                            print("\nYou can have additional special request with type 'extra' or 'more'")
                            print("Every extra additional will be charged 1 EUR!")
                            print("Special request that leave something out will not change the price!")
                            special_request = input("\nDo you want some special request?, write here: ")
                            order.add_foods(menu[choose_food - 1], special_request)
                    else:
                        print("~ ~" * 68)
                        print("Invalid input! Please enter invalid number from the menu!")
                        print("~ ~" * 68)
                else:
                    print("Invalid input! Please enter invalid number or type 'exit' when you allready done ordering ")
    
        # Remove food by entering the name of the food
        elif choice == "2":
                food_name = input("Enter the name of food in menu you want cancelled to order: ")
                order.remove_foods(food_name)
        
        # Mark the bill as paid
        elif choice == "3":
            order.mark_paid()
            break 
        
        elif choice == "4":
            break

        # If the choice ist not between 1 - 4
        else:
            print("Invalid choice! Please choose between 1 and 4!")

    # To show the invoice
    print("* *" * 68)
    order.invoice()

    # To save invoice in txt. file
    order.save_invoice()

if __name__ == "__main__":
    main()


    
    





        

    

    


    
