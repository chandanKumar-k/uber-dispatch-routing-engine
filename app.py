import os
import tkinter as tk
import customtkinter as ctk
import subprocess
from tkintermapview import TkinterMapView

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# Updated 8-Node Real-World GPS Coordinates across Bangalore City
NODES_GPS = {
    0: (12.8614, 77.6645),  # PESU E-City Campus
    1: (12.8497, 77.6591),  # E-City Phase 1 Toll Gate
    2: (12.8681, 77.6510),  # NICE Road Junction
    3: (12.9174, 77.6238),  # Silk Board Bottleneck
    4: (12.9116, 77.6388),  # HSR Layout Sector 1
    5: (12.9343, 77.6244),  # Koramangala 4th Block
    6: (12.9779, 77.5724),  # Majestic Bus Station / City Railway
    7: (12.9719, 77.6412)   # Indiranagar 100ft Road
}

NODE_NAMES = {
    0: "PESU E-City Campus",
    1: "E-City Phase 1 Toll Gate",
    2: "NICE Road Junction",
    3: "Silk Board Bottleneck",
    4: "HSR Layout Sector 1",
    5: "Koramangala 4th Block",
    6: "Majestic Central Terminal",
    7: "Indiranagar 100ft Road"
}

class UberAppSimulator(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🚖 PESU Multi-Node Ride-Sharing Dispatch Core Engine Dashboard v5.2")
        self.geometry("1150x680")

        # Start background persistent state pipeline
        exe_path = os.path.join(os.path.dirname(__file__), "uber_api2.exe")
        if not os.path.exists(exe_path):
            raise FileNotFoundError(f"Backend executable not found: {exe_path}")
        self.cpp_process = subprocess.Popen(
            [exe_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            bufsize=1
        )
        
        # Deploy fleet: Driver 1 at NICE road, Driver 2 at Majestic Terminal
        self.driver_positions = {1: 2, 2: 6} 

        # --- LEFT PANEL: NAVIGATION SYSTEMS DRAWER ---
        self.panel = ctk.CTkFrame(self, width=320, corner_radius=10)
        self.panel.pack(side="left", fill="y", padx=15, pady=15)

        ctk.CTkLabel(self.panel, text="ROUTE BOOKING PANEL", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=25)

        # Dropdowns mapping out all our 8 clean location titles
        ctk.CTkLabel(self.panel, text="Select Pickup Location Landmark:", font=ctk.CTkFont(size=11)).pack(anchor="w", padx=20, pady=2)
        self.pickup_menu = ctk.CTkOptionMenu(self.panel, values=list(NODE_NAMES.values()))
        self.pickup_menu.pack(fill="x", padx=20, pady=10)
        self.pickup_menu.set(NODE_NAMES[0]) # Default to PESU Campus

        ctk.CTkLabel(self.panel, text="Select Destination Drop Target:", font=ctk.CTkFont(size=11)).pack(anchor="w", padx=20, pady=2)
        self.drop_menu = ctk.CTkOptionMenu(self.panel, values=list(NODE_NAMES.values()))
        self.drop_menu.pack(fill="x", padx=20, pady=10)
        self.drop_menu.set(NODE_NAMES[4]) # Default to HSR Layout

        self.dispatch_btn = ctk.CTkButton(self.panel, text="Request Dispatch Route", fg_color="#10b981", hover_color="#059669", font=ctk.CTkFont(weight="bold"), command=self.calculate_dispatch)
        self.dispatch_btn.pack(fill="x", padx=20, pady=35)

        # --- RIGHT UPPER CONTAINER: INTERACTIVE GPS PANEL MAP CANVAS ---
        self.map_frame = ctk.CTkFrame(self, corner_radius=10)
        self.map_frame.pack(side="top", fill="both", expand=True, padx=15, pady=10)

        self.map_widget = TkinterMapView(self.map_frame, corner_radius=10)
        self.map_widget.pack(fill="both", expand=True)
        # Shift anchor center zoom coordinates slightly higher to capture Majestic/Indiranagar systems cleanly
        self.map_widget.set_position(12.9250, 77.6100) 
        self.map_widget.set_zoom(12)

        self.path_line = None
        self.draw_static_markers()

        # --- RIGHT LOWER CONTAINER: RUNNING TRANSACTION STREAM CONSOLE ---
        self.logger_box = ctk.CTkTextbox(self, height=130, font=ctk.CTkFont(family="Courier", size=12), corner_radius=10)
        self.logger_box.pack(side="bottom", fill="x", padx=15, pady=15)
        self.logger_box.insert("end", "[ROUTING LOG]: Connected to 8-Node C++ Dijkstra core. Network topology updated.\n")

    def draw_static_markers(self):
        for nid, gps in NODES_GPS.items():
            self.map_widget.set_marker(gps[0], gps[1], text=NODE_NAMES[nid])

    def calculate_dispatch(self):
        rev_names = {v: k for k, v in NODE_NAMES.items()}
        p_idx = rev_names[self.pickup_menu.get()]
        d_idx = rev_names[self.drop_menu.get()]

        if p_idx == d_idx:
            self.logger_box.insert("end", "[INPUT ROUTING FAULT]: Pickup and dropping landmarks cannot overlap.\n")
            return

        # Pass query array down the background text stream pipe channel
        payload = f"{p_idx} {d_idx} {self.driver_positions[1]} {self.driver_positions[2]}\n"
        try:
            self.cpp_process.stdin.write(payload)
            self.cpp_process.stdin.flush()
        except OSError as exc:
            self.logger_box.insert("end", f"[PIPE ERROR]: Unable to send payload to backend: {exc}\n")
            return

        if self.cpp_process.poll() is not None:
            self.logger_box.insert("end", "[BACKEND ERROR]: C++ engine terminated unexpectedly.\n")
            return

        response = self.cpp_process.stdout.readline()
        if not response:
            self.logger_box.insert("end", "[BACKEND ERROR]: no response from C++ engine.\n")
            return

        response = response.strip()
        parts = response.split("|")
        if len(parts) != 4:
            self.logger_box.insert("end", f"[BACKEND RESPONSE ERROR]: unexpected response: {response!r}\n")
            return

        best_d, p_time, t_time, path_str = parts
        path_nodes = [int(x) for x in path_str.split(",") if x]

        p_name = NODE_NAMES[p_idx]
        d_name = NODE_NAMES[d_idx]
        dr_name = "Driver Ramesh (Staged at NICE Road)" if best_d == "1" else "Driver Suresh (Staged at Majestic Terminal)"
        
        self.logger_box.delete("1.0", "end")
        self.logger_box.insert("end", f"==============================================================\n")
        self.logger_box.insert("end", f"🚖 EXPANDED CITY DISPATCH ACTIVE: ROUTE TRACED BY BACKEND\n")
        self.logger_box.insert("end", f"==============================================================\n")
        self.logger_box.insert("end", f"Commute Route  : {p_name} ---> {d_name}\n")
        self.logger_box.insert("end", f"Assigned Driver: {dr_name}\n")
        self.logger_box.insert("end", f"Driver ETA to Passenger: {p_time} minutes\n")
        self.logger_box.insert("end", f"Total Passenger Trip Duration: {t_time} minutes\n")
        self.logger_box.insert("end", f"==============================================================\n\n")

        # Redraw the trajectory paths lines clearly across the map canvas surface grid panels
        if self.path_line:
            self.path_line.delete()

        gps_trajectory = [NODES_GPS[nid] for nid in path_nodes]
        self.path_line = self.map_widget.set_path(gps_trajectory, color="#06b6d4", width=4)

if __name__ == "__main__":
    app = UberAppSimulator()
    app.mainloop()
# this is a beautiful UI design python app 