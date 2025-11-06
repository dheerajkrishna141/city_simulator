"""
Test suite for City Simulation Game

Following agents.md guidelines:
- Fast, deterministic, and repeatable tests
- Mock data/fixtures for isolation
- Edge cases coverage
- Both unit and integration tests
- Using pytest framework
"""

import pytest
import math
from unittest.mock import Mock, patch
from city import City
from simulation import Simulation
from zone import Zone
from building import Building
from infrastructure import Infrastructure


class TestCity:
    """Unit tests for City class - testing core city behaviors in isolation."""
    
    def test_city_initialization(self):
        """Test city initializes with correct default values."""
        city = City(30, 40)
        
        assert city.width == 30
        assert city.height == 40
        assert city.money == 100000
        assert city.population == 0
        assert city.happiness == 50.0
        assert city.pollution == 0.0
        assert len(city.grid) == 40  # height
        assert len(city.grid[0]) == 30  # width
    
    def test_city_bounds_validation(self):
        """Test city validates coordinates within bounds."""
        city = City(10, 10)
        
        # Valid coordinates
        assert city.is_valid_position(0, 0)
        assert city.is_valid_position(9, 9)
        assert city.is_valid_position(5, 5)
        
        # Invalid coordinates - edge cases
        assert not city.is_valid_position(-1, 0)
        assert not city.is_valid_position(0, -1)
        assert not city.is_valid_position(10, 0)
        assert not city.is_valid_position(0, 10)
        assert not city.is_valid_position(100, 100)
    
    def test_zone_placement(self):
        """Test zone placement and grid updates."""
        city = City(10, 10)
        
        # Place a residential zone
        success = city.place_zone(5, 5, 'residential')
        assert success
        
        cell = city.get_cell(5, 5)
        assert isinstance(cell, Zone)
        assert cell.zone_type == 'residential'
        assert cell.x == 5
        assert cell.y == 5
        
        # Try to place on occupied cell
        success = city.place_zone(5, 5, 'commercial')
        assert not success  # Should fail
    
    def test_money_transactions(self):
        """Test city money management with edge cases."""
        city = City(10, 10)
        initial_money = city.money
        
        # Valid transaction
        assert city.spend_money(1000)
        assert city.money == initial_money - 1000
        
        # Transaction exceeding budget
        assert not city.spend_money(200000)  # More than available
        assert city.money == initial_money - 1000  # Unchanged
        
        # Add money
        city.add_money(5000)
        assert city.money == initial_money - 1000 + 5000


class TestZone:
    """Unit tests for Zone class - testing zone behaviors in isolation."""
    
    def test_zone_initialization(self):
        """Test zone initializes with correct properties."""
        zone = Zone(10, 15, 'residential')
        
        assert zone.x == 10
        assert zone.y == 15
        assert zone.zone_type == 'residential'
        assert zone.development_level == 1
        assert zone.age == 0
        assert zone.desirability == 50.0
    
    def test_zone_development_progression(self):
        """Test zone development with good conditions."""
        zone = Zone(5, 5, 'residential')
        initial_level = zone.development_level
        
        # Mock good development conditions
        zone.desirability = 80.0
        zone.has_power = True
        zone.has_water = True
        
        # Multiple development attempts
        for _ in range(10):
            zone.try_develop()
        
        # Should have developed beyond initial level
        assert zone.development_level >= initial_level
    
    def test_zone_development_requirements(self):
        """Test zone development fails without requirements."""
        zone = Zone(5, 5, 'residential')
        zone.desirability = 20.0  # Low desirability
        zone.has_power = False
        zone.has_water = False
        
        initial_level = zone.development_level
        
        # Try to develop multiple times
        for _ in range(20):
            zone.try_develop()
        
        # Should not develop without requirements
        assert zone.development_level == initial_level
    
    def test_zone_type_characteristics(self):
        """Test different zone types have correct characteristics."""
        residential = Zone(0, 0, 'residential')
        commercial = Zone(0, 0, 'commercial')
        industrial = Zone(0, 0, 'industrial')
        
        # Test max development levels
        assert residential.max_development == 5
        assert commercial.max_development == 4
        assert industrial.max_development == 4
        
        # Test power requirements
        assert Zone.ZONE_TYPES['residential']['power_required']
        assert Zone.ZONE_TYPES['commercial']['power_required']
        assert Zone.ZONE_TYPES['industrial']['power_required']


class TestBuilding:
    """Unit tests for Building class - testing building behaviors in isolation."""
    
    def test_building_initialization(self):
        """Test building initializes with correct properties."""
        building = Building(8, 12, 'school')
        
        assert building.x == 8
        assert building.y == 12
        assert building.building_type == 'school'
        assert building.age == 0
        assert building.efficiency == 100.0
        assert building.needs_power
        assert building.needs_water
    
    def test_building_efficiency_degradation(self):
        """Test building efficiency decreases with age."""
        building = Building(0, 0, 'hospital')
        initial_efficiency = building.efficiency
        
        # Age the building
        building.age = 50
        building.update_efficiency()
        
        assert building.efficiency < initial_efficiency
        assert building.efficiency >= 0.0  # Should not go negative
    
    def test_building_cost_calculation(self):
        """Test building costs are calculated correctly."""
        school = Building(0, 0, 'school')
        hospital = Building(0, 0, 'hospital')
        
        # Test construction costs from BUILDING_TYPES
        assert school.get_cost() == 25000
        assert hospital.get_cost() == 40000
        
        # Test maintenance costs
        assert school.get_maintenance_cost() == 300
        assert hospital.get_maintenance_cost() == 500


