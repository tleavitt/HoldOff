from flask import Flask, request, redirect, url_for, render_template
import twilio.twiml

application = Flask(__name__)

@application.route("/")
def hello():
    return render_template('index.html')

if __name__ == "__main__":
    application.run()
SECRET_KEY = 'mysecretkey'
MY_TREE ={'Q': 'What is your name?', '1': {'1': {'Q': 'What are you looking for?', '1': {'1': 'Customer service', '1': {'Q': 'What items does it have to do with?', '1': {'1': {'#': 'Customer Service'}, '2': {'#': 'Food'}, '3': {'#': 'More Food'}, '4': {'#': 'General'}, '5': {'#': 'General'}, '1': 'Kitchen', '3': 'I just want to talk to someone', '2': 'Helpdesk'}}}}, '$': 'some stuff'}}

conversations = {}

END_MESSAGE = 'Thanks for answering our questions. We will be calling you shortly!'

@application.route("/twilio", methods=['GET', 'POST'])
def receiveText():
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
    if '%' in currentNode:
      currentAnswers.append( tuple(currentNode['Q'], from_body) )
      currentNode = currentNode['%']
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

