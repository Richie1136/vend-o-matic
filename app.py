from flask import Flask, jsonify, request

app = Flask(__name__)

# Each inventory position represents a beverage, identified by IDs 0,1, and 2.
inventory = [5,5,5]
# Track the number of quarters inserted for the current transaction.
inserted_coins = 0

@app.route("/inventory/<int:id>", methods=['PUT'])
def purchase_beverage(id):
    global inserted_coins
    # Validate the ID before accessing the inventory list.
    if id < 0 or id >= len(inventory):
        return jsonify({"Error": "Item not found"}), 404
    # Return 404 if the selected beverage is out of stock.
    if inventory[id] == 0:
        return "", 404, {"X-Coins": str(inserted_coins)}
    if inserted_coins < 2:
        return "", 403, {"X-Coins": str(inserted_coins)}
    # Dispense one beverage, regardless of how many quarters were inserted.
    inventory[id] -= 1
    # A beverage costs two quarters, return any extra quarters as change in the X-Coins header.
    coins_to_return = inserted_coins - 2
    # Reset the coin balance because the transaction is complete.
    inserted_coins = 0
    return jsonify({"quantity": 1}), 200, {
        "X-Coins": str(coins_to_return), 
        "X-Inventory-Remaining": str(inventory[id])
        }
    
@app.route("/inventory/<int:id>", methods=['GET'])
def get_inventory_item(id):
    # Prevent access to an inventory position that doesn't exist.
    if id < 0 or id >= len(inventory):
        return jsonify({"Error": "Item not found"}), 404
    else:
        return jsonify(inventory[id]), 200

@app.route("/inventory", methods=['GET'])
def get_inventory():
    return jsonify(inventory), 200

@app.route("/", methods=['DELETE'])
def return_coins():
    global inserted_coins
    # Save the refund amount before clearing the machine's coin balance.
    coins_to_return = inserted_coins
    inserted_coins = 0
    # A 204 response has no body, report the refund in the header.
    return "", 204, {"X-Coins": str(coins_to_return)}

@app.route("/", methods=['PUT'])
def insert_coins():
    global inserted_coins
    # Read the coin value from the incoming JSON request body.
    data = request.get_json()
    if not isinstance(data, dict):
        return jsonify({"Error": "Request body must be a JSON object"}), 400
    coin = data.get("coin")
    # The machine accepts only one quarter per request.
    if type(coin) is int and coin == 1:
        inserted_coins += 1
    else:
        return jsonify({"Error": "Sorry input is invalid"}), 400
    # Header values are text, so convert the count to a string.
    return "", 204, {"X-Coins": str(inserted_coins)}