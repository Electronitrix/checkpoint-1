"""main.py

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
  main.py hello <first> <last>
  greeter.py goodbye <name>
  greeter.py (-h | --help)

Options:
  -h --help                   Show this screen.
  --wants_accomodation=<ans>  Specifies if person wants accommodation or not [default: N]
  -o=<file_name>              Specifies a file to print output [default: screen]
  --db=sqlite_database        Specifies a database to persist data [default: app.db]
"""

from docopt import docopt
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker
import base
import pickle
import os.path
import random

from amity import Amity, RoomAllocation
from rooms import Room
from persons import Person

amity = Amity()
room_allocation = RoomAllocation()

def get_rooms_as_list():
    """Returns a list of rooms in database"""
    if os.path.isfile('rooms.pkl'):
        with open('rooms.pkl', 'rb') as file:
            room_objects = pickle.load(file)
        return room_objects
    else:
        return False

def get_persons_as_list():
    """Returns a list of persons in database"""
    if os.path.isfile('persons.pkl'):
        with open('persons.pkl', 'rb') as file:
            person_objects = pickle.load(file)
        return person_objects
    else:
        return False

def get_allocations_as_list():
    """Returns a list of allocations of persons to rooms"""
    if os.path.isfile('allocations.pkl'):
        with open('allocations.pkl', 'rb') as file:
            allocation_objects = pickle.load(file)
        return allocation_objects
    else:
        return "There are no existing allocations in Amity!!!"

def create_room(name, floor, room_type):
    # create room and add to application
    new_room = amity.createRoom(name, floor, room_type)
    room_objects = []
    # read from room file if it exists
    if os.path.isfile('rooms.pkl'):
        with open('rooms.pkl','rb') as file:
            room_objects = pickle.load(file)
    print "helo {0}".format(room_objects)
    room_objects.append(new_room)
    print room_objects
    # write to room file
    with open('rooms.pkl', 'wb') as file:
        pickle.dump(room_objects, file)
        print "Room Created"

def add_person(first_name, last_name, employee_type, wants_accommodation):
    # add the person and automatically allocate a room
    person_objects = []
    if os.path.isfile('persons.pkl'):
        with open('persons.pkl', 'rb') as file:
            person_objects = pickle.load(file)
    print person_objects
    new_person = amity.addPerson(len(person_objects), first_name, last_name, 
        employee_type)
    person_objects.append(new_person)
    print person_objects
    #write to persons.pkl
    with open('persons.pkl', 'wb') as file:
        pickle.dump(person_objects, file)
        print "Person Created!"
    # randomly assign an office space to person if there is one in application
    if room_type_exists("office"):
        randomly_allocate_person_a_room(new_person, employee_type, 
            wants_accommodation, "office")
    else:
        print "There is no Office space currently in database!!!"
    # randomly assign living space to fellow if he wants it
    if room_type_exists("living space"):
        if employee_type == "fellow" and wants_accommodation == "Y":
            randomly_allocate_person_a_room(new_person, employee_type, 
                wants_accommodation, "living space")
    

def randomly_allocate_person_a_room(person, employee_type, 
    wants_accommodation, room_type):
    room_objects = []
    allocation_objects = []
    if room_type == "office":
        capacity = amity.officeCapacity
    else:
        capacity = amity.livingSpaceCapacity
    # open the room file for updates
    if not os.path.isfile('rooms.pkl'):
        return ("No rooms have been created. You need to create a room "
                "first before you can add people!!!")
    with open('rooms.pkl', 'rb') as file:
        room_objects = pickle.load(file)
    
    # randomly allocate a vacant room
    random_index = random.randint(0, len(room_objects) - 1)
    searching_for_vacant_room = True
    while searching_for_vacant_room:
        if room_objects[random_index].noOfOccupants < capacity \
            and room_objects[random_index].type \
            == room_type:
            searching_for_vacant_room = False
        else:
            random_index = random.randint(0, len(room_objects) - 1)
    new_allocation = RoomAllocation(room=room_objects[random_index], 
        person=person)
    if os.path.isfile('allocations.pkl'):
        with open('allocations.pkl', 'rb') as file:
            allocation_objects = pickle.load(file)
    allocation_objects.append(new_allocation)
    room_objects[random_index].noOfOccupants += 1
    
    # write to rooms.pkl
    with open('rooms.pkl', 'wb') as file:
        pickle.dump(room_objects, file)
        print "Successfully updated number of {0} occupants!".format(room_type)
    
    # write to allocations.pkl
    with open('allocations.pkl', 'wb') as file:
        pickle.dump(allocation_objects, file)
        print "{0} has been allocated the {1} {2}.". \
            format(person.firstName, room_objects[random_index].name, 
                room_type)
    
