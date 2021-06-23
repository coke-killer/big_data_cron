from django.db import models
from watch_dog_app.models import ProjectsInfo


class DbscriptBuildingManager(models.Manager):
    @staticmethod
    def create_dbscript(dbscript_name, dbscript_version, dbscript_creatime, dbscript_status, dbscript_creater,
                        dbscript_information, dbscript_root, dbscript_timeset, dbscript_project_id):
        dbsc = DbscriptBuilding(dbscript_name=dbscript_name, dbscript_version=dbscript_version,
                                dbscript_creatime=dbscript_creatime, dbscript_status=dbscript_status,
                                dbscript_creater=dbscript_creater, dbscript_information=dbscript_information,
                                dbscript_root=dbscript_root, dbscript_timeset=dbscript_timeset,
                                dbscript_project_id=dbscript_project_id)
        dbsc.save()
        return dbsc


# 定时脚本类
class DbscriptBuilding(models.Model):
    # 定时脚本名称
    dbscript_name = (models.CharField(max_length=50))
    # 脚本版本
    dbscript_version = (models.CharField(max_length=10))
    # 创建时间
    dbscript_creatime = (models.DateField())
    # 脚本运行标志位
    dbscript_status = (models.BooleanField(default=False))
    # 创建人
    dbscript_creater = (models.CharField(max_length=20))
    # 脚本简介
    dbscript_information = (models.CharField(max_length=200))
    # 脚本存储路径
    dbscript_root = (models.CharField(max_length=100))
    # 脚本作用时间段和脚本运行频率
    dbscript_timeset = (models.CharField(max_length=50))
    # 一对多关系定义,工程和脚本表的关系为一对多，所以属性定义在脚本模型类中
    dbscript_project = models.ForeignKey(ProjectsInfo, on_delete=models.CASCADE)

    class Meta:
        db_table = 'wda_dbscript_building'
