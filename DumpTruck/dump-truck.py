# TODO: Test and read through folderdump on home PC
# TODO: Update help command's print statment
# TODO: Release PDLparse to twine after review
# TODO: Add repo banner from pintrest just find the image again
import os, sys
import signal
import time


class files:
  hexdump = f'{os.getcwd()}/hexdump.txt'
  libdump = f'{os.getcwd()}/libdump.txt'
  processdump = f'{os.getcwd()}/processdump.txt'


class utility:

  def processPath(process):
    if '.exe' in process:
      process = process[:-4]
    try:
      out = os.popen(f'powershell (Get-Process {process}).Path').read()
      for line in out.splitlines():
        if os.path.exists(line):
          return line
    except Exception as e:
      print(f'ERROR: An unknown error was encountered. \n{e}\n')
      sys.exit(1)

  def getProcesses():
    try:
      iterated = set()
      retlist = []
      output = os.popen('wmic process get description, processid').read()
      print('Please wait this may take a moment...')

      for line in output.splitlines():
        if '.exe' in line:
          index = line.find('.exe')
          item = line[index + 5:].replace(' ', '')
          itemobj = utility.nameFinder(item)
          if itemobj and itemobj not in iterated:
            retlist.append(itemobj)
            iterated.add(itemobj)

      return retlist
    except Exception as e:
      print(f'ERROR: An unknown error was encountered. \n{e}\n')
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
      print(f'ERROR: An unknown error was encountered. \n{e}\n')
      sys.exit(1)


class commands:

  def help():
    # Prints a lot of commands
    print(f'''
Command | Args | Description
----------------------------
help (N/A): Displays/outputs this menu to the console.
hexdump (file): Dumps the hex of given file to hexdump.
get-running (N/A): Records all running processes to processdump.
kill-process (name): Kills the given process if detected running.
libdump (N/A): Finds all .dll files and writes them to libdump.
rm-running (process): Kills and deletes given running process.

Below is an example of how to pass arguments to dump-truck:

  ____________Python Version____________
    python dump-truck.py hexdump TF2.exe
    python dump-truck.py libdump
    python dump-truck.py rm-running steam.exe
    python dump-truck.py get-running
    python dump-truck.py kill-process discord
  
  ____________EXE Version____________
    ./dump-truck hexdump spotify.exe
    ./dump-truck libdump
    ./dump-truck rm-running DyKnow.exe
    ./dump-truck get-running
    ./dump-truck kill-process chrome
    ''')

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
      print(f'Hexdump created on {file} at {files.hexdump}.')

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

      with open(files.libdump, 'a') as out:
        for item in dll_list:
          out.write(f'{item}\n')
        print(f'Library dump created for {base_dir} at {files.libdump}.')
    except Exception as e:
      print(f'ERROR: An unknown error was encountered. \n{e}\n')
      sys.exit(1)

  def folderdump(folder):
    # NEEDS TESTING ONCE HOME
    if not os.path.exists(folder):
      print(f'ERROR: Dumper cannot find directory {folder}.')
      sys.exit(1)
    output_dir = f'{os.getcwd()}/folderdump'
    os.mkdir(output_dir)

    for r, d, f in os.walk(folder):
      for file in f:
        os.mkdir(f'{output_dir}/{file}')
        files.hexdump = f'{output_dir}/{files.hexdump}'
        file_path = f'{r}/{file}'.replace('\\', '/')

        if '.exe' or '.dll' or '.pyc' in file:
          commands.hexdump(file_path)
        if 'LICENSE' or 'license' in file:
          license = file_path
        if 'README' or 'readme' in file:
          readme = file_path
    
    open(f'{output_dir}/LICENSE', 'w').write(open(license, 'r').read())
    open(f'{output_dir}/README.md', 'w').write(open(readme, 'r').read())

  def removeRunning(process):
    # Kills a running process and then deletes it
    proc_path = utility.processPath(process)
    if not '.exe' in process:
      process = f'{process}.exe'
    else:
      try:
        try:
          commands.killProcess(process)
        except:
          pass
        time.sleep(0.5)
        os.remove(proc_path)
      except Exception as e:
        print(f'ERROR: An unknown error was encountered. \n{e}\n')
        sys.exit(1)

  def getRunning():
    # Get all running processes
    try:
      iterated = set()
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
          iterated.add(itemobj)
        else:
          output = output.replace(line, '')

      for item in retlist:
        if item == None:
          retlist.remove(item)
        else:
          with open(files.processdump, 'a') as out:
            out.write(f'{item}\n')
      print(f'Running processes have been logged at {files.processdump}.')

    except Exception as e:
      print(f'ERROR: An unknown error was encountered. \n{e}\n')
      sys.exit(1)

  def killProcess(name):
    # Ends given process and prints completion
    if name.endswith('.exe'):
      name = name.replace('.exe', '')
    PIDlist = utility.getPID(name)
    for PID in PIDlist:
      try:
        os.kill(int(PID), signal.SIGTERM)
        print(f'Process {name} has been killed.')
      except Exception as e:
        print(f'ERROR: An unknown error was encountered. \n{e}\n')
        sys.exit(1)


class driver:

  def argHandler():
    # Made that dynamic arg handler yuhhh!
    if __file__.endswith('.py'):
      try:
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]
      except:
        pass
    if __file__.endswith('.exe'):
      try:
        arg1 = sys.argv[0]
        arg2 = sys.argv[1]
      except:
        pass

    try:
      if arg1 == 'help':
        commands.help()

      elif arg1 == 'hexdump':
        try:
          commands.hexdump(arg2)
        except Exception as e:
          if not os.path.exists(arg2):
            print(f'ERROR: Dumper cannot find {arg2} in file-system.')
            sys.exit(0)
          else:
            print(f'ERROR: An unknown error was encountered. \n{e}\n')
            sys.exit(1)
      elif arg1 == 'libdump':
        try:
          commands.libdump()
          sys.exit(0)
        except Exception as e:
          print(f'ERROR: An unknown error was encountered. \n{e}\n')
          sys.exit(1)
      elif arg1 == 'rm-running':
        try:
          if not arg2.endswith('.exe'):
            print(f'ERROR: To use rm-running you must pass a .exe file.')
            sys.exit(0)
          commands.removeRunning(arg2)
        except Exception as e:
          if not os.path.exists(arg2):
            print(f'ERROR: Dumper cannot find {arg2} in file-system.')
            sys.exit(0)
          else:
            print(f'ERROR: An unknown error was encountered. \n{e}\n')
            sys.exit(1)
      elif arg1 == 'get-running':
        try:
          commands.getRunning()
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

    except PermissionError:
      print('ERROR: Action executed without required permissions.')
      sys.exit(1)
    except UnboundLocalError:
      print('ERROR: Please try again with all required parameters.')
      sys.exit(1)
    except Exception as e:
      print(f'ERROR: An unknown error was encountered. \n{e}\n')


if __name__ == '__main__':
  driver.argHandler()
else:
  print(f'ERROR: You cannot import {__file__}.')
  sys.exit(1)
