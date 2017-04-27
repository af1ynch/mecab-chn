import os

DEFAULT_BINARY_PATH = os.path.dirname(os.path.realpath(__file__))

WAKATI = "-d " + DEFAULT_BINARY_PATH + " -O wakati"
POS = "-d " + DEFAULT_BINARY_PATH + " -O pos"
PY = "-d " + DEFAULT_BINARY_PATH + " -O pinyin"
FAN = "-d " + DEFAULT_BINARY_PATH + " -O fan"
