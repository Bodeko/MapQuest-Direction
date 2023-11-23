import urllib.parse
import requests
from tabulate import tabulate
from termcolor import colored

main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "BW8Al6QTGtw9DYzouwsy6hKdGxVjQjVd"

def get_input(prompt):
    while True:
        user_input = input(prompt).strip()
        if user_input.lower() in ('quit', 'q'):
            return None
        else:
            return user_input

def calculate_fuel(distance, fuel_efficiency):
    return (distance / 100) * fuel_efficiency

while True:
    orig = get_input("Місцезнаходження: ")
    if orig is None:
        break
    
    dest = get_input("Пункт призначення: ")
    if dest is None:
        break
    
    unit = get_input("Введіть 'km' для кілометрів або 'mile' для миль: ")
    if unit is None or unit.lower() not in ('km', 'mile'):
        print("Недійсний ввід для одиниці виміру. Будь ласка, введіть 'км' або 'миль'.")
        continue
    
    url = main_api + urllib.parse.urlencode({"key": key, "from": orig, "to": dest})
    json_data = requests.get(url).json()
    print("URL: " + url)
    json_status = json_data["info"]["statuscode"]
    
    if json_status == 0:
        print("Статус API: " + str(json_status) + " = Успішний виклик маршруту.\n")
        print("=============================================")
        print("Напрямки з " + orig + " до " + dest)
        print("Час подорожі:   " + json_data["route"]["formattedTime"])
        
        distance = json_data["route"]["distance"] * (1.61 if unit.lower() == 'km' else 1)
        print(f"Кілометри:      {colored(f'{distance:.2f}', 'red')}" if unit.lower() == 'km'
              else f"Милі:           {colored(f'{distance:.2f}', 'red')}")
        
        fuel_efficiency = float(input(f"Введіть витрату пального вашого автомобіля на 100 {'км в літрах' if unit.lower() == 'km' else 'миль'}: "))
        fuel_required = calculate_fuel(distance, fuel_efficiency)
        print(colored(f"Потрібно бензину для подорожі: {str(int(fuel_required))} л", 'yellow'))
        input("Натисніть Enter для відображення маршруту...")
        print("=============================================")
        print("Маневри:")
        distance = json_data["route"]["distance"] * (1.61 if unit.lower() == 'km' else 1)
    print(f"Кілометри:      {colored(f'{distance:.2f} км', 'red')}" if unit.lower() == 'km'
          else f"Милі:           {colored(f'{distance:.2f} миль', 'red')}")

    fuel_efficiency = float(input(f"Введіть витрату пального вашого автомобіля на 100 {'км' if unit.lower() == 'km' else 'миль'}: "))
    fuel_required = calculate_fuel(distance, fuel_efficiency)
    if unit.lower() == 'km':
        print(f"Потрібно бензину для подорожі: {colored(f'{fuel_required:.2f} л', 'yellow')}")
    else:
        print(f"Потрібно бензину для подорожі: {colored(f'{fuel_required * 3.78541:.2f} л', 'yellow')}")  # Convert gallons to liters

    input("Натисніть Enter для відображення маршруту...")
    print("=============================================")
    print("Маневри:")
    distance_unit = 'миль' if unit.lower() == 'mile' else 'км'
    maneuvers = [[step["narrative"], f"{step['distance']:.2f} {distance_unit}"] for step in json_data["route"]["legs"][0]["maneuvers"]]
    print(tabulate(maneuvers, headers=["Інструкція", "Відстань"], tablefmt="grid"))
    print("=============================================\n")