#include <iostream>
#include <vector>
#include <string>
#include <queue>
#include <climits>

using namespace std;

struct Road { 
    int destinationNode; 
    int travelTimeMinutes; 
};

class BangaloreMap {
private:
    int totalNodes;
    vector<vector<Road>> adjacencyList;

public:
    BangaloreMap(int nodes) {
        totalNodes = nodes;
        adjacencyList.resize(nodes);
    }

    void addRoad(int source, int dest, int time) {
        adjacencyList[source].push_back({dest, time});
        adjacencyList[dest].push_back({source, time});
    }

    int findShortestPath(int sourceNode, int destinationNode, vector<int>& pathSequence) {
        vector<int> travelTimes(totalNodes, INT_MAX);
        vector<int> parentNode(totalNodes, -1);
        priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> minHeap;

        travelTimes[sourceNode] = 0;
        minHeap.push({0, sourceNode});

        while (!minHeap.empty()) {
            int currentTime = minHeap.top().first;
            int currentNode = minHeap.top().second;
            minHeap.pop();

            if (currentTime > travelTimes[currentNode]) continue;

            for (const auto& road : adjacencyList[currentNode]) {
                int nextNode = road.destinationNode;
                int timeToNext = road.travelTimeMinutes;

                if (travelTimes[currentNode] + timeToNext < travelTimes[nextNode]) {
                    travelTimes[nextNode] = travelTimes[currentNode] + timeToNext;
                    parentNode[nextNode] = currentNode;
                    minHeap.push({travelTimes[nextNode], nextNode});
                }
            }
        }

        if (travelTimes[destinationNode] == INT_MAX) return -1;

        int traceNode = destinationNode;
        while (traceNode != -1) {
            pathSequence.insert(pathSequence.begin(), traceNode);
            traceNode = parentNode[traceNode];
        }

        return travelTimes[destinationNode];
    }
};

int main() {
    ios_base::sync_with_stdio(false); 
    cin.tie(NULL);

    // Initializing our new expanded 8-node urban transportation network
    BangaloreMap banyanCityMap(8);
    
    // Core E-City Grid Clusters
    banyanCityMap.addRoad(0, 1, 7);   // PESU <-> Toll Gate (7 mins)
    banyanCityMap.addRoad(0, 2, 10);  // PESU <-> NICE Road (10 mins)
    banyanCityMap.addRoad(1, 3, 25);  // Toll Gate <-> Silk Board (25 mins traffic)
    banyanCityMap.addRoad(2, 3, 14);  // NICE Road <-> Silk Board (14 mins bypass)
    
    // Central Connectivity Links
    banyanCityMap.addRoad(3, 4, 8);   // Silk Board <-> HSR Layout (8 mins)
    banyanCityMap.addRoad(3, 5, 12);  // Silk Board <-> Koramangala (12 mins)
    banyanCityMap.addRoad(4, 5, 10);  // HSR Layout <-> Koramangala (10 mins)
    banyanCityMap.addRoad(5, 7, 18);  // Koramangala <-> Indiranagar (18 mins)
    banyanCityMap.addRoad(3, 6, 35);  // Silk Board <-> Majestic Central (35 mins)
    banyanCityMap.addRoad(6, 7, 22);  // Majestic <-> Indiranagar (22 mins)

    int pickup, drop, d1_loc, d2_loc;
    while (cin >> pickup >> drop >> d1_loc >> d2_loc) {
        vector<int> path1, path2;
        int time1 = banyanCityMap.findShortestPath(d1_loc, pickup, path1);
        int time2 = banyanCityMap.findShortestPath(d2_loc, pickup, path2);

        int best_driver = (time1 <= time2) ? 1 : 2;
        int pickup_time = (best_driver == 1) ? time1 : time2;

        vector<int> tripPath;
        int trip_time = banyanCityMap.findShortestPath(pickup, drop, tripPath);

        cout << best_driver << "|" << pickup_time << "|" << trip_time << "|";
        for (size_t i = 0; i < tripPath.size(); i++) {
            cout << tripPath[i] << (i == tripPath.size() - 1 ? "" : ",");
        }
        cout << "\n" << flush;
    }
    return 0;
}
