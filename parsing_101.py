import re
import os
from collections import defaultdict 

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
    cmd = pattern.search(line).groups(0)[0]
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
def is_reject(fname):
    with open(fname) as fp:
        line = fp.readline()
        return line != "DROP"
def count_first_command(cmd_lst, cnt_dict):
    for line in cmd_lst:
        cnt_dict[line.split()[0]] = cnt_dict.get(line.split()[0], 0) + 1
    return cnt_dict
def groupby_first_command(cmd_lst, grp_dict):
    for line in cmd_lst:
        grp_dict[line.split()[0]].append(line)
    return grp_dict

drop_dic = {}
reject_dic = {}
drop_group = defaultdict(list)
reject_group = defaultdict(list)
for fname in os.listdir('/root/data/101_logs/'):
    if os.path.exists('/root/data/101_logs/' + fname + '/Authlog'):
        tmp_lst = parse('/root/data/101_logs/' + fname + '/Authlog')
        if is_reject('/root/data/101_logs/marker'):
            reject_dic = count_first_command(tmp_lst, reject_dic)
            reject_group = groupby_first_command(tmp_lst, reject_group)
        else:
            drop_dic = count_first_command(tmp_lst, drop_dic)
            drop_group = groupby_first_command(tmp_lst, drop_group)
for fname in os.listdir('/root/data/102_logs/'):
    if os.path.exists('/root/data/102_logs/' + fname + '/Authlog'):
        tmp_lst = parse('/root/data/102_logs/' + fname + '/Authlog')
        if is_reject('/root/data/102_logs/marker'):
            reject_dic = count_first_command(tmp_lst, reject_dic)
            reject_group = groupby_first_command(tmp_lst, reject_group)
        else:
            drop_dic = count_first_command(tmp_lst, drop_dic)
            drop_group = groupby_first_command(tmp_lst, drop_group)

