from flask import Flask
from flask_login import LoginManager
from extensions import db, login_manager
from config import Config
from routes import register_routes
from models import User

# 1. 先创建 Flask 应用实例
app = Flask(__name__)
app.config.from_object(Config)

# 2. 初始化扩展
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# 3. 定义用户加载器
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 4. 注册路由
register_routes(app)

# 5. 初始化数据库（必须在 app 上下文内）
with app.app_context():
    db.create_all()

# 6. 自定义过滤器（确保 app 已创建）
def mask_email(email):
    if len(email) >= 5:
        masked = '*' * 5 + email[5:]
    else:
        masked = '*' * len(email)
    return masked

app.jinja_env.filters['mask_email'] = mask_email

# 7. 运行应用
if __name__ == '__main__':
    app.run(debug=True)