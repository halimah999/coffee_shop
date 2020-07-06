import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

# db_drop_and_create_all()

# ROUTES


@app.route('/drinks', methods=['GET'])
def get_drinks():
    ''' handling GET requests for all available drinks'''
    # get  all available drinks
    drinks = Drink.query.all()
    # abort if there is no retrived drinks
    if len(drinks) == 0:
        abort(404)
    short_drinks = [drink.short() for drink in drinks]
    # return short drinks by this endpoint to view
    return json.dumps({
        'drinks': short_drinks,
        'success': True
    })


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_detail_drinks(jwt):
    ''' handling GET requests for all available drinks'''
    # get  all available drinks
    drinks = Drink.query.all()
    # abort if there is no retrived drinks
    if len(drinks) == 0:
        abort(404)
    long_drinks = [drink.long() for drink in drinks]
    # return long drinks by this endpoint to view
    return json.dumps({
        'drinks': long_drinks,
        'success': True
    })


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_drink(jwt):
    # get the drink information from request
    body = request.get_json()
    title = body.get('title')
    recipe = body.get('recipe')
    # create new drink
    drink = Drink(title=title, recipe=json.dumps(recipe))

    try:
        # insert the drink to the database
        drink.insert()
        return jsonify({
            "success": True,
            "drinks": drink.long()
        })
    except BaseException:
        abort(422)


@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(jwt, id):
    # get the selected drink by id
    drink = Drink.query.filter(Drink.id == id).one_or_none()
    if drink:
        # get request body
        body = request.get_json()
        # update title, if it is in the body
        if "title" in body:
            drink.title = body.get('title')
        # update recipe, if it is in the body
        if "recipe" in body:
            drink.recipe = json.dumps(body.get('recipe'))
    # abort if id not found
    else:
        abort(404)
    # make update in the database
    try:
        drink.update()
        return jsonify({"success": True, "drinks": [drink.long()]})
    except BaseException:
        abort(422)


@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(jwt, id):
    try:
        # get the selected drink by id
        drink = Drink.query.filter(Drink.id == id).one_or_none()
        if drink:
            # remove drink of database
            drink.delete()
            return jsonify({"success": True, "delete": id})
        else:
            # abort becuase id is not found
            abort(404)
    except BaseException:
        abort(422)


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Not found"
    }), 404


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400

'''implement error handler for AuthError'''
@app.errorhandler(AuthError)
def error_handler(exception):
    respond = jsonify(exception.error)
    respond.status_code = exception.status_code
    return respond
