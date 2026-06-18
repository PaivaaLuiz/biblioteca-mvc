from flask import Flask, render_template, request, redirect, session
from database.db import db
from models.livro import Livro
from sqlalchemy import or_


app = Flask(__name__)

app.secret_key = 'biblioteca123'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///biblioteca.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()

    if Livro.query.count() == 0:

        livros_iniciais = [

            Livro(
                titulo='Harry Potter e a Pedra Filosofal',
                autor='J. K. Rowling',
                categoria='Fantasia'
            ),

            Livro(
                titulo='Percy Jackson e o Ladrão de Raios',
                autor='Rick Riordan',
                categoria='Fantasia'
            ),

            Livro(
                titulo='O Senhor dos Anéis',
                autor='J. R. R. Tolkien',
                categoria='Fantasia'
            ),

            Livro(
                titulo='O Hobbit',
                autor='J. R. R. Tolkien',
                categoria='Fantasia'
            ),

            Livro(
                titulo='Dom Casmurro',
                autor='Machado de Assis',
                categoria='Romance'
            ),

            Livro(
                titulo='Memórias Póstumas de Brás Cubas',
                autor='Machado de Assis',
                categoria='Romance'
            ),

            Livro(
                titulo='1984',
                autor='George Orwell',
                categoria='Ficção Científica'
            ),

            Livro(
                titulo='A Revolução dos Bichos',
                autor='George Orwell',
                categoria='Ficção'
            ),

            Livro(
                titulo='O Pequeno Príncipe',
                autor='Antoine de Saint-Exupéry',
                categoria='Infantil'
            ),

            Livro(
                titulo='Sherlock Holmes: Um Estudo em Vermelho',
                autor='Arthur Conan Doyle',
                categoria='Mistério'
            )

        ]

        db.session.add_all(livros_iniciais)
        db.session.commit()

# página inicial
@app.route('/')
def inicio():
    return render_template('index.html')

# página sobre
@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

# página de livros e pesquisa
@app.route('/livros')
def livros():

    termo = request.args.get('pesquisa')

    if termo:

        lista_livros = Livro.query.filter(
            or_(
                Livro.titulo.contains(termo),
                Livro.autor.contains(termo)
            )
        ).all()

    else:

        lista_livros = Livro.query.all()

    return render_template(
        'livros.html',
        livros=lista_livros
    )

# página de contato
@app.route('/contato')
def contato():
    return render_template('contato.html')

# página de login da área administativa
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        usuario = request.form['usuario']
        senha = request.form['senha']

        if usuario == 'admin' and senha == 'admin123':

            session['admin'] = True

            return redirect('/livros')

        return "Usuário ou senha incorretos!"

    return render_template('login.html')

@app.route('/logout')
def logout():

    session.pop('admin', None)

    return redirect('/')

# cadastro dos livros
@app.route('/cadastrar-livro', methods=['GET', 'POST'])
def cadastrar_livro():

    if not session.get('admin'):
        return redirect('/login')

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

# editar livros

@app.route('/editar-livro/<int:id>', methods=['GET', 'POST'])
def editar_livro(id):

    if not session.get('admin'):
        return redirect('/login')

    livro = Livro.query.get_or_404(id)

    if request.method == 'POST':

        livro.titulo = request.form['titulo']
        livro.autor = request.form['autor']
        livro.categoria = request.form['categoria']

        db.session.commit()

        return redirect('/livros')

    return render_template(
        'editar_livro.html',
        livro=livro
    )

# excluir livros

@app.route('/excluir-livro/<int:id>')
def excluir_livro(id):

    if not session.get('admin'):
        return redirect('/login')

    livro = Livro.query.get_or_404(id)

    db.session.delete(livro)
    db.session.commit()

    return redirect('/livros')

if __name__ == '__main__':
    app.run(debug=True)