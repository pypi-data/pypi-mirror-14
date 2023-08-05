# -*- coding: utf-8 -*-

from __future__ import print_function
import random
import zmq
import sys
import time
import json
import importlib
import imp
import abc
import inspect
import os
import sys
from datetime import datetime
from six import with_metaclass

from keystone.strategy import KSStrategy, KSStrategyRunner
from keystone.sources.csv_source import KSCsvSource
from keystone.sources.app_source import KSAppUniverseSource
from keystone.performance.analyzer import KSDefaultAnalyzer, KSCumulativeAnalyzer
from keystone.drain import KSDrain
from keystone.app_client.kpdb import KPdb
from keystone.app_client.session import Session
from keystone.py3compat import PY3, builtin_mod, iteritems, unicode_type, string_types
from keystone.utils.json_utils import json_clean

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--config', help='strategy config', required=True)

def byteify(input):
    if isinstance(input, dict):
        return {byteify(key):byteify(value) for key,value in iteritems(input)}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode_type):
        return input.encode('utf-8')
    else:
        return input

def unify(input):
    if isinstance(input, dict):
        return {unify(key):unify(value) for key,value in iteritems(input)}
    elif isinstance(input, list):
        return [unify(element) for element in input]
    elif isinstance(input, string_types):
        if not PY3 and isinstance(input, bytes):
            return unicode_type(input.decode('utf8'))
        return unicode_type(input)
    else:
        return input

def loadUserStrategyClass(filename):
    try:
        strategy = None
        module = imp.load_source('UserStrategy', filename)
        for cls_name in dir(module):
            cls = getattr(module, cls_name)
            if inspect.isclass(cls) and issubclass(cls, KSStrategy) and cls.__name__ != 'KSStrategy':
                if strategy is not None:
                    raise ValueError("find multiple strategy: %s, %s"%(strategy.__name__, cls.__name__))
                else:
                    strategy = cls
    except Exception as e:
        raise ValueError("cannot find load Python code  from %s: %s"%(filename, e))
    if strategy is None:
        raise ValueError("cannot find strategy from %s"%(filename))
    return strategy

