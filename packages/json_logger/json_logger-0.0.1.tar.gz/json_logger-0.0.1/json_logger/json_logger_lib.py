import datetime
import logging
try:
    # if you're installing it it's because it's faster...
    import ujson as json
except:
    import json

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def json_logger(level="info", log_json={}, batch=None, ts_fmt='%Y-%m-%d %H:%M:%S,%f'):
    log_json["ts"] = datetime.datetime.now().strftime(ts_fmt)
    if batch:
        log_json["batch"] = batch
    try:
        log_json = json.dumps(log_json)
    except:
        # if it fails, oh well
        log_json = log_json  # make sure it's not partially changed
    if level == "info":
        log.info(log_json)
    elif level == "warn":
        log.warning(log_json)
    elif level == "error":
        log.error(log_json)
    elif level == "debug":
        log.debug(log_json)
    elif level == "print":
        print(log_json)
    else:  # default value
        log.info(log_json)
