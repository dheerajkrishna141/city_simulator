"""
Building Class - Represents individual buildings in the city

Handles specific buildings like schools, hospitals, and other structures.
"""

from typing import Dict, Any

class Building:
    """
    Represents a specific building placed in the city.
    Different from zones - these are individual structures with specific functions.
    """
    
    # Building types and their characteristics
    BUILDING_TYPES = {
        'house': {
            'color': '#228B22',  # Forest green
            'cost': 5000,
            'maintenance': 50,
            'population': 200,
            'description': 'High-density housing'
        },
        'shop': {
            'color': '#4169E1',  # Royal blue
            'cost': 8000,
            'maintenance': 100,
            'jobs': 50,
            'description': 'Commercial building'
        },
        'factory': {
            'color': '#B8860B',  # Dark goldenrod
            'cost': 15000,
            'maintenance': 200,
            'jobs': 100,
            'pollution': 10,
            'description': 'Industrial facility'
        },
        'school': {
            'color': '#FFD700',  # Gold
            'cost': 25000,
            'maintenance': 300,
            'education_range': 8,
            'description': 'Educational facility'
        },
        'hospital': {
            'color': '#FF6347',  # Tomato
            'cost': 40000,
            'maintenance': 500,
            'health_range': 10,
            'description': 'Medical facility'
        },
        'park': {
            'color': '#32CD32',  # Lime green
            'cost': 3000,
            'maintenance': 25,
            'happiness_range': 6,
            'happiness_boost': 10,
            'description': 'Recreation area'
        },
        'police_station': {
            'color': '#000080',  # Navy
            'cost': 30000,
            'maintenance': 400,
            'safety_range': 12,
            'description': 'Law enforcement'
        },
        'fire_station': {
            'color': '#DC143C',  # Crimson
            'cost': 20000,
            'maintenance': 250,
            'safety_range': 10,
            'description': 'Fire protection'
        }
    }
    
    def __init__(self, x: int, y: int, building_type: str):
        """
        Initialize a new building.
        
        Args:
            x, y: Grid coordinates
            building_type: Type of building to create
        """
        self.x = x
        self.y = y
        self.building_type = building_type
        self.construction_time = 0  # Time to build (0 = instant for now)
        self.condition = 100  # Building condition (0-100)
        self.efficiency = 1.0  # Operating efficiency (0-1)
        
        # Validate building type
        if building_type not in self.BUILDING_TYPES:
            raise ValueError(f"Invalid building type: {building_type}")
        
        self.properties = self.BUILDING_TYPES[building_type].copy()
    
    def get_color(self) -> str:
        """Get the display color for this building type."""
        # Adjust color based on condition
        if self.condition < 50:
            # Damaged buildings are darker
            return self._darken_color(self.properties['color'], 0.3)
        elif self.condition < 80:
            return self._darken_color(self.properties['color'], 0.1)
        return self.properties['color']
    
    def _darken_color(self, hex_color: str, factor: float) -> str:
        """Darken a hex color by the given factor (0-1)."""
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        # Reduce brightness
        r = int(r * (1 - factor))
        g = int(g * (1 - factor))
        b = int(b * (1 - factor))
        
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def get_cost(self) -> int:
        """Get the construction cost of this building."""
        return self.properties.get('cost', 0)
    
    def get_maintenance_cost(self) -> int:
        """Get the monthly maintenance cost of this building."""
        base_cost = self.properties.get('maintenance', 0)
        # Higher maintenance for damaged buildings
        condition_modifier = 1.0 + (100 - self.condition) / 200
        return int(base_cost * condition_modifier)
    
    def update_condition(self, city, time_passed: int = 1):
        d = 0.1 * time_passed
        
        if city.pollution > 50:
            d *= 1.5
        
        if city.money > 100000:
            d *= 0.8
        
        self.condition = max(0, self.condition - d)
        
        if self.condition > 80:
            self.efficiency = 1.0
        elif self.condition > 50:
            self.efficiency = 0.8
        elif self.condition > 20:
            self.efficiency = 0.5
        else:
            self.efficiency = 0.2
    
    def get_service_area(self) -> int:
        """Get the service radius of this building."""
        service_ranges = {
            'education_range': self.properties.get('education_range', 0),
            'health_range': self.properties.get('health_range', 0),
            'happiness_range': self.properties.get('happiness_range', 0),
            'safety_range': self.properties.get('safety_range', 0)
        }
        return max(service_ranges.values())
    
    def provides_service(self, service_type: str) -> bool:
        """Check if this building provides a specific service type."""
        service_map = {
            'education': 'education_range',
            'health': 'health_range',
            'happiness': 'happiness_range',
            'safety': 'safety_range'
        }
        return service_map.get(service_type) in self.properties
    
    def get_service_strength(self, service_type: str, distance: int) -> float:
        """
        Get the strength of service at a given distance.
        
        Args:
            service_type: Type of service to check
            distance: Distance from building
        
        Returns:
            Service strength (0-1)
        """
        service_range = 0
        if service_type == 'education':
            service_range = self.properties.get('education_range', 0)
        elif service_type == 'health':
            service_range = self.properties.get('health_range', 0)
        elif service_type == 'happiness':
            service_range = self.properties.get('happiness_range', 0)
        elif service_type == 'safety':
            service_range = self.properties.get('safety_range', 0)
        
        if service_range == 0 or distance > service_range:
            return 0.0
        
        # Linear falloff with distance
        strength = max(0, 1.0 - (distance / service_range))
        return strength * self.efficiency
    
    def get_employment(self) -> int:
        """Get number of jobs this building provides."""
        jobs = self.properties.get('jobs', 0)
        return int(jobs * self.efficiency)
    
    def get_population(self) -> int:
        """Get population capacity of this building."""
        population = self.properties.get('population', 0)
        return int(population * self.efficiency)
    
    def get_pollution(self) -> float:
        """Get pollution generated by this building."""
        pollution = self.properties.get('pollution', 0)
        return pollution * self.efficiency
    
    def get_info(self) -> Dict[str, Any]:
        """Get detailed information about this building."""
        info = {
            'type': 'building',
            'building_type': self.building_type,
            'position': (self.x, self.y),
            'condition': self.condition,
            'efficiency': self.efficiency,
            'maintenance_cost': self.get_maintenance_cost(),
            'description': self.properties.get('description', '')
        }
        
        # Add building-specific info
        if self.get_employment() > 0:
            info['jobs'] = self.get_employment()
        if self.get_population() > 0:
            info['population'] = self.get_population()
        if self.get_pollution() > 0:
            info['pollution'] = self.get_pollution()
        
        # Add service info
        for service in ['education', 'health', 'happiness', 'safety']:
            if self.provides_service(service):
                info[f'{service}_range'] = self.get_service_area()
        
        return info
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert building to dictionary for saving."""
        return {
            'type': 'building',
            'building_type': self.building_type,
            'x': self.x,
            'y': self.y,
            'condition': self.condition,
            'efficiency': self.efficiency
        }
    
    def __str__(self) -> str:
        """String representation of the building."""
        condition_desc = "Excellent" if self.condition > 80 else \
                        "Good" if self.condition > 60 else \
                        "Fair" if self.condition > 40 else \
                        "Poor" if self.condition > 20 else "Critical"
        
        return f"{self.building_type.replace('_', ' ').title()} ({condition_desc})"
