import json
from flask import *


app = Flask(__name__)


interests = ['bball', 'vball', 'soccer', 'dancing', 'running', 'fighting']
tendencies = ['dirty', 'prestine', 'alpha female', 'disorganized']

DEBUGGING = False

class user:
    def __init__(self, n = None, e = None, yr = 1, cn = [], t = [], p = []):
        self.name = n
        self.email = e
        self.year = yr
        self.course_numbers = cn
        self.tendencies = t
        self.preferences = p
        self.approved_user_emails = []
        self.mutual_list = {}

def save_db():
    db = open('db.json', 'w')

    global users_dict
    json.dump(users_dict, db)

def load_db():
    db = open('db.json')

    global users_dict
    users_dict = json.loads(db.readline())

#convert a json string to a user object
def from_json(json_in):
    json_in = json.loads(json_in)
    n_user = user(n = json_in['name'], e = json_in['email'], yr = json_in['year'], cn = json_in['course_numbers'], t = json_in['tendencies'], p = json_in['preferences'])
    return n_user

bob = user()
bob.email = 'BOB@BOB.BOB'.lower()
bob.approved_user_emails.append('amy@amy.amy')

amy = user()
amy.email = 'amy@amy.amy'.lower()
amy.approved_user_emails.append('bob@bob.bob')

e1 = {
  "approved_user_emails": ["me@me.me", "t@t.t"],
  "course_numbers": ["0000", "1111"],
  "email": "test@test.test",
  "name": "test",
  "tendencies": ["math", "party", "pink"],
  "year": 1,
  "preferences": ["wed"],
  "mutual_list": []
}

e2 = {
  "approved_user_emails": ["test@test.test", "t@t.t"],
  "course_numbers": ["2222", "3333"],
  "email": "me@me.me",
  "name": "me",
  "tendencies": ["sci", "sit", "orange"],
  "year": 1,
  "preferences": ["clean"],
  "mutual_list": []
}

e3 = {
  "approved_user_emails": ["test@test.test", 'me@me.me'],
  "course_numbers": ["4444", "5555"],
  "email": "t@t.t",
  "name": "t",
  "tendencies": ["eng", "build", "green"],
  "year": 1,
  "preferences": ["organized"],
  "mutual_list": []
}


#le_db = boto3.resource('dynamodb', region_name = 'us-west-2', endpoint_url="http://localhost:8000")
#users = le_db.Table('Users')

#a dictionary of users with emails as the keys
users_dict = {}

users_dict.update({e1['email']:e1})
users_dict.update({e2['email']:e2})
users_dict.update({e3['email']:e3})

#save_db()
load_db()


@app.route('/')
def greeting():
    return "Howdy!"


@app.route('/api/user/<email>')
#search the database for the user by their email
def get_user(email):
    
    if email in users_dict:
        return jsonify(users_dict[email])

    else:
        return "no user with email \" " + email + "\" was found in the database"



# make a new user object from the given json string
@app.route('/api/user/', methods = ['POST'])
def user_model():
    '''
    #make a user object from given json
    n_user = from_json(request.data)

    #add this user to the list of users
    #users.append(n_user)
    entry = {n_user.email:n_user.__dict__}

    #update the database
    users_dict.update(entry)
    '''

    jsn = json.loads(request.data)
    
    if len(jsn) != 8:
        return "Format is wrong. A user must have 8 feilds. Users not updated."
        
    users_dict.update({jsn['email']:jsn})
    save_db()

    if DEBUGGING:    
        #return the new user as a json string
        #return jsonify(n_user.__dict__)

        #return all users as a json file
        #return jsonify(users_dict)
        return 'Users updated.'


    return 'Users updated.'



# populate and return the mutual matches list of the user with the given email 
@app.route('/api/matches/<email>')
def find_matches(email):
    
    #get the approved list of the user with the given email
    curr_usr = users_dict[email]        
    yes_list = curr_usr['approved_user_emails']

    aprovee = {}
    #for every email in the approved list
    for user_email in yes_list:
        if user_email in users_dict:
            #find the user in the dictionary of users
            approvee = users_dict[user_email]
            
            #if the current users email is in the approvees approved list
            if curr_usr['email'] in approvee['approved_user_emails']:
                if approvee['email'] not in curr_usr['mutual_list']:
                    curr_usr['mutual_list'].append(approvee['email'])
                    approvee['mutual_list'].append(curr_usr['email'])

    save_db()
    return jsonify( {curr_usr['email']: curr_usr['mutual_list']} )

    
@app.route('/api/candidates/<email>')
def nope2():
    return "Nothing here yet.."


@app.route('/api/lists')
def give_lists():    
    return jsonify({'interests':interests, 'tendencies':tendencies})

@app.route('/dick')
def dick():
    return "you're such a dick"


@app.route('/api/user_test/<email>')
def nope0(email):
    #response = users.query(KeyConditionExpression = Key('email').eq(email))
    return email

if __name__ == '__main__':
    if DEBUGGING:
        app.debug = True
        app.run()
        
    if not DEBUGGING:
        app.run(host = '0.0.0.0')
