import pytest 
from calculation import add , BankAccount, InsufficentFunds

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("num1, num2, expected",[
    (3,2,5),
    (7,1,8),
    (12,4,16)
])
def test_add(num1, num2, expected):
    print("testing add function")
    assert add(num1, num2) == expected


def test_bank_set_initial_account(bank_account):
    
    with pytest.raises(InsufficentFunds):
        bank_account.withdraw(2000)
    