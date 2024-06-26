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
      <label for="name">이름:</label><br>
      <input type="text" id="name" name="name" required><br>
      <label for="password">패스워드:</label><br>
      <input type="password" id="password" name="password" required><br><br>
      <input type="submit" value="확인">
    </form>
    {% if error %}
    <p style="color: red;">{{ error }}</p>
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
def home():
   if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        if name in participants_info and participants_info[name] == password:
            session['name'] = name
            return redirect(url_for('result'))
        else:
            error = "이름 또는 패스워드가 잘못되었습니다."
            return render_template_string(HTML_TEMPLATE, error=error)
    return render_template_string(HTML_TEMPLATE, error=None)

@app.route('/result')
def result():
    if 'name' not in session:
        return redirect(url_for('index'))
    name = session['name']
    manito = assignments[name]
    return render_template_string(RESULT_TEMPLATE, name=name, manito=manito)

if __name__ == '__main__':
    app.run(debug=True)