from flask import Flask, request, render_template_string, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # 세션 암호화를 위한 임의의 값

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
    <form method="POST" action="/manito">
      <input type="hidden" name="name" value="{{ name }}">
      <input type="submit" value="마니또 추첨">
    </form>
    {% if manito %}
    <h3>당신의 마니또는 {{ manito }}입니다.</h3>
    {% endif %}
    <br>
    <form method="POST" action="/logout">
      <input type="submit" value="로그아웃">
    </form>
  </body>
</html>
"""

HTML_TEMPLATE_NOT_AUTHENTICATED = """
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <title>마니또 추첨기 로그인</title>
  </head>
  <body>
    <h1>마니또 추첨기</h1>
    <form method="POST" action="/login">
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

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('authenticated'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        
        if name in participants_info and participants_info[name] == password:
            session['username'] = name
            return redirect(url_for('authenticated'))
        else:
            error = '인증 실패. 이름 또는 패스워드가 올바르지 않습니다.'
            return render_template_string(HTML_TEMPLATE_NOT_AUTHENTICATED, error=error)
    
    return render_template_string(HTML_TEMPLATE_NOT_AUTHENTICATED)

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/manito', methods=['POST'])
def manito():
    if 'username' not in session:
        return redirect(url_for('login'))

    name = session['username']
    manito = assign_manito(name)
    return render_template_string(HTML_TEMPLATE_AUTHENTICATED, name=name, manito=manito)

@app.route('/records')
def records():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # 여기에 기록을 표시하는 코드를 추가하면 됩니다.

    return "여기에 기록을 표시할 HTML 템플릿을 넣으세요."

if __name__ == '__main__':
    app.run(debug=True)
