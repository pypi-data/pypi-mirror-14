Python client for Barchart OnDemand
-----------------------------------

Get a free API key at:

-  http://freemarketdataapi.barchartondemand.com/

Currently supports
~~~~~~~~~~~~~~~~~~

-  getHistory
-  getQuote
-  getFinancialHighlights (requires paid license key)

Example Code
~~~~~~~~~~~~

`See how to use the client in your project
here <https://github.com/lanshark/barchart-ondemand-client-python/blob/master/samples/main.py>`__.

To set the API\_KEY for these applications, set an environment variable
as follows:

::

    export BARCHART_API_KEY="xxxxxxxxxxxxxxxxxxxx"

To set the URL\_BASE (ondemand or marketdata) for these applications,
set an environment variable as follows:

::

    export BARCHART_URL_BASE="marketdata.websol.barchartondemand.com"

Additional remarks
~~~~~~~~~~~~~~~~~~

This project is not a `Barchart <http://www.barchartondemand.com/>`__
project. This project was forked from
`femtotrader's <http://github.com/femtotrader>`__ project and
extended/modified.

Use it at your own risk.

Some Barchart projects are available at https://github.com/barchart/
