# author: sunshine
# datetime:2022/3/21 上午11:00
from app.create_app import create_app
app = create_app('License.dat')
if __name__ == '__main__':
    app.run('0.0.0.0', port=5008)
