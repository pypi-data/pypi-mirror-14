pysentosa - Python API for sentosa trading system

.. image:: http://www.quant365.com/static/merlion.png


- pysentosa is the Python API for sentosa trading system written by Wu Fuheng

- WebSite: http://www.quant365.com (Quant365 - Trading with Science and Technology)

- OS: Linux Ubuntu 15.10 64bit

- Installation:

  .. code-block:: bash

    GITURL=https://raw.githubusercontent.com/henrywoo/pysentosa/master
    wget $GITURL/install_nanomsg.sh -O install_nanomsg.sh
    chmod u+x install_nanomsg.sh
    ./install_nanomsg.sh

    wget $GITURL/install_yaml_cpp.sh -O install_yaml_cpp.sh
    chmod u+x install_yaml_cpp.sh
    ./install_yaml_cpp.sh

    sudo apt-get install -y python-pip libboost-all-dev
    sudo pip install -U pysentosa pyyaml netifaces websocket-client nanomsg \
      setproctitle psutil

- Launch your IB TWS.

- Run your strategy to trade

  Run demo:

  .. code-block:: python

    from pysentosa.demo import run_demo
    run_demo()

  Sample code:

  .. code-block:: python

      from pysentosa import Merlion
      from ticktype import *

      m = Merlion()
      target = 'SPY'
      m.track_symbol([target, 'BITA'])
      bounds = {target: [220, 250]}
      while True:
        symbol, ticktype, value = m.get_mkdata()
        if symbol == target:
          if ticktype == ASK_PRICE and value < bounds[symbol][0]:
              oid = m.buy(symbol, 5)
              while True:
                  ord_st = m.get_order_status(oid)
                  print ORDSTATUS[ord_st]
                  if ord_st == FILLED:
                      bounds[symbol][0] -= 20
                      break
                  sleep(2)
          elif ticktype == BID_PRICE and value > bounds[symbol][1]:
              oid = m.sell(symbol, 100)
              bounds[symbol][1] += 20


.. image:: https://d2weczhvl823v0.cloudfront.net/henrywoo/pysentosa/trend.png
   :alt: Bitdeli badge
   :target: https://bitdeli.com/free
