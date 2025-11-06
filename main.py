"""
City Simulation Game - Enhanced Edition with Desirability System

A comprehensive city simulation game built with Python and tkinter.
Features zoning, infrastructure building, time progression, desirability scoring,
and dynamic building states based on proximity to amenities.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import math
from typing import Optional, Tuple
from city import City
from simulation import Simulation
from zone import Zone
from building import Building
from infrastructure import Infrastructure

class CitySimulationUI:
    """
    Main UI class that handles all graphical interface and user interactions.
    """
    
    def __init__(self, root: tk.Tk):
        """
        Initialize the UI with the given root window.
        
        Args:
            root: Main tkinter window
        """
        self.root = root
        self.city = City(50, 50)  # Create 50x50 city grid
        self.simulation = Simulation(self.city)
        
        # UI state variables
        self.current_tool = tk.StringVar(value="inspect")
        self.selected_zone_type = tk.StringVar(value="residential")
        self.selected_infrastructure = tk.StringVar(value="road")
        self.selected_building = tk.StringVar(value="school")
        
        # Canvas settings
        self.cell_size = 12  # Increased for better visibility
        self.canvas_width = 800
        self.canvas_height = 800
        self.zoom_level = 1.0
        
        # Enhanced colors and visual settings
        self.colors = {
            'empty': '#F8F8FF',      # Ghost white - cleaner background
            'residential': '#98FB98',  # Pale green - more vibrant
            'commercial': '#87CEEB',   # Sky blue
            'industrial': '#DEB887',   # Burlywood - warmer brown
            'road': '#2F4F4F',         # Dark slate gray - more realistic
            'power': '#FFD700',        # Gold
            'water': '#00CED1',        # Dark turquoise
            'grid': '#E6E6FA',         # Lavender - softer grid
            'selection': '#FF4500',    # Orange red for selection
            'disaster': '#FF0000',     # Red for disasters
            'traffic_low': '#FFFF00',  # Yellow for low traffic
            'traffic_medium': '#FFA500', # Orange for medium traffic
            'traffic_high': '#FF0000'  # Red for high traffic
        }
        
        # Enhanced color schemes for different elements
        self.zone_colors = {
            'residential': {
                'base': '#98FB98',
                'developed': '#32CD32',
                'high_density': '#228B22'
            },
            'commercial': {
                'base': '#87CEEB',
                'developed': '#4682B4',
                'high_density': '#191970'
            },
            'industrial': {
                'base': '#DEB887',
                'developed': '#CD853F',
                'high_density': '#8B4513'
            }
        }
        
        self.infrastructure_colors = {
            'road': '#2F4F4F',
            'highway': '#1C1C1C',
            'power_plant': '#FFD700',
            'water_facility': '#00CED1',
            'waste_facility': '#8B4513',
            'school': '#FFD700',
            'hospital': '#FF6347',
            'park': '#32CD32',
            'police_station': '#000080',
            'fire_station': '#DC143C',
            'subway_station': '#4B0082',
            'bridge': '#708090'
        }
        
        # Track mouse interactions
        self.last_click_pos = None
        self.dragging = False
        
        # Setup UI components
        self._setup_ui()
        self._setup_bindings()
        
        # Start simulation
        self.simulation.add_update_callback(self._on_simulation_update)
        self.simulation.start()
        
        # Start UI update loop
        self._update_ui()
    
    def _setup_ui(self):
        """Setup all UI components."""
        # Main container with paned window
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel for controls
        left_frame = ttk.Frame(main_paned, width=350)
        left_frame.pack_propagate(False)
        main_paned.add(left_frame, weight=0)
        
        # Right panel for city view
        right_frame = ttk.Frame(main_paned)
        main_paned.add(right_frame, weight=1)
        
        self._setup_left_panel(left_frame)
        self._setup_right_panel(right_frame)
    
    def _setup_left_panel(self, parent):
        """Setup the left control panel."""
        # Create notebook for tabbed interface
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tools tab
        tools_frame = ttk.Frame(notebook)
        notebook.add(tools_frame, text="Tools")
        self._setup_tools_tab(tools_frame)
        
        # Statistics tab
        stats_frame = ttk.Frame(notebook)
        notebook.add(stats_frame, text="Statistics")
        self._setup_stats_tab(stats_frame)
        
        # Desirability tab
        desirability_frame = ttk.Frame(notebook)
        notebook.add(desirability_frame, text="Desirability")
        self._setup_desirability_tab(desirability_frame)
        
        # Disasters & Traffic tab
        disasters_frame = ttk.Frame(notebook)
        notebook.add(disasters_frame, text="Disasters & Traffic")
        self._setup_disasters_tab(disasters_frame)
        
        # Simulation tab
        sim_frame = ttk.Frame(notebook)
        notebook.add(sim_frame, text="Simulation")
        self._setup_simulation_tab(sim_frame)
        
        # Save/Load tab
        file_frame = ttk.Frame(notebook)
        notebook.add(file_frame, text="File")
        self._setup_file_tab(file_frame)
    
    def _setup_tools_tab(self, parent):
        """Setup the tools tab with zoning and building controls."""
        # Tool selection with better styling
        ttk.Label(parent, text="Current Tool:", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(5, 0))
        
        tools_frame = ttk.Frame(parent)
        tools_frame.pack(fill=tk.X, pady=5)
        
        # Create styled radio buttons
        tool_buttons = [
            ("🔍 Inspect", "inspect"),
            ("🏠 Zone", "zone"),
            ("🏗️ Infrastructure", "infrastructure"),
            ("🏢 Building", "building"),
            ("💥 Demolish", "demolish")
        ]
        
        for text, value in tool_buttons:
            btn = ttk.Radiobutton(tools_frame, text=text, variable=self.current_tool, value=value)
            btn.pack(anchor=tk.W, pady=2)
        
        # Zone types
        ttk.Separator(parent, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        ttk.Label(parent, text="Zone Types:", font=("Arial", 12, "bold")).pack(anchor=tk.W)
        
        zone_frame = ttk.Frame(parent)
        zone_frame.pack(fill=tk.X, pady=5)
        
        zone_buttons = [
            ("🏘️ Residential", "residential"),
            ("🏪 Commercial", "commercial"),
            ("🏭 Industrial", "industrial")
        ]
        
        for text, value in zone_buttons:
            btn = ttk.Radiobutton(zone_frame, text=text, variable=self.selected_zone_type, value=value)
            btn.pack(anchor=tk.W, pady=2)
        
        # Infrastructure types
        ttk.Separator(parent, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        ttk.Label(parent, text="Infrastructure:", font=("Arial", 12, "bold")).pack(anchor=tk.W)
        
        infra_frame = ttk.Frame(parent)
        infra_frame.pack(fill=tk.X, pady=5)
        
        infra_buttons = [
            ("🛣️ Road", "road"),
            ("⚡ Power Plant", "power_plant"),
            ("💧 Water Facility", "water_facility"),
            ("🗑️ Waste Facility", "waste_facility")
        ]
        
        for text, value in infra_buttons:
            btn = ttk.Radiobutton(infra_frame, text=text, variable=self.selected_infrastructure, value=value)
            btn.pack(anchor=tk.W, pady=2)
        
        # Buildings
        ttk.Separator(parent, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        ttk.Label(parent, text="Buildings:", font=("Arial", 12, "bold")).pack(anchor=tk.W)
        
        building_frame = ttk.Frame(parent)
        building_frame.pack(fill=tk.X, pady=5)
        
        building_buttons = [
            ("🏫 School", "school"),
            ("🏥 Hospital", "hospital"),
            ("👮 Police Station", "police_station"),
            ("🚒 Fire Station", "fire_station"),
            ("🌳 Park", "park")
        ]
        
        for text, value in building_buttons:
            btn = ttk.Radiobutton(building_frame, text=text, variable=self.selected_building, value=value)
            btn.pack(anchor=tk.W, pady=2)
    
    def _setup_stats_tab(self, parent):
        """Setup the statistics display tab."""
        # Main stats
        ttk.Label(parent, text="City Statistics:", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(5, 10))
        
        self.stats_frame = ttk.Frame(parent)
        self.stats_frame.pack(fill=tk.X, pady=5)
        
        # Create stat labels
        self.stat_labels = {}
        stat_names = [
            ("💰 Money", "money"),
            ("👥 Population", "population"),
            ("😊 Happiness", "happiness"),
            ("💼 Employment Rate", "employment"),
            ("🌫️ Pollution", "pollution"),
            ("💵 Tax Revenue", "tax_revenue"),
            ("🔧 Maintenance Cost", "maintenance")
        ]
        
        for i, (display_name, key) in enumerate(stat_names):
            label = ttk.Label(self.stats_frame, text=f"{display_name}: --", font=("Arial", 10))
            label.grid(row=i, column=0, sticky=tk.W, pady=3)
            self.stat_labels[key] = label
        
        # Zone counts
        ttk.Separator(parent, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        ttk.Label(parent, text="Zone Counts:", font=("Arial", 12, "bold")).pack(anchor=tk.W)
        
        self.zone_stats_frame = ttk.Frame(parent)
        self.zone_stats_frame.pack(fill=tk.X, pady=5)
        
        self.zone_labels = {}
        zone_types = ["residential", "commercial", "industrial"]
        zone_icons = ["🏘️", "🏪", "🏭"]
        for i, (zone_type, icon) in enumerate(zip(zone_types, zone_icons)):
            label = ttk.Label(self.zone_stats_frame, text=f"{icon} {zone_type.capitalize()}: 0", font=("Arial", 10))
            label.grid(row=i, column=0, sticky=tk.W, pady=3)
            self.zone_labels[zone_type] = label
        
        # Building counts
        ttk.Separator(parent, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        ttk.Label(parent, text="Buildings:", font=("Arial", 12, "bold")).pack(anchor=tk.W)
        
        self.building_stats_frame = ttk.Frame(parent)
        self.building_stats_frame.pack(fill=tk.X, pady=5)
        
        self.building_labels = {}
        building_types = ["schools", "hospitals", "power_plants", "water_facilities"]
        building_icons = ["🏫", "🏥", "⚡", "💧"]
        for i, (building_type, icon) in enumerate(zip(building_types, building_icons)):
            display_name = building_type.replace("_", " ").title()
            label = ttk.Label(self.building_stats_frame, text=f"{icon} {display_name}: 0", font=("Arial", 10))
            label.grid(row=i, column=0, sticky=tk.W, pady=3)
            self.building_labels[building_type] = label
    
    def _setup_desirability_tab(self, parent):
        """Setup the desirability display tab."""
        ttk.Label(parent, text="Desirability System:", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(5, 10))
        
        # Desirability info
        info_text = """
