"""
Zone Class - Represents zoned areas in the city

Handles residential, commercial, and industrial zones with development progression.
"""

from typing import Dict, Any
import random

class Zone:
    """
    Represents a zoned area that can develop over time based on city conditions.
    """
    
    # Zone types and their characteristics
    ZONE_TYPES = {
        'residential': {
            'color': '#98FB98',  # Pale green - more vibrant
            'max_development': 5,
            'population_per_level': 50,
            'power_required': True,
            'water_required': True
        },
        'commercial': {
            'color': '#87CEEB',  # Sky blue
            'max_development': 4,
            'jobs_per_level': 30,
            'power_required': True,
            'water_required': False
        },
        'industrial': {
            'color': '#DEB887',  # Burlywood - warmer brown
            'max_development': 4,
            'jobs_per_level': 40,
            'pollution_per_level': 5,
            'power_required': True,
            'water_required': False
        }
    }
    
    def __init__(self, x: int, y: int, zone_type: str):
        """
        Initialize a new zone.
        
        Args:
            x, y: Grid coordinates
            zone_type: 'residential', 'commercial', or 'industrial'
        """
        self.x = x
        self.y = y
        self.zone_type = zone_type
        self.development_level = 0  # 0 = undeveloped, max varies by type
        self.last_growth_check = 0  # Game time when last checked for growth
        self.desirability_score = 0.0  # Desirability score (0-100)
        self.operating_state = "normal"  # normal, thriving, struggling, abandoned
        self.last_state_change = 0  # Game time when last state changed
        
        # Validate zone type
        if zone_type not in self.ZONE_TYPES:
            raise ValueError(f"Invalid zone type: {zone_type}")
        
        self.properties = self.ZONE_TYPES[zone_type].copy()
    
    def get_color(self) -> str:
        """Get the display color for this zone type."""
        base_color = self.properties['color']
        
        # Adjust color based on development level
        if self.development_level == 0:
            # Undeveloped zones are lighter
            base_color = self._lighten_color(base_color, 0.5)
        
        # Adjust color based on operating state
        if self.operating_state == "thriving":
            # Thriving zones are brighter
            base_color = self._brighten_color(base_color, 0.2)
        elif self.operating_state == "struggling":
            # Struggling zones are darker
            base_color = self._darken_color(base_color, 0.3)
        elif self.operating_state == "abandoned":
            # Abandoned zones are very dark
            base_color = self._darken_color(base_color, 0.6)
        
        return base_color
    
    def _brighten_color(self, hex_color: str, factor: float) -> str:
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        r = min(255, int(r + (255 - r) * factor))
        g = min(255, int(g + (255 - g) * factor))
        b = min(255, int(b + (255 - b) * factor))
        
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def _darken_color(self, hex_color: str, factor: float) -> str:
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        r = int(r * (1 - factor))
        g = int(g * (1 - factor))
        b = int(b * (1 - factor))
        
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def _lighten_color(self, hex_color: str, factor: float) -> str:
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        r = int(r + (255 - r) * factor)
        g = int(g + (255 - g) * factor)
        b = int(b + (255 - b) * factor)
        
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def calculate_desirability(self, city) -> float:
        """
        Calculate desirability score based on proximity to amenities and commute distance.
        
        Args:
            city: City instance to check amenities against
        
        Returns:
            Desirability score (0-100)
        """
        score = 50.0  # Base score
        
        # Proximity to parks (positive impact)
        park_bonus = self._calculate_park_proximity(city)
        score += park_bonus
        
        # Proximity to schools (positive impact)
        school_bonus = self._calculate_school_proximity(city)
        score += school_bonus
        
        # Proximity to power plants (positive impact)
        power_bonus = self._calculate_power_proximity(city)
        score += power_bonus
        
        # Commute distance to other zones (negative impact for long distances)
        commute_penalty = self._calculate_commute_penalty(city)
        score -= commute_penalty
        
        # Traffic penalty (negative impact for high traffic areas)
        traffic_penalty = self._calculate_traffic_penalty(city)
        score -= traffic_penalty
        
        # Ensure score is within bounds
        score = max(0.0, min(100.0, score))
        
        return score
    
    def _calculate_park_proximity(self, city) -> float:
        """Calculate bonus from proximity to parks."""
        bonus = 0.0
        max_distance = 10  # Maximum distance to consider
        
        for y in range(city.height):
            for x in range(city.width):
                cell = city.get_cell(x, y)
                if cell and hasattr(cell, 'infrastructure_type') and cell.infrastructure_type == 'park':
                    distance = self._manhattan_distance(self.x, self.y, x, y)
                    if distance <= max_distance:
                        # Closer parks give more bonus
                        bonus += (max_distance - distance) * 2.0
        
        return min(20.0, bonus)  # Cap at 20 points
    
    def _calculate_school_proximity(self, city) -> float:
        """Calculate bonus from proximity to schools."""
        bonus = 0.0
        max_distance = 8  # Maximum distance to consider
        
        for y in range(city.height):
            for x in range(city.width):
                cell = city.get_cell(x, y)
                if cell and hasattr(cell, 'infrastructure_type') and cell.infrastructure_type == 'school':
                    distance = self._manhattan_distance(self.x, self.y, x, y)
                    if distance <= max_distance:
                        # Closer schools give more bonus
                        bonus += (max_distance - distance) * 1.5
        
        return min(15.0, bonus)  # Cap at 15 points
    
    def _calculate_power_proximity(self, city) -> float:
        """Calculate bonus from proximity to power plants."""
        bonus = 0.0
        max_distance = 12  # Maximum distance to consider
        
        for y in range(city.height):
            for x in range(city.width):
                cell = city.get_cell(x, y)
                if cell and hasattr(cell, 'infrastructure_type') and cell.infrastructure_type == 'power_plant':
                    distance = self._manhattan_distance(self.x, self.y, x, y)
                    if distance <= max_distance:
                        # Closer power plants give more bonus
                        bonus += (max_distance - distance) * 1.0
        
        return min(10.0, bonus)  # Cap at 10 points
    
    def _calculate_commute_penalty(self, city) -> float:
        """Calculate penalty from long commute distances to other zones."""
        penalty = 0.0
        total_zones = 0
        
        for y in range(city.height):
            for x in range(city.width):
                cell = city.get_cell(x, y)
                if isinstance(cell, Zone) and cell != self:
                    distance = self._road_distance_to_zone(city, x, y)
                    if distance > 0:
                        penalty += distance * 0.5  # 0.5 points per unit of distance
                        total_zones += 1
        
        if total_zones > 0:
            penalty = penalty / total_zones  # Average penalty
        
        return min(25.0, penalty)  # Cap at 25 points
    
    def _manhattan_distance(self, x1: int, y1: int, x2: int, y2: int) -> int:
        """Calculate Manhattan distance between two points."""
        return abs(x1 - x2) + abs(y1 - y2)
    
    def _road_distance_to_zone(self, city, target_x: int, target_y: int) -> int:
        """
        Calculate road distance to another zone using A* pathfinding.
        Returns -1 if no path exists.
        """
        if (self.x, self.y) not in city.road_network or (target_x, target_y) not in city.road_network:
            return -1
        
        # Simple BFS to find shortest road path
        visited = set()
        queue = [(self.x, self.y, 0)]  # (x, y, distance)
        
        while queue:
            x, y, distance = queue.pop(0)
            
            if (x, y) == (target_x, target_y):
                return distance
            
            if (x, y) in visited:
                continue
            
            visited.add((x, y))
            
            # Check all 4 directions
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_x, new_y = x + dx, y + dy
                if (new_x, new_y) in city.road_network and (new_x, new_y) not in visited:
                    queue.append((new_x, new_y, distance + 1))
        
        return -1  # No path found
    
    def _calculate_traffic_penalty(self, city) -> float:
        """Calculate penalty from high traffic levels."""
        penalty = 0.0
        
        # Check traffic level at this zone's position
        traffic_level = city.get_traffic_level(self.x, self.y)
        
        # Traffic penalty increases with traffic level
        if traffic_level > 0:
            penalty = min(15.0, traffic_level * 2.0)  # Cap at 15 points
        
        return penalty
    
    def update_operating_state(self, city, current_time: int):
        """
        Update the operating state based on desirability score and time.
        
        Args:
            city: City instance
            current_time: Current game time
        """
        # Only update every 7 days (weekly)
        if current_time - self.last_state_change < 7:
            return
        
        # Calculate current desirability
        self.desirability_score = self.calculate_desirability(city)
        
        # Determine new state based on desirability
        if self.desirability_score >= 80:
            new_state = "thriving"
        elif self.desirability_score >= 60:
            new_state = "normal"
        elif self.desirability_score >= 30:
            new_state = "struggling"
        else:
            new_state = "abandoned"
        
        # Update state if changed
        if new_state != self.operating_state:
            self.operating_state = new_state
            self.last_state_change = current_time
    
    def can_develop(self, city) -> bool:
        """
        Check if this zone can develop further.
        
        Args:
            city: City instance to check requirements against
        
        Returns:
            True if zone can develop
        """
        # Check if already at max development
        if self.development_level >= self.properties['max_development']:
            return False
        
        # Check power requirement
        if self.properties.get('power_required', False):
            if (self.x, self.y) not in city.power_coverage:
                return False
        
        # Check water requirement
        if self.properties.get('water_required', False):
            if (self.x, self.y) not in city.water_coverage:
                return False
        
        # Check for road access (zones need road connection)
        has_road_access = False
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = self.x + dx, self.y + dy
            if (nx, ny) in city.road_network:
                has_road_access = True
                break
        
        if not has_road_access:
            return False
        
        # Zone-specific requirements
        if self.zone_type == 'residential':
            # Residential needs low pollution and some commercial nearby
            return self._check_residential_requirements(city)
        elif self.zone_type == 'commercial':
            # Commercial needs population nearby
            return self._check_commercial_requirements(city)
        elif self.zone_type == 'industrial':
            # Industrial just needs basic infrastructure
            return True
        
        return False
    
    def _check_residential_requirements(self, city) -> bool:
        """Check specific requirements for residential development."""
        # Check local pollution level
        local_pollution = 0
        neighbors = city.get_neighbors(self.x, self.y, radius=3)
        
        for nx, ny, cell in neighbors:
            if hasattr(cell, 'zone_type') and cell.zone_type == 'industrial':
                local_pollution += cell.development_level * 2
        
        if local_pollution > 10:  # Too much pollution
            return False
        
        # Check for commercial zones nearby (for jobs/shopping)
        commercial_nearby = 0
        for nx, ny, cell in neighbors:
            if hasattr(cell, 'zone_type') and cell.zone_type == 'commercial':
                commercial_nearby += 1
        
        # Need at least some commercial development or be in early game
        return commercial_nearby > 0 or city.population < 1000
    
    def _check_commercial_requirements(self, city) -> bool:
        """Check specific requirements for commercial development."""
        # Commercial needs population nearby to serve
        population_nearby = 0
        neighbors = city.get_neighbors(self.x, self.y, radius=5)
        
        for nx, ny, cell in neighbors:
            if hasattr(cell, 'zone_type') and cell.zone_type == 'residential':
                population_nearby += cell.development_level * 50
        
        # Need at least 200 people in the area to support development
        return population_nearby >= 200
    
    def attempt_development(self, city, growth_rate: float = 0.1) -> bool:
        """
        Attempt to develop this zone based on current conditions.
        
        Args:
            city: City instance
            growth_rate: Base probability of growth per attempt
        
        Returns:
            True if zone developed this turn
        """
        if not self.can_develop(city):
            return False
        
        # Calculate actual growth probability based on conditions
        actual_rate = growth_rate
        
        # Happiness affects growth rate
        happiness_modifier = (city.happiness - 50) / 100  # -0.5 to +0.5
        actual_rate += happiness_modifier * 0.05
        
        # Employment affects residential growth
        if self.zone_type == 'residential':
            employment_modifier = (city.employment_rate - 0.5) * 0.1
            actual_rate += employment_modifier
        
        # Money affects all growth (wealthy cities grow faster)
        if city.money > 50000:
            actual_rate += 0.02
        elif city.money < 10000:
            actual_rate -= 0.02
        
        # Random development check
        if random.random() < actual_rate:
            self.development_level += 1
            return True
        
        return False
    
    def get_info(self) -> Dict[str, Any]:
        """Get detailed information about this zone."""
        info = {
            'type': 'zone',
            'zone_type': self.zone_type,
            'development_level': self.development_level,
            'max_development': self.properties['max_development'],
            'position': (self.x, self.y)
        }
        
        # Add zone-specific info
        if self.zone_type == 'residential':
            info['population'] = self.development_level * self.properties['population_per_level']
        elif self.zone_type in ['commercial', 'industrial']:
            info['jobs'] = self.development_level * self.properties['jobs_per_level']
        
        if self.zone_type == 'industrial':
            info['pollution'] = self.development_level * self.properties['pollution_per_level']
        
        return info
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert zone to dictionary for saving."""
        return {
            'type': 'zone',
            'zone_type': self.zone_type,
            'development_level': self.development_level,
            'x': self.x,
            'y': self.y
        }
    
    def __str__(self) -> str:
        """String representation of the zone."""
        return f"{self.zone_type.capitalize()} Zone (Level {self.development_level})"
