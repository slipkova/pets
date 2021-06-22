import traceback

from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Global Variables

SQLITE = 'sqlite'
MYSQL = 'mysql'

Base = declarative_base()

class Animal(Base):
    __tablename__ = 'animal'

    name = Column(String(length=50), primary_key=True)
    pet = relationship('Pet', back_populates='animal')


class Pet(Base):
    __tablename__ = 'pet'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=50))
    animal_name = Column(String(50), ForeignKey('animal.name'))
    animal = relationship("Animal", back_populates="pet")
    owner = Column(String(length=200))


class Db:
    DB_ENGINE = {
        SQLITE: 'sqlite:///{DB}',
        MYSQL: 'mysql+mysqlconnector://{USERNAME}:{PASSWORD}@localhost/{DB}'
    }

    def __init__(self, dbtype='sqlite', username='', password='', dbname='persons'):
        dbtype = dbtype.lower()

        if dbtype in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[dbtype].format(DB=dbname, USERNAME=username, PASSWORD=password)
            self.engine = create_engine(engine_url, echo=False)
        else:
            print('DBType is not found in DB_ENGINE')

        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def read_all(self, order = Pet.name):
        try:
            result = self.session.query(Pet).order_by(order).all()
            return result
        except:
            return False

    def read_by_id(self, id):
        try:
            result = self.session.query(Pet).get(id)
            return result
        except:
            return False

    def read_by_Animal(self, animal='CZE'):
        try:
            result = self.session.query(Pet).join(Animal).filter(Animal.short_name.like(f'%{animal}%')).order_by(Pet.name).all()
            return result
        except:
            return False

    def read_animals(self):
        try:
            result = self.session.query(Animal).all()
            return result
        except:
            traceback.print_exc()
            return False

    def create(self, pet):
        try:
            self.session.add(pet)
            self.session.commit()
            return True
        except:
            return False

    def update(self):
        try:
            self.session.commit()
            return True
        except:
            return False

    def delete(self, id):
        try:
            Pet = self.read_by_id(id)
            self.session.delete(Pet)
            self.session.commit()
            return True
        except:
            return False

    def create_animal(self, animal):
        try:
            self.session.add(animal)
            self.session.commit()
            return True
        except:
            return False


