import os
import sqlite3
from flask import Flask

def create_app(test_config=None):
    # 建立與設定 Flask App
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'database.db'),
    )

    if test_config is None:
        # 載入實例設定 (如果有的話)
        app.config.from_pyfile('config.py', silent=True)
    else:
        # 載入測試設定
        app.config.from_mapping(test_config)

    # 確保 instance 資料夾存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 註冊 Blueprints
    from .routes.main import main_bp
    from .routes.task import task_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(task_bp)

    return app

def init_db():
    """初始化資料庫"""
    db_path = 'instance/database.db'
    schema_path = 'database/schema.sql'
    
    # 確保 instance 目錄存在
    if not os.path.exists('instance'):
        os.makedirs('instance')
        
    conn = sqlite3.connect(db_path)
    with open(schema_path, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.close()
    print("資料庫初始化完成！")
