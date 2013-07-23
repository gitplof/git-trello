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

1. Config

1.1. Save the config to ~/.gitr.json
`````python
gitr config
`````

1.2. Update de config file
`````python
gitr config -p <key:value, key2:value2, ...>
gitr config -p CREATE_LIST_ID:3726948216978264921634982764928176,USER:0
`````

2. Load

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

3. Update

`````python
gitr update -t TITLE -d DESCRIPTION -p PARAMS 

TITLE: card title
DESCRIPTION: card description
PARAMS: estimated,priority,real
`````

4. Commit
`````python
gitr commit -c COMMENT

COMMENT: card comment (required)
`````

5. Test
This argument creates a new branch for integration.

`````python
gitr test -c COMMENT

COMMENT: card comment
`````

6. Push
This argument moves the card to the list made ​​and makes a push to the repository.

`````python
gitr push -c COMMENT

COMMENT: card comment
`````

7. Reload
Move the card to the branch doing.

`````python
gitr reload
`````

8. Members
List all trello members.

`````python
gitr members
`````
