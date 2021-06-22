
from modules.pets import *



database = Db(dbtype='sqlite', dbname='pets.db')

'''
a = Animal()
a.name = "kočka"
database.session.add(a)
database.session.commit()
create_pet = Pet()
create_pet.name = "Poppy"
create_pet.animal = database.session.query(Animal).get("kočka")
create_pet.owner = "me"
database.session.add(create_pet)
database.session.commit()

'''
print(database.session.query(Animal).all())