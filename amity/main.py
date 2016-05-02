"""main.py: Contains the application functionality

Usage:
  main.py create_room (<name> <floor> <room_type>)...
  main.py add_person <first_name> <last_name> <employee_type> [--wants_accommodation=ans]
  main.py get_person_identifier <first_name> <last_name>
  main.py reallocate_person <person_identifier> <new_room_name>
  main.py loads_people <text_file>
  main.py print_allocations [-o=file_name]
  main.py print_unallocated [-o=file_name]
  main.py print_room <room_name>
  main.py save_state [--db=sqlite_database]
  main.py load_state <db_file_path>
  main.py (-h | --help)

Options:
  -h --help                    Show this screen.
  --wants_accommodation=<ans>  Specifies if person wants accommodation or not [default: N]
  -o=<file_name>               Specifies a file to print output [default: screen]
  --db=sqlite_database         Specifies a database to persist data [default: app.db]
"""

from docopt import docopt
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker
import base
import pickle
import os.path
import random
import sys

from amity import Amity
from rooms import Room
from persons import Person


# set up Amity class
amity = Amity()

def get_rooms_as_list():
    """Returns a list of rooms in database"""
    if os.path.isfile('rooms.pkl'):
        with open('rooms.pkl', 'rb') as file:
            room_objects = pickle.load(file)
        return room_objects
    else:
        return []

def get_persons_as_list():
    """Returns a list of persons in database"""
    if os.path.isfile('persons.pkl'):
        with open('persons.pkl', 'rb') as file:
            person_objects = pickle.load(file)
        return person_objects
    else:
        return []

def write_rooms(room_objects):
    """Write room from memory to pickle"""
    with open('rooms.pkl', 'wb') as file:
        pickle.dump(room_objects, file)
        print "Successfully updated room information to application"

def write_persons(person_objects):
    """Write room from memory to pickle"""
    with open('persons.pkl', 'wb') as file:
        pickle.dump(person_objects, file)
        print "Successfully updated person information to application!"

def create_room(name, floor, room_type):
    # create room and add to application
    new_room = amity.createRoom(name.lower(), floor, room_type)
    room_objects = []
    # read from room file if it exists
    room_objects = get_rooms_as_list()
    room_objects.append(new_room)
    # write to room file
    write_rooms(room_objects)

def add_person(first_name, last_name, employee_type, wants_accommodation="N"):
    # add the person and automatically allocate a room
    allocated_rooms = []
    person_objects = get_persons_as_list()
    # randomly pick an office space to assign person if there is one in 
    # application
    if room_type_exists("office", amity.officeCapacity):
        allocated_rooms.append(randomly_allocate_person_a_room(first_name, 
            last_name, employee_type, "office"))
    else:
        print "There is no vacant Office space currently in database!!!"
    # randomly pick a living space to assign fellow if he wants it
    # and there is one in the application
    if employee_type == "fellow" and wants_accommodation == "Y":
        if room_type_exists("living space", amity.livingSpaceCapacity):
            allocated_rooms.append(randomly_allocate_person_a_room(first_name, 
                last_name, employee_type, "living space"))
        else:
            print "There is no vacant Living Space to currently in database"
    new_person = amity.addPerson(len(person_objects), first_name.lower(), 
        last_name.lower(), employee_type)
    if allocated_rooms:
        # create person and add rooms to person
        for room in allocated_rooms:
            new_person.room.append(room)
            print "{0} {1} was assigned {2} {3}.".format(first_name, last_name, 
                room.name.capitalize(), room.type)
    person_objects.append(new_person)
    # write to persons.pkl
    write_persons(person_objects)
    
def randomly_allocate_person_a_room(first_name, last_name, employee_type,
    room_type):
    """Randomly allocates a room to a Person and returns assigned room"""
    if room_type == "office":
        capacity = amity.officeCapacity
    else:
        capacity = amity.livingSpaceCapacity
    
    # open the room file for updates
    if not os.path.isfile('rooms.pkl'):
        return ("No rooms have been created. You need to create a room "
                "first before you can add people!!!")
    room_objects = get_rooms_as_list()
    # randomly allocate a vacant room
    random_index = random.randint(0, len(room_objects) - 1)
    searching_for_vacant_room = True
    while searching_for_vacant_room:
        if room_objects[random_index].noOfOccupants < capacity \
            and room_objects[random_index].type == room_type:
            room_objects[random_index].noOfOccupants += 1
            searching_for_vacant_room = False
        else:
            random_index = random.randint(0, len(room_objects) - 1)
    write_rooms(room_objects)
    return room_objects[random_index]
        
def room_type_exists(room_type, room_capacity):
    """Returns true if a room exists, Returns False otherwise"""
    if os.path.isfile('rooms.pkl'):
        room_objects = get_rooms_as_list()
        for room in room_objects:
            if room.type == room_type and room.noOfOccupants < room_capacity:
                return True
    return False

