from flask import Flask, request, redirect, url_for, render_template
import twilio.twiml
from app import QueueCtrl


application = Flask(__name__)
ctrl = QueueCtrl()
ctrl.createChannel('VISA')
ctrl.createChannel('Sales')
ctrl.putNext('VISA',2.5,[('What is the meal','burger'),("Name","Tom")])
ctrl.putNext('VISA',3.5,[('What is the meal','Sandwich'),("Name","James")])
ctrl.putNext('VISA',1.5,[('What is the meal','burger'),("Name","Rebecca")])
ctrl.putNext('Sales',1.4,[('What is the meal','food'),("Name","Will")])


@application.route("/")
def home():
    channels = ['VISA','Sales']
    return render_template('index.html',channels=channels)

def formatPhone(phone):
  return '('+phone[0:3]+')'+phone[3:6]+'-'+phone[6:]

@application.route("/<pageid>")
def show(pageid):
    phone=formatPhone('1029302910')
    pid=pageid 
    QAlist = []
    more = True
    #print ctrl.empty(pid)
    if not ctrl.empty(pid):
      QAlist = ctrl.getNextFrom(pid)
    else:
      more = False
    #print QAlist
    return render_template('page.html', pid=pid, QAlist=QAlist, more=more, phone=phone)

SECRET_KEY = 'mysecretkey'
MY_TREE ={'1': {'1': {'1': {'#': 'Customer Service', 'A': 'Customer Service', 'N': 0}, '2': {'#': 'Food', 'A': 'Food', 'N': 0}, '3': {'#': 'More Food', 'A': 'Eat', 'N': 0}, 'A': 'Customer Service', 'N': 3, 'Q': 'What items does it have to do with? Press 1 for Kitchen, 2 for Food, 3 for Eat'}, '2': {'#': 'General', 'A': 'helpdesk', 'N': 0}, '3': {'#': 'General', 'A': 'just want to talk to someone', 'N': 0}, 'A': '%', 'N': 3, 'Q': 'What are you looking for? Press 1 for customer service, press 2 for helpdesk, press 3 if you just want to talk to someone'}, 'A': '%', 'N': 1, 'Q': 'Wt is your name?'}

conversations = {}

END_MESSAGE = 'Thanks for answering our questions. We will be calling you shortly!'

@application.route("/twilio", methods=['GET', 'POST'])
def receiveText():
  print conversations
  from_number = request.values.get('From', None)
  from_body = request.values.get('Body', None)

  # Allow users to restart the survey/tree at any time
  if from_body == "restart":
    if from_number in conversations:
      conversations.pop(from_number)

  if from_body == "cancel":
    if from_number in conversations:
      conversations.pop(from_number)
      return

  # If there is a current ongoing conversation
  if from_number in conversations:
    currentNode = conversations[from_number][0]
    currentAnswers = conversations[from_number][1]

    # if %, means this question is open ended Q. Go to the next regardless of body
    if currentNode['A'] == "%": 
      currentAnswers.append( tuple(currentNode['Q'], from_body) )
      currentNode = currentNode['1']
      if '#' in currentNode:
        #TODO push currentAnswers to Q
        conversations.pop(from_number)
        message = END_MESSAGE 
      else:
        conversations[from_number] = [currentNode, currentAnswers]
        message = currentNode['Q']
    # if received body is answer option, move to corresponding node in tree
    elif from_body in currentNode:
      currentAnswers.append( tuple(currentNode['Q'], currentNode[from_body]['A']) )
      currentNode = currentNode[from_body]
      if "#" in currentNode:
        # TODO: implement push to queue currentNode["#"]
        conversations.pop(from_number)
        message = END_MESSAGE
      else:
        conversations[from_number] = [currentNode, currentAnswers]
        message = currentNode['Q']
    # unrecognized response, ask the same question again
    else:
      message = currentNode['Q']
    resp = twilio.twiml.Response()
    resp.sms(message)
    return str(resp)
  # unrecognized phone number. Start new conversation at top of tree and ask first question
  else:
    currentNode = MY_TREE
    currentAnswers = []
    # send first question and store them in ongoing conversations
    message = MY_TREE["Q"]
    conversations[from_number] = [currentNode, currentAnswers]
    resp = twilio.twiml.Response()
    resp.sms(message)
    return str(resp)

if __name__ == "__main__":
    application.run()