def room_type_exists(room_type):
    room_objects = []
    if not os.path.isfile('rooms.pkl'):
        return ("No rooms have been created. You need to create a room "
                "first before you can add people!!!")
    with open('rooms.pkl', 'rb') as file:
        room_objects = pickle.load(file)

    for room in room_objects:
        if room.type == room_type:
            return True
    return False

def room_exists(room_name):
    """Checks if supplied room exists"""
    room_objects = []
    if not os.path.isfile('rooms.pkl'):
        return ("No rooms have been created. You need to create a room "
                "first before you can add reallocate someone!!!")
    with open('rooms.pkl', 'rb') as file:
        room_objects = pickle.load(file)

    for room in room_objects:
        if room.name == room_name:
            return True
    return False

def get_person_identifier(first_name, last_name):
    """Return an identifier used to locate a specific person"""
    person_objects = []
    if os.path.isfile('persons.pkl'):
        with open('persons.pkl', 'rb') as file:
            person_objects = pickle.load(file)
    for person in person_objects:
        if person.first_name == first_name and person.last_name == last_name:
            return person.identifier

def get_person(person_identifier):
    """Return person object with supplied person identifier"""
    person_objects = []
    if os.path.isfile('persons.pkl'):
        with open('persons.pkl', 'rb') as file:
            person_objects = pickle.load(file)
    for person in person_objects:
        if person.identifier == person_identifier:
            return person

def get_room(room_name):
    """Return person object and index with supplied person identifier"""
    room_objects = []
    if os.path.isfile('rooms.pkl'):
        with open('rooms.pkl', 'rb') as file:
            room_objects = pickle.load(file)
    for counter, room in enumerate(room_objects):
        if room.name == room_name:
            return (room, counter)

def identifier_is_valid(person_identifier):
    person_objects = []
    if os.path.isfile('persons.pkl'):
        with open('persons.pkl', 'rb') as file:
            person_objects = pickle.load(file)
    if person_identifier < len(person_objects)  or person_identifier >= 0:
        return True
    else:
        return False

def reallocate_person(person_identifier, room_name):
    """Transfer given person to a different room"""
    room_objects = []
    allocation_objects = []
    # check if identifier is valid
    if not identifier_is_valid(person_identifier):
        return "You entered an invalid Identifier!!!"
    # if valid, create room object
    else:
    # load room from pickle
        # read from room file if it exists
        if os.path.isfile('rooms.pkl'):
            with open('rooms.pkl','rb') as file:
                room_objects = pickle.load(file)

    # find person on allocation table
    if os.path.isfile('allocations.pkl'):
        with open('allocations.pkl', 'rb') as file:
            allocation_objects = pickle.load(file)
    else:
        return "There are no existing allocations in Amity!!!"
    person = get_person(person_identifier)
    new_room, new_room_index = get_room(room_name)
    old_room, old_room_index = get_room(room_name)
    new_allocation = RoomAllocation(person=person, room=new_room)
    searching_for_old_allocation = True
    counter = 0
    while searching_for_old_allocation:
        if allocation.person.identifier == person_identifier:
            allocation_objects[counter] = new_allocation
            searching_for_old_allocation = False
        counter += 1
    room_objects[new_room_index].noOfOccupants -= 1
    room_objects[old_room_index].noOfOccupants += 1

def loads_people(text_file):
    """Adds people to room from text file specified"""
    with open(text_file, 'rb') as file:
        data = file.read()
    person_list = data.split("\n")
    import pdb
    pdb.set_trace()
    for entry in person_list:
        person = entry.split()
        if len(person) == 4:
            add_person(person[0], person[1], person[2].lower(), person[3])
        elif len(person) == 3:
            add_person(person[0], person[1], person[2].lower(), "N")
        else:
            person_string = " ".join(person)
            print "{0} is in an invalid format and cannot be added" \
                .format(person_string)

