import datetime

with open('/root/cloud_projects/TITAN/test_first', 'a+') as f:
    f.write('\nhello world')
    f.write(str(datetime.datetime.now()))