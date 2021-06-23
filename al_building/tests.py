import os
from utils import check_utils

if __name__ == '__main__':
    val = os.popen('crontab -l')
    s = [x.strip() for x in val if x.strip() != '']
    a = []
    for i in s:
        if i.split('#')[1].__contains__('pro10') and i.split('#')[1].__contains__(' al'):
            a.append(i)
