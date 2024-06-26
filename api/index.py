from flask import Flask, request, render_template_string
import random

app = Flask(__name__)

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
  </body>
</html>
"""

def assign_manito(participants):
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
    assignments = None
    if request.method == 'POST':
        participants = request.form['participants'].split(',')
        participants = [p.strip() for p in participants]
        assignments = assign_manito(participants)
    return render_template_string(HTML_TEMPLATE, assignments=assignments)

app.run("0.0.0.0")
