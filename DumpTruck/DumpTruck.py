# TODO: Add a folder dump command where a file will be created
# with the .dll's, .exe's, A license (if found), A readme(if found) and exe hex-dumps
# TODO: Add completion and other outputs to the console
# TODO: Create a help command
import os, sys
import signal


class files:
  hexdump = f'{os.getcwd()}/hexdump.txt'
  libdump = f'{os.getcwd()}/libdump.txt'
  processdump = f'{os.getcwd()}/processdump.txt'


class utility:

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
      print(f'ERROR: An unknown error was encountered. \n{e}\n')
      sys.exit(1)


class commands:

  def hexdump(file):
    # Creates a hex dump from given file
    if not os.path.exists(file):
      print(f'ERROR: Dumper cannot find file {file}.')
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

  def dumplibs():
    # Gets all .dll files on base_dir
    try:
      dll_list = []
      base_dir = 'C:'
      for r, d, f in os.walk(base_dir):
        for file in f:
          if file.endswith('.dll'):
            item = f'{r}/{file}'
            dll_list.append(item)

      with open(files.libdump, 'a') as out:
        for item in dll_list:
          out.write(f'{item}\n')
    except Exception as e:
      print(f'ERROR: An unknown error was encountered. \n{e}\n')
      sys.exit(1)
      
  def getProcesses():
    # Get all running processes
    try:
      iterated = []
      retlist = []
      output = os.popen('wmic process get description, processid').read()
      print('Please wait this may take a moment...')
      for line in output.splitlines():
        if '.exe' in line:
          index = line.find('.exe')
          item = line[index + 5:].replace(' ', '')
          itemobj = utility.nameFinder(item)
          if not itemobj in iterated:
            retlist.append(itemobj)
          else:
            continue
          iterated.append(itemobj)
        else:
          output = output.replace(line, '')
    
      for item in retlist:
        if item == None:
          retlist.remove(item)
        else:
          with open(files.processdump, 'a') as out:
            out.write(f'{item}\n')
    except Exception as e:
      print(f'ERROR: An unknown error was encountered. \n{e}\n')
      sys.exit(1)

  def killProcess(name):
    if name.endswith('.exe'):
      name = name.replace('.exe', '')
    PIDlist = utility.getPID(name)
    for PID in PIDlist:
      try:
        os.kill(int(PID), signal.SIGTERM)
      except Exception as e:
        print(f'ERROR: An unknown error was encountered. \n{e}\n')
        sys.exit(1)


class driver:

  def argHandler():
    if __file__.endswith('.py'):
      try:
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]
        arg3 = sys.argv[3]
      except:
        pass
    if __file__.endswith('.exe'):
      try:
        arg1 = sys.argv[0]
        arg2 = sys.argv[1]
        arg3 = sys.argv[2]
      except:
        pass

    if arg1 == 'hexdump':
      try:
        commands.hexdump(arg2)
      except Exception as e:
        if not os.path.exists(arg2):
          print(f'ERROR: Dumper cannot find {arg2} in file-system.')
          sys.exit(0)
        else:
          print(f'ERROR: An unknown error was encountered. \n{e}\n')
          sys.exit(1)
    elif arg1 == 'dumplibs':
      try:
        commands.dumplibs()
        sys.exit(0)
      except Exception as e:
        print(f'ERROR: An unknown error was encountered. \n{e}\n')
        sys.exit(1)
    elif arg1 == 'get-processes':
      try:
        commands.getProcesses()
        sys.exit(0)
      except Exception as e:
        print(f'ERROR: An unknown error was encountered. \n{e}\n')
        sys.exit(1)
    elif arg1 == 'kill-process':
      try:
        commands.killProcess(arg2)
        sys.exit(0)
      except Exception as e:
        print(f'ERROR: A runtime error occurred, is the process running? \n{e}\n')
        sys.exit(1)

    else:
      print('ERROR: The given argument is not recognized, try the help command.')
      sys.exit(1)


if __name__ == '__main__':
  try:
    driver.argHandler()
  except PermissionError:
    print('ERROR: Action executed without required permissions.')
    sys.exit(1)
  except IndexError:
    print('ERROR: No were arguments passed to dumper, check help command.')
    sys.exit(1)
  except Exception as e:
    raise Exception(f'ERROR: An unknown error was encountered. \n{e}\n')

else:
  print(f'ERROR: You cannot import {__file__}.')
  sys.exit(1)
