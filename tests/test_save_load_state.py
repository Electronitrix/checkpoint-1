import os
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .context import main, persons, rooms

Base = declarative_base()


class RoomAllocationSaveLoadStateTestSuite(unittest.TestCase):
    """Tests for both save and load state of the amity room allocator"""

    def setUp(self):
        self.rooms_file = "rooms.pkl"
        self.people_file = "people.pkl"
        self.db_name = "test.db"
        engine = create_engine("sqlite:///{0}".format(self.db_name))
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def tearDown(self):
        if os.path.isfile(self.db_name):
            os.remove(self.db_name)

    def test_save_state(self):
        main.create_room("bellows", 0, "office")
        main.add_person("erika", "dike", "fellow", "Y")
        main.save_state(self.db_name)
        # query DB
        person = self.session.query(persons.Person).first()
        room = self.session.query(rooms.Room).first()
        self.assertListEqual(
            [
                ["erika", "dike", "fellow"],
                ["bellows", 0, "office"]
            ],
            [
                [person.first_name, person.last_name, person.type],
                [room.name, room.floor, room.type]
            ],
            msg=("save_state does not save appropriately!!!")
        )

    def test_load_state(self):
        main.create_room("bellows", 0, "office")
        main.add_person("erika", "dike", "fellow", "Y")
        main.save_state(self.db_name)
        main.load_state(self.db_name)
        room = main.get_list_of_objects(self.rooms_file)[-1]
        person = main.get_list_of_objects(self.people_file)[-1]
        self.assertListEqual(
            [
                ["erika", "dike", "fellow"],
                ["bellows", 0, "office"]
            ],
            [
                [person.first_name, person.last_name, person.type],
                [room.name, room.floor, room.type]
            ],
            msg=("load_state does not load appropriately!!!")
        )