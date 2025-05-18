from flask import render_template
from controllers.uninformed_controller import get_bfs_stats, get_dfs_stats, get_ucs_stats, get_iddfs_stats
from controllers.informed_controller import get_greedy_stats, get_astar_stats, get_idastar_stats, get_beam_stats
from controllers.local_search_controller import (
    get_simple_hill_climbing_stats, get_steepest_hill_climbing_stats,
    get_stochastic_hill_climbing_stats, get_simulated_annealing_stats
)
from controllers.uninformed_controller import get_bfs_stats, get_dfs_stats, get_ucs_stats, get_iddfs_stats

def compare_uninformed_controller():
    algorithm_stats = {}
    
    # BFS
    bfs_stats = get_bfs_stats()
    if bfs_stats['nodes_explored'] > 0:  # Only include if search was successful
        algorithm_stats['BFS'] = bfs_stats
        
    # DFS
    dfs_stats = get_dfs_stats()
    if dfs_stats['nodes_explored'] > 0:
        algorithm_stats['DFS'] = dfs_stats
        
    # UCS
    ucs_stats = get_ucs_stats()
    if ucs_stats['nodes_explored'] > 0:
        algorithm_stats['UCS'] = ucs_stats
        
    # IDDFS
    iddfs_stats = get_iddfs_stats()
    if iddfs_stats['nodes_explored'] > 0:
        algorithm_stats['IDDFS'] = iddfs_stats
    
    return render_template('compare_uninformed.html',
                         algorithm_stats=algorithm_stats)

def compare_informed_controller():
    algorithm_stats = {}
    
    # Greedy
    greedy_stats = get_greedy_stats()
    if greedy_stats['nodes_explored'] > 0:
        algorithm_stats['Greedy'] = greedy_stats
        
    # A*
    astar_stats = get_astar_stats()
    if astar_stats['nodes_explored'] > 0:
        algorithm_stats['A*'] = astar_stats
        
    # IDA*
    idastar_stats = get_idastar_stats()
    if idastar_stats['nodes_explored'] > 0:
        algorithm_stats['IDA*'] = idastar_stats
    
    
    return render_template('compare_informed.html',
                         algorithm_stats=algorithm_stats)

def compare_local_search_controller():
    
    algorithm_stats = {}
    
    # Simple Hill Climbing
    shc_stats = get_simple_hill_climbing_stats()
    if shc_stats['nodes_explored'] > 0:
        algorithm_stats['Simple Hill Climbing'] = shc_stats
        
    # Steepest Hill Climbing
    steepest_stats = get_steepest_hill_climbing_stats()
    if steepest_stats['nodes_explored'] > 0:
        algorithm_stats['Steepest Hill Climbing'] = steepest_stats
        
    # Stochastic Hill Climbing
    stochastic_stats = get_stochastic_hill_climbing_stats()
    if stochastic_stats['nodes_explored'] > 0:
        algorithm_stats['Stochastic Hill Climbing'] = stochastic_stats
        
    # Simulated Annealing
    sa_stats = get_simulated_annealing_stats()
    if sa_stats['nodes_explored'] > 0:
        algorithm_stats['Simulated Annealing'] = sa_stats
        
    beam_stats = get_beam_stats()
    if beam_stats['nodes_explored'] > 0:
        algorithm_stats['Beam Search'] = beam_stats
    
    return render_template('compare_local_search.html',
                         algorithm_stats=algorithm_stats)