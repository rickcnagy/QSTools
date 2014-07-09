#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""Wrapper on top of the Logger for logging QuickSchools API requests"""

import logging
import json
import sys
import random
import os
import traceback
import syslog

QS_INFO = 35
LOG_SENDER = 'QS API'
has_been_configured = False
file_out = False
silent = False


def config(sender, print_only=False, log_filename=None):
    """mirrors Logging.basicConfig(), especially setting the output stream
    sender should be sender's __file__
    file will be based on sender's name unless log_filename is specified
    """
    global has_been_configured
    global file_out

    file_out = silent
    # for logging INFO events while ignoring usual INFO level logs
    logging.addLevelName(QS_INFO, 'QS INFO')

    log_format = '%(levelname)s - %(message)s'
    log_path = filename(sender, log_filename)

    if print_only:
        logging.basicConfig(
            format=log_format, level=QS_INFO)
    else:
        logging.basicConfig(
            format=log_format, level=QS_INFO, filename=log_path)
        print("Logging to file:\n{}".format(log_path))

    syslog.openlog(LOG_SENDER)
    has_been_configured = True


def info(description, data, is_response=False, is_request=False, cc_print=False):
    """info level log messages, logs to syslog and default output stream"""
    if not should_log(): return
    check_config()
    log_message = format_for_log(description, data, is_request, is_response)
    syslog.syslog(syslog.LOG_INFO, log_message)
    logging.log(QS_INFO, log_message)
    maybe_print(log_message, cc_print)


def warning(description, data, is_response=False, is_request=False, cc_print=True):
    """same as info, but warning level"""
    if not should_log(): return
    check_config()
    log_message = format_for_log(description, data, is_request, is_response)
    syslog.syslog(syslog.LOG_ERR, log_message)
    logging.warning(log_message)
    maybe_print(log_message, cc_print)


def error(description, data, is_response=False, is_request=False, cc_print=True):
    """same as info, but error level"""
    if not should_log(): return
    check_config()
    log_message = format_for_log(description, data, is_request, is_response)
    syslog.syslog(syslog.LOG_ERR, log_message)
    logging.error(log_message)
    maybe_print(log_message, cc_print)


def critical(description, data, is_request=False, is_response=False):
    """same as info, but critical and also prints stack trace, log message, and then exits execution"""
    if not should_log(): return
    check_config()
    log_message = "CRITICAL:\n{}".format(
        format_for_log(description, data, is_request, is_response))

    syslog.syslog(syslog.LOG_CRIT, log_message)
    logging.critical(log_message)
    traceback.print_stack()
    sys.exit(log_message)


def error_or_critical(description, data, is_critical, is_request=False, is_response=False):
    """convenience method to trigger error or critical message based on is_critical param"""
    if is_critical:
        critical(description, data, is_request=is_request, is_response=is_response)
    else:
        error(description, data, is_request=is_request, is_response=is_response)


def check_config():
    """Check the config and do any necessary config.
    Return whether or not to log.
    """
    if not has_been_configured:
        config(os.getcwd(), print_only=True)
    return silent

def should_log():
    """Decide whether or not anything should be logged when a call is made"""
    return not silent

def out_is_file():
    """Tells whether the output is to file or stdout"""
    return file_out

def silence():
    """Silence all log output, even everything is all configured."""
    global silent
    silent = True

def unsilence():
    global silent
    silent = False


def maybe_print(log_message, cc_print):
    if cc_print and out_is_file():
        print '\n' + log_message


def format_for_log(description, data, is_request, is_response):
    """formats all log messages to be uniform for output and include all info."""
    description += " - RESPONSE" if is_response else ''
    description += " - REQUEST" if is_request else ''
    description += ('\n{}'.format(json.dumps(data, indent=4, sort_keys=True))
        if data else '')
    return description


def filename(path, filename):
    """Create and return a unique filename in a subdirectory called "logs".
    Subdirectory is in either path param's os cwd.
    If there's a path param, includes the sender's name (e.g. download.py).
    Filename has precedence for log filename unless None
    """
    if path:
        log_path = path if os.path.isdir(path) else os.path.dirname(path)
    else:
        log_path = os.getcwd()
    log_path += '/logs'
    if not os.path.exists(log_path):
        os.mkdir(log_path)

    fileid = filename
    if not filename:
        fileid = os.path.splitext(os.path.basename(path))[0] if not os.path.isdir(path) else 'API'

    return  '{}/{} {}.log'.format(log_path, fileid, random.randint(1, 999))
