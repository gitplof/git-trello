## Introduction ##
This script aims to make easy the work with trello and git. 

**NOTE:** It`s designed for the way we work.

### Our Workflow ###
Our philosophy is based in create one branch for each feature. Then we open a integration branch from QA branch.

### Named branched ###
The feature branches use the followeens rules

Feature: F-#trello-id (e.g F-#32)

Integration: I-#trello-id (e.g I-#32)


## Dependencies ##

Python 2.7

oauth2

gitpython


## Get starter ##
The first task is download it. You can clone the repositorie


`````python
git clone git@github.com:gitplof/git-trello.git
`````
Now, we advise set up a shortcut or alias. For unix systems you can do anything like this:


`````python
alias gitr='python $HOME/git-trello/gitr.py'
`````
Now you need to provide you keys from trello to script. [Generate key](https://trello.com/1/appKey/generate)
. You must keep you api key and you secret key.
Them you must follow [this address](https://trello.com/1/authorize?key=substitutewithyourapplicationkey&name=My+Application&expiration=never&response_type=toke://trello.com/1/authorize?key=substitutewithyourapplicationkey&name=My+Application&expiration=never&response_type=token) You must substitute API_KEY with your api_key that you get on the previos step 


Now you are ready for use this tool


## Documentation ##

### Gitr usage ###

`````python
Usage: gitr (load|rebuild|commit|push|test|config|update) [options] args

Options:
  -h, --help
  -i ID, --id=ID
  -u USER, --user=USER
  -c COMMENT, --comment=COMMENT
  -g GITPATH, --gitpath=GITPATH
  -p PARAMS, --params=PARAMS
  -t TITLE, --title=TITLE
  -d DESCRIPTION, --description=DESCRIPTION
`````

### 1. Config ###

1.1. Save the config to ~/.gitr.json
`````python
gitr config
`````

1.2. Update to config file
`````python
gitr config -p <key:value, key2:value2, ...>
gitr config -p CREATE_LIST_ID:3726948216978264921634982764928176,USER:0
`````

### 2. Load ###

2.1. Load with id

`````python
gitr load -i ID -p PARAMS

ID: card id (required)
PARAMS: estimated,priority,real (estimated is required)
`````

2.2. Load and create card

`````python
gitr load -t TITLE -d DESCRIPTION -u USERS -p PARAMS 

TITLE: card title (required)
DESCRIPTION: card description
USERS: users assigned to the card
PARAMS: estimated,priority,real (estimated is required)
`````

### 3. Update ###

`````python
gitr update -t TITLE -d DESCRIPTION -p PARAMS 

TITLE: card title
DESCRIPTION: card description
PARAMS: estimated,priority,real
`````

### 4. Commit ###

`````python
gitr commit -c COMMENT

COMMENT: card comment (required)
`````

### 5. Test ###
This argument creates a new branch for integration.

`````python
gitr test -c COMMENT

COMMENT: card comment
`````

### 6. Push ###
This argument moves the card to the list made ​​and makes a push to the repository.

`````python
gitr push -c COMMENT

COMMENT: card comment
`````

### 7. Rebuild ###
Move the card to the branch doing.

`````python
gitr rebuild
`````

### 8. Members ###

List all trello members.

`````python
gitr members
`````
