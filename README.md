# HoldOff
LinkedIn Hackathon 2015
HoldOff is customer service made easy.

Overview
--------
For customers, HoldOff makes the customer service call less painful. Instead of waiting through the automated phone messages one by one and entering the required options and being put on hold, customers simply answer a few survey questions by text and continue whatever they are doing. The business will put the customer on queue, and call them when they are ready.

For businesses, HoldOff makes the customer service process extremely easy to setup, install, and implement. All businesses have to do is enter their customer service categorization/information questions into a configuration text document and HoldOff will handle the rest. HoldOff will traverse the question decision tree, and send and read the relevant text messages to fill out the questions. Then, HoldOff will enter the customer details into separate departmental queues (specified by the business), and customer service reps simply have to visit the link and go through the queue by pressing the next button. The only additional setup that is required is creating a Twilio account and entering the flask website URL.

### HoldOff is
-flexible
-lightweight
-convenient
-open-source
-extremely configurable
-accessible for small businesses all phone users


Demo Quickstart
---------------
Configure conf file with questions and departments to your liking. Further configuration details below.

On Amazon Server or your local network:

```bash
git clone https://github.com/tleavitt/HoldOff.git
cd HoldOff
. venv/ourhackenv/bin/activate
pip install -r requirements.txt
python application.py
```

Now, find the server external URL + '/twilio' and put it on the Twilio phone number account.
e.g. http://hold-off-dev.elasticbeanstalk.com/twilio
Visit site url and you're off!

Configuration File Details
--------------------------
The config file defines a tree structure for the queries texted to customers. Customers respond to the queries 
by texting numbers back to Twilio. Once the customer reaches the bottom of the tree, they are added to the appropraite queue and notified of the wait time.

TO DO: describe Q, A, N, # 

```bash
Q Hello! How can I help you today? Press 1 to speak with our helpdesk and 2 to speak with our representatives
A %
N 2
  # Helpdesk
  A Helpdesk
  N 0
  # Representative
  A reps
  N 0
```
