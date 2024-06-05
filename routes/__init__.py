from flask import Blueprint

# Crie um Blueprint para as rotas
routes_blueprint = Blueprint('routes', __name__)

# Importe as rotas dos arquivos individuais
from .Usuarios.usuariosJonhField import usuarios_routesJohn
from .Clientes.clenteJohnField import cliente_routesJohn
from .Categorias.categoriaJohnField import categoria_routesJohn
from .Fases.FaseJohnField import fase_routesJohn
from .Tamanhos.gradePadrao import gradePadrao_routesJohn
from .Ops.GeracaoOP import GeraoOP_routesJohn
from .Ops.MovimentacaoOP import MovimentaoOP_routesJohn
from .Ops.Formulario import formulario_routesJohn
from .Fases.RoteiroPadrao import roteiroPadrao_routesJohn
from .Dashboard.Dashboard import Dashboard_routesJohn
from .Operacoes.operacao import operacao_routesJohn
from .Ops.EstornarMovimentacao import EstornoOP_routesJohn

# Registre as rotas nos blueprints
routes_blueprint.register_blueprint(usuarios_routesJohn)
routes_blueprint.register_blueprint(cliente_routesJohn)
routes_blueprint.register_blueprint(categoria_routesJohn)
routes_blueprint.register_blueprint(fase_routesJohn)
routes_blueprint.register_blueprint(gradePadrao_routesJohn)
routes_blueprint.register_blueprint(GeraoOP_routesJohn)
routes_blueprint.register_blueprint(MovimentaoOP_routesJohn)
routes_blueprint.register_blueprint(formulario_routesJohn)
routes_blueprint.register_blueprint(roteiroPadrao_routesJohn)
routes_blueprint.register_blueprint(Dashboard_routesJohn)
routes_blueprint.register_blueprint(operacao_routesJohn)
routes_blueprint.register_blueprint(EstornoOP_routesJohn)
