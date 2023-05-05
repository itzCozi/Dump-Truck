# TODO: Add arghandler and if __name__ == '__main__'
# TODO: Add a folder dump command where a file will be created 
# with the .dll's, .exe's, A license (if found), A readme(if found) and exe hex-dumps
# TODO: Add exceptions and sys.exit(1) and sys.exit(0)

import os, sys


class utility:
  
  def nameFinder(PID):
    output = os.popen(f'tasklist /svc /FI "PID eq {PID}"').read()
    for line in str(output).splitlines():
      if '.exe' in line:
        index = line.find('.exe')
        diffrence = line[0:index]
        retvalue = f'{diffrence}.exe'
        return retvalue
      
  def get_PID(process):
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
    with open(file, 'rb') as f:
      content = f.read()
      bytes = 0
      line = []

    with open('hexdump.txt', 'a') as out:
      for byte in content:
        bytes += 1
        line.append(byte)
        # For every byte print 2 hex digits without the x
        out.write('{0:0{1}x}'.format(byte, 2))

        if bytes % 16 == 0:
          out.write(' |  ')
          for b in line:
            if b >= 32 and b <= 126:
              out.write(chr(b))
            else:
              out.write('*')
          line=[]
          out.write('\n')

  def dumplibs():
    # Gets all .dll files on base_dir
    dll_list = []
    base_dir = 'C:'
    for r, d, f in os.walk(base_dir):
      for file in f:
        if file.endswith('.dll'):
          item = f'{r}/{file}'
          dll_list.append(item)

    with open('libdump.txt', 'a') as out:
      for item in dll_list:
        out.write(f'{item}\n')

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
          with open('processdump.txt', 'a') as out:
            out.write(f'{item}\n')
    except Exception as e:
      print(f'ERROR: An unknown error was encountered. \n{e}\n')
      sys.exit(1)

