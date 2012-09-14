This is extremely unstable right now. Most methods don't do any error checking and assume the user will supply the correct data. This will be unusuable to most people for the time being -- the prototype is still in its infancy stage. 

---

Description

This is a genetic algorithm that composes melodies and allows the user to play an integral part in the composition process without requiring any previous music theory knowledge. This is only possible because of how I designed the fitness function -- the user actually acts as as composer and is allowed to make a specific number of changes to the current individual. This is a unique interactive fitness function that adds a new level of user engagement and reduces user boredom.

---

RESTful API

The REST server, like its name, is a simple RESTful server that allows a user to query the database for musical and meta information surrouding a specific artist, song, or collection. Additionally, it allows a user to upload, parse, and/or store new MIDI files.

---

GAServer:
python index.py [port]

RestServer:
python index.py [port]

MongoDB:
mongod --journal --port [port] --dbpath /path/data/db/
