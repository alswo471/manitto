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

# 남은 참가자 리스트 (마니또 추첨에 사용)
remaining_participants = list(participants_info.keys())

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
    {% if manito %}
      <h3>당신의 마니또는 {{ manito }}입니다.</h3>
    {% else %}
      <h3>모든 마니또가 추첨되었습니다.</h3>
    {% endif %}
    <form method="POST" action="/draw">
      <input type="hidden" name="name" value="{{ name }}">
      <input type="hidden" name="password" value="{{ password }}">
      <input type="submit" value="다시 뽑기">
    </form>
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
    <form method="POST" action="/">
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
    if remaining_participants:
        candidates = [participant for participant in remaining_participants if participant != name]
        if not candidates:
            return None
        manito = random.choice(candidates)
        remaining_participants.remove(manito)
        return manito
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'name' in request.form and 'password' in request.form:
            name = request.form['name']
            password = request.form['password']

            # 인증 확인
            if name in participants_info and participants_info[name] == password:
                manito = assign_manito(name)
                return render_template_string(HTML_TEMPLATE_AUTHENTICATED, name=name, manito=manito, password=password)
            else:
                error = '인증 실패. 이름 또는 패스워드가 올바르지 않습니다.'
                return render_template_string(HTML_TEMPLATE_NOT_AUTHENTICATED, error=error)

    return render_template_string(HTML_TEMPLATE_NOT_AUTHENTICATED)

@app.route('/draw', methods=['POST'])
def draw():
    if 'name' in request.form and 'password' in request.form:
        name = request.form['name']
        password = request.form['password']

        # 인증 확인
        if name in participants_info and participants_info[name] == password:
            manito = assign_manito(name)
            return render_template_string(HTML_TEMPLATE_AUTHENTICATED, name=name, manito=manito, password=password)
        else:
            error = '인증 실패. 이름 또는 패스워드가 올바르지 않습니다.'
            return render_template_string(HTML_TEMPLATE_NOT_AUTHENTICATED, error=error)

    return render_template_string(HTML_TEMPLATE_NOT_AUTHENTICATED)

if __name__ == '__main__':
    app.run(debug=True)
