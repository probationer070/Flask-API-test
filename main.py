from flask import Flask
from flask_restx import Api, Resource, fields, Namespace
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///api.db'  # SQLite 데이터베이스 설정
db = SQLAlchemy(app)

api = Api(app, 
          version='1.0', 
          title='Login API', 
          description='A simple login API')

ns = Namespace("Login test", description="simple login")

# 데이터베이스 모델 정의
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

# 데이터베이스 생성 - flask 애플리케이션이 컨텍스트 밖에서 작업될 수 있음.
with app.app_context():
    db.create_all()

# Swagger에서 사용할 모델 정의
login_model = api.model('Login', {
    'username': fields.String(required=True, description='사용자명', example="cl_victor"),
    'password': fields.String(required=True, description='비밀번호', example="1234")
})

# 사용자 수정을 위한 모델
update_model = api.model('Update', {
    'username': fields.String(required=True, description='사용자명'),
    'password': fields.String(required=True, description='새로운 비밀번호')
})

# 로그인을 처리할 리소스
@ns.route('/login')
class Login(Resource):
    @api.expect(login_model)  # Swagger에서 사용할 모델 적용
    def post(self):
        data = api.payload  # Swagger UI에서 전송된 데이터 받기
        username = data.get('username')
        password = data.get('password')

        # 데이터베이스에 사용자 추가
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        return {"message": "사용자가 추가되었습니다."}, 201

    def get(self):
        # 모든 사용자 가져오기
        users = User.query.all()
        user_list = [{"id": user.id, "username": user.username, "password": user.password} for user in users]
        return {"users": user_list}, 200
    
# 사용자 수정을 위한 리소스
@ns.route('/login/<string:username>')
class UpdateUser(Resource):
    def get(self, username):
        user = User.query.filter_by(username=username).first()
        if not user:
            return {"message": "사용자를 찾을 수 없습니다."}, 404

        return {"id": user.id, 
                "username": user.username, 
                "password": user.password}, 200
    
    @api.expect(update_model)
    def put(self, username):
        data = api.payload
        new_username = data.get('username')
        new_password = data.get('password')
        
        user = User.query.filter_by(username=username).first()
        if not user:
            return {"message": "사용자를 찾을 수 없습니다."}, 404

        user.username = new_username
        user.password = new_password
        db.session.commit()

        return {"message": "사용자 정보가 수정되었습니다.",
                "user-info": {
                     "username": user.username, "password": user.password
                    }}, 200
        
    def delete(self, username):
        user = User.query.filter_by(username=username).first()
        if not user:
            return {"message": "사용자를 찾을 수 없습니다."}, 404

        db.session.delete(user)
        db.session.commit()

        return {"message": "사용자가 삭제되었습니다."}, 200

api.add_namespace(ns, "/Testing")

if __name__ == '__main__':
    app.run(debug=True)
