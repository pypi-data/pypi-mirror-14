#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A Python library for Barchart API
http://freemarketdataapi.barchartondemand.com/.
"""

from datetime import datetime
from dateutil.parser import parse
import logging
import os
import requests
import six
from collections import OrderedDict

# NOTE: you can override this with environment settings
# For Free Access (getQuote and getHistory only)
URL_BASE = "http://marketdata.websol.barchart.com"
# For paid access (requires license)
# URL_BASE = "http://ondemand.websol.barchart.com"


DATE_FMT = "%Y-%m-%d"
TIMESTAMP_NOSEP_FMT = "%Y%m%d%H%M%S"

QUOTE_TIMESTAMP_COLS = [
    "serverTimestamp",
    "tradeTimestamp",
    "preMarketTimestamp"
]
QUOTE_DATE_COLS = [
    "previousTimestamp",
    "fiftyTwoWkHighDate",
    "fiftyTwoWkLowDate",
    "exDividendDate",
    "expirationDate",
    "twelveMnthPctDate",
]

# set up for logging...
logger = logging.getLogger(__name__)

# Change to INFO to get logging...
logger.setLevel(logging.INFO)

# Look for API_KEY (required) and URL (optional)
try:
    API_KEY = os.environ["BARCHART_API_KEY"]
except:
    # NOTE: This will not work... but should fail gracefully....
    API_KEY = ""
try:
    URL_BASE = os.environ["BARCHART_URL_BASE"]
except:
    # NOTE: default is free data....
    pass
logger.info("API_KEY={0}".format(API_KEY))
logger.info("URL_BASE={0}".format(URL_BASE))


def _create_from(session):
    """
    Returns a requests.Session (if session is None)
    or session (requests_cache.CachedSession)
    """
    if session is None:
        return requests.Session()
    else:
        return session


def _parse_json_response(response):
    """
    Parse JSON response.  Checks for expected 200 OK returns json if found.

    Throws NotImplementedError exception.
    """
    status_code = response.status_code
    status_code_expected = 200
    if status_code == status_code_expected:
        try:
            response = response.json()
        # NOTE: simplejson raises JSONDecodeError, which is a subclass of ValueError...
        except ValueError:
            raise NotImplementedError("Invalid Json: {0}".format(response.text))

        try:
            if response["status"]["code"] == status_code_expected:
                return response
            else:
                raise NotImplementedError("Error code: {0} - {1}".format(
                    response["status"]["code"], response["status"]["message"]
                ))
        except Exception as err:
            raise err
    else:
        raise NotImplementedError("HTTP status code is {0} instead of {1}".format(
            status_code, status_code_expected
        ))


def _parse_timestamp(results, cols):
    """
    Returns a result where string timestamps have been parsed
    """
    for col in cols:
        try:
            if isinstance(results, list):
                for result in results:
                    s = result[col]
                    if s:
                        result[col] = parse(s)
            else:
                s = results[col]
                if s:
                    results[col] = parse(s)
        except KeyError:
            pass
    return results


def _parse_date(results, cols, date_fmt=DATE_FMT):
    """
    Returns a result where string dates have been parsed
    """
    for col in cols:
        try:
            if isinstance(results, list):
                for result in results:
                    s = result[col]
                    if s:
                        result[col] = datetime.strptime(s, date_fmt).date()
            else:
                s = results[col]
                if s:
                    results[col] = datetime.strptime(s, date_fmt).date()
        except KeyError:
            pass
    return results


def getQuote(symbols, fields=None, session=None):
    """
    Returns stock quote for one (or several) symbol(s), comma separated.

    getQuote sample query:
        http://marketdata.websol.barchart.com/getQuote.json?apikey=YOURAPIKEY&symbols=BAC,IBM,GOOG,HBAN

    Fields always returned are:

        symbol                      (string)
        name                        (string)
        dayCode                     (string) 1-9, 0, A-U
        serverTimestamp             (datetime)
        mode                        (string) R=realtime, I=delayed, D=end-of-day
        lastPrice                   (double)
        tradeTimestamp              (datetime)
        netChange                   (double)
        percentChange               (double)
        unitCode                    (string)
        open                        (double)
        high                        (double)
        low                         (double)
        close                       (double), empty if market is open
        numTrades                   (int)
        dollarVolume                (double)
        flag                        (string) c=closed, p=pre-open, s=settled
        volume                      (int)
        previousVolume              (int)

    Optional Fields (must be requested in fields) are:
        tradeSize                   (int)
        tick                        (string)  +, ., or -
        previousLastPrice           (double)
        previousTimestamp           (date)
        bid                         (double)
        bidSize                     (int)
        ask                         (double)
        askSize                     (int)
        previousClose               (double)
        settlement                  (double)
        previousSettlement          (double)
        openInterest                (double)
        fiftyTwoWkHigh              (double)
        fiftyTwoWkHighDate          (date)
        fiftyTwoWkLow               (double)
        fiftyTwoWkLowDate           (date)
        avgVolume                   (int)
        sharesOutstanding           (int)
        dividendRateAnnual          (float)
        dividendYieldAnnual         (float)
        exDividendDate              (date)
        impliedVolatility           (double)
        twentyDayAvgVol             (double)
        month                       (string)  Futures Only
        year                        (string)  Futures Only
        expirationDate              (date)    Futures Only
        lastTradingDay              (string)  Futures Only
        twelveMnthPct               (double)
        twelveMnthPctDate           (date)
        preMarketPrice              (double)
        preMarketNetChange          (double)
        preMarketPercentChange      (double)
        preMarketTimestamp          (datetime)
        afterHoursPrice             (double)
        afterHoursNetChange         (double)
        afterHoursPercentChange     (double)
        afterHoursTimestamp         (datetime)
        averageWeeklyVolume         (int)
        averageQuarterlyVolume      (int)
        exchangeMargin              (string)
    """

    endpoint = "/getQuote.json"
    url = URL_BASE + endpoint
    params = {
        "apikey": API_KEY,
        "symbols": ",".join(symbols) if isinstance(symbols, list) else symbols,
        "fields": ",".join(fields) if isinstance(fields, list) else fields
    }
    session = _create_from(session)
    logger.debug("getQuote url: {0}".format(url))
    logger.debug("getQuote params: {0}".format(params))
    response = session.get(url, params=params)
    response = _parse_json_response(response)
    results = response["results"]
    if isinstance(symbols, six.string_types):
        d = results[0]
        d = _parse_timestamp(d, QUOTE_TIMESTAMP_COLS)
        d = _parse_date(d, QUOTE_DATE_COLS)
        return d  # returns a dict
    else:
        for i, d in enumerate(results):
            d = _parse_timestamp(d, QUOTE_TIMESTAMP_COLS)
            d = _parse_date(d, QUOTE_DATE_COLS)
        return results  # returns a list of dicts


def _getSingleHistory(
    symbol,
    startDate=None,
    endDate=None,
    typ="daily",
    maxRecords=None,
    interval=None,
    order="asc",
    session=None
):
    """
    getHistory sample query:
        http://marketdata.websol.barchart.com/getHistory.json?key=YOURAPIKEY&symbol=IBM&type=daily&startDate=20140928000000

    inputs:
        symbol          (string)
        type            (enum:
                            ticks,
                            minutes,
                            nearbyMinutes,
                            formTMinutes,
                            daily (default), dailyNearest, dailyContinue,
                            weekly, weeklyNearest, weeklyContinue,
                            monthly, monthlyNearest, monthlyContinue,
                            quarterly, quarterlyNearest, quarterlyContinue,
                            yearly, yearlyNearest, yearlyContinue).
        startDate       (yyyymmdd[hhmm[ss]]) (defaults today)
        endDate         (yyyymmdd[hhmm[ss]]) (defaults today)
        maxRecords      (int)
        interval        (int) default = 1 (minutes for minute query)
        order           (enum: asc (default), desc)

    There are other optional parameters (sessionFilter, splits, dividends, volume, nearby, exchange)
    which are NOT supported at this time.

    Always returns:
        symbol          (string)
        timestamp       (datetime)
        tradingDay      (date)

    Optionally returns (if requested?):
        sessionCode     (string) G=electronic R=pit
        tickPrice       (double)
        tickSize        (int)
        open            (double)
        high            (double)
        low             (double)
        close           (double)
        volume          (int)
        openInterest    (int)
    """

    endpoint = "/getHistory.json"
    url = URL_BASE + endpoint

    params = {
        "apikey": API_KEY,
        "symbol": symbol,
        "type": typ,
        "startDate": startDate,
        "order": order,
    }
    if endDate:
        params["endDate"] = endDate
    if maxRecords:
        params["maxRecords"] = maxRecords
    if interval:
        params["interval"] = interval
    session = _create_from(session)
    logger.debug("getSingleHistory url: {0}".format(url))
    logger.debug("getSingleHistory params: {0}".format(params))
    response = session.get(url, params=params)
    response = _parse_json_response(response)
    d = response["results"]
    timestamp_cols = ["timestamp"]
    date_cols = ["tradingDay"]
    d = _parse_timestamp(d, timestamp_cols)
    d = _parse_date(d, date_cols)
    return d


def getHistory(
    symbols,
    startDate,
    endDate=None,
    typ="daily",
    maxRecords=None,
    interval=None,
    order="asc",
    session=None
):
    """
    Returns history for ONE (or SEVERAL) symbol(s)
    """
    try:
        startDate = startDate.strftime(TIMESTAMP_NOSEP_FMT)
    except Exception:
        # this should not be catching everything
        logger.error("startDate invalid: {0}".format(startDate))
        pass
    try:
        endDate = endDate.strftime(TIMESTAMP_NOSEP_FMT)
    except Exception:
        # this should not be catching everything
        logger.error("endDate invalid: {0}".format(endDate))
        pass

    d = OrderedDict()
    if isinstance(symbols, list):
        for symbol in symbols:
            d[symbol] = _getSingleHistory(
                symbol,
                startDate,
                endDate,
                typ,
                maxRecords,
                interval,
                order,
                session
            )
    else:
        d[symbols] = _getSingleHistory(
            symbols,
            startDate,
            endDate,
            typ,
            maxRecords,
            interval,
            order,
            session
        )

    return d  # returns an OrderedDict


def getFinancialHighlights(symbols, fields=None, session=None):
    """
    (CURRENTLY, This requires a PAID key...)

    Returns financial highlights for one (or several) symbol(s), comma separated.

    getFinancialHighlights sample query:
        http://ondemand.websol.barchart.com/getFinancialHighlights.json?apikey=YOURAPIKEY&symbols=BAC,IBM,GOOG,HBAN

    Fields always returned are:

        symbol                      (string)
        marketCapitalization        (int)
        insiderShareholders         (double)
        annualRevenue               (int)
        ttmRevenue                  (int)
        sharesOutstanding           (int)
        institutionalShareholders   (double)
        oneYearReturn               (double)
        threeYearReturn             (double)
        fiveYearReturn              (double)
        ttmRevenueGrowth            (int)
        fiveYearRevenueGrowth       (double)
        fiveYearEarningsGrowth      (double)
        fiveYearDividentGrowth      (double)
        annualEPS                   (double)
        annualDividendRate          (double)
        annualDividendYield         (double)

    Optional Fields (must be requested in fields) are:
        annualNetIncome             (int)
        ttmNetIncome                (double)
        ttmNetProfitMargin          (double)
        lastQtrEPS                  (double)
        ttmEPS                      (double)
        twelveMonthEPSChg           (double)
        peRatio                     (double)
        recentEarnings              (double)
        recentDividends             (double)
        recentSplit                 (string)
        beta                        (double)
    """

    endpoint = "/getFinancialHighlights.json"
    url = URL_BASE + endpoint
    params = {
        "apikey": API_KEY,
        "symbols": ",".join(symbols) if isinstance(symbols, list) else symbols,
        "fields": ",".join(fields) if isinstance(fields, list) else fields
    }
    session = _create_from(session)
    logger.debug("getFinancialHighlights url: {0}".format(url))
    logger.debug("getFinancialHighlights params: {0}".format(params))
    response = session.get(url, params=params)
    response = _parse_json_response(response)
    results = response["results"]
    if isinstance(symbols, six.string_types):
        d = results[0]
        return d  # returns a dict
    else:
        return results  # returns a list of dicts
