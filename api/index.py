from flask import Flask, request, render_template_string

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
HTML_TEMPLATE = """
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <title>마니또 추첨기</title>
  </head>
  <body>
    <h1>마니또 추첨기</h1>
    {% if authenticated %}
    <form method="POST">
      <label for="participants">참가자 이름을 쉼표로 구분하여 입력하세요:</label><br>
      <input type="text" id="participants" name="participants" required><br><br>
      <input type="submit" value="추첨하기">
    </form>
    {% if assignments %}
    <h2>추첨 결과</h2>
    <ul>
      {% for giver, receiver in assignments.items() %}
        <li>{{ giver }}의 마니또는 {{ receiver }}입니다.</li>
      {% endfor %}
    </ul>
    {% endif %}
    {% else %}
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
    {% endif %}
  </body>
</html>
"""

def assign_manito(participants):
    import random
    shuffled = participants[:]
    random.shuffle(shuffled)
    manito_assignments = {}
    for i in range(len(participants)):
        while shuffled[i] == participants[i]:
            random.shuffle(shuffled)
        manito_assignments[participants[i]] = shuffled[i]
    return manito_assignments

@app.route('/', methods=['GET', 'POST'])
def index():
    authenticated = False
    error = None
    assignments = None

    if request.method == 'POST':
        if 'name' in request.form and 'password' in request.form:
            name = request.form['name']
            password = request.form['password']

            # 인증 확인
            if name in participants_info and participants_info[name] == password:
                authenticated = True
            else:
                error = '인증 실패. 이름 또는 패스워드가 올바르지 않습니다.'

        elif 'participants' in request.form:
            participants = request.form['participants'].split(',')
            participants = [p.strip() for p in participants]
            assignments = assign_manito(participants)

    return render_template_string(HTML_TEMPLATE, authenticated=authenticated, error=error, assignments=assignments)

if __name__ == '__main__':
    app.run(debug=True)
