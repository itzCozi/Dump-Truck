# NOTE: This file is made for importing from so a user can operate the dump-truck commands through python code.

import os, sys
import signal
import time


class files:
  hexdump = f'{os.getcwd()}/hexdump.txt'.replace('\\', '/')
  libdump = f'{os.getcwd()}/libdump.txt'.replace('\\', '/')
  processdump = f'{os.getcwd()}/processdump.txt'.replace('\\', '/')


def processPath(process):
  if '.exe' in process:
    process = process[:-4]
  try:
    out = os.popen(f'powershell (Get-Process {process}).Path').read()
    for line in out.splitlines():
      if os.path.exists(line):
        return line
  except Exception as e:
    raise Exception(f'ERROR: An unknown error was encountered. \n{e}\n')
    sys.exit(1)


def getProcesses():
  try:
    iterated = set()
    retlist = []
    output = os.popen('wmic process get description, processid').read()

    for line in output.splitlines():
      if '.exe' in line:
        index = line.find('.exe')
        item = line[index + 5:].replace(' ', '')
        itemobj = nameFinder(item)
        if itemobj and itemobj not in iterated:
          retlist.append(itemobj)
          iterated.add(itemobj)

    return retlist
  except Exception as e:
    raise Exception(f'ERROR: An unknown error was encountered. \n{e}\n')
    sys.exit(1)


def nameFinder(PID):
  output = os.popen(f'tasklist /svc /FI "PID eq {PID}"').read()
  for line in str(output).splitlines():
    if '.exe' in line:
      index = line.find('.exe')
      diffrence = line[0:index]
      retvalue = f'{diffrence}.exe'
      return retvalue


def getPID(process):
  try:
    retlist = []
    output = os.popen(f'powershell ps -Name {process}').read()
    for line in output.splitlines():
      if '.' in line:
        index = line.find('  1 ')
        diffrence = line[0:index]
        list = diffrence.split('  ')
        retlist.append(list[-1].replace(' ', ''))
    return retlist
  except Exception as e:
    raise Exception(f'ERROR: An unknown error was encountered. \n{e}\n')
    sys.exit(1)


def hexdump(file):
  # Creates a hex dump from given file
  if not os.path.exists(file):
    raise FileNotFoundError(f'ERROR: Dumper cannot find file {file}.')
    sys.exit(1)

  with open(file, 'rb') as f:
    content = f.read()
    bytes = 0
    line = []

  with open(files.hexdump, 'a') as out:
    for byte in content:
      bytes += 1
      line.append(byte)
      # For every byte print 2 hex digits without the x
      out.write('{0:0{1}x} '.format(byte, 2))
      if bytes % 16 == 0:
        out.write(' |  ')
        for b in line:
          if b >= 32 and b <= 126:
            out.write(chr(b))
          else:
            out.write('*')
        line = []
        out.write('\n')


def libdump():
  # Gets all .dll files on base_dir
  try:
    dll_list = []
    base_dir = 'C:'
    for r, d, f in os.walk(base_dir):
      r = r.replace('C:', 'C:/')
      for file in f:
        if file.endswith('.dll'):
          item = f'{r}/{file}'.replace('\\', '/')
          dll_list.append(item)

    return dll_list
  except Exception as e:
    raise Exception(f'ERROR: An unknown error was encountered. \n{e}\n')
    sys.exit(1)


def folderdump(folder):
  # Gets all files in folder and dumps them
  if not os.path.exists(folder):
    raise FileNotFoundError(f'ERROR: Dumper cannot find directory {folder}.')
    sys.exit(1)
  output_dir = f'{os.getcwd()}/folderdump'
  os.mkdir(output_dir)

  for r, d, f in os.walk(folder):
    for file in f:
      # Hexdump files are stored in a folder named after the source file
      if file.endswith('.exe') or file.endswith('.dll'):
        os.mkdir(f'{output_dir}/{file}')
      files.hexdump = f'{output_dir}/{file}/hexdump.txt'
      file_path = f'{r}/{file}'.replace('\\', '/')

      if file.endswith('.exe') or file.endswith('.dll'):
        hexdump(file_path)
      elif 'LICENSE' in file:
        license = file_path
        with open(license, 'r') as f1:
          l_content = f1.read()
        open(f'{output_dir}/LICENSE', 'w').write(l_content)
      elif 'README' in file:
        readme = file_path
        with open(readme, 'r') as f2:
          r_content = f2.read()
        open(f'{output_dir}/README.md', 'w').write(r_content)


def removeRunning(process):
  # Kills a running process and then deletes it
  proc_path = processPath(process)
  if not '.exe' in process:
    process = f'{process}.exe'
  else:
    try:
      try:
        killProcess(process)
      except:
        pass
      time.sleep(0.5)
      os.remove(proc_path)
    except Exception as e:
      raise Exception(f'ERROR: An unknown error was encountered. \n{e}\n')
      sys.exit(1)


def killProcess(name):
  # Ends given process
  if name.endswith('.exe'):
    name = name.replace('.exe', '')
  PIDlist = getPID(name)
  for PID in PIDlist:
    try:
      os.kill(int(PID), signal.SIGTERM)
    except Exception as e:
      raise Exception(f'ERROR: An unknown error was encountered. \n{e}\n')
      sys.exit(1)
