from django.db import models
import datetime


class ProjectInfoManager(models.Manager):
    @staticmethod
    def create_proj(project_name, project_information, project_creatime, project_creater, project_root,
                    project_otherkey=None):
        proj = ProjectsInfo(project_name=project_name, project_information=project_information,
                            project_creatime=project_creatime, project_creater=project_creater,
                            project_root=project_root,
                            project_otherkey=project_otherkey)
        proj.save()
        return proj


# Create your models here.
class ProjectsInfo(models.Model):
    # 工程信息类
    # 工程名称
    project_name = (models.CharField(max_length=50))
    # 工程简介
    project_information = (models.CharField(max_length=200))
    # 工程创建时间
    project_creatime = (models.DateField())
    # 工程创建人
    project_creater = (models.CharField(max_length=20))
    # 工程根路径
    project_root = (models.CharField(max_length=100))
    # 工程其他信息（预留，避免后续修改类  XXX:XXX,XXX:XXX,XXX:XXX,）
    project_otherkey = (models.CharField(max_length=3000, null=True, blank=True))

    class Meta:
        db_table = 'wda_projects_info'
