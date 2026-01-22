from behave import *
import requests

URL = "http://localhost:5000"


@when('I perform incoming transfer of "{amount}" to account with pesel "{pesel}"')
def perform_incoming_transfer(context, amount, pesel):
    json_body = {
        "amount": float(amount),
        "type": "incoming"
    }
    response = requests.post(URL + f"/api/accounts/{pesel}/transfer", json=json_body)
    assert response.status_code == 200, f"Transfer failed with status {response.status_code}"
    context.last_transfer_response = response


@when('I perform outgoing transfer of "{amount}" from account with pesel "{pesel}"')
def perform_outgoing_transfer(context, amount, pesel):
    json_body = {
        "amount": float(amount),
        "type": "outgoing"
    }
    response = requests.post(URL + f"/api/accounts/{pesel}/transfer", json=json_body)
    assert response.status_code == 200, f"Transfer failed with status {response.status_code}"
    context.last_transfer_response = response


@when('I try to perform outgoing transfer of "{amount}" from account with pesel "{pesel}"')
def try_perform_outgoing_transfer(context, amount, pesel):
    json_body = {
        "amount": float(amount),
        "type": "outgoing"
    }
    response = requests.post(URL + f"/api/accounts/{pesel}/transfer", json=json_body)
    context.last_transfer_response = response


@when('I perform express transfer of "{amount}" from account with pesel "{pesel}"')
def perform_express_transfer(context, amount, pesel):
    json_body = {
        "amount": float(amount),
        "type": "express"
    }
    response = requests.post(URL + f"/api/accounts/{pesel}/transfer", json=json_body)
    assert response.status_code == 200, f"Express transfer failed with status {response.status_code}"
    context.last_transfer_response = response


@then('Account with pesel "{pesel}" has balance equal to "{balance}"')
def check_account_balance(context, pesel, balance):
    response = requests.get(URL + f"/api/accounts/{pesel}")
    assert response.status_code == 200
    account = response.json()
    actual_balance = account["balance"]
    expected_balance = float(balance)
    assert actual_balance == expected_balance, \
        f"Expected balance {expected_balance}, but got {actual_balance}"


@then('Transfer should fail with status code "{status_code}"')
def check_transfer_failure(context, status_code):
    assert context.last_transfer_response.status_code == int(status_code), \
        f"Expected status {status_code}, but got {context.last_transfer_response.status_code}"
