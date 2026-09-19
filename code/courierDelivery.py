import util
import search

class courierDelivery(search.SearchProblem):

    def __init__(self, start_state, goal_state, connectionsFile, heuristicsFile, trackTypeFile, needsHeuristic = False):

        self.start_state = start_state
        self.goal_state = goal_state
        self.needsHeuristic = needsHeuristic
        self.vertices = []
        self.weights = { # Also depends on the track type's assumed speed limits
            'M': 1.0, # Main Roads/ Highways receive no penalty
            'S': 1.2, # Standard Roads have a minimal penalty
            'N': 1.8  # Narrow Roads have a significant penalty as they require the courier to travel via a bike
        }
        self.switchCost = {
            'M': 0.0, # No need to switch
            'S': 0.0, # No need to switch
            'N': 3.0  # Only Narrow Roads have a switching cost since the van has to wait for a bike to come and a handover has to be done
        }

        with open(connectionsFile) as connections:
            dataConnections = connections.read()

        with open(heuristicsFile) as heuristics:
            dataHeuristics = heuristics.read()

        with open(trackTypeFile) as trackTypes:
            dataTrackType = trackTypes.read()

        dataConnections = dataConnections.split('\n')
        dataHeuristics = dataHeuristics.split('\n')
        dataTrackType = dataTrackType.split('\n')

        self.graph = {}
        self.heuristicDict = {}

        # setting up the vertex list for the graph
        for each in dataConnections[0].split(','):
            if each == '': # Skips first entry which is blank
                continue
            self.vertices.append(each)


        # Gets all the distances between Areas
        for i in range(1, len(dataConnections)): # starts from the second line

            if dataConnections[i].strip() == '':
                continue
            # To prevent the program from crashing if it encounters an empty line at the bottom of the CSV
            
            connection_row = dataConnections[i].split(',')
            heuristics_row = dataHeuristics[i].split(',')
            trackType_row = dataTrackType[i].split(',')

            for j in range(1, len(connection_row)):
                destination = self.vertices[j-1]
                distance = float(connection_row[j])
                heuristic = float(heuristics_row[j])
                trackType =  trackType_row[j].strip()

                self.heuristicDict[(self.vertices[i-1], destination)] = heuristic

                if distance != 0 and distance != -1 and trackType != '-1': # To make sure the track is directly reachable from the current node
                    cost = (distance * self.weights[trackType]) + self.switchCost[trackType]
                    edge = (destination, cost, trackType)
                    self.graph.setdefault(self.vertices[i-1], []).append(edge)

        # print(self.vertices)


    def getStartState(self):
        return self.start_state

    def isGoalState(self, state):
        return state == self.goal_state

    def getSuccessors(self, state):
        successors = []
        
        # self.graph.get(state, []) prevents a KeyError if a node has no edges
        for destination, cost, trackType in self.graph.get(state, []):
            
            successor = destination
            action = destination  # The "action" is simply traveling to that area
            stepCost = cost
            
            successors.append((successor, action, stepCost))
            
        return successors

    def getCostOfActions(self, actions):
        total_cost = 0
        current_state = self.getStartState()

        for action in actions:
            validAction = False
            for destination, cost, trackType in self.graph.get(current_state, []):
                if action == destination:
                    total_cost += cost
                    current_state = destination
                    validAction = True
                    break
            if not validAction:
                 return -1

        return total_cost


    def getHeuristic(self, state):
        if not self.needsHeuristic:
            return 0

        return self.heuristicDict[(state, self.goal_state)]

        

    # Helper function to display the graph as I work with the problem
    def print_graph(self):
        print(f"{'Courier Routing Graph':^60}")
        print("=" * 60)
        
        for origin, edges in self.graph.items():
            print(f"Area: {origin}")
            print(f"   {'Destination':<20} | {'Cost':<5} | {'Track'}")
            print("   " + "-" * 45)
            
            for destination, distance, track_type in edges:
                print(f"   {destination:<20} | {distance:<5.1f} |   {track_type}")
        print("\n" + "=" * 60)

# def main():
#     courier = courierDelivery('Saddar (Hub)', 'Korangi', "..\csv\Connections.csv", "..\csv\heuristics.csv", "..\csv\TrackType.csv", True)
#     # courier.print_graph()

#     # print(search.dijkstraSearch(courier))
#     # print(search.aStarSearch(courier))
# main()