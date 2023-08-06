# encoding: utf-8
from communication.server.protocol import function_code
from communication.server.protocol.protocol import ProtocolMessage


__author__ = 'Yonka'

HEADER_SIZE = 20
CLIENT_ID_SIZE = 4
REQID_SIZE = 4
PC_SIZE = 4
LEN_SIZE = 4
MAX_SIZE = 15000000


def new_strategy_hb_msg():
    return ProtocolMessage(function_code.HEARTBEAT, 0, function_code.STRATEGY, "")


def new_strategy_hb_ack_msg(req_id: int=0):
    return ProtocolMessage(function_code.ACK, req_id, function_code.STRATEGY, "")