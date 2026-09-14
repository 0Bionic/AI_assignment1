import courierDelivery
import robotNavigation
import search

def run_comparative_analysis(test_cases):
    print("==========================================================")
    print(" SEARCH ALGORITHM COMPARATIVE ANALYSIS")
    print("==========================================================")
    
    for case_name, problem in test_cases:
        print("\nTest Case: " + case_name)
        print("-" * 58)
        
        # Run both searches
        d_path, d_nodes, d_cost = search.dijkstraSearch(problem)
        a_path, a_nodes, a_cost = search.aStarSearch(problem)
        
        # Format the start state into the path if it's a Courier problem (string state)
        start_state = problem.getStartState()
        if isinstance(start_state, str): 
            d_route = start_state + " ➔ " + " ➔ ".join(d_path)
            a_route = start_state + " ➔ " + " ➔ ".join(a_path)
        else:
            d_route = ", ".join(d_path)
            a_route = ", ".join(a_path)
        
        # Print Dijkstra Results
        print("Algorithm : Dijkstra")
        print("Cost      : " + str(d_cost))
        print("Expanded  : " + str(d_nodes))
        print("Route     : " + d_route)
        print()
        
        # Print A* Results
        print("Algorithm : A*")
        print("Cost      : " + str(a_cost))
        print("Expanded  : " + str(a_nodes))
        print("Route     : " + a_route)
        print("==========================================================")




# Run the script
# run_comparative_analysis(test_cases)

def __init__():

    # ---------------------------------------------------------
    # Test Case Setup
    # ---------------------------------------------------------

    # 1. Robot Navigation Grids
    obstacles_none = []
    obstacles_simple_wall = [(2, 1), (2, 2), (2, 3)]
    obstacles_maze_trap = [(1, 1), (2, 1), (3, 1), (3, 2), (3, 3), (2, 3)]

    # 2. CSV File Paths (ensure these match your local files)
    conn_file = '../csv/connections.csv'
    heur_file = '../csv/heuristics.csv'
    track_file = '../csv/trackType.csv'

    test_cases = [
        # Robot Navigation Tests
        ("Robot: Clear Grid (0,4 to 6,0)", 
        robotNavigation.robotNavigation(7, 5, (0,4), (6,0), obstacles_none)),
        
        ("Robot: Simple Wall (0,2 to 6,2)", 
        robotNavigation.robotNavigation(7, 5, (0,2), (6,2), obstacles_simple_wall)),
        
        ("Robot: Maze Trap (0,2 to 4,2)", 
        robotNavigation.robotNavigation(5, 5, (0,2), (4,2), obstacles_maze_trap)),

        # Courier Delivery Tests
        ("Courier: South to East (Saddar to Korangi)", 
        courierDelivery.courierDelivery('Saddar (Hub)', 'Korangi', conn_file, heur_file, track_file, True)),
        
        ("Courier: West to Central (Orangi Town to DHA)", 
        courierDelivery.courierDelivery('Orangi Town', 'DHA', conn_file, heur_file, track_file, True)),
        
        ("Courier: Cross-City (Lyari to Gulistan-e-Johar)", 
        courierDelivery.courierDelivery('Lyari', 'Gulistan-e-Johar', conn_file, heur_file, track_file, True))
    ]

    print(search.searchWithStopovers(courierDelivery.courierDelivery('Saddar (Hub)', 'Korangi', conn_file, heur_file, track_file, True), ['FB Area', 'Gulistan-e-Johar', 'Korangi', 'Orangi Town', 'PECHS']))
    
    # run_comparative_analysis(test_cases)

__init__()