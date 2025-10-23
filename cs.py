from flask import Flask, render_template
from urls.adm.setor import bp_setor
from urls.adm.servicos import bp_servicos
from urls.adm.empregados import bp_empregados
from urls.adm.locais import bp_locais
from urls.adm.ocorrencias import bp_ocorrencias
from urls.adm.prestadores import bp_prestadores

app = Flask(__name__)
app.register_blueprint(bp_setor)
app.register_blueprint(bp_servicos)
app.register_blueprint(bp_empregados)
app.register_blueprint(bp_locais)
app.register_blueprint(bp_ocorrencias)
app.register_blueprint(bp_prestadores)


@app.route('/')
def cs():
    return render_template('index.html')


@app.route('/menu_adm')
def menu_adm():
    return render_template('menu_adm.html')


@app.route('/menu_pre')
def menu_pre():
    return render_template('menu_pre.html')


@app.route('/menu_sol')
def menu_sol():
    return render_template('menu_sol.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
