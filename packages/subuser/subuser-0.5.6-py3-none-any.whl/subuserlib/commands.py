# -*- coding: utf-8 -*-
"""
This module helps us figure out which subuser subcommands can be called.
"""

#external imports
import os
#internal imports
import subuserlib.executablePath
import subuserlib.paths

def getBuiltIn():
  """
  Get a list of the names of the built in subuser commands.
  """
  try:
    commands = set(os.listdir(subuserlib.paths.getSubuserCommandsDir()))
    return [command[8:] for command in commands if command.startswith("subuser-") and not command.endswith("~")] # Filter out the files that don't start with subuser- and remove the "subuser-" prefixes.
  except OSError:
    return []

def getExternal():
  """
  Return the list of "external" subuser commands.  These are not built in commands but rather stand alone executables which appear in the user's $PATH and who's names start with "subuser-"
  """
  def isPathToCommand(path):
    directory, executableName = os.path.split(path)
    return executableName.startswith("subuser-")
  externalCommandPaths = subuserlib.executablePath.queryPATH(isPathToCommand)
  externalCommands = []
  subuserPrefixLength=len("subuser-")
  for externalCommandPath in externalCommandPaths:
    commandDir, executableName = os.path.split(externalCommandPath)
    commandName = executableName[subuserPrefixLength:]
    externalCommands.append(commandName)
  return list(set(externalCommands)) # remove duplicate entries

def getCommands():
  """
  Returns a list of commands that may be called by the user.
  """
  return list(set(getBuiltIn() + getExternal()))

def getPath(command):
  builtInCommandPath = os.path.join(subuserlib.paths.getSubuserCommandsDir(),"subuser-" + command)
  if os.path.exists(builtInCommandPath):
    return (builtInCommandPath)
  else:
    externalCommandPath = subuserlib.executablePath.which("subuser-"+command)
    if externalCommandPath:
      return externalCommandPath
    else:
      return subuserlib.executablePath.which("subuser-"+command)
