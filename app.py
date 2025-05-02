from flask import Flask
from routes.home_routes import home_routes_bp, bfs_routes_bp, dfs_routes_bp, ucs_routes_bp, iddfs_routes_bp

app = Flask(__name__, template_folder='views')
app.register_blueprint(home_routes_bp)
app.register_blueprint(bfs_routes_bp)
app.register_blueprint(dfs_routes_bp)
app.register_blueprint(ucs_routes_bp)
app.register_blueprint(iddfs_routes_bp)

if __name__ == '__main__':
    app.run(debug=True)