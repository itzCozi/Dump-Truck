import os, sys
import signal
import time


class files:
  hexdump = f'{os.getcwd()}/hexdump.txt'.replace('\\', '/')
  tempdump = f'{os.getcwd()}/tempdump.txt'.replace('\\', '/')
  libdump = f'{os.getcwd()}/libdump.txt'.replace('\\', '/')
  processdump = f'{os.getcwd()}/processdump.txt'.replace('\\', '/')


class utility:

  def processPath(process):
    # Returns the running processes path
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
    # Outputs all running processes
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
    # Gets a process name from PID
    output = os.popen(f'tasklist /svc /FI "PID eq {PID}"').read()
    for line in str(output).splitlines():
      if '.exe' in line:
        index = line.find('.exe')
        diffrence = line[0:index]
        retvalue = f'{diffrence}.exe'
        return retvalue

  def getPID(process):
    # Returns a process PID from name
    if '.exe' in process:
      process = process.replace('.exe', '')
    try:
      retlist = []
      output = os.popen(f'powershell ps -Name {process}').read()
      for line in output.splitlines():
        if '(' in line:
          index = line.find('  SI ')
        if '.' in line:
          diffrence = line[0:index]
          list = diffrence.split('  ')
          retlist.append(list[-1].replace(' ', ''))
      return retlist
    except Exception:
      print(f'ERROR: Cannot find process {process}.')
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
print-running (N/A): Prints all of the running processes. 
folderdump (dir): Dumps all files in a folder to output folder.
kill-process (name): Kills the given process if detected running.
libdump (N/A): Finds all .dll files and writes them to libdump.
tempdump (N\A): Dumps all temp files to a .txt file.
rm-running (process): Kills and deletes given running process.
find-process (process): Prints the path of the given executable.
getPID (name): Outputs the PID of the input if running as process.
getNAME (PID): Returns the name of given process ID.

