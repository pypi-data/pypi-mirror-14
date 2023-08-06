#!/usr/bin/python3
# Copyright (C) 2015 Bitquant Research Laboratories (Asia) Limited
# Released under the Simplified BSD License
import my_path
import time
import algobroker
import pprint


class StrategyAlert(algobroker.Strategy):

    def __init__(self):
        algobroker.Strategy.__init__(self, "strategy_alert",
                                     ['ticker_yahoo',
                                      'ticker_bitcoin'])
        self.time_limits = {}
        self.state = {}
        self.prev_state = {}
        self.limits = {}
        self.quotes = {}
        self.maintainence = 60 * 30
        self.bitcoin_source = "bravenewcoin"
        self.alerts = [
            {'cmd': 'alert',
             'type': 'sms',
             'to': 'trader1'
             },
            {'cmd': 'alert',
             'type': 'web'
             }
        ]
        self.send_control("ticker_bitcoin",
                          {"cmd" : "set",
                           "exchanges" : [self.bitcoin_source]})

    def test_limits(self):
        for i in self.limits.keys():
            if i in self.limits and i in self.quotes:
                limits = self.limits[i]
                if limits[0] != None and self.quotes[i] <= limits[0]:
                    self.state[i] = "low"
                elif limits[1] != None and self.quotes[i] >= limits[1]:
                    self.state[i] = "high"
                else:
                    self.state[i] = "ok"

    def send_notices(self):
        msg = ""
        for k, v in self.state.items():
            if k in self.prev_state:
                prev_state = self.prev_state[k]
            else:
                prev_state = "none"
            if v == "high" or v == "low":
                if prev_state != v:
                    msg += "%s - %f - %s | " % (k, self.quotes[k],
                                                v)
        if msg != "":
            for alert in self.alerts:
                alert['text'] = msg
                self.send_action(alert)
        for k, v in self.state.items():
            self.prev_state[k] = v

    def test(self):
        work_message = {'cmd': 'log',
                        'item': 'hello'}
        self.send_action(work_message)
        work_message = {'cmd': 'alert',
                        'type': 'sms',
                        'to': 'trader1',
                        'text': 'hello and happy trading'}
        self.send_action(work_message)

    def process_control(self, data):
        algobroker.Strategy.process_control(self, data)
        if data['cmd'] == "set":
            if 'limits' in data:
                self.debug("setting limits")
                self.debug(pprint.pformat(data))
                self.limits = data['limits']
            if 'alerts' in data:
                self.alerts = data['alerts']

    def process_data(self, data):
        self.debug("running alert loop")
        self.debug(data)
        if "ticker_yahoo" in data:
            quotes = data['ticker_yahoo']
            for k, v in quotes.items():
                if 'last' in v:
                    self.quotes[k] = float(v['last'])
        elif "ticker_bitcoin" in data:
            quotes = data['ticker_bitcoin']
            if self.bitcoin_source in quotes:
                self.quotes['XBT'] = \
                     float(quotes[self.bitcoin_source]['last'])
        self.test_limits()
        self.send_notices()

if __name__ == "__main__":
    qm = StrategyAlert()
    qm.run()
