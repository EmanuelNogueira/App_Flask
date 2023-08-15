from flask import Flask, render_template, request, redirect, session, flash, url_for

# Request = Ajuda a pegar as informações do formulário
# Redirect = Função de redirecionamento
# Session = Retenha informações por mais de um ciclo de request (Quardando informações nos cookies do navegador)


# class =  Criando um objeto ----
class Jogo:
    # "__init__" é o construtor de classe, e é executado quando um objeto é criado
    # É o parâmetro do método em Python quando criado um objeto, usado para acessar o nosso objeto através de algum outro nome ou outro parâmetro.
    def __init__(self, problema, setor, descricao):
        self.problema = problema
        self.setor = setor
        self.descricao = descricao


# Parâmetros Globais
jogo1 = Jogo("Alteração da logo", "Tecnologia", "A logo foi mudada mas o site ainda não está atualizado.")
jogo2 = Jogo("Mudança na Nav", "Saúde", "A nav precisa ser alterada pois não há responsividade.")
jogo3 = Jogo("Novo site", "Saúde", "É necessário a cração do novo site para o fluxo de pacientes.")

# Lista para lista.HTML
lista = [jogo1, jogo2, jogo3]

# Users 
class Usuario: 
    def __init__(self, nome, nickname, senha):
        self.nome = nome 
        self.nickname = nickname 
        self.senha = senha 

usuario1 = Usuario("Emanuel Pinto Nogueira", "Manel", "manel16")    
usuario2 = Usuario("Maria Cristina", "Cris", "maria778")   
usuario3 = Usuario("Felipe Rocha", "Lipe", "felipe676")  

# dicionário com todos os itens 
usuarios = { usuario1.nickname : usuario1, usuario2.nickname : usuario2, usuario3.nickname : usuario3}


app = Flask(__name__)  # Garante rodar o app
# É necessário essa chave de autenticação (criptografia) pois assim outro usuário não poderá alterar as informações de outros usuários
# Podemos dar qualquer nome para essa chave
app.secret_key = "relampagomarquinhos"


@app.route("/")
def home():
    if "usuario_logado" not in session or session["usuario_logado"] == None:
        return render_template("Lista.html", titulo="Lista de Chamadas", jogos=lista, user="Fazer Login")   
    else:
        return render_template("Lista.html", titulo="Lista de Chamadas", jogos=lista, user="Fazer Logout")    


@app.route("/new")
def new():
    # Se não houver uma  chave "usuário_logado" não sessão (Que está como uma chave no meu "Autenticar"), ele não será logado e será enviado para a página de login
    # Ou se o "usuario logado == None" (Na qual está no meu Logout) ele será redirecionado para a página de de 'Login'.
    if "usuario_logado" not in session or session["usuario_logado"] == None:
        flash("Faça o login para continuar")
        return redirect(url_for('login', proxima=url_for('new')))
    return render_template("new.html", titulo="Nova Chamada")


# "Criar" é uma página de meio termo
@app.route(
    "/criar",
    methods=[
        "POST",
    ],
)  # Flask como padrão só coloca que aceita o método como "GET" e  tem que falar que ele tem que aceitar o método "POST"
def criar():
    problema = request.form["problema"]
    setor = request.form["setor"]
    descricao = request.form["descricao"]

    # Criando um objeto
    jogo = Jogo(problema, setor, descricao)

    # Append = Adicionar algo dentro de uma lista
    lista.append(jogo)

    # Redirecionar de volta para a página de listagem após a criação
    return redirect(url_for('home'))


@app.route("/login")
def login():
    # Pegando as informações da próxima página
    proxima = request.args.get("proxima")
    
    if "usuario_logado" not in session or session["usuario_logado"] == None:
        return render_template("login.html", proxima=proxima)
    else:
        return redirect(url_for('logout'))
    

# Essa rota verifica se realmente estarei hapto a logar em meu "login"
@app.route(
    "/autenticar",
    methods=[
        "POST",
    ],
)  # vai verificar credenciais corretas do usuário
def autenticar():

#Fará uma verificação para ver e autenticar corretamente meu usuário
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + " logado com sucesso ")
            proxima_pagina = request.form["proxima"]
            return redirect(url_for('home'))
        else:
            flash("Senha incorreta")
            return redirect(url_for('login'))
    else:
        # Caso falhe:
        flash("Usuário não encontrado")
        return redirect(url_for('login'))


@app.route("/logout")
def logout():
    # Tirar o Login do usuário
    session["usuario_logado"] = None
    flash("Logout efetuado com sucesso!")
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