🏠 Zone Desirability System:

• Parks: +20 points (within 10 tiles)
• Schools: +15 points (within 8 tiles)  
• Power Plants: +10 points (within 12 tiles)
• Commute Distance: -0.5 points per tile

Operating States:
• Thriving (80-100): Bright colors
• Normal (60-79): Standard colors
• Struggling (30-59): Darker colors
• Abandoned (0-29): Very dark colors

States update weekly based on desirability!
        """
        
        info_label = ttk.Label(parent, text=info_text, font=("Arial", 9), justify=tk.LEFT)
        info_label.pack(anchor=tk.W, pady=5)
        
        # Current zone desirability display
        ttk.Separator(parent, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        ttk.Label(parent, text="Selected Zone Info:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        
        self.desirability_frame = ttk.Frame(parent)
        self.desirability_frame.pack(fill=tk.X, pady=5)
        
        self.desirability_labels = {}
        desirability_fields = [
            ("Score", "score"),
            ("State", "state"),
            ("Park Bonus", "park_bonus"),
            ("School Bonus", "school_bonus"),
            ("Power Bonus", "power_bonus"),
            ("Commute Penalty", "commute_penalty")
        ]
        
        for i, (display_name, key) in enumerate(desirability_fields):
            label = ttk.Label(self.desirability_frame, text=f"{display_name}: --", font=("Arial", 9))
            label.grid(row=i, column=0, sticky=tk.W, pady=2)
            self.desirability_labels[key] = label
    
    def _setup_disasters_tab(self, parent):
        """Setup the disasters and traffic display tab."""
        ttk.Label(parent, text="Disaster & Traffic System:", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(5, 10))
        
        # Disaster info
        disaster_info = """
