import datetime
from betfairlightweight.errors import apierrorhandling
from betfairlightweight.parse import apiparsedata, apiparseaccount, apiparsebetting, apiparsescores
from betfairlightweight.apimethod import Login, Logout, KeepAlive, BettingRequest, AccountRequest, ScoresRequest


def login(api):
    response = Login(api).call()
    if not apierrorhandling.api_login_error_handling(response):
        return
    return response


def keep_alive(api):
    response = KeepAlive(api).call()
    if not apierrorhandling.api_keep_alive_error_handling(response):
        return
    return response


def logout(api):
    response = Logout(api).call()
    if not apierrorhandling.api_logout_error_handling(response):
        return
    return response


# Betting requests


def list_event_types(api, params=None, session=None, parsed=True):
    if not params:
        params = {'filter': {}}
    response = BettingRequest(api, 'SportsAPING/v1.0/listEventTypes', params).call(session)
    if response:
        (response, raw_response, sent) = response
        if not apierrorhandling.api_betting_error_handling(response, params):
            return
        if parsed:
            return [apiparsedata.EventType(sent, raw_response, x) for x in response['result']]
        else:
            return response


def list_competitions(api, params=None, session=None, parsed=True):
    if not params:
        params = {'filter': {}}
    response = BettingRequest(api, 'SportsAPING/v1.0/listCompetitions', params).call(session)
    if response:
        (response, raw_response, sent) = response
        if not apierrorhandling.api_betting_error_handling(response, params):
            return
        if parsed:
            return [apiparsedata.Competition(sent, raw_response, x) for x in response['result']]
        else:
            return response


def list_time_ranges(api, params=None, session=None, parsed=True):
    if not params:
        params = {'filter': {},
                  'granularity': 'DAYS'}
    response = BettingRequest(api, 'SportsAPING/v1.0/listTimeRanges', params).call(session)
    if response:
        (response, raw_response, sent) = response
        if not apierrorhandling.api_betting_error_handling(response, params):
            return
        if parsed:
            return [apiparsedata.TimeRange(sent, raw_response, x) for x in response['result']]
        else:
            return response


def list_events(api, params=None, session=None, parsed=True):
    if not params:
        params = {'filter': {}}
    response = BettingRequest(api, 'SportsAPING/v1.0/listEvents', params).call(session)
    if response:
        (response, raw_response, sent) = response
        if not apierrorhandling.api_betting_error_handling(response, params):
            return
        if parsed:
            return [apiparsedata.Event(sent, raw_response, x) for x in response['result']]
        else:
            return response


def list_market_types(api, params=None, session=None, parsed=True):
    if not params:
        params = {'filter': {}}
    response = BettingRequest(api, 'SportsAPING/v1.0/listMarketTypes', params).call(session)
    if response:
        (response, raw_response, sent) = response
        if not apierrorhandling.api_betting_error_handling(response, params):
            return
        if parsed:
            return [apiparsedata.MarketType(sent, raw_response, x) for x in response['result']]
        else:
            return response


def list_countries(api, params=None, session=None, parsed=True):
    if not params:
        params = {'filter': {}}
    response = BettingRequest(api, 'SportsAPING/v1.0/listCountries', params).call(session)
    if response:
        (response, raw_response, sent) = response
        if not apierrorhandling.api_betting_error_handling(response, params):
            return
        if parsed:
            return [apiparsedata.Country(sent, raw_response, x) for x in response['result']]
        else:
            return response


def list_venues(api, params=None, session=None, parsed=True):
    if not params:
        params = {'filter': {}}
    response = BettingRequest(api, 'SportsAPING/v1.0/listVenues', params).call(session)
    if response:
        (response, raw_response, sent) = response
        if not apierrorhandling.api_betting_error_handling(response, params):
            return
        if parsed:
            return [apiparsedata.Venue(sent, raw_response, x) for x in response['result']]
        else:
            return response


def list_market_catalogue(api, params=None, session=None, parsed=True):
    if not params:
        params = {'filter': {},
                  'maxResults': '1'}
    response = BettingRequest(api, 'SportsAPING/v1.0/listMarketCatalogue', params).call(session)
    if response:
        (response, raw_response, sent) = response
        if not apierrorhandling.api_betting_error_handling(response, params):
            return
        if parsed:
            return [apiparsedata.MarketCatalogue(sent, raw_response, x) for x in response['result']]
        else:
            return response


def list_market_book(api, params=None, session=None, parsed=True):
    if not params:
        params = {'marketIds': ['1.122618187']}
    response = BettingRequest(api, 'SportsAPING/v1.0/listMarketBook', params).call(session)
    if response:
        (response, raw_response, sent) = response
        if not apierrorhandling.api_betting_error_handling(response, params):
            return
        if parsed:
            return [apiparsedata.MarketBook(sent, raw_response, x) for x in response['result']]
        else:
            return response

# order requests


def place_orders(api, params, session=None, parsed=True):  # atomic
    response = BettingRequest(api, 'SportsAPING/v1.0/placeOrders', params).call(session)
    if response:
        (response, raw_response, sent) = response
        date_time_received = datetime.datetime.now()
        apierrorhandling.api_order_error_handling(response, params)
        if 'error' in response:
            return
        if parsed:
            return apiparsebetting.PlaceOrder(sent, raw_response, response['result'], date_time_received)
        else:
            return response


