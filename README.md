# 🚖 Intelligent City-Wide Ride-Sharing & Fleet Dispatch Routing Engine

A high-performance backend geospatial routing simulation built in C++ utilizing graph optimization algorithms, paired with an asynchronous Python desktop visualization dashboard interface.

## 🛠️ Architecture & Core Components
- **Algorithmic Routing Pipeline (C++)**: Models an 8-node transportation topology of high-congestion zones in Bangalore using an explicit Adjacency List graph network structure. Min-heap priority queues (`std::priority_queue`) execute Dijkstra’s Shortest Path Algorithm to calculate absolute minimum travel weights.
- **Persistent Inter-process Communication**: A persistent, unbuffered subprocess standard I/O stream bridge pipes calculated spatial trajectories and node integers directly to the visual layer.
- **Geographic Dashboard Wrapper (Python)**: An asynchronous `customtkinter` desktop dashboard that embeds an interactive OpenStreetMap engine via `tkintermapview`, translating raw node matrices into physical GPS path arrays in real time.

## 🗺️ Simulated Urban Nodes Map
- Node 0: PESU E-City Campus (Central Hub)
- Node 1: Electronic City Phase 1 Toll Gate
- Node 2: NICE Road Intersection
- Node 3: Silk Board Traffic Bottleneck
- Node 4: HSR Layout Sector 1
- Node 5: Koramangala 4th Block Startup Hub
- Node 6: Majestic Central Transit Terminal
- Node 7: Indiranagar 100ft Commercial Road
