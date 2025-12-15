from flask import Flask, request, jsonify
from src.accounts_registry import AccountsRegistry
from src.personal_account import PersonalAccount

app = Flask(__name__)
registry = AccountsRegistry()


@app.route("/api/accounts", methods=['POST'])
def create_account():
    """Create a new personal account"""
    data = request.get_json()
    print(f"Create account request: {data}")
    
    if not data or "name" not in data or "surname" not in data or "pesel" not in data:
        return jsonify({"error": "Missing required fields"}), 400
    
    account = PersonalAccount(data["name"], data["surname"], data["pesel"])
    success, message = registry.add_account(account)
    
    if not success:
        return jsonify({"error": message}), 409
    
    return jsonify({"message": "Account created"}), 201


@app.route("/api/accounts", methods=['GET'])
def get_all_accounts():
    """Get all accounts"""
    print("Get all accounts request received")
    accounts = registry.get_all_accounts()
    accounts_data = [
        {
            "name": acc.first_name, 
            "surname": acc.last_name, 
            "pesel": acc.pesel, 
            "balance": acc.balance
        } 
        for acc in accounts
    ]
    return jsonify(accounts_data), 200


@app.route("/api/accounts/count", methods=['GET'])
def get_account_count():
    """Get total number of accounts"""
    print("Get account count request received")
    count = registry.count_accounts()
    return jsonify({"count": count}), 200


@app.route("/api/accounts/<pesel>", methods=['GET'])
def get_account_by_pesel(pesel):
    """Get account by PESEL"""
    print(f"Get account by PESEL request: {pesel}")
    account = registry.find_by_pesel(pesel)
    
    if account is None:
        return jsonify({"error": "Account not found"}), 404
    
    account_data = {
        "name": account.first_name,
        "surname": account.last_name,
        "pesel": account.pesel,
        "balance": account.balance
    }
    return jsonify(account_data), 200


@app.route("/api/accounts/<pesel>", methods=['PATCH'])
def update_account(pesel):
    """Update account (only name and/or surname)"""
    print(f"Update account request: {pesel}")
    account = registry.find_by_pesel(pesel)
    
    if account is None:
        return jsonify({"error": "Account not found"}), 404
    
    data = request.get_json()
    
    if "name" in data:
        account.first_name = data["name"]
    if "surname" in data:
        account.last_name = data["surname"]
    
    return jsonify({"message": "Account updated"}), 200


@app.route("/api/accounts/<pesel>", methods=['DELETE'])
def delete_account(pesel):
    """Delete account by PESEL"""
    print(f"Delete account request: {pesel}")
    success = registry.delete_account(pesel)
    
    if not success:
        return jsonify({"error": "Account not found"}), 404
    
    return jsonify({"message": "Account deleted"}), 200


@app.route("/api/accounts/<pesel>/transfer", methods=['POST'])
def transfer(pesel):
    """Transfer money to/from account"""
    print(f"Transfer request for PESEL: {pesel}")
    
    account = registry.find_by_pesel(pesel)
    if account is None:
        return jsonify({"error": "Account not found"}), 404
    
    data = request.get_json()
    
    if not data or "amount" not in data or "type" not in data:
        return jsonify({"error": "Missing required fields"}), 400
    
    amount = data["amount"]
    transfer_type = data["type"]
    
    if transfer_type == "incoming":
        account.incoming_transfer(amount)
        return jsonify({"message": "Zlecenie przyjęto do realizacji"}), 200
    
    elif transfer_type == "outgoing":
        success = account.outgoing_transfer(amount)
        if not success:
            return jsonify({"error": "Insufficient funds"}), 422
        return jsonify({"message": "Zlecenie przyjęto do realizacji"}), 200
    
    elif transfer_type == "express":
        success = account.express_outgoing_transfer(amount)
        if not success:
            return jsonify({"error": "Insufficient funds"}), 422
        return jsonify({"message": "Zlecenie przyjęto do realizacji"}), 200
    
    else:
        return jsonify({"error": "Unknown transfer type"}), 400


if __name__ == '__main__':
    app.run(debug=True)