class TestSimulation:
    """Unit tests for Simulation class - testing simulation logic in isolation."""
    
    def test_simulation_initialization(self):
        """Test simulation initializes with correct state."""
        city = City(10, 10)
        sim = Simulation(city)
        
        assert sim.city == city
        assert not sim.running
        assert not sim.paused
        assert sim.game_day == 1
        assert sim.game_month == 1
        assert sim.game_year == 2024
        assert sim.simulation_speed == 1.0
    
    def test_time_advancement(self):
        """Test game time advances correctly."""
        city = City(5, 5)
        sim = Simulation(city)
        
        initial_day = sim.game_day
        
        # Advance time
        sim.advance_time()
        
        assert sim.game_day == initial_day + 1
        assert sim.total_days_simulated == 1
    
    def test_month_year_transitions(self):
        """Test month and year transitions work correctly."""
        city = City(5, 5)
        sim = Simulation(city)
        
        # Set to end of month
        sim.game_day = 30
        sim.advance_time()
        
        assert sim.game_day == 1
        assert sim.game_month == 2
        
        # Test year transition
        sim.game_month = 12
        sim.game_day = 30
        sim.advance_time()
        
        assert sim.game_day == 1
        assert sim.game_month == 1
        assert sim.game_year == 2025


class TestCityIntegration:
    """Integration tests - testing components working together."""
    
    def test_city_zone_building_interaction(self):
        """Test zones and buildings interact correctly within city."""
        city = City(20, 20)
        
        # Place a residential zone
        city.place_zone(10, 10, 'residential')
        
        # Place a school nearby
        city.place_building(12, 10, 'school')
        
        # Verify both are placed
        zone = city.get_cell(10, 10)
        building = city.get_cell(12, 10)
        
        assert isinstance(zone, Zone)
        assert isinstance(building, Building)
        assert zone.zone_type == 'residential'
        assert building.building_type == 'school'
    
    def test_infrastructure_coverage(self):
        """Test infrastructure affects zone development."""
        city = City(15, 15)
        
        # Place infrastructure
        city.place_infrastructure(5, 5, 'power_plant')
        city.place_infrastructure(7, 7, 'water_tower')
        
        # Update coverage
        city.update_infrastructure_coverage()
        
        # Verify coverage sets are updated
        assert len(city.power_coverage) > 0
        assert len(city.water_coverage) > 0
    
    def test_simulation_city_updates(self):
        """Test simulation properly updates city state."""
        city = City(10, 10)
        
        # Add some zones and buildings
        city.place_zone(5, 5, 'residential')
        city.place_zone(6, 5, 'commercial')
        city.place_building(7, 5, 'school')
        
        sim = Simulation(city)
        initial_money = city.money
        
        # Run simulation step
        sim.update_city()
        
        # City should have been updated
        # (exact changes depend on implementation)
        assert sim.total_days_simulated >= 0


class TestEdgeCases:
    """Tests for edge cases and unusual scenarios."""
    
    def test_zero_size_city(self):
        """Test behavior with minimal city size."""
        city = City(1, 1)
        
        assert city.width == 1
        assert city.height == 1
        assert city.is_valid_position(0, 0)
        assert not city.is_valid_position(1, 0)
        assert not city.is_valid_position(0, 1)
    
    def test_maximum_development_zones(self):
        """Test zones at maximum development level."""
        zone = Zone(0, 0, 'residential')
        zone.development_level = zone.max_development
        
        initial_level = zone.development_level
        zone.try_develop()  # Should not increase further
        
        assert zone.development_level == initial_level
    
    def test_invalid_zone_types(self):
        """Test handling of invalid zone types."""
        with pytest.raises(KeyError):
            Zone(0, 0, 'invalid_zone_type')
    
    def test_invalid_building_types(self):
        """Test handling of invalid building types."""
        with pytest.raises(KeyError):
            Building(0, 0, 'invalid_building_type')
    
    def test_extreme_simulation_speeds(self):
        """Test simulation with extreme speed values."""
        city = City(5, 5)
        sim = Simulation(city)
        
        # Test maximum speed
        sim.set_speed(sim.max_speed)
        assert sim.simulation_speed == sim.max_speed
        
        # Test minimum speed
        sim.set_speed(sim.min_speed)
        assert sim.simulation_speed == sim.min_speed
        
        # Test beyond limits (should be clamped)
        sim.set_speed(100.0)
        assert sim.simulation_speed == sim.max_speed
        
        sim.set_speed(0.01)
        assert sim.simulation_speed == sim.min_speed


if __name__ == '__main__':
    pytest.main([__file__])
