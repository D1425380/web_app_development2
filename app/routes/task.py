from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.task import Task
from app.models.user import User

task_bp = Blueprint('task', __name__)

@task_bp.route('/tasks/new')
def new_task():
    """顯示新增任務頁面"""
    users = User.get_all()
    return render_template('tasks/new.html', users=users)

@task_bp.route('/tasks/add', methods=['POST'])
def add_task():
    """處理新增任務請求"""
    title = request.form.get('title')
    description = request.form.get('description')
    priority = request.form.get('priority', '中')
    due_date = request.form.get('due_date')
    assigned_to = request.form.get('assigned_to')

    # 基本驗證
    if not title:
        flash('任務標題為必填項目！', 'error')
        return redirect(url_for('task.new_task'))

    data = {
        'title': title,
        'description': description,
        'priority': priority,
        'due_date': due_date if due_date else None,
        'assigned_to': assigned_to if assigned_to != "" else None
    }

    if Task.create(data):
        flash('任務建立成功！', 'success')
        return redirect(url_for('main.index'))
    else:
        flash('任務建立失敗，請稍後再試。', 'error')
        return redirect(url_for('task.new_task'))

@task_bp.route('/tasks/<int:id>')
def task_detail(id):
    """顯示任務詳情"""
    task = Task.get_by_id(id)
    if not task:
        flash('找不到該任務！', 'error')
        return redirect(url_for('main.index'))
    return render_template('tasks/detail.html', task=task)

@task_bp.route('/tasks/<int:id>/edit')
def edit_task(id):
    """顯示編輯任務頁面"""
    task = Task.get_by_id(id)
    users = User.get_all()
    if not task:
        flash('找不到該任務！', 'error')
        return redirect(url_for('main.index'))
    return render_template('tasks/edit.html', task=task, users=users)

@task_bp.route('/tasks/<int:id>/update', methods=['POST'])
def update_task(id):
    """處理更新任務請求"""
    title = request.form.get('title')
    description = request.form.get('description')
    status = request.form.get('status')
    priority = request.form.get('priority')
    due_date = request.form.get('due_date')
    assigned_to = request.form.get('assigned_to')

    if not title:
        flash('任務標題為必填項目！', 'error')
        return redirect(url_for('task.edit_task', id=id))

    data = {
        'title': title,
        'description': description,
        'status': status,
        'priority': priority,
        'due_date': due_date if due_date else None,
        'assigned_to': assigned_to if assigned_to != "" else None
    }

    if Task.update(id, data):
        flash('任務更新成功！', 'success')
        return redirect(url_for('task.task_detail', id=id))
    else:
        flash('任務更新失敗。', 'error')
        return redirect(url_for('task.edit_task', id=id))

@task_bp.route('/tasks/<int:id>/delete', methods=['POST'])
def delete_task(id):
    """刪除任務"""
    if Task.delete(id):
        flash('任務已刪除。', 'success')
    else:
        flash('任務刪除失敗。', 'error')
    return redirect(url_for('main.index'))
