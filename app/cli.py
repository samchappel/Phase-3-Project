#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from datetime import datetime
import colorama

from models import Owner, Pet, Provider, Service

from helpers import update_pet, print_pet, add_new_pet, query_pets, create_new_dropwalk, book_house_sitting

engine = create_engine('sqlite:///wagging_rights.db')
session = sessionmaker(bind=engine)()

YES = ['y', 'ye', 'yes']
NO = ['n','no']
line = '-'*50 #adds line
line_db = '\n' + line + '\n' #adds line with double spacing


if __name__ == '__main__':
    #Intro: welcome to the CLI, pick a store


    colorama.init()

    print(colorama.Fore.YELLOW +'''
██╗    ██╗ █████╗  ██████╗  ██████╗ ██╗███╗   ██╗ ██████╗ ██████╗ ██╗ ██████╗ ██╗  ██╗████████╗███████╗
██║    ██║██╔══██╗██╔════╝ ██╔════╝ ██║████╗  ██║██╔════╝ ██╔══██╗██║██╔════╝ ██║  ██║╚══██╔══╝██╔════╝
██║ █╗ ██║███████║██║  ███╗██║  ███╗██║██╔██╗ ██║██║  ███╗██████╔╝██║██║  ███╗███████║   ██║   ███████╗
██║███╗██║██╔══██║██║   ██║██║   ██║██║██║╚██╗██║██║   ██║██╔══██╗██║██║   ██║██╔══██║   ██║   ╚════██║
╚███╔███╔╝██║  ██║╚██████╔╝╚██████╔╝██║██║ ╚████║╚██████╔╝██║  ██║██║╚██████╔╝██║  ██║   ██║   ███████║
 ╚══╝╚══╝ ╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝

                                        |\_/|
                                        | @ @   Woof!
                                        |   <>              _
                                        |  _/\------____ ((| |))
                                        |               `--' |
                                    ____|_       ___|   |___.'
                                    /_/_____/____/_______|

''' + colorama.Style.RESET_ALL)

    print("Welcome to Wagging Rights CLI!")
    print('')
    while True:
        try:
            # Ask user to input their ID number (corresponds with owner_id)
            owner_id = int(input("""Please enter your Owner ID to get started.

ENTER: """))
            break
        except ValueError:
            print("Please enter a valid Owner ID.")

    # Ask user to input their ID number (corresponds with owner_id)
    # Use owner_id to query Owners table and return owner name.
    owner_name = session.query(Owner.name).filter(Owner.id == owner_id).first()[0].split(" ")[0]
    # Print Welcome, {Name} and prompt them to input whether they would like to manage pets or appointments.
    print('\n' + line + '\n')
    print(f"Welcome, {owner_name}! What would you like to do today?")
    print('')
    print(f'Please Enter:')


#MAIN MENU" START:
    main_menu = True
    while main_menu:
        task = int(input(f"""
    1 - View Your Pet Profile(s)
    2 - Book An Appointment

ENTER: """))

#"PET MENU" START:
        if task == 1:
            pet_menu = True
            while pet_menu:
                print('\n' + line + '\n')
                print("Your Pet Profile(s):")
                print('')
                # Use owner_id to query Pets table and return all pets associated with that owner.
                pets = session.query(Pet).filter(Pet.owner_id == owner_id).all()
                for pet in pets:
                    print(pet)
                # Prompt user to select from options to Add Pet, Update Pet, Remove Pet
                option = int(input("""Please Enter:

    1 - Add A Pet
    2 - Update A Pet
    3 - Remove A Pet
    4 - Return To Task Menu

ENTER: """))

#"ADD OPTION" START:
                if option == 1:
                    add = True
                    while add:
                        print('\n' +'\n')
                        print('')
                        print("Please provide information about your new pet!")
                        print(line)
                        print('')
                        name = input("Name: ")
                        age = int(input("Age: "))
                        breed = input("Breed: ")
                        temperament = input("Temperament: ")
                        treats = input("Favorite Treats: ")
                        notes = input("Additional Notes/Special Needs: ")
                        add_new_pet(session, name, age, breed, temperament, treats, notes, owner_id)
                        yes_no = input("""
Would you like to add another pet? Y/N: """).lower()
                        if yes_no.lower() in YES:
                            continue
                        elif yes_no.lower() in NO:
                            print("Routing you back to the main menu...")
                            add = False
                            continue
