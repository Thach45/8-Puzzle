from flask import Blueprint, render_template
from controllers.uninformed_controller import home_controller,bfs_controller, dfs_controller, ucs_controller, iddfs_controller


home_routes_bp = Blueprint('home_routes', __name__)
bfs_routes_bp =  Blueprint('bfs_routes', __name__)
dfs_routes_bp =  Blueprint('dfs_routes', __name__)
ucs_routes_bp =  Blueprint('ucs_routes', __name__)
iddfs_routes_bp =  Blueprint('iddfs_routes', __name__)

@home_routes_bp.route('/')
def home():
    return home_controller()

@bfs_routes_bp.route('/bfs')
def bfs():
    return bfs_controller()
@dfs_routes_bp.route('/dfs')
def dfs():
    return dfs_controller()
@ucs_routes_bp.route('/ucs')
def ucs():
    return ucs_controller()
@iddfs_routes_bp.route('/iddfs')
def iddfs():
    return iddfs_controller()