def get_person_identifier(first_name, last_name):
    """Return an identifier used to locate a specific person"""
    person_objects = get_persons_as_list()
    first_name, last_name = first_name.lower(), last_name.lower()
    found_match = False
    for person in person_objects:
        if person.firstName == first_name and person.lastName == last_name:
            print "{0} {1}'s identifier: {2}".format(first_name.upper(), \
                last_name.upper(), person.identifier)
            found_match = True
    if not found_match:
        print "No match was found for {0} {1}.".format(first_name, last_name)

def get_person(person_identifier):
    """Return a tuple of a 
    person object that has the supplied person identifier
    and its position in the list of person objects
    """
    person_objects = get_persons_as_list()
    for counter, person in enumerate(person_objects):
        if person.identifier == person_identifier:
            return (person, counter)
    return (None, None)

def get_room(room_name):
    """
    Return a tuple of a
    room object that has the supllied person identifier
    and its position in the list of person objects
    """
    room_objects = get_rooms_as_list()
    for counter, room in enumerate(room_objects):
        if room.name == room_name:
            return (room, counter)
    return (None, None)

def identifier_is_valid(person_identifier):
    "Checks if the person_identifier parameter passed in is valid"
    person_objects = get_persons_as_list()
    if person_identifier < len(person_objects)  and person_identifier >= 0:
        return True
    else:
        return False

def reallocate_person(person_identifier, room_name):
    """Transfer given person to a different room or perform fresh allocation
    if the person had not been allocated a room. 
    Also perform fresh allocation if person had not been allocated a room of
    that type.
    """
    # check if identifier is valid
    if not identifier_is_valid(person_identifier):
        print "FAILURE!!! You entered an Invalid Identifier."
        return
    # if valid, load room from pickle
    room_objects = get_rooms_as_list()
    # find person on allocation table
    person_to_reallocate, person_index = get_person(person_identifier)
    # get the new room object and check vacancy
    new_room, new_room_index = get_room(room_name)
    if new_room.noOfOccupants >= amity.officeCapacity and \
        new_room.type == "office":
        print "FAILURE!!! The room you selected has no vacancy."
        return
    if new_room.noOfOccupants >= amity.livingSpaceCapacity and \
        new_room.type == "living space":
        print "FAILURE!!! The room you selected has no vacancy."
        return

    reallocation_successful = False
    room_index = None
    for room_index in range(len(person_to_reallocate.room)):
        if person_to_reallocate.room[room_index].type == new_room.type:
            person_to_reallocate.room.pop(room_index)
            person_to_reallocate.room.append(new_room)
            old_room, old_room_index = get_room(person_to_reallocate.
                room[room_index].name)
            room_objects[new_room_index].noOfOccupants += 1
            room_objects[old_room_index].noOfOccupants -= 1
            reallocation_successful = True
            print ("{0} Successfully moved from {1} to {2}".format \
                (person_to_reallocate.firstName, old_room.name, new_room.name))
    
    # check that this is not an attempt to allocate living space to staff
    if person_to_reallocate.type == "staff" and new_room.type == "living space":
        print "FAILURE!!! You cannot allocate 'living space' to staff"
        return
    # fresh allocation if person has not been allocated room of this type 
    # before or not allocated at all
    elif not reallocation_successful or room_index is None:
        person_to_reallocate.room.append(new_room)
        room_objects[new_room_index].noOfOccupants += 1
        print ("{0} Successfully allocated {1} {2}".format \
                (person_to_reallocate.firstName, new_room.name, new_room.type))    
    
    # apply changes to person_objects
    person_objects = get_persons_as_list()
    person_objects[person_index] = person_to_reallocate

    # write to pickle
    write_persons(person_objects)
    write_rooms(room_objects)

            
def loads_people(text_file):
    """Adds people to room from text file specified"""
    with open(text_file, 'rb') as file:
        data = file.read()
    person_list = data.split("\n")
    for entry in person_list:
        person = entry.split()
        if len(person) == 4:
            add_person(person[0].lower(), person[1].lower(), \
                person[2].lower(), person[3])
        elif len(person) == 3:
            add_person(person[0].lower(), person[1].lower(), \
                person[2].lower(), "N")
        else:
            person_string = " ".join(person)
            print "{0} is in an invalid format and cannot be added" \
                .format(person_string)

def get_allocations_as_dict():
    """Get allocation table from pkl file and return as dictionary"""
    person_objects = get_persons_as_list()
    allocation_dict = {}
    for person in person_objects:
        for room in person.room:
            key = room.name
            allocation_dict[key] = allocation_dict.get(key, []) + \
                [person.firstName + " " + \
                person.lastName]
    return allocation_dict