#"ADD OPTION" END.


#"UPDATE OPTION" START:
                elif option == 2:
                    update = True
                    while update:
                        print(line)
                        pet_id = int(input(f"""You've selected update! Enter the ID of the pet you want to update.

ENTER: """))
                        pet = session.query(Pet).filter(Pet.id == pet_id, Pet.owner_id == owner_id).first()
                        if not pet:
                            print(f"""Invalid ID. Please enter a valid ID that belongs to your pet.

ENTER: """)
                            continue
                        else:
                            print('')
                            field = int(input(f"""What updates would you like to make for {pet.name}? 
1 - Name 
2 - Age 
3 - Breed 
4 - Temperament
5 - Treats
6 - Notes

ENTER: """))
                            if field.isdigit() and int(field) >= 1 and int(field) <= 6:
                                print(f"""Invalid entry. Please enter a number between 1 and 6.""")
                                continue
                            else:
                                new_value = input(f"""Enter the new value for {field}:

ENTER: """)
                                update_pet(session, pet, field, new_value)
                                print_pet(pet)
                                yes_no = input("Would you like to update another pet? Yes/No: ").lower()
                                if yes_no.lower() in YES:
                                    continue
                                elif yes_no.lower() in NO:
                                    print("Routing you back to the main menu...")
                                    update = False

#"UPDATE OPTION" END.


#"REMOVE OPTION" START:
                elif option == 3:
                    remove = True
                    while remove:
                        print('')
                        pet_idx = int(input(f"""Please provide a valid Pet ID for the pet you wish to remove.

ENTER: """))
                        pets = session.query(Pet).filter(Pet.id == pet_idx).first()
                        if pets.owner_id == owner_id:
                            print('')
                            print(pets)
                            yes_no = input("Do you wish to delete this pet? (Y/N): \n")
                            if yes_no.lower() in YES:
                                session.delete(pets)
                                session.commit()
                                print('Your pet has been removed successfully!')
                                rem_another = input('Would you like to remove another pet? (Y/N): \n')
                                if rem_another.lower() in YES:
                                    continue
                                elif rem_another.lower() in NO:
                                    print("Routing you back to main menu...")
                                    remove = False
                                else:
                                    print('')
                                    print('ERROR: Please select a valid Pet ID.')
                                    continue
                    else:
                        print('')
                        print('ERROR: Please select a valid Pet ID.')
                        continue
#"REMOVE OPTION" END.


#"BACK OPTION" START:
                elif option == 4:
                    pet_menu = False
#"BACK OPTION" END.


                else:
                    print("Invalid input.")
#"PET MENU" END.





