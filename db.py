####### CREATE DB IF NOT EXIST
import os, json
if not os.path.exists('db.json'):
    db = {'token': 'None'}
    js = json.dumps(db, indent=2)
    with open('db.json', 'w') as outfile:
        outfile.write(js)
    print('Input token in "None" (db.json)')
    exit()

############WORK WITH DBs##########
def read_db():
    with open('db.json', 'r') as openfile:
        db = json.load(openfile)
        return db

def write_db(db):
    js = json.dumps(db, indent=2)
    with open('db.json', 'w') as outfile:
        outfile.write(js)