Below is an example of how to pass arguments to dump-truck:

  ____________Python Version____________
    python dump-truck.py hexdump TF2.exe
    python dump-truck.py libdump
    python dump-truck.py getNAME 8294
    python dump-truck.py folderdump Desktop/JTSP
    python dump-truck.py rm-running steam.exe
    python dump-truck.py getPID firefox
    python dump-truck.py get-running
    python dump-truck.py print-running
    python dump-truck.py kill-process discord
    python dump-truck.py find-process notepad++
    python dump-truck.py tempdump
  
  ____________EXE Version____________
    ./dump-truck hexdump spotify.exe
    ./dump-truck libdump
    ./dump-truck getNAME 8294
    ./dump-truck folderdump Desktop/JTSP
    ./dump-truck rm-running DyKnow.exe
    ./dump-truck getPID code
    ./dump-truck get-running
    ./dump-truck print-running
    ./dump-truck kill-process chrome
    ./dump-truck find-process notepad++
    ./dump-truck tempdump
    ''')
    sys.exit(0)

  def hexdump(file):
    # Creates a hex dump from given file
    if not os.path.exists(file):
      print(f'ERROR: Dumper cannot find file {file}.')
      sys.exit(1)

    with open(file, 'rb') as f:
      content = f.read()
      bytes = 0
      line = []
    f.close()

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
      out.close()
      print(f'Hexdump created on {file} at {files.hexdump}.')

  def tempdump():  # Add to (Commands&Arguments) wiki
    # Dumps all files in temp directorys
    win_files = []
    user_files = []
    win_temp = 'C:/Windows/Temp'
    user_temp = f'C:/Users/{os.getlogin()}/AppData/Local/Temp'
    for wr, wd, wf in os.walk(win_temp):
      for winfile in wf:
        foo = f'{wr}/{winfile}'
        win_files.append(foo)
    for ur, ud, uf in os.walk(user_temp):
      for tempfile in uf:
        bar = f'{ur}/{tempfile}'
        user_files.append(bar)

    with open(files.tempdump, 'a') as out:
      for file in win_files:
        out.write(f'{file}\n'.replace('\\', '/'))
      for file2 in user_files:
        out.write(f'{file2}\n'.replace('\\', '/'))
      out.close()
      print(f'Tempdump created at {files.tempdump}.')

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
        out.close()
        print(f'Library dump created for {base_dir} at {files.libdump}.')
    except Exception as e:
      print(f'ERROR: An unknown error was encountered. \n{e}\n')
      sys.exit(1)

  def folderdump(folder):
    # Gets all files in given folder and dumps them
    if not os.path.exists(folder):
      print(f'ERROR: Dumper cannot find directory {folder}.')
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
        manifest = f'{output_dir}/MANIFEST'

        with open(manifest, 'a') as log:
          log.write(f'{file}\n')
        log.close()

        if file.endswith('.exe') or file.endswith('.dll'):
          commands.hexdump(file_path)
        elif 'LICENSE' in file:
          license = file_path
          with open(license, 'r') as f1:
            l_content = f1.read()
          f1.close()
          open(f'{output_dir}/LICENSE', 'w').write(l_content)
        elif 'README' in file:
          readme = file_path
          with open(readme, 'r') as f2:
            r_content = f2.read()
          f2.close()
          open(f'{output_dir}/README.md', 'w').write(r_content)
    print(f'Dumped folder and created output at {output_dir}.')

  def removeRunning(process):
    # Kills a running process and then deletes it
    if not '.exe' in process:
      process = f'{process}.exe'
    proc_path = utility.processPath(process)

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
          out.close()
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
    try:
      if __file__.endswith('.py'):
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]
      if __file__.endswith('.exe'):
        arg1 = sys.argv[0]
        arg2 = sys.argv[1]
    except:
      pass

    try:
      if arg1 == 'help':
        commands.help()
        sys.exit(0)
      elif arg1 == 'hexdump':
        try:
          commands.hexdump(arg2)
          sys.exit(0)
        except Exception as e:
          if not os.path.exists(arg2):
            print(f'ERROR: Dumper cannot find {arg2} in file-system.')
            sys.exit(1)
          else:
            print(f'ERROR: An unknown error was encountered. \n{e}\n')
            sys.exit(1)
      elif arg1 == 'tempdump':
        try:
          commands.tempdump()
          sys.exit(0)
        except Exception as e:
          print(f'ERROR: An unknown error was encountered. \n{e}\n')
          sys.exit(1)
      elif arg1 == 'libdump':
        try:
          commands.libdump()
          sys.exit(0)
        except Exception as e:
          print(f'ERROR: An unknown error was encountered. \n{e}\n')
          sys.exit(1)
      elif arg1 == 'folderdump':
        try:
          commands.folderdump(arg2)
          sys.exit(0)
        except FileExistsError:
          print('ERROR: A dumpfolder already exists in this directory.')
          sys.exit(1)
        except Exception as e:
          print(f'ERROR: An unknown error was encountered. \n{e}\n')
          sys.exit(1)
      elif arg1 == 'rm-running':
        try:
          commands.removeRunning(arg2)
          sys.exit(0)
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
      elif arg1 == 'print-running':
        try:
          print(utility.getProcesses())
          sys.exit(0)
        except Exception as e:
          print(f'ERROR: An unknown error was encountered. \n{e}\n')
          sys.exit(1)
      elif arg1 == 'kill-process' or 'kill':
        try:
          commands.killProcess(arg2)
          sys.exit(0)
        except Exception as e:
          print(f'ERROR: A runtime error occurred, is the process running? \n{e}\n')
          sys.exit(1)
      elif arg1 == 'find-process':
        try:
          print(utility.processPath(arg2))
          sys.exit(0)
        except Exception as e:
          print(f'ERROR: A runtime error occurred, is the process running? \n{e}\n')
          sys.exit(1)
      elif arg1 == 'getPID':
        try:
          print(utility.getPID(arg2))
          sys.exit(0)
        except Exception as e:
          print(f'ERROR: Did you input the correct process name after the command. \n{e}\n')
          sys.exit(1)
      elif arg1 == 'getNAME':
        try:
          print(utility.nameFinder(arg2))
          sys.exit(0)
        except Exception as e:
          print(f'ERROR: Did you enter a valid PID after the command. \n{e}\n')
          sys.exit(1)

      else:
        print('ERROR: The given argument is not recognized, try the help command.')
        sys.exit(1)

    except PermissionError:
      print('ERROR: Action executed without required permissions.')
      sys.exit(1)
    except UnboundLocalError:
      print('ERROR: Please try again with a valid argument.')
      sys.exit(1)
    except Exception as e:
      print(f'ERROR: An unknown error was encountered. \n{e}\n')
      sys.exit(1)


if __name__ == '__main__':
  driver.argHandler()
else:
  print(f'ERROR: You cannot import {__file__}.')
  sys.exit(1)
