import os

import courierDelivery
import robotNavigation
import search

# CSV paths (relative to this file)
code_dir = os.path.dirname(os.path.abspath(__file__))
csv_dir = os.path.join(code_dir, "..", "csv")
conn_file = os.path.join(csv_dir, "Connections.csv")
heur_file = os.path.join(csv_dir, "heuristics.csv")
track_file = os.path.join(csv_dir, "TrackType.csv")


def format_route(problem, path):
    start = problem.getStartState()
    if isinstance(start, str):
        # Courier: states are area names, actions are destinations
        if not path:
            return start
        return start + " -> " + " -> ".join(path)
    # Robot: start is a (x, y) coordinate, actions are move names
    if not path:
        return str(start)
    return str(start) + " | " + ", ".join(path)


def run_one_comparison(case_name, dijkstra_problem, astar_problem):
    d_path, d_nodes, d_cost = search.dijkstraSearch(dijkstra_problem)
    a_path, a_nodes, a_cost = search.aStarSearch(astar_problem)

    d_route = format_route(dijkstra_problem, d_path)
    a_route = format_route(astar_problem, a_path)

    print()
    print("=" * 60)
    print("Test Case: " + case_name)
    print("-" * 60)

    print("Algorithm : Dijkstra")
    print("Cost      : " + str(d_cost))
    print("Expanded  : " + str(d_nodes))
    print("Route     : " + d_route)
    print()
    print("Algorithm : A*")
    print("Cost      : " + str(a_cost))
    print("Expanded  : " + str(a_nodes))
    print("Route     : " + a_route)
    print()
    print("Same cost?        : " + str(d_cost == a_cost or abs(float(d_cost) - float(a_cost)) < 0.0001))
    print("Nodes saved by A* : " + str(d_nodes - a_nodes))
    print("=" * 60)

    return {
        "name": case_name,
        "d_cost": d_cost,
        "a_cost": a_cost,
        "d_nodes": d_nodes,
        "a_nodes": a_nodes,
    }


def show_heuristic_effect(case_name, problem_without_h, problem_with_h):
    path0, nodes0, cost0 = search.aStarSearch(problem_without_h)
    path1, nodes1, cost1 = search.aStarSearch(problem_with_h)

    print()
    print("~" * 60)
    print("Heuristic Effect: " + case_name)
    print("-" * 60)
    print("A* WITHOUT heuristic (h = 0):")
    print("  Cost     : " + str(cost0))
    print("  Expanded : " + str(nodes0))
    print("A* WITH heuristic:")
    print("  Cost     : " + str(cost1))
    print("  Expanded : " + str(nodes1))
    print("Cost unchanged?       : " + str(abs(float(cost0) - float(cost1)) < 0.0001))
    print("Fewer nodes with heur : " + str(nodes0 - nodes1))
    print("Route (with heuristic): " + format_route(problem_with_h, path1))
    print("~" * 60)

    return {
        "name": case_name,
        "cost_no_h": cost0,
        "cost_with_h": cost1,
        "nodes_no_h": nodes0,
        "nodes_with_h": nodes1,
    }


def print_summary(title, results):
    print()
    print("#" * 60)
    print(title)
    print("#" * 60)
    for r in results:
        print()
        print("Case          : " + r["name"])
        print("Dijkstra cost : " + str(r["d_cost"]) + "  |  A* cost : " + str(r["a_cost"]))
        print("Dijkstra exp  : " + str(r["d_nodes"]) + "  |  A* exp  : " + str(r["a_nodes"]))
        print("Nodes saved   : " + str(r["d_nodes"] - r["a_nodes"]))
    print("#" * 60)