'''
StrategyClient

Run backtesting using a config
config format:
{
    "in_url": string, stdin url for ipc, e.g. "tcp://127.0.0.1:55555",
    "drain_url": string, drain url for ipc, e.g. "tcp://127.0.0.1:55556",
    "syn_url": string, syn url for synchronize zmq.publisher socket
    "session": string, uuid,
    "filename": "/Users/rk/Desktop/share_folder/keystone-strategy-engine/node/strategy.py",
    "startingCash": int, 100000, 起始资金
    "startTime": string, 起始时间
    "endTime": string, 结束时间
    "benchmark": dict, {'sid':000001, 'column': 'close'}， 基准
    "riskless": float, 年化无风险利率
    "tradingDays": int, 年交易日
    "tradingHours": int, 日交易时间
    "sampleRate": string, [DAY, HOUR, MINUTE, SECOND]
    "stopPercentage": float, in [0.0,1.0], 止损点
    "historyCapacity": int, history capacity, 要保存的历史长度
    "instanceMatch": bool, 实时撮合
    "sources": [
        {"type": "csv", 文件类型，目前只有csv
         "path": "/Users/rk/Desktop/share_folder/keystone-strategy-engine/data/market.csv", 文件路径
         "dt_column": "dt", 时间列
         "dt_format": "%Y-%m-%d %H:%M:%S", 时间格式
         "price_column": "price", 价格列
         "sid_column": "sid", security code column
         "delimiter": "," csv文件分隔符
        },
        ..., 
        ...]
 }
'''
class StrategyClient(with_metaclass(abc.ABCMeta)):
    # outstream_factory = OutStream
    # outstream_factory.flush_interval = 0.0
    session = Session()
    context = zmq.Context()
    def __init__(self, config):
        if isinstance(config, string_types):
            config = json.loads(config)
        elif isinstance(config, dict):
            config = dict(config)
        else:
            raise TypeError("input config MUST BE 'string' or 'dict'")
        print(config, file=sys.stderr)
        self.config = unify(config)
        self.check_config(config)
        self.strategy_runner = KSStrategyRunner()
        self.init_session()
        self.init_strategy_runner()
        self.init_socket()
        if 'io_redircet' not in config or config['io_redircet'] == True:
            self.io_redirect()

    def check_config(self, config):
        pass

    def run(self):
        self.strategy_runner.run()

    def init_session(self):
        self.session.auth = None
        if 'session' in self.config:
            Session.session = self.config['session']
        self.session_uuid = Session.session

    def init_strategy_runner(self):
        config = self.config
        try:
            # load user strategy class
            userStrategy = loadUserStrategyClass(config['filename'])
            # init source
            sources = config['sources']
            for source_config in sources:
                source = self._get_source(source_config)
                self.strategy_runner.addSource(source)
            # use user strategy class
            self.strategy_runner.setStrategy(userStrategy)
            # benchmark
            if "benchmark" in config:
                benchmark = config["benchmark"]
                if "sid" in benchmark:
                    self.strategy_runner.setBenchmark(benchmark["column"], benchmark["sid"])
                else:
                    self.strategy_runner.setBenchmark(benchmark["column"])
            # instance match
            if "instanceMatch" in config:
                self.strategy_runner.setInstantMatch()
            # history
            if "historyCapacity" in config:
                self.strategy_runner.setHistoryCapacity(config["historyCapacity"])
            # start time and end time
            if "startTime" in config:
                # dt = datetime.strptime(config["startTime"], '%Y-%m-%d %H:%M:%S')
                dt = datetime.utcfromtimestamp(config["startTime"])
                self.strategy_runner.setStartTime(dt)
            if "endTime" in config:
                # dt = datetime.strptime(config["endTime"], '%Y-%m-%d %H:%M:%S')
                dt = datetime.utcfromtimestamp(config['endTime'])
                self.strategy_runner.setEndTime(dt)
            # analyzer
            default_analyzer = KSDefaultAnalyzer()
            self.strategy_runner.attachAnalyzer(default_analyzer)
            # stop percentage
            if "stopPercentage" in config:
                self.strategy_runner.setStopPercentage(config["stopPercentage"])
            # drain address
            if "drain_url" in config and "syn_url" in config:
                self.strategy_runner.setDrainAddress(config["drain_url"], config["syn_url"])
            # riskless
            if "riskless" in config:
                self.strategy_runner.setRiskless(config["riskless"])
            # tradingDays
            if "tradingDays" in config:
                self.strategy_runner.setTradingDays(config["tradingDays"])
            # tradingDays
            if "tradingHours" in config:
                self.strategy_runner.setTradingDays(config["tradingHours"])
            # sampleRate
            if "sampleRate" in config:
                self.strategy_runner.setSampleRate(config["sampleRate"])
        except Exception as e:
            raise ValueError("Initilize strategy config error: %s"%(e))

    '''
    def _get_source(self, source_config):
        src_type = source_config['type'].lower()
        if source_config['type'].lower() == "csv":
            source = KSCsvSource(source_config['path'], source_config['dt_column'], source_config['dt_format'])
            # price data or security data
            if 'sid_column' in source_config:
                if 'price_column' in source_config:
                    source.tagAsPriceData(source_config['sid_column'], source_config['price_column'])
                else:
                    source.tagAsSecurityData(source_config['sid_column'])
            # delimiter
            if 'delimiter' in source_config:
                source.setDelimiter(source_config['delimiter'])
            return source
        else:
            raise ValueError("cannot support source type \"%s\""%(src_type))
    '''
    def _get_source(self, source_config):
        source = KSAppUniverseSource(source_config['path'], source_config['basket'])
        # print(source.to_dict(), file=sys.stderr)
        return source

    def init_socket(self):
        config = self.config
        stdin_socket = self.context.socket(zmq.DEALER)
        # stdin_socket.linger = 1000
        stdin_socket.setsockopt_string(zmq.IDENTITY, self.session_uuid)
        stdin_socket.connect(config['in_url'])
        self.stdin_socket = stdin_socket

        # following code is moved to drain.py
        # stdout_socket = self.context.socket(zmq.PUB)
        # stdout_socket.linger = 1000
        # stdout_socket.bind(config['drain_url'])
        # self.stdout_socket = stdout_socket

    def io_redirect(self):
        self._forward_input()
        # sys.stdout = self.outstream_factory(self.session, self.stdout_socket, u'stdout')
        # sys.stderr = self.outstream_factory(self.session, self.stdout_socket, u'stderr')

    def _forward_input(self):
        if PY3:
            self._sys_raw_input = builtin_mod.input
            builtin_mod.input = self.raw_input
        else:
            self._sys_raw_input = builtin_mod.raw_input
            self._sys_eval_input = builtin_mod.input
            builtin_mod.raw_input = self.raw_input
            builtin_mod.input = lambda prompt='': eval(self.raw_input(prompt))

    def raw_input(self, prompt=''):
        """Forward raw_input to frontends
        Raises
        ------
        StdinNotImplentedError if active frontend doesn't support stdin.
        """
        return self._input_request(prompt, password=False)

    def _input_request(self, prompt, password=False):
        # Flush output before making the request.
        sys.stderr.flush()
        sys.stdout.flush()
        # flush the stdin socket, to purge stale replies
        while True:
            try:
                self.stdin_socket.recv_multipart(zmq.NOBLOCK)
            except zmq.ZMQError as e:
                if e.errno == zmq.EAGAIN:
                    break
                else:
                    raise

        # Send the input request.
        content = json_clean(dict(prompt=prompt, password=password))
        msg = self.session.send(self.stdin_socket, 'input_request', content = content)
        # print("sending input request: " + msg.__str__(), file=sys.stderr)

        # Await a response.
        while True:
            try:
                ident, reply = self.session.recv(self.stdin_socket,0)
                # print("*********ident(%s), recieve %s"%(ident, reply), file=sys.stderr)
            except Exception as e:
                print("Invalid Message", file=sys.stderr)
                raise e
            except KeyboardInterrupt:
                # re-raise KeyboardInterrupt, to truncate traceback
                raise KeyboardInterrupt
            else:
                break
        try:
            # value = reply['content']['value'].encode('utf8', "replace")
            value = reply['content']['value']
        except:
            print("Bad input_reply", file=sys.stderr)
            # self.log.error("Bad input_reply: %s", parent)
            value = ''
        if value == '\x04':
            # EOF
            raise EOFError
        return value

