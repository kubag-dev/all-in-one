# README contents
1. Description
2. Architectural concept
3. Run the app

#  1. Description

## State of the application at the last quarter of 2025

It's only a backbone for the future application, current concept is jack of all trades off-line/local application,
starting with a single todo module (that in fact is a starting mock and most likely will be depricated as software revolves)
it's a starting point from which an app with few (not yet planned) modules will be developed that will have some functionalities working between them.

## Plans for the app development

For now there is no long term plan, first part is todo app, that ought to be perfected (or just polished) before moving to more grounded and planned functionalities.
This module is only backend part, mayhaps in the future there will be frontend, although it is quite so unlikely. Plans for now are the export endpoints for communication and give usable GUI in form of HTML templates (probably based on Jinja).

<br/>

# 2. Architectural concept

## Backend
Written in python, based on FastApi, connected with database (probably SQL, for now it's sqlite), some kind of ORM required, GUI in Jinja templates, for now running on gunicorns but in the future it's planned to be available as docker container (maybe separate module).

Current tools:
- python
- fastapi
- sqlite
- sqlmodel
- jinja
- uvicorn

## Folder structure
### Simple modules
```
-root
-- core         / apps internal communication
-- home         / landing page
-- todo         / module
--- models      / database models
--- repository  / interaction with database
--- routes      / endpoints
--- schemas     / send/received data serialization
```
Each directory also can have helpers that some times might be just placed in root directory of a module.

### Advanced modules with custom logic
<font color="ORANGE">**WIP**</font> (no current need)

## Code/Architectural conventions
The project goes with my own interpretation of **clean code** and **clean architecture** guidelines by Uncle Bob, nothing is written, it's only my interpretation. If there will be decision on them there will be a separate file containg rules. For code formatting **Black** is used.

- **fetch** is reserved for managing the database and data around the app, **get** is reserved for HTTP methods
# 3. Run the app
It's only a development build, requiring environment with <font color="ORANGE">**python3.12**</font> with installed packages from `requirements.txt`

Try from a project root folder

`fastapi dev main.py`
