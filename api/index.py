from flask import Flask, request, render_template_string
import random

app = Flask(__name__)

# 고정적으로 설정된 참가자 및 패스워드 정보
participants_info = {
    '지민재': '121',
    '윤석환': '122',
    '박준성': '123',
    '정예은': '124',
    '김수민': '125',
    '정은지': '126'
}

# HTML 템플릿
HTML_TEMPLATE_AUTHENTICATED = """
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <title>마니또 추첨기</title>
  </head>
  <body>
    <h1>마니또 추첨기</h1>
    <h2>안녕하세요, {{ name }}님!</h2>
    <h3>당신의 마니또는 {{ manito }}입니다.</h3>
  </body>
</html>
"""

HTML_TEMPLATE_NOT_AUTHENTICATED = """
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <title>마니또 추첨기</title>
  </head>
  <body>
    <h1>마니또 추첨기</h1>
    <form method="POST">
      <label for="name">이름:</label><br>
      <input type="text" id="name" name="name" required><br><br>
      <label for="password">패스워드:</label><br>
      <input type="password" id="password" name="password" required><br><br>
      <input type="submit" value="로그인">
    </form>
    {% if error %}
    <p style="color: red;">{{ error }}</p>
    {% endif %}
  </body>
</html>
"""

def assign_manito(name):
    participants = list(participants_info.keys())
    participants.remove(name)
    random.shuffle(participants)
    return participants[0]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'name' in request.form and 'password' in request.form:
            name = request.form['name']
            password = request.form['password']

            # 인증 확인
            if name in participants_info and participants_info[name] == password:
                manito = assign_manito(name)
                return render_template_string(HTML_TEMPLATE_AUTHENTICATED, name=name, manito=manito)
            else:
                error = '인증 실패. 이름 또는 패스워드가 올바르지 않습니다.'
                return render_template_string(HTML_TEMPLATE_NOT_AUTHENTICATED, error=error)

    return render_template_string(HTML_TEMPLATE_NOT_AUTHENTICATED)

if __name__ == '__main__':
    app.run(debug=True)
