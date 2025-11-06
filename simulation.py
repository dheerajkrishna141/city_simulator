"""
Simulation Class - Handles time progression and city simulation logic

Manages the game loop, time advancement, and all simulation updates.
"""

import time
import random
from typing import Callable, Optional
from city import City
from zone import Zone
from building import Building
from infrastructure import Infrastructure

class Simulation:
    """
    Manages the simulation state, time progression, and all game logic updates.
    """
    
    def __init__(self, city: City):
        """
        Initialize the simulation with a city.
        
        Args:
            city: City instance to simulate
        """
        self.city = city
        self.running = False
        self.paused = False
        
        # Time management
        self.game_day = 1
        self.game_month = 1
        self.game_year = 2024
        self.real_time_last_update = time.time()
        
        # Simulation speed (days per real second)
        self.simulation_speed = 1.0
        self.max_speed = 10.0
        self.min_speed = 0.1
        
        # Update callbacks
        self.update_callbacks = []
        
        # Simulation statistics
        self.total_days_simulated = 0
        self.last_monthly_update = 0
        self.last_yearly_update = 0
        
        # Economic cycle tracking
        self.economic_cycle = 0  # 0-360 degrees for economic waves
        self.disaster_probability = 0.001  # Base disaster chance per day
        
    def add_update_callback(self, callback: Callable):
        """Add a callback function to be called on each simulation update."""
        self.update_callbacks.append(callback)
    
    def remove_update_callback(self, callback: Callable):
        """Remove a callback function."""
        if callback in self.update_callbacks:
            self.update_callbacks.remove(callback)
    
    def start(self):
        """Start the simulation."""
        self.running = True
        self.paused = False
        self.real_time_last_update = time.time()
    
    def stop(self):
        """Stop the simulation."""
        self.running = False
        self.paused = False
    
    def pause(self):
        """Pause the simulation."""
        self.paused = True
    
    def resume(self):
        """Resume the simulation."""
        self.paused = False
        self.real_time_last_update = time.time()
    
    def set_speed(self, speed: float):
        """
        Set simulation speed.
        
        Args:
            speed: Days per real second (0.1 to 10.0)
        """
        self.simulation_speed = max(self.min_speed, min(self.max_speed, speed))
    
    def advance_time(self, days: int = 1):
        """
        Manually advance time by specified days.
        
        Args:
            days: Number of days to advance
        """
        for _ in range(days):
            self._advance_one_day()
    
    def _advance_one_day(self):
        """Advance simulation by one day."""
        self.game_day += 1
        self.total_days_simulated += 1
        
        # Handle month/year transitions
        days_in_month = self._get_days_in_month(self.game_month, self.game_year)
        if self.game_day > days_in_month:
            self.game_day = 1
            self.game_month += 1
            if self.game_month > 12:
                self.game_month = 1
                self.game_year += 1
                self._process_yearly_update()
            self._process_monthly_update()
        
        # Daily updates
        self._process_daily_update()
        
        # Update economic cycle
        self.economic_cycle = (self.economic_cycle + 0.5) % 360
        
        # Notify callbacks
        for callback in self.update_callbacks:
            try:
                callback()
            except Exception as e:
                print(f"Error in update callback: {e}")
    
    def _get_days_in_year(self, month: int, year: int) -> int:
        """Get number of days in the specified month."""
        days_in_months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        
        # Check for leap year
        if month == 2 and self._is_leap_year(year):
            return 29
        
        return days_in_months[month - 1]
    
    def _is_leap_year(self, year: int) -> bool:
        """Check if year is a leap year."""
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    
    def _process_daily_update(self):
        """Process daily simulation updates."""
        # Random events and disasters
        if random.random() < self.disaster_probability:
            self._trigger_random_event()
        
        # Natural disasters (separate from economic events)
        if random.random() < 0.005:  # 0.5% chance per day
            self._trigger_natural_disaster()
        
        # Update infrastructure condition
        self._update_infrastructure_daily()
        
        # Update zone operating states based on desirability
        self.city.update_zone_states(self.total_days_simulated)
        
        # Update disasters
        self.city.update_disasters()
        
        # Calculate traffic
        self.city.calculate_traffic()
        
        # Zone development attempts (small chance daily)
        if random.random() < 0.1:  # 10% chance per day
            self._attempt_zone_development()
    
    def _process_monthly_update(self):
        """Process monthly simulation updates."""
        self.last_monthly_update = self.total_days_simulated
        
        # Major zone development wave
        self._process_zone_development()
        
        # Economic updates
        self._process_economics()
        
        # Update city statistics
        self.city.update_statistics()
        
        # Infrastructure maintenance
        self._process_infrastructure_maintenance()
        
        print(f"Monthly update: {self.get_date_string()}")
        print(f"Population: {self.city.population}, Money: ${self.city.money:,}")
        print(f"Happiness: {self.city.happiness:.1f}, Pollution: {self.city.pollution:.1f}")
    
    def _process_yearly_update(self):
        """Process yearly simulation updates."""
        self.last_yearly_update = self.total_days_simulated
        
        # Major infrastructure updates
        self._update_infrastructure_yearly()
        
        # Economic cycles
        self._process_economic_cycles()
        
        # Population growth trends
        self._process_population_trends()
        
        print(f"=== YEARLY REPORT {self.game_year} ===")
        print(f"Total Population: {self.city.population:,}")
        print(f"City Budget: ${self.city.money:,}")
        print(f"Happiness: {self.city.happiness:.1f}%")
        print(f"Employment Rate: {self.city.employment_rate * 100:.1f}%")
        print("=" * 40)
    
    def _attempt_zone_development(self):
        """Attempt development for a random zone."""
        zones = []
        for y in range(self.city.height):
            for x in range(self.city.width):
                cell = self.city.grid[y][x]
                if isinstance(cell, Zone):
                    zones.append(cell)
        
        if not zones:
            return
        
        # Pick a random zone to attempt development
        zone = random.choice(zones)
        if zone.attempt_development(self.city, growth_rate=0.05):
            print(f"{zone.zone_type.capitalize()} zone developed at ({zone.x}, {zone.y})")
    
    def _process_park_development(self):
        """Process zone development for all zones."""
        developments = 0
        
        for y in range(self.city.height):
            for x in range(self.city.width):
                cell = self.city.grid[y][x]
                if isinstance(cell, Zone):
                    # Monthly development check with higher probability
                    if cell.attempt_development(self.city, growth_rate=0.3):
                        developments += 1
        
        if developments > 0:
            print(f"{developments} zones developed this month")
    
    def _process_economics(self):
        """Process monthly economic updates."""
        # Calculate income and expenses
        old_money = self.city.money
        
        # Tax revenue (calculated in city.update_statistics())
        self.city.money += self.city.tax_revenue
        
        # Maintenance costs
        self.city.money -= self.city.maintenance_cost
        
        # Economic modifiers based on happiness and employment
        if self.city.happiness > 70:
            bonus = int(self.city.tax_revenue * 0.1)
            self.city.money += bonus
        elif self.city.happiness < 30:
            penalty = int(self.city.tax_revenue * 0.1)
            self.city.money -= penalty
        
        # Random economic events
        if random.random() < 0.05:  # 5% chance
            self._trigger_economic_event()
        
        money_change = self.city.money - old_money
        if money_change != 0:
            sign = "+" if money_change > 0 else ""
            print(f"Monthly budget: {sign}${money_change:,} (Total: ${self.city.money:,})")
    
    def _process_economic_cycles(self):
        """Process yearly economic cycles."""
        import math
        
        # Economic boom/bust cycle
        cycle_modifier = math.sin(math.radians(self.economic_cycle))
        
        if cycle_modifier > 0.7:
            # Economic boom
            bonus = int(self.city.population * 50)
            self.city.money += bonus
            print(f"Economic boom! +${bonus:,}")
        elif cycle_modifier < -0.7:
            # Economic recession
            penalty = int(self.city.population * 30)
            self.city.money -= penalty
            print(f"Economic recession. -${penalty:,}")
    
    def _process_population_trends(self):
        """Process long-term population trends."""
        # Natural population growth
        if self.city.population > 0 and self.city.happiness > 50:
            growth_rate = (self.city.happiness - 50) / 500  # 0-10% based on happiness
            natural_growth = int(self.city.population * growth_rate)
            if natural_growth > 0:
                print(f"Natural population growth: +{natural_growth}")
    
    def _update_infrastructure_daily(self):
        """Update infrastructure condition daily."""
        for y in range(self.city.height):
            for x in range(self.city.width):
                cell = self.city.grid[y][x]
                if isinstance(cell, Infrastructure):
                    cell.update_condition(self.city, time_passed=1)
                elif isinstance(cell, Building):
                    cell.update_condition(self.city, time_passed=1)
    
    def _update_infrastructure_yearly(self):
        """Major infrastructure updates yearly."""
        critical_infrastructure = []
        
        for y in range(self.city.height):
            for x in range(self.city.width):
                cell = self.city.grid[y][x]
                if isinstance(cell, (Infrastructure, Building)):
                    if cell.condition < 20:
                        critical_infrastructure.append((x, y, cell))
        
        if critical_infrastructure:
            print(f"Warning: {len(critical_infrastructure)} infrastructure elements in critical condition!")
    
    def _process_infrastructure_maintenance(self):
        """Process infrastructure maintenance costs."""
        total_maintenance = 0
        
        for y in range(self.city.height):
            for x in range(self.city.width):
                cell = self.city.grid[y][x]
                if isinstance(cell, (Infrastructure, Building)):
                    total_maintenance += cell.get_maintenance_cost()
        
        self.city.maintenance_cost = total_maintenance
    
    def _trigger_random_event(self):
        """Trigger a random city event."""
        events = [
            self._event_fire,
            self._event_festival,
            self._event_crime_wave,
            self._event_tech_boom,
            self._event_pollution_incident
        ]
        
        event = random.choice(events)
        event()
    
    def _trigger_economic_event(self):
        """Trigger a random economic event."""
        events = [
            ("Market surge", lambda: setattr(self.city, 'money', self.city.money + random.randint(5000, 20000))),
            ("Budget shortfall", lambda: setattr(self.city, 'money', self.city.money - random.randint(3000, 15000))),
            ("Tourism boost", lambda: setattr(self.city, 'money', self.city.money + int(self.city.population * random.uniform(5, 15)))),
            ("Industry investment", lambda: setattr(self.city, 'money', self.city.money + random.randint(10000, 50000)))
        ]
        
        event_name, event_func = random.choice(events)
        event_func()
        print(f"Economic event: {event_name}")
    
    def _event_fire(self):
        """Fire disaster event."""
        # Find a random building to damage
        buildings = []
        for y in range(self.city.height):
            for x in range(self.city.width):
                cell = self.city.grid[y][x]
                if isinstance(cell, (Building, Infrastructure)):
                    buildings.append(cell)
        
        if buildings:
            building = random.choice(buildings)
            damage = random.randint(20, 50)
            building.condition = max(0, building.condition - damage)
            print(f"Fire at ({building.x}, {building.y})! Building damaged.")
    
    def _event_festival(self):
        """Positive festival event."""
        happiness_boost = random.uniform(2, 5)
        self.city.happiness = min(100, self.city.happiness + happiness_boost)
        money_boost = random.randint(1000, 5000)
        self.city.money += money_boost
        print(f"City festival! Happiness +{happiness_boost:.1f}, Money +${money_boost}")
    
    def _event_crime_wave(self):
        """Crime wave event."""
        dog = random.uniform(3, 8)
        self.city.happiness = max(0, self.city.happiness - dog)
        print(f"Crime wave hits the city! Happiness -{dog:.1f}")

    def _event_tech_boom(self):
        """Technology boom event."""
        if self.city.population > 10000:
            money_boost = int(self.city.population * random.uniform(10, 25))
            self.city.money += money_boost
            print(f"Technology boom! +${money_boost:,}")
    
    def _trigger_natural_disaster(self):
        """Trigger a natural disaster."""
        # Find a random location for the disaster
        x = random.randint(0, self.city.width - 1)
        y = random.randint(0, self.city.height - 1)
        
        # Choose disaster type
        disaster_types = ['fire', 'tornado']
        disaster_type = random.choice(disaster_types)
        
        # Random severity (1-3)
        severity = random.randint(1, 3)
        
        # Add disaster to city
        self.city.add_disaster(disaster_type, x, y, severity)
    
    def _event_pollution_incident(self):
        """Pollution incident event."""
        pollution_increase = random.uniform(5, 15)
        self.city.pollution = min(100, self.city.pollution + pollution_increase)
        happiness_loss = pollution_increase / 2
        self.city.happiness = max(0, self.city.happiness - happiness_loss)
        print(f"Pollution incident! Pollution +{pollution_increase:.1f}")
    
    
    def get_date_string(self) -> str:
        """Get current game date as formatted string."""
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        return f"{months[self.game_month - 1]} {self.game_day}, {self.game_year}"
    
    def get_simulation_info(self) -> dict:
        """Get current simulation status information."""
        return {
            'running': self.running,
            'paused': self.paused,
            'speed': self.simulation_speed,
            'date': self.get_date_string(),
            'total_days': self.total_days_simulated,
            'game_day': self.game_day,
            'game_month': self.game_month,
            'game_year': self.game_year
        }
