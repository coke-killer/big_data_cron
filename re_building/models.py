from django.db import models
from watch_dog_app.models import ProjectsInfo


# Create your models here.
# 定时算法管理类
class ReportBuildingManager(models.Manager):
    @staticmethod
    def create_report(report_name, report_version, report_creatime, report_status, report_creater,
                      report_information, report_root, report_timeset, report_project_id):
        repo = ReportBuilding(report_name=report_name, report_version=report_version,
                              report_creatime=report_creatime, report_status=report_status,
                              report_creater=report_creater, report_information=report_information,
                              report_root=report_root, report_timeset=report_timeset,
                              report_project_id=report_project_id)
        repo.save()
        return repo


# 定时算法类
class ReportBuilding(models.Model):
    # 定时算法名称
    report_name = (models.CharField(max_length=50))
    # 算法版本
    report_version = (models.CharField(max_length=10))
    # 创建时间
    report_creatime = (models.DateField())
    # 脚本运行标志位
    report_status = (models.BooleanField(default=False))
    # 创建人
    report_creater = (models.CharField(max_length=20))
    # 算法简介
    report_information = (models.CharField(max_length=200))
    # 算法存储路径
    report_root = (models.CharField(max_length=100))
    # 算法作用时间段和脚本运行频率
    report_timeset = (models.CharField(max_length=50))
    # 一对多关系定义,工程和脚本表的关系为一对多，所以属性定义在脚本模型类中
    report_project = models.ForeignKey(ProjectsInfo, on_delete=models.CASCADE)

    class Meta:
        db_table = 'wda_report_building'
