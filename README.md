# ThreatAgentSelector

The ThreatAgentSelector app is a web tool that automates the selection of threat agents in order to assess the system security and be aware of the risks.
The tool is fully documanted in the paper:  
[https://pdfs.semanticscholar.org/e53b/0284602dcf355cfb6b8f5aac6a4ac9959f10.pdf]

The application is developed using the following technologies:

## SERVER-SIDE
* Python 3
* Django framework
* sqlite
## CLIENT-SIDE
* HTML, CSS (BOOTSTRAP)

## Configuration guide
### Software Requirements

* Python 3
* Django
* MySQL

**N.B.:** In order to use and start the application you need to:

* Install django using command: bash pip3 install Django

* Run server typing: bash python3 manage.py runserver

App available on: http://127.0.0.1:8000

## Docker available:
### COMMANDS
* sudo docker build -t threatagentselector .
* sudo docker run -dp 8001:8000 threatagentselector

App available on: localhost:8001

