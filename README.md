## Gitr usage ##

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

0. Config

0.1. Save the config to ~/.gitr.json
`````python
gitr config
`````

0.2. Update de config file
`````python
gitr config -p <key:value, key2:value2, ...>
gitr config -p CREATE_LIST_ID:3726948216978264921634982764928176,USER:0
`````

1. Load

1.1. Load with id

`````python
gitr load -i ID -p PARAMS

ID: card id (required)
PARAMS: estimated,priority,real (estimated is required)
`````

1.2. Load and create card

`````python
gitr load -t TITLE -d DESCRIPTION -u USERS -p PARAMS 

TITLE: card title (required)
DESCRIPTION: card description
USERS: users assigned to the card
PARAMS: estimated,priority,real (estimated is required)

2. Update
`````python
gitr update -t TITLE -d DESCRIPTION -p PARAMS 

TITLE: card title
DESCRIPTION: card description
PARAMS: estimated,priority,real
`````

3. Commit
`````python
gitr commit -c COMMENT

COMMENT: card comment (required)
`````

4. Test
This argument creates a new branch for integration.

`````python
gitr test -c COMMENT

COMMENT: card comment
`````

5. Push
This argument moves the card to the list made ​​and makes a push to the repository.

`````python
gitr push -c COMMENT

COMMENT: card comment
`````

6. Reload
Move the card to the branch doing.

`````python
gitr reload
`````

7. Members
List all trello members.

`````python
gitr members
`````



