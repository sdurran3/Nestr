import json
from flask import *
app = Flask(__name__)

interests = ['bball', 'vball', 'soccer']
tendencies = ['dirty', 'prestine', 'alpha female']

class user:
    def __init__(self, gname = None, gemail = None, gyear = 1, gcourse_numbers = [], gtendencies = []):
        self.name = gname
        self.email = gemail
        self.year = gyear
        self.course_numbers = gcourse_numbers
        self.tendencies = gtendencies
        self.approved_user_emails = []
        self.preferences = []
        self.mutual_list = []


#convert a json string to a user object
def from_json(json_in):
    json_in = json.loads(json_in)
    n_user = user(gname = json_in['name'], gemail = json_in['email'], gyear = json_in['year'], gcourse_numbers = json_in['course_numbers'], gtendencies = json_in['tendencies'])
    return n_user

bob = user()
bob.approved_user_emails.append('amy@amy.amy')

amy = user()
amy.approved_user_emails.append('bob@bob.bob')

    
#le_db = boto3.resource('dynamodb', region_name = 'us-west-2', endpoint_url="http://localhost:8000")
#users = le_db.Table('Users')
users = {}

@app.route('/')
def greeting():
    return "Oh hai guize!"


# make a new user object from the given json string
@app.route('/api/user/', methods = ['POST'])
def user_model():
    #make a user object from given json
    n_user = from_json(request.data)

    #set the email field to the email
    n_user.email = email.lower()

    #add this user to the list of users
    #users.append(n_user)
    entry = {n_user.email:n_user.__dict__}
    #make the new user as a json string
    #return jsonify(n_user.__dict__)

    users.update(entry)
    
    return jsonify(users)


# populate and return the mutual matches list of the user with the given email 
@app.route('/api/matches/<email>')
def find_matches(email):

    bob = user()
    bob.email = 'BOB@BOB.BOB'.lower()
    bob.approved_user_emails.append('amy@amy.amy')

    amy = user()
    amy.email = 'amy@amy.amy'.lower()
    amy.approved_user_emails.append('bob@bob.bob')
    
    #get the approved list of the user with the given email
    le_user = bob
        
    yes_list = le_user.approved_user_emails

    #for every email in the approved list
    for un_user in yes_list:
        #find the user
        un_user = amy
        
        #if the current users email is in the approvees approved list
        if le_user.email in un_user.approved_user_emails:
            le_user.mutual_list.append(un_user.email)
            un_user.mutual_list.append(le_user.email)

    
    return jsonify({le_user.email:le_user.mutual_list})

    
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
    app.debug = True
    app.run()
