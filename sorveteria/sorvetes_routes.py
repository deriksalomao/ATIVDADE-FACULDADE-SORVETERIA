from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from .sorvetes_model import SorveteNaoEncontrado, get_sorvetes, listar_categorias, post_sorvete, adicionar_categoria, get_categoria_byId, delete_sorvete, del_cetegoria, atualizar_categoria, get_sorvete_byId,atualizar_sorvete

sorvetes_blueprint = Blueprint('sorveteria', __name__)

@sorvetes_blueprint.route('/', methods=['GET'])
def getIndex():
    return "TESTE"

@sorvetes_blueprint.route('/categorias', methods=['GET'])
def get_categorias():
    try:
        categorias = listar_categorias()
        return render_template("categoria.html", categorias=categorias)
    except SorveteNaoEncontrado:
        return "CATEGORIAS NÃO ENCONTRADAS"
    except Exception as e:
        return f"Erro: {e}"

@sorvetes_blueprint.route('/categorias/adicionar', methods=['GET'])
def add_categori_page():
    return render_template('criarCategorias.html')

@sorvetes_blueprint.route('/categorias', methods=['POST'])
def create_categoria():
    categoria = request.form['Categoria']
    adicionar_categoria(categoria)
    return redirect(url_for('sorveteria.get_categorias'))

@sorvetes_blueprint.route('/categorias/<int:id_categoria>', methods=['GET'])
def get_categoria(id_categoria):
    try:
        categoria = get_categoria_byId(id_categoria)
        return render_template('Categoria_id.html', categoria=categoria)
    except SorveteNaoEncontrado:
        return jsonify({'message': 'CATEGORIA NÃO ENCONTRADA'}), 404

@sorvetes_blueprint.route('/categorias/<int:id_categoria>/delete', methods=['POST'])
def delete_categoria(id_categoria):
    try:
        del_cetegoria(id_categoria)
        return redirect(url_for('sorveteria.get_categorias'))
    except SorveteNaoEncontrado:
        return jsonify({'message': 'CATEGORIA NÃO ENCONTRADA'}), 404

@sorvetes_blueprint.route('/categorias/<int:id_categoria>/editar', methods=['GET'])
def editar_categoria_page(id_categoria):
    try:
        categoria = get_categoria_byId(id_categoria)
        return render_template('Categoria_update.html', categoria=categoria)
    except SorveteNaoEncontrado:
        return jsonify({'message': 'CATEGORIA NÃO ENCONTRADA'}), 404

@sorvetes_blueprint.route('/categorias/<int:id_categoria>/update', methods=['POST'])
def update_categoria(id_categoria):
    if request.form.get('_method') == 'PUT':
        try:
            nome = request.form['Categoria']
            atualizar_categoria(id_categoria, {'Categoria': nome})
            return redirect(url_for('sorveteria.get_categoria', id_categoria=id_categoria))
        except SorveteNaoEncontrado:
            return jsonify({'message': 'CATEGORIA NÃO ENCONTRADA'}), 404
    else:
        return jsonify({'message': 'METÓDO NÃO PERMITIDO'}), 405

@sorvetes_blueprint.route('/sorvetes', methods=['GET'])
def get_sorvetes_route():
    try:
        sorvetes = get_sorvetes()
        return render_template("sorvete.html", sorvetes=sorvetes)
    except SorveteNaoEncontrado:
        return "SORVETES NÃO ENCONTRADOS"
    except Exception as e:
        return f"Erro: {e}"

@sorvetes_blueprint.route('/sorvetes/adicionar', methods=['GET'])
def add_sorvete_page():
    categorias = listar_categorias()
    return render_template('criarSorvetes.html', categorias=categorias)

@sorvetes_blueprint.route('/sorvetes', methods=['POST'])
def create_sorvete():
    sabor = request.form['Sabor']
    categoria_id = request.form['Categoria_Id']
    preco = request.form['Preco']
    quantidade = request.form['Quantidade']
    post_sorvete(sabor, categoria_id, preco, quantidade)
    return redirect(url_for('sorveteria.get_sorvetes_route'))

@sorvetes_blueprint.route('/sorvetes/<int:id_sorvete>', methods=['GET'])
def get_sorvete(id_sorvete):
    try:
        sorvete = get_sorvete_byId(id_sorvete)
        return render_template('Sorvete_id.html', sorvete=sorvete)
    except SorveteNaoEncontrado:
        return jsonify({'message': 'SORVETE NÃO ENCONTRADO'}), 404

@sorvetes_blueprint.route('/sorvetes/<int:id_sorvete>/delete', methods=['POST'])
def delete_sorvete_route(id_sorvete):
    try:
        delete_sorvete(id_sorvete)
        return redirect(url_for('sorveteria.get_sorvetes_route'))
    except SorveteNaoEncontrado:
        return jsonify({'message': 'SORVETE NÃO ENCONTRADO'}), 404
    
@sorvetes_blueprint.route('/sorvetes/<int:id_sorvete>/editar', methods=['GET'])
def editar_sorvete_page(id_sorvete):
    try:
        sorvete = get_sorvete_byId(id_sorvete)
        categorias = listar_categorias()  
        return render_template('Sorvete_update.html', sorvete=sorvete, categorias=categorias)
    except SorveteNaoEncontrado:
        return jsonify({'message': 'SORVETE NÃO ENCONTRADO'}), 404

@sorvetes_blueprint.route('/sorvetes/<int:id_sorvete>/update', methods=['POST'])
def update_sorvete(id_sorvete):
    if request.form.get('_method') == 'PUT':
        try:
            sabor = request.form['Sabor']
            categoria_id = request.form['Categoria_Id']
            preco = request.form['Preco']
            quantidade = request.form['Quantidade']
            atualizar_sorvete(id_sorvete, sabor, categoria_id, preco, quantidade)
            return redirect(url_for('sorveteria.get_sorvete', id_sorvete=id_sorvete))
        except SorveteNaoEncontrado:
            return jsonify({'message': 'SORVETE NÃO ENCONTRADO'}), 404
    else:
        return jsonify({'message': 'METÓDO NÃO PERMITIDO'}), 405