🚨 Disaster System:

• Fire Disasters: Damage buildings within radius
• Tornado Disasters: Large area damage
• Emergency Services: Fire stations and police stations
• Disaster Risk: Affects zone desirability

🚦 Traffic System:

• Daily Traffic Calculation: Based on commutes
• Traffic Levels: Low (Yellow) → Medium (Orange) → High (Red)
• Traffic Penalty: Reduces zone desirability
• Road Network: Affects commute efficiency
        """
        
        info_label = ttk.Label(parent, text=disaster_info, font=("Arial", 9), justify=tk.LEFT)
        info_label.pack(anchor=tk.W, pady=5)
        
        # Active disasters
        ttk.Separator(parent, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        ttk.Label(parent, text="Active Disasters:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        
        self.disasters_frame = ttk.Frame(parent)
        self.disasters_frame.pack(fill=tk.X, pady=5)
        
        self.disasters_label = ttk.Label(self.disasters_frame, text="No active disasters", font=("Arial", 9))
        self.disasters_label.pack(anchor=tk.W)
        
        # Traffic info
        ttk.Separator(parent, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        ttk.Label(parent, text="Traffic Information:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        
        self.traffic_frame = ttk.Frame(parent)
        self.traffic_frame.pack(fill=tk.X, pady=5)
        
        self.traffic_labels = {}
        traffic_fields = [
            ("Total Road Segments", "road_segments"),
            ("High Traffic Areas", "high_traffic"),
            ("Average Traffic Level", "avg_traffic")
        ]
        
        for i, (display_name, key) in enumerate(traffic_fields):
            label = ttk.Label(self.traffic_frame, text=f"{display_name}: --", font=("Arial", 9))
            label.grid(row=i, column=0, sticky=tk.W, pady=2)
            self.traffic_labels[key] = label
    
    def _setup_simulation_tab(self, parent):
        """Setup the simulation control tab."""
        # Time display
        ttk.Label(parent, text="Simulation Control:", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(5, 10))
        
        self.date_label = ttk.Label(parent, text="Date: --", font=("Arial", 10))
        self.date_label.pack(anchor=tk.W, pady=2)
        
        self.speed_label = ttk.Label(parent, text="Speed: 1.0x", font=("Arial", 10))
        self.speed_label.pack(anchor=tk.W, pady=2)
        
        # Control buttons
        control_frame = ttk.Frame(parent)
        control_frame.pack(fill=tk.X, pady=10)
        
        self.pause_button = ttk.Button(control_frame, text="Pause", 
                                     command=self._toggle_simulation)
        self.pause_button.pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(control_frame, text="Advance Day", 
                  command=lambda: self.simulation.advance_time(1)).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(control_frame, text="Advance Month", 
                  command=lambda: self.simulation.advance_time(30)).pack(side=tk.LEFT, padx=5)
        
        # Speed control
        ttk.Separator(parent, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        ttk.Label(parent, text="Simulation Speed:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        
        speed_frame = ttk.Frame(parent)
        speed_frame.pack(fill=tk.X, pady=5)
        
        self.speed_var = tk.DoubleVar(value=1.0)
        speed_scale = ttk.Scale(speed_frame, from_=0.1, to=10.0, variable=self.speed_var,
                               orient=tk.HORIZONTAL, command=self._on_speed_change)
        speed_scale.pack(fill=tk.X, pady=2)
        
        # Preset speed buttons
        preset_frame = ttk.Frame(parent)
        preset_frame.pack(fill=tk.X, pady=5)
        
        for speed, text in [(0.5, "0.5x"), (1.0, "1x"), (2.0, "2x"), (5.0, "5x")]:
            ttk.Button(preset_frame, text=text, width=6,
                      command=lambda s=speed: self._set_speed(s)).pack(side=tk.LEFT, padx=2)
    
    def _setup_file_tab(self, parent):
        """Setup the save/load file operations tab."""
        ttk.Label(parent, text="File Operations:", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(5, 10))
        
        file_frame = ttk.Frame(parent)
        file_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(file_frame, text="Save City", command=self._save_city).pack(fill=tk.X, pady=2)
        ttk.Button(file_frame, text="Load City", command=self._load_city).pack(fill=tk.X, pady=2)
        ttk.Button(file_frame, text="New City", command=self._new_city).pack(fill=tk.X, pady=2)
        
        ttk.Separator(parent, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        # Quick save/load
        ttk.Label(parent, text="Quick Save:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        quick_frame = ttk.Frame(parent)
        quick_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(quick_frame, text="Quick Save", 
                  command=lambda: self._save_city("quicksave.city")).pack(fill=tk.X, pady=1)
        ttk.Button(quick_frame, text="Quick Load", 
                  command=lambda: self._load_city("quicksave.city")).pack(fill=tk.X, pady=1)
        
        # City info
        ttk.Separator(parent, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        ttk.Label(parent, text="City Info:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        
        self.city_info_text = tk.Text(parent, height=8, width=30, wrap=tk.WORD)
        self.city_info_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Scrollbar for text
        scrollbar = ttk.Scrollbar(self.city_info_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.city_info_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.city_info_text.yview)
    
    def _setup_right_panel(self, parent):
        """Setup the right panel with city canvas."""
        # Canvas container with scrollbars
        canvas_container = ttk.Frame(parent)
        canvas_container.pack(fill=tk.BOTH, expand=True)
        
        # Create canvas with scrollbars
        self.canvas = tk.Canvas(canvas_container, bg=self.colors['empty'],
                               width=self.canvas_width, height=self.canvas_height)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(canvas_container, orient=tk.VERTICAL, command=self.canvas.yview)
        h_scrollbar = ttk.Scrollbar(canvas_container, orient=tk.HORIZONTAL, command=self.canvas.xview)
        
        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack scrollbars and canvas
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Set scroll region
        self.canvas.configure(scrollregion=(0, 0, 
                                          self.city.width * self.cell_size,
                                          self.city.height * self.cell_size))
        
        # Control panel above canvas
        control_panel = ttk.Frame(parent)
        control_panel.pack(fill=tk.X, pady=(0, 5))
        
        # View controls with icons
        ttk.Label(control_panel, text="View Controls:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=(5, 2))
        
        ttk.Button(control_panel, text="🔍 Zoom In", width=10,
                  command=self._zoom_in).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_panel, text="🔍 Zoom Out", width=10,
                  command=self._zoom_out).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_panel, text="🏠 Reset View", width=12,
                  command=self._reset_view).pack(side=tk.LEFT, padx=2)
        
        # Status bar
        status_frame = ttk.Frame(control_panel)
        status_frame.pack(side=tk.RIGHT, padx=5)
        
        # Info label for mouse position
        self.info_label = ttk.Label(status_frame, text="Ready", font=("Arial", 9))
        self.info_label.pack(side=tk.RIGHT)
        
        # Tool indicator
        self.tool_indicator = ttk.Label(status_frame, text="Tool: Inspect", font=("Arial", 9, "bold"))
        self.tool_indicator.pack(side=tk.RIGHT, padx=(0, 10))
    
    def _setup_bindings(self):
        """Setup event bindings for mouse and keyboard interactions."""
        # Canvas mouse events
        self.canvas.bind("<Button-1>", self._on_canvas_click)
        self.canvas.bind("<B1-Motion>", self._on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_canvas_release)
        self.canvas.bind("<Button-3>", self._on_canvas_right_click)  # Right click for panning
        self.canvas.bind("<B3-Motion>", self._on_canvas_pan)
        self.canvas.bind("<ButtonRelease-3>", self._on_canvas_right_release)
        self.canvas.bind("<Motion>", self._on_canvas_motion)
        self.canvas.bind("<MouseWheel>", self._on_canvas_wheel)
        
        # Pan state tracking
        self.panning = False
        self.pan_start_x = 0
        self.pan_start_y = 0
        
        # Keyboard shortcuts
        self.root.bind("<Control-s>", lambda e: self._save_city())
        self.root.bind("<Control-o>", lambda e: self._load_city())
        self.root.bind("<Control-n>", lambda e: self._new_city())
        self.root.bind("<space>", lambda e: self._toggle_simulation())
        
        # Tool shortcuts
        self.root.bind("1", lambda e: self._set_tool("inspect"))
        self.root.bind("2", lambda e: self._set_tool("zone"))
        self.root.bind("3", lambda e: self._set_tool("infrastructure"))
        self.root.bind("4", lambda e: self._set_tool("building"))
        self.root.bind("5", lambda e: self._set_tool("demolish"))
        
        # Track tool changes
        self.current_tool.trace('w', self._on_tool_change)
    
    def _canvas_to_grid(self, canvas_x: int, canvas_y: int) -> Tuple[int, int]:
        """Convert canvas coordinates to grid coordinates."""
        # Get the current scroll position from the canvas
        scroll_x = self.canvas.canvasx(0)
        scroll_y = self.canvas.canvasy(0)
        
        # Convert to grid coordinates - account for zoom level
        grid_x = int((canvas_x + scroll_x) / (self.cell_size * self.zoom_level))
        grid_y = int((canvas_y + scroll_y) / (self.cell_size * self.zoom_level))
        
        # Ensure we're within bounds
        grid_x = max(0, min(grid_x, self.city.width - 1))
        grid_y = max(0, min(grid_y, self.city.height - 1))
        
        return grid_x, grid_y
    
    def _grid_to_canvas(self, grid_x: int, grid_y: int) -> Tuple[int, int]:
        """Convert grid coordinates to canvas coordinates."""
        # Get the current scroll position from the canvas
        scroll_x = self.canvas.canvasx(0)
        scroll_y = self.canvas.canvasy(0)
        
        # Convert to canvas coordinates - account for zoom level
        canvas_x = int(grid_x * self.cell_size * self.zoom_level - scroll_x)
        canvas_y = int(grid_y * self.cell_size * self.zoom_level - scroll_y)
        
        return canvas_x, canvas_y
    
    def _on_canvas_click(self, event):
        """Handle canvas click events."""
        grid_x, grid_y = self._canvas_to_grid(event.x, event.y)
        self.last_click_pos = (grid_x, grid_y)
        
        if not self.city.is_valid_position(grid_x, grid_y):
            return
        
        tool = self.current_tool.get()
        
        if tool == "inspect":
            self._inspect_cell(grid_x, grid_y)
        elif tool == "zone":
            self._place_zone(grid_x, grid_y)
        elif tool == "infrastructure":
            self._place_infrastructure(grid_x, grid_y)
        elif tool == "building":
            self._place_building(grid_x, grid_y)
        elif tool == "demolish":
            self._demolish_cell(grid_x, grid_y)
        
        self._update_canvas()
    
    def _on_canvas_drag(self, event):
        """Handle canvas drag events."""
        if self.current_tool.get() in ["zone", "infrastructure"]:
            grid_x, grid_y = self._canvas_to_grid(event.x, event.y)
            if (grid_x, grid_y) != self.last_click_pos and self.city.is_valid_position(grid_x, grid_y):
                if self.current_tool.get() == "zone":
                    self._place_zone(grid_x, grid_y)
                elif self.current_tool.get() == "infrastructure":
                    self._place_infrastructure(grid_x, grid_y)
                self.last_click_pos = (grid_x, grid_y)
                self._update_canvas()
    
    def _on_canvas_release(self, event):
        """Handle canvas mouse release events."""
        self.last_click_pos = None
    
    def _on_canvas_motion(self, event):
        """Handle canvas mouse motion for info display."""
        grid_x, grid_y = self._canvas_to_grid(event.x, event.y)
        
        if self.city.is_valid_position(grid_x, grid_y):
            cell = self.city.get_cell(grid_x, grid_y)
            if cell is None:
                self.info_label.config(text=f"Empty ({grid_x}, {grid_y})")
            else:
                self.info_label.config(text=f"{str(cell)} ({grid_x}, {grid_y})")
        else:
            self.info_label.config(text="Out of bounds")
    
    def _on_canvas_wheel(self, event):
        """Handle mouse wheel for zooming."""
        if event.delta > 0:
            self._zoom_in()
        else:
            self._zoom_out()
    
    def _on_canvas_right_click(self, event):
        """Handle right click to start panning."""
        self.panning = True
        self.pan_start_x = event.x
        self.pan_start_y = event.y
        self.canvas.config(cursor="fleur")  # Change cursor to indicate panning
    
    def _on_canvas_pan(self, event):
        """Handle mouse drag for panning."""
        if self.panning:
            dx = event.x - self.pan_start_x
            dy = event.y - self.pan_start_y
            
            # Update scroll position
            self.canvas.xview_scroll(-dx, "units")
            self.canvas.yview_scroll(-dy, "units")
            
            self.pan_start_x = event.x
            self.pan_start_y = event.y
            self._update_canvas()
    
    def _on_canvas_right_release(self, event):
        """Handle right click release to stop panning."""
        self.panning = False
        self.canvas.config(cursor="")
    
    def _inspect_cell(self, x: int, y: int):
        """Show detailed information about a cell."""
        cell = self.city.get_cell(x, y)
        
        if cell is None:
            info = f"Empty land at ({x}, {y})\n\nThis area can be zoned or used for infrastructure."
        else:
            cell_info = cell.get_info()
            info = f"{str(cell)} at ({x}, {y})\n\n"
            
            for key, value in cell_info.items():
                if key not in ['type', 'position']:
                    display_key = key.replace('_', ' ').title()
                    if isinstance(value, float):
                        info += f"{display_key}: {value:.1f}\n"
                    elif isinstance(value, int):
                        info += f"{display_key}: {value:,}\n"
                    else:
                        info += f"{display_key}: {value}\n"
        
        # Show power and water coverage
        in_power = (x, y) in self.city.power_coverage
        in_water = (x, y) in self.city.water_coverage
        on_road = (x, y) in self.city.road_network
        
        info += f"\nUtilities:\n"
        info += f"Power: {'Yes' if in_power else 'No'}\n"
        info += f"Water: {'Yes' if in_water else 'No'}\n"
        info += f"Road Access: {'Yes' if on_road else 'No'}\n"
        
        # Add desirability info for zones
        if isinstance(cell, Zone):
            desirability = cell.calculate_desirability(self.city)
            info += f"\nDesirability Score: {desirability:.1f}/100\n"
            info += f"Operating State: {cell.operating_state.title()}\n"
        
        messagebox.showinfo("Cell Information", info)
    
    def _place_zone(self, x: int, y: int):
        """Place a zone at the specified position."""
        zone_type = self.selected_zone_type.get()
        
        if self.city.place_zone(x, y, zone_type):
            self.info_label.config(text=f"Placed {zone_type} zone at ({x}, {y})")
        else:
            self.info_label.config(text=f"Cannot place zone at ({x}, {y}) - position occupied")
    
    def _place_infrastructure(self, x: int, y: int):
        """Place infrastructure at the specified position."""
        infra_type = self.selected_infrastructure.get()
        
        if self.city.place_infrastructure(x, y, infra_type):
            cost = Infrastructure(x, y, infra_type).get_cost()
            self.info_label.config(text=f"Placed {infra_type} at ({x}, {y}) - Cost: ${cost:,}")
        else:
            cell = self.city.get_cell(x, y)
            if cell is not None:
                self.info_label.config(text=f"Cannot place {infra_type} - position occupied")
            else:
                cost = Infrastructure(x, y, infra_type).get_cost()
                self.info_label.config(text=f"Cannot place {infra_type} - insufficient funds (need ${cost:,})")
    
    def _place_building(self, x: int, y: int):
        """Place a building at the specified position."""
        building_type = self.selected_building.get()
        
        # Buildings are implemented as infrastructure for simplicity
        if self.city.place_infrastructure(x, y, building_type):
            cost = Infrastructure(x, y, building_type).get_cost()
            self.info_label.config(text=f"Placed {building_type} at ({x}, {y}) - Cost: ${cost:,}")
        else:
            cell = self.city.get_cell(x, y)
            if cell is not None:
                self.info_label.config(text=f"Cannot place {building_type} - position occupied")
            else:
                cost = Infrastructure(x, y, building_type).get_cost()
                self.info_label.config(text=f"Cannot place {building_type} - insufficient funds (need ${cost:,})")
    
    def _demolish_cell(self, x: int, y: int):
        """Demolish/remove content at the specified position."""
        cell = self.city.get_cell(x, y)
        
        if cell is None:
            self.info_label.config(text=f"Nothing to demolish at ({x}, {y})")
            return
        
        # Confirm demolition for expensive items
        if isinstance(cell, Infrastructure) and cell.get_cost() > 1000:
            if not messagebox.askyesno("Confirm Demolition", 
                                     f"Demolish {str(cell)}? This cannot be undone."):
                return
        
        if self.city.remove_cell(x, y):
            self.info_label.config(text=f"Demolished {str(cell)} at ({x}, {y})")
        else:
            self.info_label.config(text=f"Cannot demolish at ({x}, {y})")
    
    def _zoom_in(self):
        """Zoom in on the city view."""
        if self.zoom_level < 3.0:
            self.zoom_level = min(3.0, self.zoom_level * 1.2)
            self._update_canvas()
    
    def _zoom_out(self):
        """Zoom out from the city view."""
        if self.zoom_level > 0.3:
            self.zoom_level = max(0.3, self.zoom_level / 1.2)
            self._update_canvas()
    
    def _reset_view(self):
        """Reset zoom and scroll to default."""
        self.zoom_level = 1.0
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)
        self._update_canvas()
    
    def _toggle_simulation(self):
        """Toggle simulation pause/resume."""
        if self.simulation.paused:
            self.simulation.resume()
            self.pause_button.config(text="Pause")
        else:
            self.simulation.pause()
            self.pause_button.config(text="Resume")
    
    def _on_speed_change(self, value):
        """Handle simulation speed change."""
        speed = float(value)
        self.simulation.set_speed(speed)
        self.speed_label.config(text=f"Speed: {speed:.1f}x")
    
    def _set_speed(self, speed: float):
        """Set simulation speed to specific value."""
        self.speed_var.set(speed)
        self.simulation.set_speed(speed)
        self.speed_label.config(text=f"Speed: {speed:.1f}x")
    
    def _set_tool(self, tool: str):
        """Set the current tool and update UI."""
        self.current_tool.set(tool)
    
    def _on_tool_change(self, *args):
        """Handle tool change and update UI indicators."""
        tool = self.current_tool.get()
        tool_names = {
            'inspect': '🔍 Inspect',
            'zone': '🏠 Zone',
            'infrastructure': '🏗️ Infrastructure',
            'building': '🏢 Building',
            'demolish': '💥 Demolish'
        }
        
        tool_name = tool_names.get(tool, tool.title())
        self.tool_indicator.config(text=f"Tool: {tool_name}")
        
        # Update cursor based on tool
        cursor_map = {
            'inspect': 'hand2',
            'zone': 'crosshair',
            'infrastructure': 'crosshair',
            'building': 'crosshair',
            'demolish': 'X_cursor'
        }
        
        self.canvas.config(cursor=cursor_map.get(tool, 'arrow'))
    
    def _save_city(self, filename: Optional[str] = None):
        """Save the current city to file."""
        if filename is None:
            filename = filedialog.asksaveasfilename(
                defaultextension=".city",
                filetypes=[("City files", "*.city"), ("All files", "*.*")]
            )
        
        if filename:
            if self.city.save_to_file(filename):
                messagebox.showinfo("Save Successful", f"City saved to {filename}")
            else:
                messagebox.showerror("Save Failed", "Failed to save city file")
    
    def _load_city(self, filename: Optional[str] = None):
        """Load a city from file."""
        if filename is None:
            filename = filedialog.askopenfilename(
                filetypes=[("City files", "*.city"), ("All files", "*.*")]
            )
        
        if filename:
            if self.city.load_from_file(filename):
                messagebox.showinfo("Load Successful", f"City loaded from {filename}")
                self._update_canvas()
                self._update_stats()
            else:
                messagebox.showerror("Load Failed", "Failed to load city file")
    
    def _new_city(self):
        """Create a new city."""
        if messagebox.askyesno("New City", "Create new city? Current progress will be lost."):
            self.city = City(50, 50)
            self.simulation.city = self.city
            self._update_canvas()
            self._update_stats()
    
    def _update_canvas(self):
        """Update the city canvas display with enhanced graphics."""
        self.canvas.delete("all")
        
        cell_display_size = int(self.cell_size * self.zoom_level)
        
        # Draw grid if zoomed in enough
        if self.zoom_level > 0.8:
            for x in range(self.city.width + 1):
                x_pos = x * cell_display_size
                self.canvas.create_line(x_pos, 0, x_pos, self.city.height * cell_display_size,
                                      fill=self.colors['grid'], width=1)
            
            for y in range(self.city.height + 1):
                y_pos = y * cell_display_size
                self.canvas.create_line(0, y_pos, self.city.width * cell_display_size, y_pos,
                                      fill=self.colors['grid'], width=1)
        
        # Draw city cells with enhanced graphics
        for y in range(self.city.height):
            for x in range(self.city.width):
                cell = self.city.get_cell(x, y)
                
                x_pos = x * cell_display_size
                y_pos = y * cell_display_size
                
                # Determine cell color and style
                if cell is None:
                    # Empty cell with subtle pattern
                    color = self.colors['empty']
                    outline_color = self.colors['grid']
                    self._draw_empty_cell(x_pos, y_pos, cell_display_size, color, outline_color)
                else:
                    # Get enhanced color from cell
                    color = self._get_enhanced_color(cell)
                    outline_color = self._get_outline_color(cell)
                    self._draw_cell_with_effects(x_pos, y_pos, cell_display_size, cell, color, outline_color)
                
                # Draw disaster effects
                self._draw_disaster_effects(x_pos, y_pos, cell_display_size, x, y)
                
                # Draw traffic effects
                self._draw_traffic_effects(x_pos, y_pos, cell_display_size, x, y)
        
        # Update scroll region
        self.canvas.configure(scrollregion=(0, 0, 
                                          self.city.width * cell_display_size,
                                          self.city.height * cell_display_size))
    
    def _draw_empty_cell(self, x: int, y: int, size: int, color: str, outline_color: str):
        """Draw an empty cell with subtle pattern."""
        # Main rectangle
        self.canvas.create_rectangle(x, y, x + size, y + size,
                                   fill=color, outline=outline_color, width=1)
        
        # Add subtle diagonal lines for texture
        if size > 8:
            self.canvas.create_line(x + 2, y + 2, x + size - 2, y + size - 2,
                                  fill=outline_color, width=1, dash=(2, 2))
    
    def _draw_cell_with_effects(self, x: int, y: int, size: int, cell, color: str, outline_color: str):
        """Draw a cell with enhanced visual effects."""
        # Main rectangle with gradient effect
        self.canvas.create_rectangle(x, y, x + size, y + size,
                                   fill=color, outline=outline_color, width=2)
        
        # Add visual effects based on cell type
        if isinstance(cell, Zone):
            self._draw_zone_effects(x, y, size, cell)
        elif isinstance(cell, Infrastructure):
            self._draw_infrastructure_effects(x, y, size, cell)
    
    def _draw_zone_effects(self, x: int, y: int, size: int, zone):
        """Draw visual effects for zones."""
        # Development level indicators
        if zone.development_level > 0:
            # Draw building-like shapes
            building_height = min(size // 3, zone.development_level * 2)
            building_width = size // 2
            
            # Building base
            building_x = x + (size - building_width) // 2
            building_y = y + size - building_height - 2
            
            # Draw multiple buildings for higher development
            for i in range(min(zone.development_level, 3)):
                offset = i * (building_width // 3)
                self.canvas.create_rectangle(building_x + offset, building_y,
                                           building_x + offset + building_width // 2, building_y + building_height,
                                           fill=self._darken_color(zone.get_color(), 0.3), outline="black", width=1)
                
                # Windows
                if size > 12:
                    window_size = max(1, size // 8)
                    self.canvas.create_oval(building_x + offset + 2, building_y + 2,
                                          building_x + offset + window_size, building_y + window_size,
                                          fill="yellow", outline="")
        
        # Zone type indicator
        if size > 10:
            zone_symbols = {
                'residential': '🏠',
                'commercial': '🏪',
                'industrial': '🏭'
            }
            symbol = zone_symbols.get(zone.zone_type, '')
            if symbol:
                self.canvas.create_text(x + size // 2, y + size // 2, text=symbol, font=("Arial", max(6, size // 3)))
    
    def _draw_infrastructure_effects(self, x: int, y: int, size: int, infrastructure):
        """Draw visual effects for infrastructure."""
        infra_type = infrastructure.infrastructure_type
        
        # Infrastructure-specific symbols
        symbols = {
            'road': '🛣️',
            'highway': '🛣️',
            'power_plant': '⚡',
            'water_facility': '💧',
            'waste_facility': '🗑️',
            'school': '🏫',
            'hospital': '🏥',
            'park': '🌳',
            'police_station': '👮',
            'fire_station': '🚒',
            'subway_station': '🚇',
            'bridge': '🌉'
        }
        
        symbol = symbols.get(infra_type, '')
        if symbol and size > 8:
            self.canvas.create_text(x + size // 2, y + size // 2, text=symbol, font=("Arial", max(6, size // 3)))
        
        # Special effects for certain infrastructure
        if infra_type == 'power_plant':
            # Add power lines effect
            for i in range(3):
                line_x = x + (i + 1) * size // 4
                self.canvas.create_line(line_x, y + 2, line_x, y + size - 2,
                                      fill="yellow", width=2)
        
        elif infra_type == 'road':
            # Add road markings
            if size > 6:
                self.canvas.create_line(x + size // 2, y, x + size // 2, y + size,
                                      fill="white", width=1, dash=(2, 2))
    
    def _get_enhanced_color(self, cell) -> str:
        """Get enhanced color for a cell with development level consideration."""
        if isinstance(cell, Zone):
            return cell.get_color()  # Zone colors already include state effects
        
        elif isinstance(cell, Infrastructure):
            infra_type = cell.infrastructure_type
            return self.infrastructure_colors.get(infra_type, cell.get_color())
        
        return cell.get_color()
    
    def _get_outline_color(self, cell) -> str:
        """Get outline color for a cell."""
        if isinstance(cell, Zone):
            return "black" if cell.development_level > 0 else self.colors['grid']
        elif isinstance(cell, Infrastructure):
            return "black"
        return self.colors['grid']
    
    def _darken_color(self, hex_color: str, factor: float) -> str:
        """Darken a hex color by the given factor (0-1)."""
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        r = int(r * (1 - factor))
        g = int(g * (1 - factor))
        b = int(b * (1 - factor))
        
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def _draw_disaster_effects(self, x: int, y: int, size: int, grid_x: int, grid_y: int):
        """Draw disaster effects on the canvas."""
        # Check for disaster risk at this position
        disaster_risk = self.city.get_disaster_risk(grid_x, grid_y)
        
        if disaster_risk > 0:
            # Draw disaster warning overlay
            alpha = min(0.7, disaster_risk / 100.0)
            overlay_color = self.colors['disaster']
            
            # Create semi-transparent overlay
            self.canvas.create_rectangle(x, y, x + size, y + size,
                                       fill=overlay_color, outline="", stipple="gray50")
            
            # Add disaster warning symbol
            if size > 8:
                self.canvas.create_text(x + size // 2, y + size // 2, 
                                      text="🚨", font=("Arial", max(6, size // 4)))
    
    def _draw_traffic_effects(self, x: int, y: int, size: int, grid_x: int, grid_y: int):
        """Draw traffic effects on the canvas."""
        # Check if this is a road with traffic
        cell = self.city.get_cell(grid_x, grid_y)
        if cell and hasattr(cell, 'infrastructure_type') and cell.infrastructure_type == 'road':
            traffic_level = self.city.get_traffic_level(grid_x, grid_y)
            
            if traffic_level > 0:
                # Determine traffic color based on level
                if traffic_level <= 3:
                    traffic_color = self.colors['traffic_low']
                elif traffic_level <= 6:
                    traffic_color = self.colors['traffic_medium']
                else:
                    traffic_color = self.colors['traffic_high']
                
                # Draw traffic overlay
                self.canvas.create_rectangle(x, y, x + size, y + size,
                                           fill=traffic_color, outline="", stipple="gray25")
                
                # Add traffic symbol
                if size > 8:
                    self.canvas.create_text(x + size // 2, y + size // 2, 
                                          text="🚦", font=("Arial", max(6, size // 4)))
    
    def _update_stats(self):
        """Update the statistics display."""
        # Update main stats
        stats = {
            'money': f"${self.city.money:,}",
            'population': f"{self.city.population:,}",
            'happiness': f"{self.city.happiness:.1f}%",
            'employment': f"{self.city.employment_rate * 100:.1f}%",
            'pollution': f"{self.city.pollution:.1f}",
            'tax_revenue': f"${self.city.tax_revenue:,}/month",
            'maintenance': f"${self.city.maintenance_cost:,}/month"
        }
        
        for key, value in stats.items():
            if key in self.stat_labels:
                label_text = key.replace('_', ' ').title() + ": " + value
                self.stat_labels[key].config(text=label_text)
        
        # Update zone counts
        for zone_type, count in self.city.zone_counts.items():
            if zone_type in self.zone_labels:
                self.zone_labels[zone_type].config(text=f"{zone_type.capitalize()}: {count}")
        
        # Update building counts
        for building_type, count in self.city.building_counts.items():
            if building_type in self.building_labels:
                display_name = building_type.replace("_", " ").title()
                self.building_labels[building_type].config(text=f"{display_name}: {count}")
        
        # Update city info text
        self.city_info_text.delete(1.0, tk.END)
        info = f"""City Overview:
Grid Size: {self.city.width} x {self.city.height}
Total Zones: {sum(self.city.zone_counts.values())}
Power Coverage: {len(self.city.power_coverage)} tiles
Water Coverage: {len(self.city.water_coverage)} tiles
Road Network: {len(self.city.road_network)} tiles

Financial Status:
Net Income: ${self.city.tax_revenue - self.city.maintenance_cost:,}/month
"""
        
        if self.city.money < 10000:
            info += "\n⚠️ WARNING: Low funds!"
        if self.city.happiness < 30:
            info += "\n⚠️ WARNING: Low happiness!"
        if self.city.pollution > 70:
            info += "\n⚠️ WARNING: High pollution!"
        
        # Add disaster and traffic info
        info += f"\n\nDisaster & Traffic Status:"
        info += f"\nActive Disasters: {len(self.city.active_disasters)}"
        info += f"\nRoad Network: {len(self.city.road_network)} tiles"
        info += f"\nHigh Traffic Areas: {len([t for t in self.city.traffic_levels.values() if t > 6])}"
        
        self.city_info_text.insert(1.0, info)
        
        # Update disaster and traffic displays
        self._update_disasters_display()
        self._update_traffic_display()
    
    def _on_simulation_update(self):
        """Called when simulation updates."""
        # Update date display
        sim_info = self.simulation.get_simulation_info()
        self.date_label.config(text=f"Date: {sim_info['date']}")
        
        # Update city statistics
        self.city.update_statistics()
    
    def _update_ui(self):
        """Main UI update loop."""
        # Update simulation
        if self.simulation.update():
            # Simulation advanced, update displays
            self._update_stats()
            
            # Occasionally update canvas for visual changes
            if self.simulation.total_days_simulated % 7 == 0:  # Weekly
                self._update_canvas()
        
        # Schedule next update
        self.root.after(100, self._update_ui)  # Update every 100ms
    
    def _update_disasters_display(self):
        """Update the disasters display."""
        if self.city.active_disasters:
            disaster_text = "Active Disasters:\n"
            for disaster in self.city.active_disasters:
                disaster_text += f"• {disaster['type'].title()} at ({disaster['x']}, {disaster['y']}) - Severity: {disaster['severity']}\n"
        else:
            disaster_text = "No active disasters"
        
        self.disasters_label.config(text=disaster_text)
    
    def _update_traffic_display(self):
        """Update the traffic display."""
        total_roads = len(self.city.road_network)
        high_traffic = len([t for t in self.city.traffic_levels.values() if t > 6])
        avg_traffic = sum(self.city.traffic_levels.values()) / len(self.city.traffic_levels) if self.city.traffic_levels else 0
        
        self.traffic_labels['road_segments'].config(text=f"Total Road Segments: {total_roads}")
        self.traffic_labels['high_traffic'].config(text=f"High Traffic Areas: {high_traffic}")
        self.traffic_labels['avg_traffic'].config(text=f"Average Traffic Level: {avg_traffic:.1f}")


def main():
    """Main entry point for the city simulation game."""
    # Create the main tkinter window
    root = tk.Tk()
    root.title("City Simulation Game - Enhanced Edition with Desirability System")
    root.geometry("1400x900")  # Increased window size for better graphics
    root.resizable(True, True)
    
    # Set minimum window size
    root.minsize(1000, 700)  # Increased minimum size
    
    # Create and start the game UI
    game_ui = CitySimulationUI(root)
    
    # Start the main event loop
    root.mainloop()


if __name__ == "__main__":
    main()
