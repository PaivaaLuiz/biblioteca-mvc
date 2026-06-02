from flask import Flask, render_template, request, redirect
from database.db import db
from models.livro import Livro

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///biblioteca.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# página inicial
@app.route('/')
def inicio():
    return render_template('index.html')

# página sobre
@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

# página de livros
@app.route('/livros')
def livros():
    return render_template('livros.html')

# página de contato
@app.route('/contato')
def contato():
    return render_template('contato.html')

# página de login da área administativa
@app.route('/login')
def login():
    return render_template('login.html')

# cadastro dos livros
@app.route('/cadastrar-livro', methods=['GET', 'POST'])
def cadastrar_livro():

    if request.method == 'POST':

        titulo = request.form['titulo']
        autor = request.form['autor']
        categoria = request.form['categoria']

        novo_livro = Livro(
            titulo=titulo,
            autor=autor,
            categoria=categoria
        )

        db.session.add(novo_livro)
        db.session.commit()

        return redirect('/livros')

    return render_template('cadastrar_livro.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)