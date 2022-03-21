# author: sunshine
# datetime:2022/3/21 上午9:13
from sanic.views import HTTPMethodView
from sanic.blueprints import Blueprint
from datetime import datetime
from sanic.response import text
m_bp = Blueprint('m1')

class M1(HTTPMethodView):
    def get(self, request):
        return text(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))


m_bp.add_route(M1.as_view(), '/m1')
