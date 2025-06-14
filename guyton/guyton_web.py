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

            if (request.form['sv'] and request.form['svr'] and request.form['svv']
            and request.form['sap'] and request.form['dap']
            and request.form['hr'] and request.form['ppv']):
                sv = float(request.form['sv'])
                svr = float(request.form['svr'])
                svv = float(request.form['svv'])
                sap = float(request.form['sap'])
                dap = float(request.form['dap'])
                hr = float(request.form['hr'])
                ppv = float(request.form['ppv'])
            
            # all extra values are given
            if (request.form['cvpb'] and request.form['mapb'] and request.form['cob']
            and request.form['sv'] and request.form['svr'] and request.form['svv']
            and request.form['sap'] and request.form['dap']
            and request.form['hr'] and request.form['ppv']):
                result = pmsa(cvp, map, co, age, height, weight, cvpb, mapb, cob, sv, svr, svv,
                    sap, dap, hr, ppv)
                return render_template('form.html', calculation_success=True,
                                   cvp=cvp, map=map, co=co, age=int(age), height=int(height), weight=int(weight),
                                   cvpb=cvpb, mapb=mapb, cob=cob,
                                   pmsa=result[0], pvr=result[1], eh=result[2], rvr=result[3], power=result[4], cpo=result[5],
                                   epower=result[6], evol=result[7],
                                   cart=result[8], rart=result[9],
                                   rven=result[10], ea=result[11], eadyn=result[12],
                                   )
            # only "before" extra values are given
            if request.form['cvpb'] and request.form['mapb'] and request.form['cob']:
                result = pmsa(cvp, map, co, age, height, weight, cvpb, mapb, cob)
                return render_template('form.html', calculation_success=True,
                                   cvp=cvp, map=map, co=co, age=int(age), height=int(height), weight=int(weight),
                                   cvpb=cvpb, mapb=mapb, cob=cob,
                                   pmsa=result[0], pvr=result[1], eh=result[2], rvr=result[3], power=result[4], cpo=result[5],
                                   epower=result[6], evol=result[7],
                                   )
            # only down block of extra values are given
            if (request.form['sv'] and request.form['svr'] and request.form['svv']
            and request.form['sap'] and request.form['dap']
            and request.form['hr'] and request.form['ppv']):
                result = pmsa(cvp, map, co, age, height, weight, 0, 0, 0, sv, svr, svv,
                    sap, dap, hr, ppv)
                return render_template('form.html', calculation_success=True,
                                   cvp=cvp, map=map, co=co, age=int(age), height=int(height), weight=int(weight),
                                   cvpb=0, mapb=0, cob=0,
                                   pmsa=result[0], pvr=result[1], eh=result[2], rvr=result[3], power=result[4], cpo=result[5],
                                   epower=result[6], evol=result[7],
                                   cart=result[8], rart=result[9],
                                   rven=result[10], ea=result[11], eadyn=result[12],
                                   )
            # only basic values are given
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