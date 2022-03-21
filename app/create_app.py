# author: sunshine
# datetime:2022/3/21 上午10:58
from sanic_cors import CORS
from sanic import Sanic
from sanic.blueprints import Blueprint
from app.manage.m1 import m_bp
from app.license_utils import LicenseDecode


def create_app(license_file):
    """初始化app
    """
    LicenseDecode(license_path=license_file).license_check()
    app = Sanic('a1')

    # 跨域
    CORS(app)

    # 添加blueprint
    component_bp = Blueprint.group(
        m_bp,
        url_prefix='/api'
    )
    app.blueprint(component_bp)
    return app
