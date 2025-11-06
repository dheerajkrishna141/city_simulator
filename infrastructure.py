"""
Infrastructure Class - Represents city infrastructure elements

Handles roads, power plants, water facilities, and other infrastructure.
"""

from typing import Dict, Any

class Infrastructure:
    """
    Represents infrastructure elements like roads, power plants, and utilities.
    """
    
    # Infrastructure types and their characteristics
    INFRASTRUCTURE_TYPES = {
        'road': {
            'color': '#696969',  # Dim gray
            'cost': 100,
            'maintenance': 5,
            'description': 'Transportation network'
        },
        'power_plant': {
            'color': '#FFD700',  # Gold
            'cost': 50000,
            'maintenance': 1000,
            'power_output': 1000,
            'pollution': 20,
            'coverage_radius': 10,
            'description': 'Electrical power generation'
        },
        'water_facility': {
            'color': '#00CED1',  # Dark turquoise
            'cost': 30000,
            'maintenance': 600,
            'water_output': 800,
            'coverage_radius': 8,
            'description': 'Water treatment and distribution'
        },
        'waste_facility': {
            'color': '#8B4513',  # Saddle brown
            'cost': 25000,
            'maintenance': 500,
            'waste_capacity': 500,
            'coverage_radius': 6,
            'description': 'Waste management and recycling'
        },
        'subway_station': {
            'color': '#4B0082',  # Indigo
            'cost': 40000,
            'maintenance': 800,
            'transport_capacity': 2000,
            'coverage_radius': 5,
            'description': 'Underground transportation hub'
        },
        'bridge': {
            'color': '#708090',  # Slate gray
            'cost': 5000,
            'maintenance': 50,
            'description': 'River or terrain crossing'
        },
        'highway': {
            'color': '#2F4F4F',  # Dark slate gray
            'cost': 500,
            'maintenance': 25,
            'description': 'High-speed transportation'
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
            'fire_response_range': 8,
            'description': 'Fire protection and emergency response'
        },
    }

    
    def __init__(self, x: int, y: int, infrastructure_type: str):
        """
        Initialize new infrastructure.
        
        Args:
            x, y: Grid coordinates
            infrastructure_type: Type of infrastructure to create
        """
        self.x = x
        self.y = y
        self.infrastructure_type = infrastructure_type
        self.condition = 100  # Infrastructure condition (0-100)
        self.efficiency = 1.0  # Operating efficiency (0-1)
        self.age = 0  # Age in game time units
        self.upgrade_level = 0  # Upgrade level (0 = basic)
        
        # Validate infrastructure type
        if infrastructure_type not in self.INFRASTRUCTURE_TYPES:
            raise ValueError(f"Invalid infrastructure type: {infrastructure_type}")
        
        self.properties = self.INFRASTRUCTURE_TYPES[infrastructure_type].copy()
    
    def get_color(self) -> str:
        """Get the display color for this infrastructure type."""
        base_color = self.properties['color']
        
        # Adjust color based on condition
        if self.condition < 50:
            return self._darken_color(base_color, 0.4)
        elif self.condition < 80:
            return self._darken_color(base_color, 0.2)
        
        # Upgraded infrastructure is brighter
        if self.upgrade_level > 0:
            return self._brighten_color(base_color, 0.1 * self.upgrade_level)
        
        return base_color
    
    def _darken_color(self, hex_color: str, factor: float) -> str:
        """Darken a hex color by the given factor (0-1)."""
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        r = int(r * (1 - factor))
        g = int(g * (1 - factor))
        b = int(b * (1 - factor))
        
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def _brighten_color(self, hex_color: str, factor: float) -> str:
        """Brighten a hex color by the given factor (0-1)."""
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        r = min(255, int(r + (255 - r) * factor))
        g = min(255, int(g + (255 - g) * factor))
        b = min(255, int(b + (255 - b) * factor))
        
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def get_cost(self) -> int:
        """Get the construction cost of this infrastructure."""
        base_cost = self.properties.get('cost', 0)
        # Upgrades increase cost
        upgrade_multiplier = 1 + (self.upgrade_level * 0.5)
        return int(base_cost * upgrade_multiplier)
    
    def get_maintenance_cost(self) -> int:
        """Get the maintenance cost of this infrastructure."""
        base_maintenance = self.properties.get('maintenance', 0)
        
        # Factor in condition (poor condition = higher maintenance)
        condition_multiplier = 1.0 + (100 - self.condition) / 100
        
        # Factor in upgrades
        upgrade_multiplier = 1 + (self.upgrade_level * 0.3)
        
        return int(base_maintenance * condition_multiplier * upgrade_multiplier)
    
    def update_condition(self, city, time_passed: int = 1):
        """
        Update infrastructure condition over time.
        
        Args:
            city: City instance for context
            time_passed: Time units that have passed
        """
        self.age += time_passed
        
        # Base degradation rate
        degradation_rate = 0.2 * time_passed
        
        # Roads degrade faster with heavy use
        if self.infrastructure_type in ['road', 'highway']:
            traffic_factor = min(2.0, city.population / 10000)
            degradation_rate *= traffic_factor
        
        # Pollution affects infrastructure
        if city.pollution > 50:
            degradation_rate *= 1.3
        
        # Better maintenance if city is wealthy
        if city.money > 200000:
            degradation_rate *= 0.7
        
        self.condition = max(0, self.condition - degradation_rate)
        
        # Update efficiency based on condition
        if self.condition > 90:
            self.efficiency = 1.0
        elif self.condition > 70:
            self.efficiency = 0.9
        elif self.condition > 50:
            self.efficiency = 0.7
        elif self.condition > 30:
            self.efficiency = 0.5
        else:
            self.efficiency = 0.3
    
    def can_upgrade(self) -> bool:
        """Check if this infrastructure can be upgraded."""
        return self.upgrade_level < 3 and self.condition > 50
    
    def upgrade(self, city) -> bool:
        """
        Upgrade this infrastructure if possible.
        
        Args:
            city: City instance to check budget
        
        Returns:
            True if upgrade successful
        """
        if not self.can_upgrade():
            return False
        
        upgrade_cost = self.get_cost() * (self.upgrade_level + 1)
        
        if city.money < upgrade_cost:
            return False
        
        city.money -= upgrade_cost
        self.upgrade_level += 1
        self.efficiency = min(1.0, self.efficiency + 0.2)
        
        return True
    
    def get_output(self, output_type: str) -> float:
        """
        Get the output of this infrastructure for a specific type.
        
        Args:
            output_type: 'power', 'water', 'waste', 'transport'
        
        Returns:
            Output value modified by efficiency and upgrades
        """
        base_output = 0
        
        if output_type == 'power':
            base_output = self.properties.get('power_output', 0)
        elif output_type == 'water':
            base_output = self.properties.get('water_output', 0)
        elif output_type == 'waste':
            base_output = self.properties.get('waste_capacity', 0)
        elif output_type == 'transport':
            base_output = self.properties.get('transport_capacity', 0)
        
        if base_output == 0:
            return 0
        
        # Apply efficiency and upgrade modifiers
        upgrade_bonus = 1 + (self.upgrade_level * 0.25)
        return base_output * self.efficiency * upgrade_bonus
    
    def get_coverage_radius(self) -> int:
        """Get the coverage radius of this infrastructure."""
        base_radius = self.properties.get('coverage_radius', 0)
        # Upgrades can extend coverage
        return base_radius + self.upgrade_level
    
    def get_pollution(self) -> float:
        """Get pollution generated by this infrastructure."""
        base_pollution = self.properties.get('pollution', 0)
        if base_pollution == 0:
            return 0
        
        # Upgrades can reduce pollution
        pollution_reduction = self.upgrade_level * 0.15
        final_pollution = base_pollution * (1 - pollution_reduction)
        return max(0, final_pollution * self.efficiency)
    
    def affects_position(self, x: int, y: int) -> bool:
        """Check if this infrastructure affects the given position."""
        radius = self.get_coverage_radius()
        if radius == 0:
            return False
        
        distance_sq = (self.x - x) ** 2 + (self.y - y) ** 2
        return distance_sq <= radius ** 2
    
    def get_effect_strength(self, x: int, y: int) -> float:
        """
        Get the strength of effect at the given position.
        
        Returns:
            Effect strength (0-1)
        """
        radius = self.get_coverage_radius()
        if radius == 0:
            return 0
        
        distance = ((self.x - x) ** 2 + (self.y - y) ** 2) ** 0.5
        if distance > radius:
            return 0
        
        # Linear falloff with distance
        strength = max(0, 1.0 - (distance / radius))
        return strength * self.efficiency
    
    def requires_connection(self) -> bool:
        """Check if this infrastructure requires connection to road network."""
        connection_required = ['power_plant', 'water_facility', 'waste_facility', 'subway_station']
        return self.infrastructure_type in connection_required
    
    def get_info(self) -> Dict[str, Any]:
        """Get detailed information about this infrastructure."""
        info = {
            'type': 'infrastructure',
            'infrastructure_type': self.infrastructure_type,
            'position': (self.x, self.y),
            'condition': self.condition,
            'efficiency': self.efficiency,
            'age': self.age,
            'upgrade_level': self.upgrade_level,
            'maintenance_cost': self.get_maintenance_cost(),
            'description': self.properties.get('description', '')
        }
        
        # Add type-specific info
        for output_type in ['power', 'water', 'waste', 'transport']:
            output = self.get_output(output_type)
            if output > 0:
                info[f'{output_type}_output'] = output
        
        radius = self.get_coverage_radius()
        if radius > 0:
            info['coverage_radius'] = radius
        
        pollution = self.get_pollution()
        if pollution > 0:
            info['pollution'] = pollution
        
        return info
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert infrastructure to dictionary for saving."""
        return {
            'type': 'infrastructure',
            'infrastructure_type': self.infrastructure_type,
            'x': self.x,
            'y': self.y,
            'condition': self.condition,
            'efficiency': self.efficiency,
            'age': self.age,
            'upgrade_level': self.upgrade_level
        }
    
    def __str__(self) -> str:
        """String representation of the infrastructure."""
        name = self.infrastructure_type.replace('_', ' ').title()
        if self.upgrade_level > 0:
            name += f" (Level {self.upgrade_level + 1})"
        
        condition_desc = "Excellent" if self.condition > 80 else \
                        "Good" if self.condition > 60 else \
                        "Fair" if self.condition > 40 else \
                        "Poor" if self.condition > 20 else "Critical"
        
        return f"{name} ({condition_desc})"
