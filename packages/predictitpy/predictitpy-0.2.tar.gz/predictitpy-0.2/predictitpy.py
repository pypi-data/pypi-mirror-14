import urllib2 as _urllib2
import json as _json
from dateutil import parser as _parser
import datetime as _dt

__author__ = 'Adam J. Gray'

__ROOT_URL = 'https://www.predictit.org/api/marketdata/ticker/'


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
    url = __ROOT_URL + market_ticker
    f = _urllib2.urlopen(url)
    parsed_data = _json.loads(f.read())
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
    ts = _parser.parse(market['TimeStamp'])
    return ts


class Client:
    """ A client for accessing and caching PredictIt.org market data.

    """
    def __init__(self, cache_age_seconds=60):
        """ Create a cached client.

        :param cache_age_seconds:
            The maximum age to leave things in the cache for.

        :return:
        """
        self.__cache_age_seconds = cache_age_seconds
        self.__cache = {}

    def get_market(self, market_ticker, refresh_cache=False):
        """ Get a dict of all the contracts in a given PredictIt market.

        :param market_ticker:
            The ticker associated with the market. So for example, for the 2016 Democratic Nomination
            it would be DNOM16
            It turns out that you also specify a full contract ticker, like SANDERS.DNOM16 and it will
            also return the full market (all contracts in the market).

        :param refresh_cache:
            Whether to refresh the cache entry for this market.

        :return:
            A dict for the whole market.
        """
        if market_ticker not in self.__cache:
            market = get_market(market_ticker)
            self.__cache[market_ticker] = (_dt.datetime.utcnow(), market)
        elif (_dt.datetime.utcnow() - self.__cache[market_ticker][0]).total_seconds() > self.__cache_age_seconds:
            market = get_market(market_ticker)
            self.__cache[market_ticker] = (_dt.datetime.utcnow(), market)
        return self.__cache[market_ticker][1]

    def get_contract(self, contract_ticker, refresh_cache=False):
        """ Get a given contract, given its ticker (eg SANDERS.DNOM16) from a dict of the market.

        :param contract_ticker:
            The full ticker for a contract. Eg SANDERS.DNOM16

        :param refresh_cache:
            Whether to refresh the cache entry for the associated market.

        :return:
            A dict for that contract.
        """
        market_ticker = contract_ticker.split('.', 1)[1]
        market = self.get_market(market_ticker, refresh_cache=refresh_cache)
        return get_contract(market, contract_ticker)

    def get_timestamp(self, market_ticker, refresh_cache=False):
        """ Get a parsed version of the timestamp associated with the market dict.

        :param market_ticker:
            The ticker associated with the market. So for example, for the 2016 Democratic Nomination
            it would be DNOM16
            It turns out that you also specify a full contract ticker, like SANDERS.DNOM16 and it will
            also return the full market (all contracts in the market).

        :param refresh_cache:
            Whether to refresh the cache entry for the associated market.

        :return:
            A datetime.datetime representing when the data in the market was valid.
        """
        market = self.get_market(market_ticker, refresh_cache=refresh_cache)
        return get_timestamp(market)

