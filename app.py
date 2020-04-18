from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('mongodb://skylark:skylark@54.180.94.231', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.projectTreeon                      # 'dbsparta'라는 이름의 db를 만듭니다.


## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('treeon_front.html')

## API 역할을 하는 부분
@app.route('/information', methods=['GET'])
def job_list():
	# 1. db에서 데이터 가져오기.
    res = list(db.information.find({},{'_id':0}))
    return jsonify({'result': 'success', 'data' : res, 'msg': '완료'})

@app.route('/runpython', methods=['GET'])
def run_python():
    import treeon_incruit
    import treeon_jobkorea
    import treeon_peopleNjob
    import treeon_saramIn
    return 'Success!'

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
