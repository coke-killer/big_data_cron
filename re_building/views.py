# __author__: "Yu Dongyue"
# date: 2021/6/2
from django.shortcuts import render
from django.views.generic import View
from re_building.models import ReportBuilding, ReportBuildingManager
from django.shortcuts import render, redirect, HttpResponse, reverse
from utils import check_utils as util
from utils import crontab_utils as cron
from watch_dog_app.models import ProjectsInfo
import datetime
import os
from django.core.paginator import Paginator


# Create your views here.
class InsertReportView(View):
    def get(self, request, pj_id):
        return render(request, 're_building/insert_report.html', {'pj_id': pj_id})

    def post(self, request, pj_id):
        report_file = request.FILES['report_file']
        pj_id = request.POST.get('pj_id')
        name = report_file.name
        version = util.remove_spaces(request.POST.get('version'))
        information = util.remove_spaces(request.POST.get('information'))
        creater = util.remove_spaces(request.POST.get('creater'))
        timeset = request.POST.get('timeset')
        if not all([name, version, information, creater, timeset]):
            return render(request, 're_building/insert_report.html', {'errmsg': '数据不完整', 'pj_id': pj_id})
        if ReportBuilding.objects.filter(report_project_id=pj_id).filter(report_name=name).first() is not None:
            return render(request, 're_building/insert_report.html', {'errmsg': '该算法名称已存在', 'pj_id': pj_id})
        # 业务逻辑,开始上传文件
        save_path = None
        try:
            proj = ProjectsInfo.objects.filter(id=pj_id).first()
            s1 = proj.project_root
            save_path = '%s/reports/%s' % (s1, name)
            save_file_path = '%s/reports' % s1
            if not os.path.exists(save_file_path):
                os.mkdir(save_file_path)
            print(save_path)
            with open(save_path, 'wb') as f:
                for content in report_file.chunks():
                    f.write(content)
            ReportBuildingManager.create_report(report_name=name, report_version=version,
                                                report_creatime=datetime.datetime.now(),
                                                report_status=0,
                                                report_creater=creater, report_information=information,
                                                report_root=save_path, report_timeset=timeset,
                                                report_project_id=pj_id)
        except:
            if os.path.exists(save_path):
                # 如果目标路径存在原文件的话就先删除
                os.remove(save_path)
            ReportBuilding.objects.filter(report_name=name).delete()
            return HttpResponse('创建失败请重新创建')
        # return HttpResponse('创建成功')
        return redirect(reverse('report:all_report', kwargs={'pj_id': pj_id, 'pg': 1}))


class AllReportView(View):
    def get(self, request, pj_id, pg):
        # 1、查询出所有算法的信息
        res = ReportBuilding.objects.filter(report_project_id=pj_id).filter(
            report_name__isnull=False).order_by()
        # 2 分页,每页显示一条
        paginator = Paginator(res, 3)
        page = paginator.page(pg)
        val = os.popen('crontab -l')
        s = [x.strip() for x in val if x.strip() != '']
        a = []
        for i in s:
            if i.split('#')[1].__contains__('pro' + str(pj_id)) and i.split('#')[1].__contains__(' re'):
                a.append(i)
        return render(request, 're_building/all_report.html', {'page': page, 'pj_id': pj_id, 'a': a})


class SelectReportView(View):
    def get(self, request, re_id):
        """分页"""
        # 1、查询出所有工程的信息
        # print(pg)
        re_info = ReportBuilding.objects.get(id=re_id)
        pj_info = ProjectsInfo.objects.get(id=re_info.report_project_id)
        return render(request, 're_building/select_report.html', {'re_info': re_info, 'pj_info': pj_info})


class DeleteReportView(View):
    def get(self, request, pj_id, re_id):
        re_info = ReportBuilding.objects.filter(id=re_id).first()
        if os.path.exists(re_info.report_root):
            os.remove(re_info.report_root)
        ReportBuilding.objects.filter(id=re_id).first().delete()
        comment = 're_' + re_info.report_name + '_scr' + str(re_info.id) + '_pro' + str(
            re_info.report_project_id)
        cron.del_task(comment)
        return redirect(reverse('report:all_report', kwargs={'pj_id': pj_id, 'pg': 1}))


class UpdateReportView(View):
    def post(self, request):
        pj_id = request.POST.get('pj_id')
        re_id = request.POST.get('re_id')
        re_version = util.remove_spaces(request.POST.get('version'))
        re_creater = util.remove_spaces(request.POST.get('creater'))
        re_timeset = request.POST.get('timeset')
        if not all([pj_id, re_id, re_version, re_creater, re_timeset]):
            pj_info = ProjectsInfo.objects.filter(id=pj_id).first()
            re_info = ReportBuilding.objects.filter(id=re_id).first()
            return render(request, 're_building/select_report.html',
                          {'errmsg': '参数不完整', 'pj_info': pj_info, 're_info': re_info})
        re_info = ReportBuilding.objects.filter(id=re_id).first()
        if re_info.report_timeset == re_timeset:
            ReportBuilding.objects.filter(id=re_id).update(report_version=re_version,
                                                           report_creater=re_creater,
                                                           report_creatime=datetime.datetime.now())
        else:
            if re_info.report_status == 1:
                comment = 're_' + re_info.report_name + '_scr' + str(re_info.id) + '_pro' + str(
                    re_info.report_project_id)
                print(comment)
                cron.del_task(comment)
                ReportBuilding.objects.filter(id=re_id).update(report_status=0, report_version=re_version,
                                                               report_timeset=re_timeset,
                                                               report_creater=re_creater,
                                                               report_creatime=datetime.datetime.now())
            else:
                ReportBuilding.objects.filter(id=re_id).update(report_version=re_version,
                                                               report_timeset=re_timeset,
                                                               report_creater=re_creater,
                                                               report_creatime=datetime.datetime.now())
        return redirect('report:select_report', re_id=re_id)


class StartReportView(View):
    def get(self, request, re_id):
        re_info = ReportBuilding.objects.filter(id=re_id).first()
        if re_info.report_status == 1:
            return redirect('report:select_report', re_id=re_id)
        else:
            try:
                command = 'python3 ' + re_info.report_root
                cron_exp = re_info.report_timeset
                comment = 're_' + re_info.report_name + '_scr' + str(re_info.id) + '_pro' + str(
                    re_info.report_project_id)
                cron.add_task(command=command, cron_exp=cron_exp, comment=comment)
                ReportBuilding.objects.filter(id=re_id).update(report_status=1)
            except:
                return HttpResponse('启动失败')
        return redirect('report:select_report', re_id=re_id)


class StopReportView(View):
    def get(self, request, re_id):
        re_info = ReportBuilding.objects.filter(id=re_id).first()
        if re_info.report_status == 0:
            return redirect('report:select_report', re_id=re_id)
        else:
            try:
                comment = 're_' + re_info.report_name + '_scr' + str(re_info.id) + '_pro' + str(
                    re_info.report_project_id)
                cron.del_task(comment)
                ReportBuilding.objects.filter(id=re_id).update(report_status=0)
            except:
                return HttpResponse('停止失败')
        return redirect('report:select_report', re_id=re_id)
