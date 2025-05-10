from flask import Flask
from routes.home_routes import (
    home_routes_bp, bfs_routes_bp, dfs_routes_bp, ucs_routes_bp, iddfs_routes_bp,
    greedy_routes_bp, a_star_routes_bp, ida_star_routes_bp, beam_search_routes_bp,
    simple_hill_climbing_routes_bp, steepest_hill_climbing_routes_bp,
    simulated_annealing_routes_bp, stochastic_hill_climbing_routes_bp,
    and_or_routes_bp, no_observation_routes_bp, partial_observation_routes_bp,
    forward_checking_routes_bp, backtracking_routes_bp
)

app = Flask(__name__, template_folder='views')
app.register_blueprint(home_routes_bp)

# Uninformed Search
app.register_blueprint(bfs_routes_bp)
app.register_blueprint(dfs_routes_bp)
app.register_blueprint(ucs_routes_bp)
app.register_blueprint(iddfs_routes_bp)

# Informed Search
app.register_blueprint(greedy_routes_bp)
app.register_blueprint(a_star_routes_bp)
app.register_blueprint(ida_star_routes_bp)
app.register_blueprint(beam_search_routes_bp)

# Local Search
app.register_blueprint(simple_hill_climbing_routes_bp)
app.register_blueprint(steepest_hill_climbing_routes_bp)
app.register_blueprint(simulated_annealing_routes_bp)
app.register_blueprint(stochastic_hill_climbing_routes_bp)

# Advanced Search
app.register_blueprint(and_or_routes_bp)
app.register_blueprint(no_observation_routes_bp)
app.register_blueprint(partial_observation_routes_bp)

# Constraint Satisfaction Problems
app.register_blueprint(forward_checking_routes_bp)
app.register_blueprint(backtracking_routes_bp)
if __name__ == '__main__':
    app.run(debug=True)