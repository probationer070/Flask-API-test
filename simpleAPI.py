from flask import Flask
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(app, version='1.0', title='Login API', description='A simple login API')

# 가장 간단한 형태의 인증을 위한 사용자 데이터
users = {
    "user1": "password1",
    "user2": "password2"
}

# Swagger에서 사용할 모델 정의
login_model = api.model('Login', {
    'username': fields.String(required=True, description='사용자명'),
    'password': fields.String(required=True, description='비밀번호')
})

# 로그인을 처리할 리소스
@api.route('/login')
class Login(Resource):
    @api.expect(login_model)  # Swagger에서 사용할 모델 적용
    def post(self):
        # Request Parser를 사용하여 요청 데이터 파싱
        # args = login_parser.parse_args()
        # username = args['username']
        # password = args['password']

        data = api.payload  # Swagger UI에서 전송된 데이터 받기
        username = data.get('username')
        password = data.get('password')

        # 유저가 존재하고, 비밀번호가 일치하면 로그인 성공
        if username in users and users[username] == password:
            return {"message": "로그인 성공"}, 200
        else:
            return {"message": "유효하지 않은 사용자명 또는 비밀번호"}, 401

    def get(self):
        return {"users": users}, 200

if __name__ == '__main__':
    app.run(debug=True)
