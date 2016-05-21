"""main.py: Contains the application functionality

Usage:
  main.py create_room (<name> <floor> <room_type>)...
  main.py add_person <first_name> <last_name> <employee_type> [--wants_accommodation=ans]
  main.py print_person_identifier <first_name> <last_name>
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

import pickle
import os.path
import sys
import textwrap

from docopt import docopt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import base
from amity.amity import Amity
from persons.fellow import Fellow
from persons.person import Person
from persons.staff import Staff
from rooms.living_space import LivingSpace
from rooms.office import Office
from rooms.room import Room

# set up Amity class
amity = Amity()

# set up file names
rooms_file = "rooms.pkl"
people_file = "people.pkl"


def get_list_of_objects(file_name):
    """Returns a list of rooms in pickle file"""
    if os.path.isfile(file_name):
        with open(file_name, 'rb') as file:
            object_list = pickle.load(file)
        return object_list
    else:
        return []


def write_to_pickle(object_list, file_name):
    """Write room from memory to pickle"""
    with open(file_name, 'wb') as file:
        pickle.dump(object_list, file)


def create_room(name, floor, room_type):
    """ Create room and add to application"""
    room_type = room_type.lower()
    if amity.is_room_type_valid(room_type):
        rooms = get_list_of_objects(rooms_file)
        new_room = amity.create_room(len(rooms), name.lower(),
                                     floor, room_type)
        add_room_to_application(rooms, new_room)
        print "You have successfully created room - {0}".format(name.upper())
    else:
        print "Failure!!! You entered an Invalid room type."


def add_room_to_application(rooms, new_room):
    """Add room to list of rooms"""
    rooms.append(new_room)
    write_to_pickle(rooms, rooms_file)


def add_person(first_name, last_name, employee_type, wants_accommodation="N"):
    """Add the person and automatically allocate a room"""
    try:
        rooms = get_list_of_objects(rooms_file)
        people = get_list_of_objects(people_file)
        new_person, errors = amity.add_person(len(people),
                                              first_name.lower(),
                                              last_name.lower(),
                                              employee_type,
                                              wants_accommodation,
                                              rooms)
        for error in errors:
            print "{0} Please create a new room of this type.".format(error)
        if new_person:
            print "\n".join(
                ["{0} was allocated {1}.".format(str(new_person).
                 upper(), str(room).capitalize())
                 for room in new_person.rooms]
            )
            people.append(new_person)
            write_to_pickle(people, people_file)
            write_to_pickle(rooms, rooms_file)

    except ValueError as error:
        print error[0]


def print_person_id(first_name, last_name):
    """Print an identifier used to locate a specific person"""
    people = get_list_of_objects(people_file)
    first_name, last_name = first_name.lower(), last_name.lower()
    try:
        id = amity.get_person_id(first_name, last_name,
                                 people)
        print "{0} {1}'s identifier: {2}".format(
            first_name.upper(), last_name.upper(), id)

    except ValueError as error:
        print error[0]


def reallocate_person(person_id, room_name):
    """
    Transfer given person to a different room or perform fresh allocation
    if the person had not been allocated a room.
    Also perform fresh allocation if person had not been allocated a room of
    this type.
    """
    people = get_list_of_objects(people_file)
    rooms = get_list_of_objects(rooms_file)
    try:
        person = amity.reallocate_person(
            person_id, room_name.lower(), people, rooms)
        if person:
            people[person_id] = person
            write_to_pickle(people, people_file)
            write_to_pickle(rooms, rooms_file)
            print("Successfully allocated {0} the {1}.".
                  format(person, person.rooms[-1]))
    except ValueError as error:
        print error[0]
    except RuntimeError as error:
        print error[0]


def loads_people(text_file):
    """Adds people to room from text file specified"""
    with open(text_file, 'rb') as file:
        data = file.read()
    people = data.split("\n")
    for each in people:
        person = each.split()
        # import pdb; pdb.set_trace()
        if len(person) == 4:
            add_person(person[0].lower(), person[1].lower(),
                       person[2].lower(), person[3])
        elif len(person) == 3:
            add_person(person[0].lower(), person[1].lower(),
                       person[2].lower())
        else:
            person_string = " ".join(person)
            print "{0} is in an invalid format and cannot be added" \
                .format(person_string)


def print_allocations(output):
    """Prints all allocations to screen by default.
    Prints to a text file if that is provided.
    """
    people = get_list_of_objects(people_file)
    rooms = get_list_of_objects(rooms_file)
    allocation_dict = amity.get_allocations_as_dict(people, rooms)
    if not allocation_dict:
        print ("There are no allocations in memory. You can either enter "
               "new data or load data from database")
        return

    allocation_list = prepare_allocations_output(allocation_dict)
    if output == "screen":
        print "".join(allocation_list)
    elif output[-4:] == ".txt":
        write_to_txt("".join(allocation_list), output)
    else:
        print ("You must enter a file name with a .txt extension to save"
               " to file")


def prepare_allocations_output(allocations):
    """Prepare the allocations to be displayed to user
    Args:
        allocations -- a dictionary containing room name as key and person
                       name as value
    Returns:
        output -- a list of allocations
    """
    output = []
    line_width = 51
    for key in allocations:
        temp = []
        temp.append(key.upper() + "\n")
        temp.append("-" * line_width)
        temp.append("\n")
        for person in allocations[key]:
            temp.append(person.upper() + ", ")
        temp[-1] = temp[-1][:-2]
        room_info = textwrap.fill("".join(temp), line_width)
        output.append(room_info)
        output.append("\n\n")
    return output


def write_to_txt(allocations, output):
    """write a string to a text file"""
    with open(output, 'w') as file:
        file.write("".join(allocations))


def print_unallocated(output):
    """Prints all Persons that have not been allocated a room"""
    people = get_list_of_objects(people_file)
    unallocated_persons = amity.get_unallocated_people(people)
    output_message = ["LIST OF ALL UNALLOCATED PEOPLE\n\n"]
    for person in unallocated_persons:
        output_message.append(person)
        output_message.append("\n")
    if output == "screen":
        print "".join(output_message)
    elif output[-4:] == ".txt":
        write_to_txt(output_message, output)
    else:
        print ("You must enter a file name with a .txt extension to save"
               " to file")


def print_room(room_name):
    """Prints names of occupants in a room"""
    people = get_list_of_objects(people_file)
    allocation_dict = amity.get_allocations_as_dict(people)
    print "NAMES OF PEOPLE IN {0}\n".format(room_name.upper())
    try:
        for person_name in allocation_dict[room_name]:
            print "{0}".format(person_name).upper()
        print "\n"
    except KeyError:
        print "There is no one in this Room!!!\n"


def save_state(db_name):
    """Moves files from pickle to the database"""
    # delete db file if it already exists
    if os.path.isfile(db_name):
        os.remove(db_name)
    try:
        session = setup_database(db_name)
        people = get_list_of_objects(people_file)
        rooms = get_list_of_objects(rooms_file)
        session.add_all(rooms)
        session.add_all(people)
        session.commit()
        print "Successfully Stored application data in database"

        # delete pickle files
        os.remove(rooms_file)
        os.remove(people_file)
    except:
        print "Error: {0}".format(sys.exc_info()[1])
        session.rollback()
    finally:
        session.close()


def setup_database(db_name):
    """set up database"""
    engine = create_engine("sqlite:///{0}".format(db_name))
    base.Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


def load_state(db_name):
    """Loads data from database into application"""
    session = setup_database(db_name)
    try:
        rooms = load_rooms_from_db(session)
        load_people_from_db(session, rooms)
    except:
        print "Error: {0}".format(sys.exc_info()[1])
        session.rollback()
    finally:
        session.close()


def load_rooms_from_db(session):
    """load rooms from database to memory"""
    number_of_rooms = session.query(Room).group_by(Room.mem_id).count()
    rooms = session.query(Room).filter(Room.id <= number_of_rooms).all()
    rooms = recreate_room(rooms)
    if rooms:
        write_to_pickle(rooms, rooms_file)
        print "Loaded all rooms from database into application"
    else:
        print "There was no record for Office or Living space in database"
    return rooms


def load_people_from_db(session, rooms):
    """load people from database to memory"""
    people = session.query(Person).all()
    people = recreate_person(people, rooms)
    if people:
        write_to_pickle(people, people_file)
        print "Loaded all records for people from database into application"
    else:
        print "There was no record for Fellow or Staff in database."


def recreate_person(people, rooms):
    """Recreates Person object for each person record in the list supplied
    This is done because sqlalchemy does not save state the second time
    around without this step for some reason I don't yet know about
    """
    processed_people = []
    for person in people:
        if person.type == "fellow":
            processed_people.append(Fellow(
                                    mem_id=person.mem_id,
                                    first_name=person.first_name,
                                    last_name=person.last_name,
                                    ))
        else:
            processed_people.append(Staff(
                                    mem_id=person.mem_id,
                                    first_name=person.first_name,
                                    last_name=person.last_name,
                                    ))
        repopulate_rooms(person, processed_people, rooms)
    return processed_people


def repopulate_rooms(person, people, rooms):
    """
    Do a reallocation of rooms to person
    """
    for room in person.rooms:
        amity.reallocate_person(person.mem_id, room.name, people, rooms)


def recreate_room(rooms):
    """Recreates Person object for each person record in the list supplied
    This is done because sqlalchemy does not save state the second time
    around without this step for some reason I don't yet know about
    """
    processed_rooms = []
    for room in rooms:
        if room.type == "office":
            processed_rooms.append(Office(
                                   mem_id=room.mem_id,
                                   name=room.name,
                                   floor=room.floor,
                                   no_of_occupants=0,
                                   capacity=room.capacity,
                                   ))
        else:
            processed_rooms.append(LivingSpace(
                                   mem_id=room.mem_id,
                                   name=room.name,
                                   floor=room.floor,
                                   no_of_occupants=0,
                                   capacity=room.capacity,
                                   ))
    return processed_rooms

if __name__ == '__main__':
    arguments = docopt(__doc__)

    # if an argument called hello was passed, execute the hello logic.
    if arguments['create_room']:
        for i, (room, floor, type) in enumerate(
            zip(arguments['<name>'], arguments['<floor>'],
                arguments['<room_type>'])):
            create_room(room, int(floor), type)
    elif arguments['add_person']:
        add_person(arguments['<first_name>'], arguments['<last_name>'],
                   arguments['<employee_type>'].lower(),
                   arguments['--wants_accommodation']
                   )
    elif arguments['print_person_identifier']:
        print_person_id(arguments['<first_name>'], arguments['<last_name>'])
    elif arguments['reallocate_person']:
        reallocate_person(int(arguments['<person_identifier>']),
                          arguments['<new_room_name>'])
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