def cancel_orders(api, params=None, session=None, parsed=True):
    if not params:
        params = {}  # cancel ALL orders
    response = BettingRequest(api, 'SportsAPING/v1.0/cancelOrders', params).call(session)
    if response:
        (response, raw_response, sent) = response
        date_time_received = datetime.datetime.now()
        apierrorhandling.api_order_error_handling(response, params)
        if 'error' in response:
            return
        if parsed:
            if params:
                return apiparsebetting.CancelOrder(sent, raw_response, response['result'], date_time_received)
            else:
                return apiparsebetting.CancelAllOrders(sent, raw_response, response['result'], date_time_received)
        else:
            return response


def update_orders(api, params, session=None, parsed=True):
    response = BettingRequest(api, 'SportsAPING/v1.0/updateOrders', params).call(session)
    if response:
        (response, raw_response, sent) = response
        date_time_received = datetime.datetime.now()
        apierrorhandling.api_order_error_handling(response, params)
        if 'error' in response:
            return
        if parsed:
            return apiparsebetting.UpdateOrder(sent, raw_response, response['result'], date_time_received)
        else:
            return response


def replace_orders(api, params, session=None, parsed=True):
    response = BettingRequest(api, 'SportsAPING/v1.0/replaceOrders', params).call(session)
    if response:
        (response, raw_response, sent) = response
        date_time_received = datetime.datetime.now()
        apierrorhandling.api_order_error_handling(response, params)
        if 'error' in response:
            return
        if parsed:
            return apiparsebetting.ReplaceOrder(sent, raw_response, response['result'], date_time_received)
        else:
            return response


def list_current_orders(api, params=None, session=None, parsed=True):  # todo handle moreAvailable
    if not params:
        params = {'dateRange': {}}
    response = BettingRequest(api, 'SportsAPING/v1.0/listCurrentOrders', params).call(session)
    if response:
        (response, raw_response, sent) = response
        if not apierrorhandling.api_betting_error_handling(response, params):
            return
        if parsed:
            return apiparsedata.CurrentOrders(sent, raw_response, response['result'])
        else:
            return response


def list_cleared_orders(api, params=None, session=None, parsed=True):  # todo handle moreAvailable & groupby params
    if not params:
        params = {'betStatus': 'SETTLED',
                  'settledDateRange': {},
                  'recordCount': '1000'}
    response = BettingRequest(api, 'SportsAPING/v1.0/listClearedOrders', params).call(session)
    if response:
        (response, raw_response, sent) = response
        if not apierrorhandling.api_betting_error_handling(response, params):
            return
        if parsed:
            return apiparsedata.ClearedOrders(sent, raw_response, response['result'])
        else:
            return response


def list_market_profit_and_loss(api, params=None, session=None, parsed=True):
    if not params:
        params = {'marketIds': ['1.122617964']}
    response = BettingRequest(api, 'SportsAPING/v1.0/listMarketProfitAndLoss', params).call(session)
    if response:
        (response, raw_response, sent) = response
        if not apierrorhandling.api_betting_error_handling(response, params):
            return
        if parsed:
            return [apiparsedata.MarketProfitLoss(sent, raw_response, x) for x in response['result']]
        else:
            return response


def list_race_status(api, params, session=None, parsed=True):
    response = ScoresRequest(api, 'ScoresAPING/v1.0/listRaceDetails', params).call(session)
    if response:
        (response, raw_response, sent) = response
        if not apierrorhandling.api_betting_error_handling(response, params):
            return
        if parsed:
            return [apiparsescores.RaceStatus(sent, raw_response, x) for x in response['result']]
        else:
            return response


# account requests  # todo account error handling


def get_account_funds(api, params=None, session=None, parsed=True):
    if not params:
        params = {'wallet': 'UK'}  # AUSTRALIAN
    response = AccountRequest(api, 'AccountAPING/v1.0/getAccountFunds', params).call(session)
    if response:
        (response, raw_response, sent) = response
        if parsed:
            return apiparseaccount.AccountFunds(sent, raw_response, response['result'])
        else:
            return response


def get_account_details(api, params=None, session=None, parsed=True):
    if not params:
        params = {}
    response = AccountRequest(api, 'AccountAPING/v1.0/getAccountDetails', params).call(session)
    if response:
        (response, raw_response, sent) = response
        if parsed:
            return apiparseaccount.AccountDetails(sent, raw_response, response['result'])
        else:
            return response


def get_account_statement(api, params=None, session=None, parsed=True):
    if not params:
        params = {'itemDateRange': {},
                  'includeItem': 'ALL'}
    response = AccountRequest(api, 'AccountAPING/v1.0/getAccountStatement', params).call(session)
    if response:
        (response, raw_response, sent) = response
        if parsed:
            return apiparseaccount.AccountStatement(sent, raw_response, response['result'])
        else:
            return response


def list_currency_rates(api, params=None, session=None, parsed=True):
    if not params:
        params = {'fromCurrency': 'GBP'}
    response = AccountRequest(api, 'AccountAPING/v1.0/listCurrencyRates', params).call(session)
    if response:
        (response, raw_response, sent) = response
        if parsed:
            return [apiparseaccount.CurrencyRate(sent, raw_response, x) for x in response['result']]
        else:
            return response


def transfer_funds(api, params=None, session=None, parsed=True):
    if not params:
        params = {'from': 'UK',
                  'to': 'AUSTRALIAN',
                  'amount': '0.01'}
    response = AccountRequest(api, 'AccountAPING/v1.0/transferFunds', params).call(session)
    if response:
        (response, raw_response, sent) = response
        if parsed:
            return apiparseaccount.TransferFunds(sent, raw_response, response['result'])
        else:
            return response
