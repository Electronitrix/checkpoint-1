[![Build Status](https://travis-ci.org/andela-cdike/checkpoint-1.svg?branch=master)](https://travis-ci.org/andela-cdike/checkpoint-1)
[![Coverage Status](https://coveralls.io/repos/github/Electronitrix/checkpoint-1/badge.svg?branch=master)](https://coveralls.io/github/Electronitrix/checkpoint-1?branch=master)

# checkpoint-1 - Room Allocation Software

# INTRODUCTION
This is a room allocation software for Andela's Amity campus. It is a command line application that randomly allocates a recently added staff to an office and a recently added fellow to an office and living space if the fellow states that he wants accomodation. The app information is persisted in an sqlite database and must be loaded first before previously saved allocation information can be accessed.


# FEATURES
The features of this app are accessed via the command line. The command line is implemented with docopt while the app infomation is stored in pickle until user gives the command to persist the data. Features of this app include:

1. Create room: You could creater multiple rooms at a time.
2. Add a person: staff or fellow.
3. Get a person's identifier.
4. Load people information from a text file and automatically add them to the application.
5. Reallocate a person.
6. Allocate a person using the same reallocate command.
7. Print all allocations either to screen or to a text file.
8. Print names of all those who do not have an allocation to screen or a text file.
9. Print names of all occupants of a specified room.
10. Persist the information on the app to a database. If no database is specified, a default - "app.db" is used.
11. Load information from the database into the application.


# COMMANDS

Usage:
*  main.py create_room (<name> <floor> <room_type>)...
*  main.py add_person <first_name> <last_name> <employee_type> [--wants_accommodation=ans]
*  main.py get_person_identifier <first_name> <last_name>
*  main.py reallocate_person <person_identifier> <new_room_name>
*  main.py loads_people <text_file>
*  main.py print_allocations [-o=file_name]
*  main.py print_unallocated [-o=file_name]
*  main.py print_room <room_name>
*  main.py save_state [--db=sqlite_database]
*  main.py load_state <db_file_path>
*  main.py (-h | --help)

Options:
*  -h --help                    Show this screen.
*  --wants_accommodation=<ans>  Specifies if person wants accommodation or not [default: N]
*  -o=<file_name>               Specifies a file to print output [default: screen]
*  --db=sqlite_database         Specifies a database to persist data [default: app.db]
