# Assignment 1
# /Users/brimurray/Desktop/Homework1/data/data.csv
# System Argument: data.csv data
import pathlib
import sys
import re
import pickle

# Create Person class to save employee information
class Person:
    def __init__(self, last, first, mi, id, phone):
        self.id = id  # key
        self.last = last
        self.first = first
        self.mi = mi
        self.phone = phone

    def display(self):
        print("Employee ID: ", self.id)
        print(self.first, self.mi, self.last)
        print(self.phone)


# Validate IDs
def valid(ID, seen_og):
    seen = seen_og

    # Check for duplicate IDs based on what has already been seen
    # If unique ID is given, add ID to list of seen IDs
    # If ID has been seen before input is invalid
    if ID not in seen:
        seen.add(ID)
        return True
    else:
        print("Duplicate IDs not allowed")
        return False


# Format text to align with guidelines
def process_text(text_in, employees):
    seen = set() # set of seen IDs

    # Split list of employee information
    # Before: text_in = [xzy, abc]
    # After: text_in = [[x,y,z], [a,b,c]]
    for i in range(len(text_in)):
        text_in[i] = text_in[i].split(",")

    # create Person objects from employee info
    for object in text_in:
        # capitalize first, middle, last name
        object[0] = object[0].capitalize()
        object[1] = object[1].capitalize()
        object[2] = object[2].capitalize()

        # Validate middle initial
        if not object[2]:
            object[2] = "X"

        # Validate ID
        id_format = "[A-Za-z]{2}[0-9]{4}"
        while not(re.match(id_format, object[3]) and valid(object[3], seen)):
            print("Invalid ID: ", object[3])
            print("ID is 2 letters followed by 4 digits")
            object[3] = input("Enter valid ID: ")

        # Validate phone number
        phone_format = "\d{3}-\d{3}-\d{4}"
        while not(re.match(phone_format, object[4])):
            print("Invalid phone#: ", object[4])
            print("Correct format is 123-456-7890")
            object[4] = input("Enter valid phone#: ")

        # save as object in dictionary based on employee id
        employees[object[3]] = (Person(object[0], object[1], object[2], object[3], object[4]))


if __name__ == '__main__':
    employees = {} # dictionary to save employee info

    filename = input("Enter your filename as a system argument: ")
    if len(sys.argv) < 2:
        print(sys.argv)
        print('Please enter a valid filename as a system argument')
        quit()

    rel_path = sys.argv[1]
    with open(pathlib.Path.cwd().joinpath(rel_path), 'r') as f:
        text_in = f.readlines()[1:] # skip header
        process_text(text_in, employees)

    # Pickle file
    pickle.dump(employees, open('employees.pickle', 'wb'))
    # Read pickle
    employees_in = pickle.load(open('employees.pickle', 'rb'))
    # Display results
    print("\n\n- - - EMPLOYEE LIST - - -")
    for employee in employees.keys():
        employees[employee].display()
        print()
