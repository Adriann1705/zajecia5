

import pytest
from src.manager import Manager
from src.models import Parameters
from src.models import Bill


def test_apartment_costs_with_optional_parameters():
    manager = Manager(Parameters())
    manager.bills.append(Bill(
        apartment='apart-polanka',
        date_due='2025-03-15',
        settlement_year=2025,
        settlement_month=2,
        amount_pln=1250.0,
        type='rent'
    ))

    manager.bills.append(Bill(
        apartment='apart-polanka',
        date_due='2024-03-15',
        settlement_year=2024,
        settlement_month=2,
        amount_pln=1150.0,
        type='rent'
    ))

    manager.bills.append(Bill(
        apartment='apart-polanka',
        date_due='2024-02-02',
        settlement_year=2024,
        settlement_month=1,
        amount_pln=222.0,
        type='electricity'
    ))

    costs = manager.get_apartment_costs('apartment-1', 2024, 1)
    assert costs is None

    costs = manager.get_apartment_costs('apart-polanka', 2024, 3)
    assert costs == 0.0

    costs = manager.get_apartment_costs('apart-polanka', 2024, 1)
    assert costs == 222.0

    costs = manager.get_apartment_costs('apart-polanka', 2025, 1)
    assert costs == 910.0
    
    costs = manager.get_apartment_costs('apart-polanka', 2024)
    assert costs == 1372.0

    costs = manager.get_apartment_costs('apart-polanka')
    assert costs == 3532.0
def test_apartment_costs():
    parameters = Parameters()
    manager = Manager(parameters)
    assert manager.get_apartment_costs('apart-polanka', 2025, 1) == 910
    assert manager.get_apartment_costs('apart', 2025, 1) == None
    assert manager.get_apartment_costs('apart-polanka', 2024, 1) == 0.0 
    assert manager.get_apartment_costs('apart-polanka', 2025, 2) == 0.0 
    assert manager.get_apartment_costs('apart-polanka', 2025, 15) == 0.0 

def test_apartment_settlement():
    parameters = Parameters()
    manager = Manager(parameters)
    settlement1 = manager.get_apartment_settlement('apart-polanka', 2025, 1)
    assert settlement1 is not None
    assert settlement1.month == 1
    assert settlement1.year == 2025
    assert settlement1.total_bills_pln == 910.0
    assert settlement1.total_rent_pln == 0.0
    assert settlement1.total_due_pln == -910.0
    settlement2 = manager.get_apartment_settlement('apart-polanka', 2025, 7)
    assert settlement2 is not None
    assert settlement2.month == 7
    assert settlement2.year == 2025
    assert settlement2.total_bills_pln == 0.0
    assert settlement2.total_rent_pln == 0.0
    assert settlement2.total_due_pln == 0.0

def test_tenant_settlement():
    manager = Manager(Parameters())
    apartment_settlement = manager.get_apartment_settlement('apart-polanka', 2025, 1)
    settlements_many = manager.get_tenant_settlement(apartment_settlement)
    assert isinstance(settlements_many, list)
    assert len(settlements_many) == 3
    expected_share_many = 910.0 / 3.0
    tenant_ids = [settlement.tenant for settlement in settlements_many]
    assert 'tenant-1' in tenant_ids
    assert 'tenant-2' in tenant_ids
    assert 'tenant-3' in tenant_ids
    for settlement in settlements_many:
        assert settlement.apartment_settlement == 'apart-polanka'
        assert settlement.year == 2025
        assert settlement.month == 1
        assert settlement.rent_pln == 0.0
        assert settlement.bills_pln == pytest.approx(expected_share_many)
        assert settlement.total_due_pln == pytest.approx(expected_share_many)
        assert settlement.balance_pln == pytest.approx(-expected_share_many)

    manager.tenants = {'tenant-1': manager.tenants['tenant-1']}
    settlement1 = manager.get_tenant_settlement(apartment_settlement)
    assert isinstance(settlement1, list)
    assert len(settlement1) == 1
    assert settlement1[0].tenant == 'tenant-1'
    assert settlement1[0].bills_pln == 910.0
    assert settlement1[0].total_due_pln == 910.0
    assert settlement1[0].balance_pln == -910.0

    manager.tenants = {}
    settlement2 = manager.get_tenant_settlement(apartment_settlement)
    assert isinstance(settlement2, list)
    assert len(settlement2) == 0