def print_allocations(output):
    """Prints all allocations to screen by default.
    Prints to a text file if that is provided.
    """
    allocation_dict = get_allocations_as_dict()
    if not allocation_dict:
        print "There are no allocations in database"
        return
    # prepare the output message
    allocation_list = []
    for key in allocation_dict:
        allocation_list.append(key.upper() + "\n")
        allocation_list.append("-------------------------------------------\n")
        for person in allocation_dict[key]:
            allocation_list.append(person.upper() + ", ")
        allocation_list[-1] = allocation_list[-1][:-2]
        allocation_list.append("\n\n")
    if output == "screen":
        print "".join(allocation_list)
    elif output[-4:] == ".txt":
        with open(output, 'w') as file:
           file.write("".join(allocation_list))
    else:
        print ("You must enter a file name with a .txt extension to save"
                " to file")

def find_all_unallocated_persons():
    """
    Searches the database for all persons that have not been assigned
    a room.
    """
    allocation_dict = get_allocations_as_dict()
    person_objects = get_persons_as_list()
    unallocated_persons = []
    for person in person_objects:
        found_match = False
        for key, value in allocation_dict.iteritems():
            if "{0} {1}".format(person.firstName, person.lastName) in value:
                found_match = True
        if not found_match:
            unallocated_persons.append("{0} {1}".format(person.firstName. \
                upper(), person.lastName.upper()))
    return unallocated_persons

def print_unallocated(output):
    """Prints all Persons that have not been allocated a room"""
    unallocated_persons = find_all_unallocated_persons()
    output_message = ["LIST OF ALL UNALLOCATED PEOPLE\n\n"]
    for person in unallocated_persons:
        output_message.append(person)
        output_message.append("\n")
    if output == "screen":
        print "".join(output_message)
    elif output[-4:] == ".txt":
        with open(output, 'w') as file:
            file.write("".join(output_message))
    else:
        print ("You must enter a file name with a .txt extension to save"
                " to file")

def print_room(room_name):
    """Prints names of occupants in a room"""
    allocation_dict = get_allocations_as_dict()
    print "NAMES OF PEOPLE IN {0}\n".format(room_name.upper())
    try:
        for person_name in allocation_dict[room_name]:
            print "{0}".format(person_name).upper()
        print "\n"
    except KeyError:
        print "There is no one in this Room!!!\n"

def save_state(db_name):
    """Moves files from pickle to the database"""
    # set up database
    engine = create_engine("sqlite:///{0}".format(db_name))
    base.Base.metadata.create_all(engine, checkfirst=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # delete db file if it already exists
    if os.path.isfile(db_name):
        os.remove(db_name)
    
    try:
        # read and copy objects from rooms.pkl into db
        person_objects = get_persons_as_list()
        session.add_all(person_objects)
        session.commit()
        print "Successfully Stored application data in database"
        
        # delete pickle files
        os.remove("rooms.pkl")
        os.remove("persons.pkl")
        
    except:
        print "Error: {0}".format(sys.exc_info()[1])
        session.rollback()

def load_state(db_name):
    """Loads data from database into application"""
    # set up database
    engine = create_engine("sqlite:///{0}".format(db_name))
    base.Base.metadata.create_all(engine, checkfirst=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    # load persons
    person_objects = session.query(Person).all()
    if person_objects:
        write_persons(person_objects)
        print "Loaded all records for people from database into application"
    else:
        print "Failure!!! No person has been added to database."         
    
    # load rooms 
    room_objects = session.query(Room).all()
    session.close()
    if room_objects:
        room_dict = {}
        for room in room_objects:
            key = room.name
            room_dict[key] = room_dict.get(key, []) + [room]
        room_objects = []
        for key in room_dict:
            room_dict[key][0].noOfOccupants = len(room_dict[key])
            room_objects.append(room_dict[key][0])
        write_rooms(room_objects)
        print "Loaded all rooms from database into application"
    else:
        print "Failure!!! No Room has been added to database"

if __name__ == '__main__':
    arguments = docopt(__doc__)
    print arguments

    # if an argument called hello was passed, execute the hello logic.
    if arguments['create_room']:
        for i in range(len(arguments['<name>'])):
            create_room(arguments['<name>'][i], int(arguments['<floor>'][i]), arguments['<room_type>'][i])
    elif arguments['add_person']:
        add_person(arguments['<first_name>'], arguments['<last_name>'], arguments['<employee_type>'].lower(), arguments['--wants_accommodation'])
    elif arguments['get_person_identifier']:
        get_person_identifier(arguments['<first_name>'], arguments['<last_name>'])
    elif arguments['reallocate_person']:
        reallocate_person(int(arguments['<person_identifier>']), arguments['<new_room_name>'])
    elif arguments['loads_people']:
        loads_people(arguments['<text_file>'])
    elif arguments['print_allocations']:
        print_allocations(arguments['-o'])
    elif arguments['print_unallocated']:
        print_unallocated(arguments['-o'])
    elif arguments['print_room']:
        print_room(arguments['<room_name>'])
    elif arguments['save_state']:
        save_state(arguments['--db'])
    elif arguments['load_state']:
        load_state(arguments['<db_file_path>'])