#"APPOINTMENT MENU" START:
        elif task == 2:
            appointment_menu = True
            while appointment_menu:
                print(line_db)
                print("Your Pets with upcoming bookings:")
                print(line_db)
                query = session.query(Pet).filter(Pet.owner_id == owner_id).all()
                pets = [pet for pet in query]
                for pet in pets:
                    print(pet.name)
                print(f'Appointment(s): ')
                for pet in pets:
                    services = session.query(Service).filter(Service.pet_id == pet.id).all()
                    for service in services:
                        if service.pet_id == pet.id:
                            print('')
                            print(service)
                            print(line)
                request = int(input("""
Please Enter:

    1 - Request A New Appointment
    2 - Cancel An Appointment
    3 - View A List Of Our Providers
    4 - Go Back To Main Menu

ENTER: """))
# NEW REQUEST START

                if request == 1:
                    print('')
                    print("Which pet are you scheduling this appointment for?")
                    print('')
                    query_pets(session, owner_id)
                    id = int(input("Enter Pet ID you would like to schedule for: "))

                    name = session.query(Pet.name).filter(Pet.id == id).first()[0]

                    appt_type = int(input(f"""What type of appointment are you scheduling for {name}?
PLEASE ENTER:
1 - Drop-in
2 - Walking
3 - House-sitting

ENTER: """))

                    fees = {"Drop-In": 50, "Walking": 35, "House-Sitting": 70}

                    if appt_type == 1 or appt_type == 2:

                        if appt_type == 1:
                            service = "Drop-In"

                        elif appt_type == 2:
                            service = "Walking"

                        print(f"You selected {service}, which costs ${fees[service]}.00 per session.")

                        date_input = input("""
What date would you like to schedule this service for?
Enter using MM/DD/YYYY format

ENTER: """)

                        print(f"You selected {date_input} for your service date.")

                        time_input = input("""
This service can be scheduled between the hours of 8:00 AM and 5:00 PM.
What time would you like to schedule this service for?
Enter using HH:MM format (do not include 'AM' or 'PM')

ENTER: """) + ":00"

                        print(f"You selected {time_input} as your start time for this service.")

                        formatter = "%m/%d/%Y %H:%M:%S"

                        string_datetime = f"{date_input} {time_input}"

                        formatted_datetime = datetime.strptime(string_datetime, formatter)

                        add_note = input("Please enter any notes for this service request: ")

                        create_new_dropwalk(session=session, pet_id=id, request=service, start_date=formatted_datetime, fee=f"${fees[service]}.00", notes=add_note)

                    elif appt_type == 3:
                        service = "House-Sitting"
                        print(f"You selected {service}, which costs ${fees[service]}.00 per session.")
                        start_date_str = input("""What date would you like this service to start?
Please enter in MM/DD/YYYY format: """)

                        print(f"You've selected to book house-sitting beginning {start_date_str}.")

                        end_date_str = input("""What date would you like this service to end?
Please enter in MM/DD/YYYY format: """)

                        print(f"You've selected to book house-sitting through {end_date_str}.")

                        start_date = datetime.strptime(start_date_str, "%m/%d/%Y").date()
                        end_date = datetime.strptime(end_date_str, "%m/%d/%Y").date()

                        notes = input("Please Enter Any Notes For This Service Request: ")

                        book_house_sitting(session, id, start_date, end_date, notes)

                        next = input("Would you like to schedule another appointment? Y/N: ")
                        print("Routing you back to the main menu...")

                    else:
                        print("Please enter a valid input.")
# NEW REQUEST END


#"CANCEL REQUEST" START:
                elif request == 2:
                    cancel = True
                    while cancel:
                        print('')
                        service_idx = int(input(f"""Please provide the Service ID of the service you wish to cancel.

ENTER: """))
                        service = session.query(Service).filter(Service.id == service_idx).first()
                        print(line_db)
                        print(service)
                        print(line)
                        print('')
                        yes_no = input("Do you wish to cancel this service? (Y/N): ")
                        if yes_no.lower() in YES:
                            session.delete(service)
                            session.commit()
                            print(line_db)
                            print('Your service has been removed successfully!')
                            print('')
                            rem_another = input(f'Would You like to remove another service? (Y/N): ')
                            if rem_another.lower() in YES:
                                continue
                            elif rem_another.lower() in NO:
                                print("Routing you back to appointment menu...")
                                cancel = False
                                appointment_menu = True
                        elif yes_no.lower() in NO:
                            print("Routing you back to appointment menu...")
                            cancel = False
                            appointment_menu = False
                            continue
#"CANCEL REQUEST" END.


#"VIEW PROVIDERS" START:
                elif request == 3:
                    view = True
                    while view:
                        print('')
                        providers = session.query(Provider).all()
                        print('-'*50)
                        print('')
                        print("Available Providers:")
                        print('')
                        for provider in providers:
                            print(f"Provider ID: {provider.id} | Provider Name: {provider.name} | Provider Email: {provider.email}")
                            print('')
                        back = input('Would you like to return to appointment menu? (Y/N): \n')
                        if back.lower() in YES:
                            view = False
#"VIEW PROVIDERS" END

#GO BACK
                elif request == 4:
                    appointment_menu = False

#If Invalid Input
        else:
            print("Please enter a valid input.")

    # print('Thank you for using the Wagging Rights CLI!\n ')
    # Add loop for pet menu.