def main():
    print("=" * 60)
    print("COMPARATIVE ANALYSIS: A* vs Dijkstra")
    print("=" * 60)

    robot_results = []
    courier_results = []
    heuristic_results = []

    # Obstacle layouts for robot tests
    obstacles_none = []
    obstacles_wall = [(2, 1), (2, 2), (2, 3)]
    obstacles_maze = [(1, 1), (2, 1), (3, 1), (3, 2), (3, 3), (2, 3)]
    obstacles_cluttered = [
        (0, 3), (1, 1), (1, 3), (2, 1), (3, 1),
        (3, 3), (3, 4), (5, 2), (5, 0), (5, 3),
    ]

    # -------------------------------------------------
    # DOMAIN 1: Robot Navigation
    # -------------------------------------------------
    print()
    print("#" * 60)
    print("DOMAIN 1: Robot Navigation")
    print("#" * 60)

    # For each case: Dijkstra gets needs_heuristic=False,
    # A* gets needs_heuristic=True (Euclidean distance).

    robot_results.append(run_one_comparison(
        "Robot: Clear grid (0,4) -> (6,0)",
        robotNavigation.robotNavigation(7, 5, (0, 4), (6, 0), obstacles_none, False),
        robotNavigation.robotNavigation(7, 5, (0, 4), (6, 0), obstacles_none, True),
    ))

    robot_results.append(run_one_comparison(
        "Robot: Wall barrier (0,2) -> (6,2)",
        robotNavigation.robotNavigation(7, 5, (0, 2), (6, 2), obstacles_wall, False),
        robotNavigation.robotNavigation(7, 5, (0, 2), (6, 2), obstacles_wall, True),
    ))

    robot_results.append(run_one_comparison(
        "Robot: Maze trap (0,2) -> (4,2)",
        robotNavigation.robotNavigation(5, 5, (0, 2), (4, 2), obstacles_maze, False),
        robotNavigation.robotNavigation(5, 5, (0, 2), (4, 2), obstacles_maze, True),
    ))

    robot_results.append(run_one_comparison(
        "Robot: Cluttered (0,4) -> (6,0)",
        robotNavigation.robotNavigation(7, 5, (0, 4), (6, 0), obstacles_cluttered, False),
        robotNavigation.robotNavigation(7, 5, (0, 4), (6, 0), obstacles_cluttered, True),
    ))

    robot_results.append(run_one_comparison(
        "Robot: Short hop (1,1) -> (3,3)",
        robotNavigation.robotNavigation(7, 5, (1, 1), (3, 3), obstacles_none, False),
        robotNavigation.robotNavigation(7, 5, (1, 1), (3, 3), obstacles_none, True),
    ))

    robot_results.append(run_one_comparison(
        "Robot: Corner to corner (0,0) -> (6,4)",
        robotNavigation.robotNavigation(7, 5, (0, 0), (6, 4), obstacles_wall, False),
        robotNavigation.robotNavigation(7, 5, (0, 0), (6, 4), obstacles_wall, True),
    ))

    # Heuristic effect on a few robot cases
    heuristic_results.append(show_heuristic_effect(
        "Robot: Cluttered (0,4) -> (6,0)",
        robotNavigation.robotNavigation(7, 5, (0, 4), (6, 0), obstacles_cluttered, False),
        robotNavigation.robotNavigation(7, 5, (0, 4), (6, 0), obstacles_cluttered, True),
    ))
    heuristic_results.append(show_heuristic_effect(
        "Robot: Short hop (1,1) -> (3,3)",
        robotNavigation.robotNavigation(7, 5, (1, 1), (3, 3), obstacles_none, False),
        robotNavigation.robotNavigation(7, 5, (1, 1), (3, 3), obstacles_none, True),
    ))

    # -------------------------------------------------
    # DOMAIN 2: Courier Delivery
    # -------------------------------------------------
    print()
    print("#" * 60)
    print("DOMAIN 2: Courier Delivery")
    print("#" * 60)

    courier_results.append(run_one_comparison(
        "Courier: Saddar (Hub) -> Korangi",
        courierDelivery.courierDelivery("Saddar (Hub)", "Korangi", conn_file, heur_file, track_file, False),
        courierDelivery.courierDelivery("Saddar (Hub)", "Korangi", conn_file, heur_file, track_file, True),
    ))

    courier_results.append(run_one_comparison(
        "Courier: Orangi Town -> DHA",
        courierDelivery.courierDelivery("Orangi Town", "DHA", conn_file, heur_file, track_file, False),
        courierDelivery.courierDelivery("Orangi Town", "DHA", conn_file, heur_file, track_file, True),
    ))

    courier_results.append(run_one_comparison(
        "Courier: Lyari -> Gulistan-e-Johar",
        courierDelivery.courierDelivery("Lyari", "Gulistan-e-Johar", conn_file, heur_file, track_file, False),
        courierDelivery.courierDelivery("Lyari", "Gulistan-e-Johar", conn_file, heur_file, track_file, True),
    ))

    courier_results.append(run_one_comparison(
        "Courier: Clifton -> North Nazimabad",
        courierDelivery.courierDelivery("Clifton", "North Nazimabad", conn_file, heur_file, track_file, False),
        courierDelivery.courierDelivery("Clifton", "North Nazimabad", conn_file, heur_file, track_file, True),
    ))

    courier_results.append(run_one_comparison(
        "Courier: Malir -> PECHS",
        courierDelivery.courierDelivery("Malir", "PECHS", conn_file, heur_file, track_file, False),
        courierDelivery.courierDelivery("Malir", "PECHS", conn_file, heur_file, track_file, True),
    ))

    courier_results.append(run_one_comparison(
        "Courier: SITE Area -> Gulshan-e-Iqbal",
        courierDelivery.courierDelivery("SITE Area", "Gulshan-e-Iqbal", conn_file, heur_file, track_file, False),
        courierDelivery.courierDelivery("SITE Area", "Gulshan-e-Iqbal", conn_file, heur_file, track_file, True),
    ))

    courier_results.append(run_one_comparison(
        "Courier: Baldia Town -> II Chundrigar Road",
        courierDelivery.courierDelivery("Baldia Town", "II Chundrigar Road", conn_file, heur_file, track_file, False),
        courierDelivery.courierDelivery("Baldia Town", "II Chundrigar Road", conn_file, heur_file, track_file, True),
    ))

    # Heuristic effect on a few courier cases
    heuristic_results.append(show_heuristic_effect(
        "Courier: Saddar (Hub) -> Korangi",
        courierDelivery.courierDelivery("Saddar (Hub)", "Korangi", conn_file, heur_file, track_file, False),
        courierDelivery.courierDelivery("Saddar (Hub)", "Korangi", conn_file, heur_file, track_file, True),
    ))
    heuristic_results.append(show_heuristic_effect(
        "Courier: Lyari -> Gulistan-e-Johar",
        courierDelivery.courierDelivery("Lyari", "Gulistan-e-Johar", conn_file, heur_file, track_file, False),
        courierDelivery.courierDelivery("Lyari", "Gulistan-e-Johar", conn_file, heur_file, track_file, True),
    ))

    # -------------------------------------------------
    # Summaries
    # -------------------------------------------------
    print_summary("SUMMARY - Robot Navigation", robot_results)
    print_summary("SUMMARY - Courier Delivery", courier_results)

    print()
    print("#" * 60)
    print("SUMMARY - Heuristic Effect on A*")
    print("#" * 60)
    for h in heuristic_results:
        print()
        print("Case              : " + h["name"])
        print("Cost without h    : " + str(h["cost_no_h"]))
        print("Cost with h       : " + str(h["cost_with_h"]))
        print("Expanded without h: " + str(h["nodes_no_h"]))
        print("Expanded with h   : " + str(h["nodes_with_h"]))
    print("#" * 60)

    print()
    print("Analysis complete.")


if __name__ == "__main__":
    main()