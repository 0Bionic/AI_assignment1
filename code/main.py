import search
import util
import robotNavigation
import courierDelivery

def run_comparative_analysis(test_cases):
    # Print the table header
    print(f"{'Test Case':<18} | {'Algorithm':<10} | {'Cost':<5} | {'Expanded':<9} | {'Route (First 4 Moves)'}")
    print("-" * 75)
    
    for case_name, problem in test_cases:
        # Run both searches
        d_path, d_nodes, d_cost = search.dijkstraSearch(problem)
        a_path, a_nodes, a_cost = search.aStarSearch(problem)
        
        # Format routes for clean terminal display (truncate long paths)
        d_route_snip = ", ".join(d_path) + ("")
        a_route_snip = ", ".join(a_path) + ("")
        
        # Print results row for Dijkstra
        print(f"{case_name:<18} | {'Dijkstra':<10} | {d_cost:<5} | {d_nodes:<9} | {d_route_snip}")
        # Print results row for A* (leaving test case name blank for readability)
        print(f"{'':<18} | {'A*':<10} | {a_cost:<5} | {a_nodes:<9} | {a_route_snip}")
        print("-" * 75)

# Example Usage:
# test_cases = [
#     ("Robot: Corner", RobotNavigation(7, 5, (0,4), (6,0), obstacles)),
#     ("Robot: Middle", RobotNavigation(7, 5, (3,2), (6,0), obstacles))
# ]
# run_comparative_analysis(test_cases)

def main():
    height = 5
    width = 7
    start_pos_1 = (0,4)
    goal_pos = (6,0)

    obstacle_locations = [(0,3), (1,1), (1,3), (2,1), (3,1), (3,3), (3,4), (5,2), (5,0), (5,3)]

    robot = robotNavigation.robotNavigation(width, height, start_pos_1, goal_pos, obstacle_locations, True)
    robot.printCurrentState()
    print("Successors= " + str(robot.getSuccessors(start_pos_1)))
    print("h(n)= " + str(robot.getHeuristic(start_pos_1)))
    print(robot.getCostOfActions(['right', 'right', 'down', 'down', 'down'])) #incorrect path, should print -1
    print(robot.getCostOfActions(['right', 'right', 'down', 'down', 'right', 'right', 'down', 'right', 'right', 'down']))

    dijkstra_result = search.dijkstraSearch(robot)
    aStar_result = search.aStarSearch(robot)
    print(dijkstra_result)
    print(aStar_result)

    test_cases = [
    ("Robot: Corner", robotNavigation.robotNavigation(7, 5, (0,4), (6,0), obstacle_locations)),
    ("Robot: Middle", robotNavigation.robotNavigation(7, 5, (3,2), (6,0), obstacle_locations))
    ]
    # run_comparative_analysis(test_cases)

    
    return 0

main()