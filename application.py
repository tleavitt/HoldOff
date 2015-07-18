from flask import Flask, request, redirect, url_for, render_template
import twilio.twiml
import configParser as cfp

application = Flask(__name__)

@application.route("/")
def hello():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
SECRET_KEY = 'mysecretkey'
MY_TREE = cfp.parseConfigFile("conf")
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


    if from_body in currentNode:
      currentAnswers.append( (currentNode['Q'], currentNode[from_body]['A']) )
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
