import re
import os
from datetime import dateime
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

def get_timestamp(line):
    '''
    Takes line from Authlog and returns datetime object for the timestamp of the line
    '''  
    spl_arr = line.split()
    date_str = spl_arr[0] + ' ' + spl_arr[1] + ' ' + spl_arr[2]
    return datetime.strptime(date_str, '%b %d %H:%M:%S')

def is_disconnect(line):
    return "Disconnected from " in line

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
    start_time = None
    end_time = None
    usr_cmds = []
    with open(fname) as file:
        #loop through each line
        line = file.readline()
        while line:
            # Parse timestamp of first line
            if start_time is None:
                start_time = get_timestamp(line)

            # If cwd is in line and is not from '/' process line
            cwd = non_basedir_command(line)
            if cwd != [] and cwd != '/':
                process(line, usr_cmds)

            disconn = is_disconnect(line)
            if disconn:
                end_time = get_timestamp(line)

            line = file.readline()


    return usr_cmds, start_time, end_time

def is_reject(fname):
    with open(fname) as fp:
        line = fp.readline()
        return line != "REJECT\n"
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

rej_cnt = 0
drop_cnt = 0

rej_n_cmds = []
drop_n_cmds = []

rej_time = []
drop_time = []

for fname in os.listdir('/root/data/101_logs/'):
    if os.path.exists('/root/data/101_logs/' + fname + '/Authlog'):
        tmp_lst, tmp_st, tmp_end = parse('/root/data/101_logs/' + fname + '/Authlog')
        tmp_diff = None if tmp_end is None else (tmp_end - tmp_st).seconds
        if is_reject('/root/data/101_logs/' + fname + '/marker'):
            reject_dic = count_first_command(tmp_lst, reject_dic)
            reject_group = groupby_first_command(tmp_lst, reject_group)
            rej_n_cmds.append(len(tmp_lst))
            rej_cnt += 1
            rej_time.append(tmp_diff)
        else:
            drop_dic = count_first_command(tmp_lst, drop_dic)
            drop_group = groupby_first_command(tmp_lst, drop_group)
            drop_n_cmds.append(len(tmp_lst))
            drop_cnt += 1
            drop_time.append(tmp_diff)

for fname in os.listdir('/root/data/102_logs/'):
    if os.path.exists('/root/data/102_logs/' + fname + '/Authlog'):
        tmp_lst, tmp_st, tmp_end = parse('/root/data/102_logs/' + fname + '/Authlog')
        tmp_diff = None if tmp_end is None else (tmp_end - tmp_st).seconds
        if is_reject('/root/data/102_logs/' + fname + '/marker'):
            reject_dic = count_first_command(tmp_lst, reject_dic)
            reject_group = groupby_first_command(tmp_lst, reject_group)
            rej_n_cmds.append(len(tmp_lst))
            rej_cnt += 1
            rej_time.append(tmp_diff)
        else:
            drop_dic = count_first_command(tmp_lst, drop_dic)
            drop_group = groupby_first_command(tmp_lst, drop_group)
            drop_n_cmds.append(len(tmp_lst))
            drop_cnt += 1
            drop_time.append(tmp_diff)
