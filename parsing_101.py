import re

def non_basedir_command(line):
    '''
    Function that will return the current working
    directory of line.
    '''
    pattern = re.compile('cwd:([\/|\w]+) filename')
    cwd = re.findall(pattern, line)
    if len(cwd) == 0:
        return []
    else:
        return cwd[0] 

def process(line, usr_cmds):
    ''' 
    Function to process user commands. Currently
    just adds command to list
    '''
    pattern = re.compile('filename:.+\]: (.+)')
    cmd = pattern.search(line)
    usr_cmds.append(cmd)

def parse(fname):
    '''
    Parses through entire authlog file.
    '''
    usr_cmds = []
    with open(fname) as file:
        #loop through each line
        line = file.readline()
        while line:
            # If cwd is in line and is not from '/' process line
            cwd = non_basedir_command(line)
            if cwd != [] and cwd != '/':
                process(line, usr_cmds)
            line = file.readline()

    return usr_cmds
