from django.db import models
from watch_dog_app.models import ProjectsInfo


# Create your models here.
# 定时算法管理类
class AlgorithmBuildingManager(models.Manager):
    @staticmethod
    def create_algorithm(algorithm_name, algorithm_version, algorithm_creatime, algorithm_status, algorithm_creater,
                         algorithm_information, algorithm_root, algorithm_timeset, algorithm_project_id):
        algo = AlgorithmBuilding(algorithm_name=algorithm_name, algorithm_version=algorithm_version,
                                 algorithm_creatime=algorithm_creatime, algorithm_status=algorithm_status,
                                 algorithm_creater=algorithm_creater, algorithm_information=algorithm_information,
                                 algorithm_root=algorithm_root, algorithm_timeset=algorithm_timeset,
                                 algorithm_project_id=algorithm_project_id)
        algo.save()
        return algo


# 定时算法类
class AlgorithmBuilding(models.Model):
    # 定时算法名称
    algorithm_name = (models.CharField(max_length=50))
    # 算法版本
    algorithm_version = (models.CharField(max_length=10))
    # 创建时间
    algorithm_creatime = (models.DateField())
    # 脚本运行标志位
    algorithm_status = (models.BooleanField(default=False))
    # 创建人
    algorithm_creater = (models.CharField(max_length=20))
    # 算法简介
    algorithm_information = (models.CharField(max_length=200))
    # 算法存储路径
    algorithm_root = (models.CharField(max_length=100))
    # 算法作用时间段和脚本运行频率
    algorithm_timeset = (models.CharField(max_length=50))
    # 一对多关系定义,工程和脚本表的关系为一对多，所以属性定义在脚本模型类中
    algorithm_project = models.ForeignKey(ProjectsInfo, on_delete=models.CASCADE)

    class Meta:
        db_table = 'wda_algorithm_building'
