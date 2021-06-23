# __author__: "Yu Dongyue"
# date: 2021/6/2
from django.shortcuts import render
from django.views.generic import View
from db_building.models import DbscriptBuilding, DbscriptBuildingManager
from django.shortcuts import render, redirect, HttpResponse, reverse
from utils import check_utils as util
from utils import crontab_utils as cron
from watch_dog_app.models import ProjectsInfo
import datetime
import os
from django.core.paginator import Paginator


# Create your views here.
class InsertDbscriptView(View):
    def get(self, request, pj_id):
        return render(request, 'db_building/insert_dbscript.html', {'pj_id': pj_id})

    def post(self, request, pj_id):
        dbscript_file = request.FILES['dbscript_file']
        pj_id = request.POST.get('pj_id')
        name = dbscript_file.name
        version = util.remove_spaces(request.POST.get('version'))
        information = util.remove_spaces(request.POST.get('information'))
        creater = util.remove_spaces(request.POST.get('creater'))
        timeset = request.POST.get('timeset')
        if not all([name, version, information, creater, timeset]):
            return render(request, 'db_building/insert_dbscript.html', {'errmsg': '数据不完整', 'pj_id': pj_id})
        if DbscriptBuilding.objects.filter(dbscript_project_id=pj_id).filter(dbscript_name=name).first() is not None:
            return render(request, 'db_building/insert_dbscript.html', {'errmsg': '该算法名称已存在', 'pj_id': pj_id})
        # 业务逻辑,开始上传文件
        save_path = None
        try:
            proj = ProjectsInfo.objects.filter(id=pj_id).first()
            s1 = proj.project_root
            save_path = '%s/dbscripts/%s' % (s1, name)
            save_file_path = '%s/dbscripts' % s1
            if not os.path.exists(save_file_path):
                os.mkdir(save_file_path)
            print(save_path)
            with open(save_path, 'wb') as f:
                for content in dbscript_file.chunks():
                    f.write(content)
            DbscriptBuildingManager.create_dbscript(dbscript_name=name, dbscript_version=version,
                                                      dbscript_creatime=datetime.datetime.now(),
                                                      dbscript_status=0,
                                                      dbscript_creater=creater, dbscript_information=information,
                                                      dbscript_root=save_path, dbscript_timeset=timeset,
                                                      dbscript_project_id=pj_id)
        except:
            if os.path.exists(save_path):
                # 如果目标路径存在原文件的话就先删除
                os.remove(save_path)
            DbscriptBuilding.objects.filter(dbscript_name=name).delete()
            return HttpResponse('创建失败请重新创建')
        # return HttpResponse('创建成功')
        return redirect(reverse('dbscript:all_dbscript', kwargs={'pj_id': pj_id, 'pg': 1}))


class AllDbscriptView(View):
    def get(self, request, pj_id, pg):
        # 1、查询出所有算法的信息
        als = DbscriptBuilding.objects.filter(dbscript_project_id=pj_id).filter(
            dbscript_name__isnull=False).order_by()
        # 2 分页,每页显示一条
        paginator = Paginator(als, 3)
        page = paginator.page(pg)
        # val = os.popen('crontab -l')
        # for i in val:
        #     if i.split("#")
        val = os.popen('crontab -l')
        s = [x.strip() for x in val if x.strip() != '']
        print(s)
        a = []
        for i in s:
            if i.split('#')[1].__contains__('pro' + str(pj_id)) and i.split('#')[1].__contains__(' db'):
                a.append(i)
                print(a)
        return render(request, 'db_building/all_dbscript.html', {'page': page, 'pj_id': pj_id, 'a': a})


class SelectDbscriptView(View):
    def get(self, request, db_id):
        """分页"""
        # 1、查询出所有工程的信息
        # print(pg)
        db_info = DbscriptBuilding.objects.get(id=db_id)
        pj_info = ProjectsInfo.objects.get(id=db_info.dbscript_project_id)
        return render(request, 'db_building/select_dbscript.html', {'db_info': db_info, 'pj_info': pj_info})


