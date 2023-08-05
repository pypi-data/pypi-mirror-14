#!/usr/bin/env python
import logging
import subprocess
import sys

logging.getLogger().setLevel(logging.INFO)


def isMac():
  """Are we on mac?"""
  return 'darwin' == sys.platform


def isLin():
  """Are we on linux?"""
  return sys.platform.startswith('linux')


def isWin():
  """Are we on windows?"""
  return sys.platform == 'cygwin' or sys.platform.startswith('win')


class Rebooter():

  def __init__(self, operation='reboot', delay=False, reason=None, force=False):
    """Restarts / shutdowns system

    Args:
      operation - str; one of possible operations: rebobot / shutdown
      delay - int; delay in seconds; will not be executed on Mac OS X
      reason - str; reason why you conduct restart
      force - bool; force operatioon. Risky!
    """

    switches = []

    if operation not in ['reboot', 'shutdown']:
      raise Exception('Unrecognized operation.')

    if isWin():
      command = ['shutdown']
      if operation == 'reboot':
        command.append('/r')
      else:
        command.append('/s')
      if delay:
        command.append('/t')
        command.append(str(delay))
      if reason is not None:
        command.append('/c "%s"' % reason)
      if force:
        command.append('/force')
    elif isMac():
      # On Mac use AppleScript, as shutdown requires root
      if operation == 'reboot':
        operation = 'restart'
      else:
        operation = 'shut down'
      osascript = 'tell app "Finder" to %s' % operation
      command = ['osascript', '-e', osascript]
    elif isLin():
      if force:
        command = ['reboot', '-f']
        if command == ['shutdown']:
          command.append('-p')
      else:
        command = ['shutdown']
        if operation == 'reboot':
          command.append('-r')
        else:
          command.append('-h')
        if not delay:
          command.append('now')
          command.append(reason)
        else:
          # Appending reason as another list item, will spawn:
          # 'Failed to parse time specification'
          command.append('-t %i sec %s' % (delay, reason))
    else:
      raise Exception('Unrecognized system.')

    logging.info("Will restart/shutdown machine using command: '%s'" % command)
    try:
      subprocess.check_output(command, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
      print e.output
      if e.output.find('root') != -1:
        logging.warning("To make it work on Linux, 'sudo chmod u+s /sbin/shutdown'"
                        "'sudo chmod u+s /sbin/reboot' or modify sudoers file")