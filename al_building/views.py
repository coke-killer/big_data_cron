# __author__: "Yu Dongyue"
# date: 2021/6/2
from django.shortcuts import render
from django.views.generic import View
from al_building.models import AlgorithmBuilding, AlgorithmBuildingManager
from django.shortcuts import render, redirect, HttpResponse, reverse
from utils import check_utils as util
from utils import crontab_utils as cron
from watch_dog_app.models import ProjectsInfo
import datetime
import os
from django.core.paginator import Paginator


# Create your views here.
class InsertAlgorithmView(View):
    def get(self, request, pj_id):
        return render(request, 'al_building/insert_algorithm.html', {'pj_id': pj_id})

    def post(self, request, pj_id):
        algorithm_file = request.FILES['algorithm_file']
        pj_id = request.POST.get('pj_id')
        name = algorithm_file.name
        version = util.remove_spaces(request.POST.get('version'))
        information = util.remove_spaces(request.POST.get('information'))
        creater = util.remove_spaces(request.POST.get('creater'))
        timeset = request.POST.get('timeset')
        if not all([name, version, information, creater, timeset]):
            return render(request, 'al_building/insert_algorithm.html', {'errmsg': '数据不完整', 'pj_id': pj_id})
        if AlgorithmBuilding.objects.filter(algorithm_project_id=pj_id).filter(algorithm_name=name).first() is not None:
            return render(request, 'al_building/insert_algorithm.html', {'errmsg': '该算法名称已存在', 'pj_id': pj_id})
        # 业务逻辑,开始上传文件
        save_path = None
        try:
            proj = ProjectsInfo.objects.filter(id=pj_id).first()
            s1 = proj.project_root
            save_path = '%s/algorithms/%s' % (s1, name)
            save_file_path = '%s/algorithms' % s1
            if not os.path.exists(save_file_path):
                os.mkdir(save_file_path)
            print(save_path)
            with open(save_path, 'wb') as f:
                for content in algorithm_file.chunks():
                    f.write(content)
            AlgorithmBuildingManager.create_algorithm(algorithm_name=name, algorithm_version=version,
                                                      algorithm_creatime=datetime.datetime.now(),
                                                      algorithm_status=0,
                                                      algorithm_creater=creater, algorithm_information=information,
                                                      algorithm_root=save_path, algorithm_timeset=timeset,
                                                      algorithm_project_id=pj_id)
        except:
            if os.path.exists(save_path):
                # 如果目标路径存在原文件的话就先删除
                os.remove(save_path)
            AlgorithmBuilding.objects.filter(algorithm_name=name).delete()
            return HttpResponse('创建失败请重新创建')
        # return HttpResponse('创建成功')
        return redirect(reverse('algorithm:all_algorithm', kwargs={'pj_id': pj_id, 'pg': 1}))


class AllAlgorithmView(View):
    def get(self, request, pj_id, pg):
        # 1、查询出所有算法的信息
        als = AlgorithmBuilding.objects.filter(algorithm_project_id=pj_id).filter(
            algorithm_name__isnull=False).order_by()
        # 2 分页,每页显示一条
        paginator = Paginator(als, 3)
        page = paginator.page(pg)
        # val = os.popen('crontab -l')
        # for i in val:
        #     if i.split("#")
        val = os.popen('crontab -l')
        s = [x.strip() for x in val if x.strip() != '']
        a = []
        for i in s:
            if i.split('#')[1].__contains__('pro' + str(pj_id)) and i.split('#')[1].__contains__(' al'):
                a.append(i)
        return render(request, 'al_building/all_algorithm.html', {'page': page, 'pj_id': pj_id, 'a': a})


class SelectAlgorithmView(View):
    def get(self, request, al_id):
        """分页"""
        # 1、查询出所有工程的信息
        # print(pg)
        al_info = AlgorithmBuilding.objects.get(id=al_id)
        pj_info = ProjectsInfo.objects.get(id=al_info.algorithm_project_id)
        return render(request, 'al_building/select_algorithm.html', {'al_info': al_info, 'pj_info': pj_info})


