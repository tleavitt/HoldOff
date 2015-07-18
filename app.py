from flask import Flask, request, redirect
import twilio.twiml

app = Flask(__name__)

SECRET_KEY = 'mysecretkey'
MY_TREE = { "Q" : "What is your name?", "1" : { "1": "foo", 0 : {"#" : "some val"}, "2": "bar", 1 : {"#" : "another val"} } }

conversations = {}

@app.route("/", methods=['GET', 'POST'])
def receiveText():
  from_number = request.values.get('From', None)
  from_body = request.values.get('Body', None)

  # Allow users to restart the survey/tree at any time
  if from_body == "restart":
    if from_number in conversations:
      conversations.pop(from_number)

  # If there is a current ongoing conversation
  if from_number in conversations:
    currentNode = conversations[from_number][0]
    currentAnswers = conversations[from_number[1]
    if from_body in currentNode:
      currentNode = from_body
      if currentNode

  else:
    currentNode = MY_TREE
    currentAnswers = {}
    # send first question and store them in ongoing conversations
    message = MY_TREE["Q"]
    conversations[from_number] = [currentNode, currentAnswers]
    resp = twilio.twiml.Response()
    resp.message(message)
    return str(resp)

  




if __name__ == "__main__":
    app.run()
