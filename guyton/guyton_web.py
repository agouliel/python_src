from flask import Flask, request, render_template
from guyton_calc import pmsa

app = Flask(__name__)

@app.route('/calculator', methods=['GET','POST'])
def calculator():
    if request.method == 'POST':
        if (request.form['cvp'] and request.form['map'] and request.form['co']
            and request.form['age'] and request.form['height'] and request.form['weight']):
            cvp = float(request.form['cvp'])
            map = float(request.form['map'])
            co = float(request.form['co'])
            if request.form['cvpb'] and request.form['mapb'] and request.form['cob']:
                cvpb = float(request.form['cvpb'])
                mapb = float(request.form['mapb'])
                cob = float(request.form['cob'])
            age = float(request.form['age'])
            height = float(request.form['height'])
            weight = float(request.form['weight'])

            if request.form['cvpb'] and request.form['mapb'] and request.form['cob']:
                result = pmsa(cvp, map, co, age, height, weight, cvpb, mapb, cob)
                return render_template('form.html', calculation_success=True,
                                   cvp=cvp, map=map, co=co, age=int(age), height=int(height), weight=int(weight),
                                   cvpb=cvpb, mapb=mapb, cob=cob,
                                   pmsa=result[0], pvr=result[1], eh=result[2], rvr=result[3], power=result[4], cpo=result[5],
                                   epower=result[6], evol=result[7],
                                   )
            else:
                result = pmsa(cvp, map, co, age, height, weight)
                return render_template('form.html', calculation_success=True,
                                   cvp=cvp, map=map, co=co, age=int(age), height=int(height), weight=int(weight),
                                   pmsa=result[0], pvr=result[1], eh=result[2], rvr=result[3], power=result[4], cpo=result[5])
        else:
            # https://medium.com/@alanbanks229/part-2-of-2-introduction-to-python-flask-29b58adbabaf
            # https://github.com/alanbanks229/flask_calculator_app
            return render_template('form.html', calculation_success=False, error='Please submit all values')
    
    return render_template('form.html')