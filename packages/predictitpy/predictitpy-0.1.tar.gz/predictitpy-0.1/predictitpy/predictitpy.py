import json
import urllib2
from dateutil import parser

__author__ = 'Adam J. Gray'

ROOT_URL = 'https://www.predictit.org/api/marketdata/ticker/'


def get_market(market_ticker):
    """ Get a dict of all the contracts in a given PredictIt market.

    :param market_ticker:
        The ticker associated with the market. So for example, for the 2016 Democratic Nomination
        it would be DNOM16
        It turns out that you also specify a full contract ticker, like SANDERS.DNOM16 and it will
        also return the full market (all contracts in the market).

    :return:
        A dict for the whole market.
    """
    url = ROOT_URL + market_ticker
    f = urllib2.urlopen(url)
    parsed_data = json.loads(f.read())
    return parsed_data


def get_contract(market, ticker):
    """ Get a given contract, given its ticker (eg SANDERS.DNOM16) from a dict of the market.

    :param market:
        A dict representing the market as returned by get_market.

    :param ticker:
        The full ticker for a contract. Eg SANDERS.DNOM16

    :return:
        A dict for that contract.
    """
    contracts = market['Contracts']
    matching = [c for c in contracts if c['TickerSymbol'] == ticker][0]
    return matching



def get_timestamp(market):
    """ Get a parsed version of the timestamp associated with the market dict.

    :param market:
        A dict representation of the market as returned by get_market.

    :return:
        A datetime.datetime representing when the data in the market was valid.
    """
    ts = parser.parse(market['TimeStamp'])
    return ts

