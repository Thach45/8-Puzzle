from flask import Blueprint, render_template
from controllers.uninformed_controller import home_controller,bfs_controller, dfs_controller, ucs_controller, iddfs_controller
from controllers.andor_search_controller import andor_controller
from controllers.compare_controller import compare_uninformed_controller, compare_informed_controller, compare_local_search_controller
from controllers.no_observation_controller import no_observation_controller
from controllers.partial_observation_controller import partial_observation_controller
from controllers.informed_controller import greedy_controller, a_star_controller, ida_star_controller, beam_search_controller
from controllers.local_search_controller import simple_hill_climbing_controller, steepest_hill_climbing_controller, simulated_annealing_controller, stochastic_hill_climbing_controller
from controllers.forward_checking_controller import forward_checking_controller

home_routes_bp = Blueprint('home_routes', __name__)
bfs_routes_bp = Blueprint('bfs_routes', __name__)
dfs_routes_bp = Blueprint('dfs_routes', __name__)
ucs_routes_bp = Blueprint('ucs_routes', __name__)
backtracking_routes_bp = Blueprint('backtracking_routes', __name__)
iddfs_routes_bp = Blueprint('iddfs_routes', __name__)
greedy_routes_bp = Blueprint('greedy_routes', __name__)
a_star_routes_bp = Blueprint('a_star_routes', __name__)
ida_star_routes_bp = Blueprint('ida_star_routes', __name__)
beam_search_routes_bp = Blueprint('beam_search_routes', __name__)
simple_hill_climbing_routes_bp = Blueprint('simple_hill_climbing_routes', __name__)
steepest_hill_climbing_routes_bp = Blueprint('steepest_hill_climbing_routes', __name__)
simulated_annealing_routes_bp = Blueprint('simulated_annealing_routes', __name__)
stochastic_hill_climbing_routes_bp = Blueprint('stochastic_hill_climbing_routes', __name__)
and_or_routes_bp = Blueprint('and_or_routes', __name__)
no_observation_routes_bp = Blueprint('no_observation_routes', __name__)
partial_observation_routes_bp = Blueprint('partial_observation_routes', __name__)
forward_checking_routes_bp = Blueprint('forward_checking_routes', __name__)
ac_3_routes_bp = Blueprint('ac_3_routes', __name__)
q_learning_routes_bp = Blueprint('q_learning_routes', __name__)
compare_uninformed_routes_bp = Blueprint('compare_uninformed_routes', __name__)
compare_informed_routes_bp = Blueprint('compare_informed_routes', __name__)
compare_local_search_routes_bp = Blueprint('compare_local_search_routes', __name__)

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

@greedy_routes_bp.route('/greedy')
def greedy():
    return greedy_controller()

@a_star_routes_bp.route('/a-star')
def a_star():
    return a_star_controller()

@ida_star_routes_bp.route('/ida-star')
def ida_star():
    return ida_star_controller()

@beam_search_routes_bp.route('/beam')
def beam_search():
    return beam_search_controller()

@simple_hill_climbing_routes_bp.route('/simple-hill-climbing')
def simple_hill_climbing():
    return simple_hill_climbing_controller()

@steepest_hill_climbing_routes_bp.route('/steepest-hill-climbing')
def steepest_hill_climbing():
    return steepest_hill_climbing_controller()

@simulated_annealing_routes_bp.route('/simulated-annealing')
def simulated_annealing():
    return simulated_annealing_controller()

@stochastic_hill_climbing_routes_bp.route('/stochastic-hill-climbing')
def stochastic_hill_climbing():
    return stochastic_hill_climbing_controller()

# @and_or_routes_bp.route('/and-or')
# def and_or():
#     return andor_controller()

@and_or_routes_bp.route('/and-or')
def and_or_tree():
    # return andor_controller()
    return render_template('and-or.html')

@no_observation_routes_bp.route('/no-observation')
def no_observation():
    return no_observation_controller()

@partial_observation_routes_bp.route('/partial-observation')
def partial_observation():
    # return partial_observation_controller()
    return render_template('partial_observation.html')
@forward_checking_routes_bp.route('/forward-checking')
def forward_checking():
    return forward_checking_controller()
@backtracking_routes_bp.route('/backtracking')
def backtracking():
    return render_template('backtracking.html')
@ac_3_routes_bp.route('/ac3')
def ac_3():
    return render_template('ac-3.html')
@q_learning_routes_bp.route('/q-learning')
def q_learning():
    return render_template('q-learning.html')

@compare_uninformed_routes_bp.route('/compare/uninformed')
def compare_uninformed():
    return compare_uninformed_controller()

@compare_informed_routes_bp.route('/compare/informed')
def compare_informed():
    return compare_informed_controller()

@compare_local_search_routes_bp.route('/compare/local-search')
def compare_local_search():
    return compare_local_search_controller()
