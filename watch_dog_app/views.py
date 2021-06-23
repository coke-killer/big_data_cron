from django.views.generic import View
from django.http import request
from django.shortcuts import render, redirect, HttpResponse
import time, datetime
from watch_dog_app.models import ProjectsInfo, ProjectInfoManager
from TITAN import settings
import os
import shutil
import happybase
from django.core.paginator import Paginator
from utils import check_utils as util


class AllProjectView(View):
    def get(self, request, pg):
        # 1、查询出所有工程的信息
        # print(pg)
        pjs = ProjectsInfo.objects.filter(project_name__isnull=False).order_by()
        # 2 分页,每页显示一条
        paginator = Paginator(pjs, 10)
        # print('总共条数:')
        # print(paginator.num_pages)  # 总共条数
        # print('每页页码:')
        # print(paginator.page_range)  # 每页页码
        # 获取第一页的内容
        page = paginator.page(pg)
        return render(request, 'watch_dog_app/all_project.html', {'page': page})


class InsertProjectView(View):
    def get(self, request):
        '''显示添加工程页面'''
        return render(request, 'watch_dog_app/insert_projects.html')

    def post(self, request):
        # 校验数据
        project_name = util.remove_spaces(request.POST.get('name'))
        project_information = util.remove_spaces(request.POST.get('information'))
        project_creater = util.remove_spaces(request.POST.get('creater'))
        if not all([project_name, project_information, project_creater]):
            return render(request, 'watch_dog_app/insert_projects.html', {'errmsg': '数据不完整'})
        if ProjectsInfo.objects.filter(project_name=project_name).first() is not None:
            return render(request, 'watch_dog_app/insert_projects.html', {'errmsg': '该工程名称已存在'})
        # 业务逻辑文件初始化
        project_root = None
        connection = None
        name1 = None
        name2 = None
        try:
            # 初始化mysql记录
            ProjectInfoManager.create_proj(request.POST.get('name'), request.POST.get('information'),
                                           datetime.datetime.now(),
                                           request.POST.get('creater'),
                                           '', None)
            proj = ProjectsInfo.objects.get(project_name=project_name)
            # 初始化项目文件夹
            # project_root = os.path.join(settings.BASE_DIR, 'project/pro_' + str(proj.id))
            project_root = os.path.join(os.path.abspath(os.path.dirname(os.getcwd())), proj.project_name)
            project_template = os.path.join(os.path.abspath(os.path.dirname(os.getcwd())), 'project_template')
            shutil.copytree(project_template, project_root)
            ProjectsInfo.objects.filter(project_name=project_name).update(project_root=project_root)
            # 初始化hbase
            # hbase_pool = happybase.ConnectionPool(size=3, host='Master', port=9090, table_prefix=proj.project_name,protocol='compact', transport='framed')
            connection = happybase.Connection('Master', table_prefix=proj.project_name)  # 在连接的时候创建项目空间
            # 创建底层数仓表格
            connection.open()
            name1 = 'DB_level0'
            families1 = {
                "TimeSe": dict(),
                "Alarm": dict(),
                "Tag": dict()
            }
            connection.create_table(name1, families1)  # 如果连接时，有传递表前缀参数时，真实表名将会是："{}_{}".format(table_prefix,name)
            # 创建业务集市表格
            name2 = 'DB_level1'
            families2 = {
                "Business": dict()
            }
            connection.create_table(name2, families2)  # 如果连接时，有传递表前缀参数时，真实表名将会是："{}_{}".format(table_prefix,name)
        except:
            if os.path.exists(project_root):
                # 如果目标路径存在原文件夹的话就先删除
                shutil.rmtree(project_root)
            ProjectsInfo.objects.filter(project_name=project_name).delete()
            if b'DB_level0' in connection.tables():
                connection.delete_table(name1, True)
            if b'DB_level1' in connection.tables():
                connection.delete_table(name2, True)
            return HttpResponse('创建失败请重新创建')
        finally:
            connection.close()
        return redirect('project:all_project', pg=1)


class SelectProjectView(View):
    def get(self, request, pj_id):
        """分页"""
        # 1、查询出所有工程的信息
        # print(pg)
        pj_info = ProjectsInfo.objects.get(id=pj_id)
        return render(request, 'watch_dog_app/select_projects.html', {'pj_info': pj_info})


class DeleteProjectView(View):
    def get(self, request, pj_id):
        proj = ProjectsInfo.objects.get(id=pj_id)
        project_root = proj.project_root
        if os.path.exists(project_root):
            # 如果目标路径存在原文件夹的话就先删除
            shutil.rmtree(project_root)
        ProjectsInfo.objects.filter(id=pj_id).first().delete()
        print(proj)
        connection = happybase.Connection('Master', table_prefix=proj.project_name)  # 在连接的时候创建项目空间
        connection.open()
        if b'DB_level0' in connection.tables():
            connection.delete_table('DB_level0', True)
        if b'DB_level1' in connection.tables():
            connection.delete_table('DB_level1', True)
        return redirect('project:all_project', pg=1)


class UpdateProjectView(View):
    def post(self, request):
        pj_id = request.POST.get('id')
        p_name = util.remove_spaces(request.POST.get('name'))
        p_information = util.remove_spaces(request.POST.get('information'))
        p_creater = util.remove_spaces(request.POST.get('creater'))
        if not all([pj_id, p_name, p_information, p_creater]):
            pj_info = ProjectsInfo.objects.filter(id=pj_id).first()
            return render(request, 'watch_dog_app/select_projects.html', {'errmsg': '数据不完整', 'pj_info': pj_info})
        if ProjectsInfo.objects.exclude(id=pj_id).filter(project_name=p_name).first() is not None:
            pj_info = ProjectsInfo.objects.filter(id=pj_id).first()
            return render(request, 'watch_dog_app/select_projects.html', {'errmsg': '该工程名称已存在', 'pj_info': pj_info})
        # print(pj_id)
        # print(p_name)
        # print(p_information)
        # print(p_creater)
        # print(type(pj_id))
        ProjectsInfo.objects.filter(id=pj_id).update(project_name=p_name, project_information=p_information,
                                                     project_creater=p_creater,
                                                     project_creatime=datetime.datetime.now())

        return redirect('project:select_project', pj_id=pj_id)

    pass
