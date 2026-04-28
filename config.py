import os
from dotenv import load_dotenv

# 載入 .env 檔案
load_dotenv()

class Config:
    """基礎配置"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change'
    DATABASE = os.environ.get('DATABASE_PATH') or os.path.join(
        os.path.abspath(os.path.dirname(__file__)), 'instance', 'database.db'
    )

class DevelopmentConfig(Config):
    """開發環境配置"""
    DEBUG = True

class ProductionConfig(Config):
    """生產環境配置"""
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
