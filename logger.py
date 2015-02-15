import logging
import sys

log = logging.getLogger("GW2Events")
log.setLevel(logging.DEBUG)
# Setup the console logging
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] - %(name)s(%(levelname)s): %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)
