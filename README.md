# Coffee Shop Full Stack

## Full Stack Nano - IAM Final Project

The aim of this project is to show the various of drinks in coffe shop. Beside that, to add many features, depending on who is the users. hence,this project focus to make project more secure by authorization and authentication. thereby,The information is showing to public is not the same information showing to barista and to manager. And this property what we called Authorization. Also the user need to Login and identaction . And this property what we called Authentication
Udacity has decided to open a new digitally enabled cafe for students to order drinks, socialize, and study hard. But they need help setting up their menu experience.

in this application to public users can see names and and graphics. while baristas also can view the recipe information. the managers users beside view information of drinks,can edit drinks lists by create new drink ,delete an existent drink or modification some information about selected drink.

## Tasks

in this project we have three parts to work on it :
1.  Third party auth0 system (setup auth0)                                
2.  Backend
3.  Frontend


### setup auth0
after creating new account in auth0 , there are set of steps as following:
1. creating new application
2. selecting type of application which here is Single Page Application
3. configuring this applications by determine allowed callback URLs , logout URLs and so on .
4. creating new API for this application and determine name ,identifier,signing algorithm for token
5. configuring this API by enable options in RBAC setting for permission and role.  
6. creating permission which is
    - `get:drinks-detail`
    - `post:drinks`
    - `patch:drinks`
    - `delete:drinks`
7. creating the roles here is barista and manager .
8. assigning user and permissions for each role
    - Barista
        - can `get:drinks-detail`
    - Manager
        - can perform all actions

### Backend


After setup and run virtual environment, navigate to the /backend directory and Install all dependencies which found in requirement.txt by run:

```bash
pip install -r requirements.txt
```

####  Running the server

 within the `./src` directory runing:

```bash
export FLASK_APP=api.py;
```

To run the server, execute:

```bash
flask run --reload
```
#### Configure Auth.py

 updating the code in the `/backend/src/auth/auth.py` . which means the value of 
 `AUTH0_DOMAIN`, `ALGORITHMS` ,`API_AUDIENCE` should be updated

#### Test endpoints
the test our enpoints in this project will be done with [Postman](https://getpostman.com) as following :
1. Importing the postman collection `./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json`
2. Updateing barista and manager separately by Right-clicking the collection folder for barista and manager, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs)
4. Running the collection and correcting the errors.
5. Saving and exporting the collection 

#### Implement The Server

to implement the server we have two important files `./src/auth/auth.py` and 2. `./src/api.py`
1. `./src/auth/auth.py` we have four methods 
 - `get_token_auth_header()`: 
 **required**:
 in this method is to get the header from the request and it will raise an AuthError if no header.in addition,try to split bearer and the token with raise an AuthError if the header is malformed.
 **return**:
  the token part of the header if there is no AuthError
 - `check_permissions(permission, payload)`
     **inputs**
      * permission: string permission 
      * payload: decoded jwt payload
     **required**:
      it will raise an AuthError if permissions are not included in the payload and if the requested permission string is not in the payload permissions array
    **return** 
      true if there is no AuthError

 - `verify_decode_jwt(token)`
     **inputs**
      * token: a json web token 
     **required**:
      it will raise an AuthError if Auth0 token are not with key id ,token_expired,invalid  audience and issuer,invalid token , or key.
     **return** 
      return the decoded payload if there is no AuthError
 - `@requires_auth(permission)`
     *inputs*
      * permission: string permission
     **required**:
        it will  get  `token` from  `get_token_auth_header` method,decode the `jwt` from `verify_decode_jwt` method, and validate claims and check the requested permission from `check_permissions` method 
    **return** 
      return the decorator which passes the decoded payload to the decorated method
2. `./src/api.py` in this file implementing set of endpoints

### Frontend
#### Installing Dependencies

1. Installing Node and NPM

This project based on Nodejs and Node Package Manager (NPM). so, we need to install Node from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

2. Installing Ionic Cli

The Ionic Command Line Interface is required to serve and build the frontend. Instructions for installing the CLI  is in the [Ionic Framework Docs](https://ionicframework.com/docs/installation/cli).

3. Installing project dependencies

our project uses NPM to manage software dependencies.So, we have to open the terminal and run:
```bash
npm install
```
#### Configure Enviornment Variables

- we should open `./src/environments/environments.ts` and ensure each variable reflects the system we using for the backend.

#### Running our Frontend in Dev Mode

To run the development server, cd into the `frontend` directory and run:

```bash
ionic serve
```