class DeleteDbscriptView(View):
    def get(self, request, pj_id, db_id):
        db_info = DbscriptBuilding.objects.filter(id=db_id).first()
        if os.path.exists(db_info.dbscript_root):
            os.remove(db_info.dbscript_root)
        DbscriptBuilding.objects.filter(id=db_id).first().delete()
        comment = 'db_' + db_info.dbscript_name + '_scr' + str(db_info.id) + '_pro' + str(
            db_info.dbscript_project_id)
        cron.del_task(comment)
        return redirect(reverse('dbscript:all_dbscript', kwargs={'pj_id': pj_id, 'pg': 1}))


class UpdateDbscriptView(View):
    def post(self, request):
        pj_id = request.POST.get('pj_id')
        db_id = request.POST.get('db_id')
        db_version = util.remove_spaces(request.POST.get('version'))
        db_creater = util.remove_spaces(request.POST.get('creater'))
        db_timeset = request.POST.get('timeset')
        if not all([pj_id, db_id, db_version, db_creater, db_timeset]):
            pj_info = ProjectsInfo.objects.filter(id=pj_id).first()
            db_info = DbscriptBuilding.objects.filter(id=db_id).first()
            return render(request, 'db_building/select_dbscript.html',
                          {'errmsg': '参数不完整', 'pj_info': pj_info, 'db_info': db_info})
        db_info = DbscriptBuilding.objects.filter(id=db_id).first()
        if db_info.dbscript_timeset == db_timeset:
            DbscriptBuilding.objects.filter(id=db_id).update(dbscript_version=db_version,
                                                              dbscript_creater=db_creater,
                                                              dbscript_creatime=datetime.datetime.now())
        else:
            if db_info.dbscript_status == 1:
                comment = 'db_' + db_info.dbscript_name + '_scr' + str(db_info.id) + '_pro' + str(
                    db_info.dbscript_project_id)
                print(comment)
                cron.del_task(comment)
                DbscriptBuilding.objects.filter(id=db_id).update(dbscript_status=0, dbscript_version=db_version,
                                                                  dbscript_timeset=db_timeset,
                                                                  dbscript_creater=db_creater,
                                                                  dbscript_creatime=datetime.datetime.now())
            else:
                DbscriptBuilding.objects.filter(id=db_id).update(dbscript_version=db_version,
                                                                  dbscript_timeset=db_timeset,
                                                                  dbscript_creater=db_creater,
                                                                  dbscript_creatime=datetime.datetime.now())
        return redirect('dbscript:select_dbscript', db_id=db_id)


class StartDbscriptView(View):
    def get(self, request, db_id):
        db_info = DbscriptBuilding.objects.filter(id=db_id).first()
        if db_info.dbscript_status == 1:
            return redirect('dbscript:select_dbscript', db_id=db_id)
        else:
            try:
                command = 'python3 ' + db_info.dbscript_root
                cron_exp = db_info.dbscript_timeset
                comment = 'db_' + db_info.dbscript_name + '_scr' + str(db_info.id) + '_pro' + str(
                    db_info.dbscript_project_id)
                cron.add_task(command=command, cron_exp=cron_exp, comment=comment)
                DbscriptBuilding.objects.filter(id=db_id).update(dbscript_status=1)
            except:
                return HttpResponse('启动失败')
        return redirect('dbscript:select_dbscript', db_id=db_id)


class StopDbscriptView(View):
    def get(self, request, db_id):
        db_info = DbscriptBuilding.objects.filter(id=db_id).first()
        if db_info.dbscript_status == 0:
            return redirect('dbscript:select_dbscript', db_id=db_id)
        else:
            try:
                comment = 'db_' + db_info.dbscript_name + '_scr' + str(db_info.id) + '_pro' + str(
                    db_info.dbscript_project_id)
                cron.del_task(comment)
                DbscriptBuilding.objects.filter(id=db_id).update(dbscript_status=0)
            except:
                return HttpResponse('停止失败')
        return redirect('dbscript:select_dbscript', db_id=db_id)
