from flask import Flask, render_template
from urls.adm.SelectSetor import bp_setor
from urls.adm.SelectServico import bp_servicos
from urls.adm.SelectEmpregado import bp_empregados
from urls.adm.SelectPrestador import bp_prestadores
from urls.adm.SelectLocal import bp_local
from urls.adm.SelectTipo_ocorrencia import bp_tpOcorrencias

app = Flask(__name__)

app.register_blueprint(bp_setor)
app.register_blueprint(bp_servicos)
app.register_blueprint(bp_empregados)
app.register_blueprint(bp_prestadores)
app.register_blueprint(bp_local)
app.register_blueprint(bp_tpOcorrencias)
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
