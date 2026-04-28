from flask import Blueprint, render_template, request
from app.models.task import Task

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    任務列表首頁
    1. 呼叫 Task.get_all() 取得任務清單
    2. 渲染 index.html
    """
    tasks = Task.get_all()
    return render_template('index.html', tasks=tasks)