def get_allocations_as_dict():
    """Get allocation table from pkl file and return as dictionary"""
    if os.path.isfile('allocations.pkl'):
        with open('allocations.pkl', 'rb') as file:
            allocation_objects = pickle.load(file)
    else:
        return "There are no existing allocations in Amity!!!"
    allocation_dict = {}
    for allocation in allocation_objects:
        key = allocation.room.name
        allocation_dict[key] = allocation_dict.get(key, []) + \
            [allocation.person.firstName + " " + allocation.person.lastName]
    return allocation_dict

def print_allocations(output):
    """Prints all allocations to screen by default.
    Prints to a text file if that is provided.
    """
    allocation_dict = get_allocations_as_dict()
    # prepare the output message
    allocation_list = []
    for key in allocation_dict:
        allocation_list.append(key.upper() + "\n")
        allocation_list.append("-------------------------------------------\n")
        for person in allocation_dict[key]:
            allocation_list.append(person.upper() + ", ")
        allocation_list[-1] = allocation_list[-1][:-2]
        allocation_list.append("\n\n")
    print output
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
            unallocated_persons.append("{0} {1}".format(person.firstName, 
                person.lastName))
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
    allocation_objects = get_allocations_as_list()
    print "NAMES OF PEOPLE IN {0}".format(room_name.upper())
    found_match = False
    for allocation in allocation_objects:
        if allocation.room.name == room_name:
            found_match = True
            print "{0} {1}".format(allocation.person.firstName, 
                allocation.person.lastName)
    if not found_match:
        print "There is no one in this Room!!!"

def save_state(db_name):
    """Moves files from pickle to the database"""
    #set up database
    engine = create_engine("sqlite:///{0}".format(db_name))
    base.Base.metadata.create_all(engine, checkfirst=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # read and copy objects from rooms.pkl into db
        room_objects = get_rooms_as_list()
        #import pdb
        #pdb.set_trace()
        for room in room_objects:
            session.add(room)
            session.commit()

        # read and copy objects from persons.pkl into db
        person_objects = get_persons_as_list()
        for person in person_objects:
            session.add(person)
            session.commit()

        # read and copy objects from allocations.pkl into db
        allocation_objects = get_allocations_as_list()
        for allocation in allocation_objects:
            session.add(allocation)
            session.commit()

        print "Successfully Stored application data in database"
    except:
        session.rollback()

def load_state(db_name):
    """Loads data from database into application"""
    #set up database
    engine = create_engine("sqlite:///{0}".format(db_name))
    import pdb
    pdb.set_trace()
    base.Base.metadata.create_all(engine, checkfirst=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    # load rooms 
    room_objects = session.query(Room).all()
    # write to rooms.pkl file
    with open('rooms.pkl', 'wb') as file:
        pickle.dump(room_objects, file)
        print "Loaded all rooms from database into application"

    # load persons
    person_objects = session.query(Person).all()
    # write to persons.pkl file
    with open('persons.pkl', 'wb') as file:
        pickle.dump(person_objects, file)
        print "Loaded all records for people from database into application"

    # load allocation table
    allocation_objects = session.query(RoomAllocation).all()
    # write to allocations.pkl file
    with open('allocations.pkl', 'wb') as file:
        pickle.dump(allocation_objects, file)
        print  "Loaded all allocations from database into application"

    print "Successfully copied all data from database into application"

def hello(name,last):
    print('Hello, {0}'.format(name))
    print('last, {0}'.format(last))



def goodbye(name):
    print('Goodbye, {0}'.format(name))

if __name__ == '__main__':
    arguments = docopt(__doc__)
    print arguments

    # if an argument called hello was passed, execute the hello logic.
    if arguments['hello']:
        hello(arguments['<name>'],arguments['<last>'])
    elif arguments['goodbye']:
        goodbye(arguments['<name>']) 
    elif arguments['create_room']:
        for i in range(len(arguments['<name>'])):
            create_room(arguments['<name>'][i], int(arguments['<floor>'][i]), arguments['<room_type>'][i])
    elif arguments['add_person']:
        add_person(arguments['<first_name>'], arguments['<last_name>'], arguments['<employee_type>'].lower(), arguments['--wants_accommodation'])
    elif arguments['get_person_identifier']:
        get_person_identifier(arguments['<first_name>'], arguments['<last_name>'])
    elif arguments['reallocate_person']:
        reallocate_person(arguments['<person_identifier>'], arguments['<new_room_name>'])
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