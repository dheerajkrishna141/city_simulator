"""
Simple test runner for City Simulation - runs without external dependencies

This provides basic testing capability following agents.md guidelines
without requiring pytest installation.
"""

import sys
import traceback
from city import City
from simulation import Simulation
from zone import Zone
from building import Building
from infrastructure import Infrastructure


class SimpleTestRunner:
    """Basic test runner that mimics pytest functionality."""
    
    def __init__(self):
        self.tests_run = 0
        self.tests_passed = 0
        self.tests_failed = 0
        self.failures = []
    
    def run_test(self, test_func, test_name):
        """Run a single test function."""
        try:
            self.tests_run += 1
            test_func()
            self.tests_passed += 1
            print(f"✓ {test_name}")
        except Exception as e:
            self.tests_failed += 1
            self.failures.append((test_name, str(e), traceback.format_exc()))
            print(f"✗ {test_name}: {str(e)}")
    
    def assert_equal(self, actual, expected, message=""):
        """Basic assertion for equality."""
        if actual != expected:
            raise AssertionError(f"Expected {expected}, got {actual}. {message}")
    
    def assert_true(self, condition, message=""):
        """Basic assertion for true condition."""
        if not condition:
            raise AssertionError(f"Expected True, got False. {message}")
    
    def assert_false(self, condition, message=""):
        """Basic assertion for false condition."""
        if condition:
            raise AssertionError(f"Expected False, got True. {message}")
    
    def print_summary(self):
        """Print test run summary."""
        print(f"\n{'='*50}")
        print(f"Tests run: {self.tests_run}")
        print(f"Passed: {self.tests_passed}")
        print(f"Failed: {self.tests_failed}")
        
        if self.failures:
            print(f"\nFailures:")
            for name, error, trace in self.failures:
                print(f"\n{name}: {error}")


def test_city_initialization():
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


def test_city_bounds_validation():
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


def test_zone_initialization():
    """Test zone initializes with correct properties."""
    zone = Zone(10, 15, 'residential')
    
    assert zone.x == 10
    assert zone.y == 15
    assert zone.zone_type == 'residential'
    assert zone.development_level == 0  # Starts at 0, not 1
    assert zone.last_growth_check == 0
    assert zone.desirability_score == 0.0  # Attribute is desirability_score, not desirability


def test_zone_type_characteristics():
    """Test different zone types have correct characteristics."""
    residential = Zone(0, 0, 'residential')
    commercial = Zone(0, 0, 'commercial')
    industrial = Zone(0, 0, 'industrial')
    
    # Test max development levels via properties dict
    assert residential.properties['max_development'] == 5
    assert commercial.properties['max_development'] == 4
    assert industrial.properties['max_development'] == 4


def test_building_initialization():
    """Test building initializes with correct properties."""
    building = Building(8, 12, 'school')
    
    assert building.x == 8
    assert building.y == 12
    assert building.building_type == 'school'
    assert building.construction_time == 0  # No age attribute, but construction_time exists
    assert building.condition == 100  # Building condition attribute
    assert building.efficiency == 1.0  # Building efficiency attribute


def test_simulation_initialization():
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


def test_time_advancement():
    """Test game time advances correctly."""
    city = City(5, 5)
    sim = Simulation(city)
    
    initial_day = sim.game_day
    
    # Advance time
    sim.advance_time()
    
    assert sim.game_day == initial_day + 1
    assert sim.total_days_simulated == 1


def test_city_zone_integration():
    """Integration test - zones work within city."""
    city = City(20, 20)
    
    # Place a residential zone
    success = city.place_zone(10, 10, 'residential')
    assert success
    
    cell = city.get_cell(10, 10)
    assert isinstance(cell, Zone)
    assert cell.zone_type == 'residential'
    assert cell.x == 10
    assert cell.y == 10


def test_money_management():
    """Test city money management with edge cases."""
    city = City(10, 10)
    initial_money = city.money
    
    # Test that infrastructure placement costs money
    success = city.place_infrastructure(5, 5, 'road')
    assert success
    assert city.money < initial_money  # Money should be deducted
    
    # Test that zones don't cost money
    current_money = city.money
    success = city.place_zone(6, 6, 'residential')
    assert success
    assert city.money == current_money  # No money deducted for zones
    
    # Test insufficient funds by trying to place expensive infrastructure
    city.money = 100  # Set very low money
    success = city.place_infrastructure(7, 7, 'power_plant')  # Expensive
    assert not success  # Should fail due to insufficient funds


def run_all_tests():
    """Run all tests using the simple test runner."""
    runner = SimpleTestRunner()
    
    # List of test functions to run
    tests = [
        (test_city_initialization, "City Initialization"),
        (test_city_bounds_validation, "City Bounds Validation"),
        (test_zone_initialization, "Zone Initialization"),
        (test_zone_type_characteristics, "Zone Type Characteristics"),
        (test_building_initialization, "Building Initialization"),
        (test_simulation_initialization, "Simulation Initialization"),
        (test_time_advancement, "Time Advancement"),
        (test_city_zone_integration, "City-Zone Integration"),
        (test_money_management, "Money Management"),
    ]
    
    print("Running City Simulation Tests")
    print("=" * 50)
    
    for test_func, test_name in tests:
        runner.run_test(test_func, test_name)
    
    runner.print_summary()
    return runner.tests_failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
