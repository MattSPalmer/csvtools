import logging

log = logging.getLogger("mylog")
log.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    "%(asctime)s %(levelname)-10s %(message)s")

# Log to file
fh = logging.FileHandler(__name__ + '_debug.log', "w")
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
log.addHandler(fh)

# Log to stdout too
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
sh.setFormatter(formatter)
log.addHandler(sh)

if __name__ == '__main__':
    # Test it
    log.debug("Some message")
    # log.error("An error!")
    try:
        log.info("I'm going to try something() here...")
    except:
        log.exception("Ouch! An exception occured!")