class DeleteAlgorithmView(View):
    def get(self, request, pj_id, al_id):
        al_info = AlgorithmBuilding.objects.filter(id=al_id).first()
        if os.path.exists(al_info.algorithm_root):
            os.remove(al_info.algorithm_root)
        AlgorithmBuilding.objects.filter(id=al_id).first().delete()
        comment = 'al_' + al_info.algorithm_name + '_scr' + str(al_info.id) + '_pro' + str(
            al_info.algorithm_project_id)
        cron.del_task(comment)
        return redirect(reverse('algorithm:all_algorithm', kwargs={'pj_id': pj_id, 'pg': 1}))


class UpdateAlgorithmView(View):
    def post(self, request):
        pj_id = request.POST.get('pj_id')
        al_id = request.POST.get('al_id')
        al_version = util.remove_spaces(request.POST.get('version'))
        al_creater = util.remove_spaces(request.POST.get('creater'))
        al_timeset = request.POST.get('timeset')
        if not all([pj_id, al_id, al_version, al_creater, al_timeset]):
            pj_info = ProjectsInfo.objects.filter(id=pj_id).first()
            al_info = AlgorithmBuilding.objects.filter(id=al_id).first()
            return render(request, 'al_building/select_algorithm.html',
                          {'errmsg': '参数不完整', 'pj_info': pj_info, 'al_info': al_info})
        al_info = AlgorithmBuilding.objects.filter(id=al_id).first()
        if al_info.algorithm_timeset == al_timeset:
            AlgorithmBuilding.objects.filter(id=al_id).update(algorithm_version=al_version,
                                                              algorithm_creater=al_creater,
                                                              algorithm_creatime=datetime.datetime.now())
        else:
            if al_info.algorithm_status == 1:
                comment = 'al_' + al_info.algorithm_name + '_scr' + str(al_info.id) + '_pro' + str(
                    al_info.algorithm_project_id)
                print(comment)
                cron.del_task(comment)
                AlgorithmBuilding.objects.filter(id=al_id).update(algorithm_status=0, algorithm_version=al_version,
                                                                  algorithm_timeset=al_timeset,
                                                                  algorithm_creater=al_creater,
                                                                  algorithm_creatime=datetime.datetime.now())
            else:
                AlgorithmBuilding.objects.filter(id=al_id).update(algorithm_version=al_version,
                                                                  algorithm_timeset=al_timeset,
                                                                  algorithm_creater=al_creater,
                                                                  algorithm_creatime=datetime.datetime.now())
        return redirect('algorithm:select_algorithm', al_id=al_id)


class StartAlgorithmView(View):
    def get(self, request, al_id):
        al_info = AlgorithmBuilding.objects.filter(id=al_id).first()
        if al_info.algorithm_status == 1:
            return redirect('algorithm:select_algorithm', al_id=al_id)
        else:
            try:
                command = 'python3 ' + al_info.algorithm_root
                cron_exp = al_info.algorithm_timeset
                comment = 'al_' + al_info.algorithm_name + '_scr' + str(al_info.id) + '_pro' + str(
                    al_info.algorithm_project_id)
                cron.add_task(command=command, cron_exp=cron_exp, comment=comment)
                AlgorithmBuilding.objects.filter(id=al_id).update(algorithm_status=1)
            except:
                return HttpResponse('启动失败')
        return redirect('algorithm:select_algorithm', al_id=al_id)


class StopAlgorithmView(View):
    def get(self, request, al_id):
        al_info = AlgorithmBuilding.objects.filter(id=al_id).first()
        if al_info.algorithm_status == 0:
            return redirect('algorithm:select_algorithm', al_id=al_id)
        else:
            try:
                comment = 'al_' + al_info.algorithm_name + '_scr' + str(al_info.id) + '_pro' + str(
                    al_info.algorithm_project_id)
                cron.del_task(comment)
                AlgorithmBuilding.objects.filter(id=al_id).update(algorithm_status=0)
            except:
                return HttpResponse('停止失败')
        return redirect('algorithm:select_algorithm', al_id=al_id)
