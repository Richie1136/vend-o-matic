# Vend-O-Matic - Marigold Assessment

A beverage vending machine API built with Python and Flask

The machine offers three beverages, with five of each initially available.
Each beverage costs two US quarters, and quarters are inserted one at a time.

Customers can check inventory, purchase one beverage per transaction, and request their inserted coins back.
Successful purchases return any extra quarters as change.

## Requirements

- Python 3
- pip

## Setup and Run

### Clone the repository and navigate into the project folder

```bash
git clone https://github.com/Richie1136/vend-o-matic.git
cd vend-o-matic
 ```

From the project folder, create a virtual environment:

```bash
python3 -m venv .venv
```
Activate it:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Start the server:

```bash
python -m flask --app app run --port 5001
```

The API is available at http://127.0.0.1:5001.

## API Usage

Run these commands in a second terminal while the server is running.

### Insert one quarter

```bash
curl -i -X PUT http://127.0.0.1:5001/ \  
  -H "Content-Type: application/json" \
  -d '{"coin": 1}'
  ```

  Expected response when starting with no inserted coins:

  - Status: 204 NO CONTENT
  - Header: X-Coins: 1
  - No response body.

  ### Return coins

  ```bash
  curl -i -X DELETE http://127.0.0.1:5001/
  ```

  Expected response after inserting one quarter:

  - Status: 204 NO CONTENT
  - Header: X-Coins: 1
  - No response body

  ### Get Beverage Inventory

  ```bash
  curl -i -X GET http://127.0.0.1:5001/inventory
  ```

  Expected response assuming no beverages have been purchased since starting the server:

  - Status: 200 OK
  - Body: [5,5,5]

  ### Get Inventory for one beverage.

  ```bash
  curl -i -X GET http://127.0.0.1:5001/inventory/0
  ```

  Expected result which assumes that none of beverage 0 has been purchased since the server started:

  - Status: 200 OK
  - Body: 5

  ### Purchase a beverage

  - Starting with no inserted coins, run the "insert one quarter" command twice, then run the 
  purchase command below.

  ```bash
  curl -i -X PUT http://127.0.0.1:5001/inventory/0
  ```

  Expected result when entering 2 quarters, in order to purchase a beverage

  - Status: 200 OK
  - Header: X-Coins: 0, X-Inventory-Remaining: 4
  - body: {"quantity": 1}

  ## Assumptions

  - Beverage IDs are 0,1,2.
  - Failed purchases leave inserted coins available for another attempt or a refund using DELETE /.
  - Inventory and coin balance are stored in memory. Restarting the server resets the inventory to [5,5,5]
  and the coin balance to 0.