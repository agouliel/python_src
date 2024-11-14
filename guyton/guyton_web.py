from flask import Flask, request, render_template
from guyton_calc import pmsa

app = Flask(__name__)

@app.route('/calculator', methods=['GET','POST'])
def calculator():
    if request.method == 'POST':
        cvp = float(request.form['cvp'])
        map = float(request.form['map'])
        co = float(request.form['co'])
        age = float(request.form['age'])
        height = float(request.form['height'])
        weight = float(request.form['weight'])

        result = pmsa(cvp, map, co, age, height, weight)

        return render_template('result.html', pmsa=result[0], pvr=result[1], eh=result[2], rvr=result[3], power=result[4], cpo=result[5])
    
    return render_template('form.html')