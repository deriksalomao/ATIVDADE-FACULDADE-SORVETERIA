from config import db
from config import app

class Categorias(db.Model):
    __tablename__ = 'categorias'
    Id = db.Column(db.Integer, primary_key=True)
    Categoria = db.Column(db.String(100), nullable=False)

    def __init__(self, Categoria):
        self.Categoria = Categoria

    def to_dict(self):
        return {'Id': self.Id, 'Categoria': self.Categoria}

class Sorvetes(db.Model):
    __tablename__ = 'sorvetes'
    Id = db.Column(db.Integer, primary_key=True)
    Sabor = db.Column(db.String(100), nullable=False)
    Categoria_Id = db.Column(db.Integer, db.ForeignKey('categorias.Id'), nullable=False)
    Preco = db.Column(db.Float, nullable=False)
    Quantidade = db.Column(db.Integer, nullable=False)

    categoria = db.relationship('Categorias', backref=db.backref('sorvetes', lazy=True))

    def __init__(self, Sabor, Categoria_Id, Preco, Quantidade):
        self.Sabor = Sabor
        self.Categoria_Id = Categoria_Id
        self.Preco = Preco
        self.Quantidade = Quantidade

    def to_dict(self):
        return {
            'Id': self.Id,
            'Sabor': self.Sabor,
            'Categoria_Id': self.Categoria_Id,
            'Preco': self.Preco,
            'Quantidade': self.Quantidade,
            'Categoria': self.categoria.Categoria
        }

class SorveteNaoEncontrado(Exception):
    pass

def get_sorvetes():
    sorvetes = Sorvetes.query.all()
    return [sorvete.to_dict() for sorvete in sorvetes]

def listar_categorias():
    categorias = Categorias.query.all()
    return [categoria.to_dict() for categoria in categorias]

def get_sorvete_byId(id_sorvete):
    sorvete = Sorvetes.query.get(id_sorvete)
    if not sorvete:
        raise SorveteNaoEncontrado
    return sorvete.to_dict()

def get_categoria_byId(id_categoria):
    categoria = Categorias.query.get(id_categoria)
    if not categoria:
        raise SorveteNaoEncontrado
    return categoria.to_dict()

def delete_sorvete(id_sorvete):
    sorvete = Sorvetes.query.get(id_sorvete)
    if not sorvete:
        raise SorveteNaoEncontrado
    db.session.delete(sorvete)
    db.session.commit()

def del_cetegoria(id_categoria):
    categoria = Categorias.query.get(id_categoria)
    if not categoria:
        raise SorveteNaoEncontrado
    db.session.delete(categoria)
    db.session.commit()

def adicionar_categoria(nome_categoria):
    with app.app_context():
        categoria = Categorias(Categoria=nome_categoria)
        db.session.add(categoria)
        db.session.commit()

def post_sorvete(sabor, categoria_id, preco, quantidade):
    with app.app_context():
        sorvete = Sorvetes(Sabor=sabor, Categoria_Id=categoria_id, Preco=preco, Quantidade=quantidade)
        db.session.add(sorvete)
        db.session.commit()

def atualizar_categoria(id_categoria, novos_dados):
    categoria = Categorias.query.get(id_categoria)
    if not categoria:
        raise SorveteNaoEncontrado
    categoria.Categoria = novos_dados['Categoria']  
    db.session.commit() 

def atualizar_sorvete(id_sorvete, sabor, categoria_id, preco, quantidade):
    sorvete = Sorvetes.query.get(id_sorvete)
    if not sorvete:
        raise SorveteNaoEncontrado
    sorvete.Sabor = sabor
    sorvete.Categoria_Id = categoria_id
    sorvete.Preco = preco
    sorvete.Quantidade = quantidade
    db.session.commit()