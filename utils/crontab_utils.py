# __author__: "Yu Dongyue"
# date: 2021/6/3
from crontab import CronTab


# 创建当前用户的crontab，当然也可以创建其他用户的，但得有足够权限
# 增加任务
def add_task(command, cron_exp, comment):
    """
    :param command: 需要定时运行的脚本 command='python3/tmp/pycharm_project_300/myTest.py'
    :param cron_exp: 设置任务执行周期，每两分钟执行一次 cron_exp='*/1****'
    :param comment: 定时任务名称 AL_name_id;DB_name_id;Re_name_id
    :return: None
    """
    cron = CronTab(user='root')
    job = cron.new(command=command, comment=comment)
    job.setall(cron_exp)
    cron.write()


# 删除任务
def del_task(job_name):
    del_cron = CronTab(user='root')
    iter = del_cron.find_comment(job_name)
    for job in iter:
        del_cron.remove(job)
    del_cron.write()


# 编辑一个任务
def update_task(job_name, new_command):
    cron = CronTab(user='root')
    iter_job = cron.find_comment(job_name)
    for job in iter_job:
        job.set_command(new_command)
    cron.write()


if __name__ == '__main__':
    del_task('db_ert.py_scr5_pro32')