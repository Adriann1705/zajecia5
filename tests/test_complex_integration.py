import pytest
from src.manager import Manager
from src.models import Parameters
from src.models import Bill


def test_apartment_costs():
    parameters = Parameters()
    manager = Manager(parameters)
    assert manager.get_apartment_costs('apart-polanka', 2025, 1) == 910
    assert manager.get_apartment_costs('apart', 2025, 1) == None
    assert manager.get_apartment_costs('apart-polanka', 2024, 1) == 0.0 
    assert manager.get_apartment_costs('apart-polanka', 2025, 2) == 0.0 