from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.task import Task
from app.models.user import User

task_bp = Blueprint('task', __name__)

@task_bp.route('/tasks/new')
def new_task():
    """
    顯示新增任務頁面
    1. 呼叫 User.get_all() 供表單選擇分配對象
    2. 渲染 tasks/new.html
    """
    pass

@task_bp.route('/tasks/add', methods=['POST'])
def add_task():
    """
    處理新增任務請求
    1. 從 request.form 讀取資料
    2. 驗證資料後呼叫 Task.create()
    3. 重導向至首頁
    """
    pass

@task_bp.route('/tasks/<int:id>')
def task_detail(id):
    """
    顯示任務詳情
    1. 呼叫 Task.get_by_id(id)
    2. 渲染 tasks/detail.html
    """
    pass

@task_bp.route('/tasks/<int:id>/edit')
def edit_task(id):
    """
    顯示編輯任務頁面
    1. 呼叫 Task.get_by_id(id)
    2. 呼叫 User.get_all()
    3. 渲染 tasks/edit.html
    """
    pass

@task_bp.route('/tasks/<int:id>/update', methods=['POST'])
def update_task(id):
    """
    處理更新任務請求
    1. 從 request.form 讀取資料
    2. 呼叫 Task.update()
    3. 重導向至詳情頁或首頁
    """
    pass

@task_bp.route('/tasks/<int:id>/status', methods=['POST'])
def update_status(id):
    """
    快速更新任務狀態
    1. 讀取新狀態
    2. 呼叫 Task.update_status()
    3. 重導向回來源頁面
    """
    pass

@task_bp.route('/tasks/<int:id>/delete', methods=['POST'])
def delete_task(id):
    """
    刪除任務
    1. 呼叫 Task.delete(id)
    2. 重導向至首頁
    """
    pass