class StrategyRunner(object):
    def run(self, config):
        client = StrategyClient(config)
        client.run()

class StrategyDebugger(object):
    def __init__(self, *args, **kwargs):
        # set datetime break point condition
        # err = self.pdb.do_break_at_function(self.strategy_runner.strategyInstance.onData, 
        #     cond = "self._datetimeBreakPointCls.is_break_at_datetime(data.time())")
        # if err:
        #     print >>sys.stderr, err
        # self.pdb.onecmd('')

        # debug mode also send all data in drain
        KSDrain.send_data = True

    def execute_cmd(self, cmds):
        for cmd in cmds:
            self.pdb.onecmd(cmd)

    def run(self, config):
        # get absolute file path
        config['filename'] = os.path.abspath(config['filename'])
        # init strategy client
        client = StrategyClient(config)        # initialize KPdb
        self.pdb = KPdb(config['filename'],
            client.session, 
            config['notify_url'], 
            config['syn_url'],  
            config['control_url'], 
            datetime_break_func=client.strategy_runner.strategyClass.onData,
            datetime_break_cond="self._datetimeBreakPointCls.is_break_at_datetime(data.time())",
            stdout=sys.stdout);
        self.pdb.use_rawinput = True
        self.pdb.run('client.run()', globals(), locals())


