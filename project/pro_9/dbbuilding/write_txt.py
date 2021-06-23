import time
with open("/root/cloud_projects/TITAN/project/pro_9/dbbuilding/output.txt", "a", encoding='utf-8') as f:
# with open(r"output.txt", "a", encoding='utf-8') as f:
    timeArray = time.localtime()
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    f.write('\n' + otherStyleTime)