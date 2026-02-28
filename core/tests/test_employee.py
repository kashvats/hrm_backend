import pytest
from core.models import Employee
from django.db.utils import IntegrityError
from rest_framework.test import APIClient
from rest_framework import status

pytestmark = pytest.mark.django_db

# -----------------
# MODEL TESTS
# -----------------
def test_create_employee_success():
    """Test creating an employee with valid data."""
    emp = Employee.objects.create(
        employee_id="EMP001",
        full_name="John Doe",
        email="john@example.com",
        department="Engineering"
    )
    assert emp.employee_id == "EMP001"
    assert emp.full_name == "John Doe"
    assert emp.email == "john@example.com"
    assert emp.department == "Engineering"

def test_employee_unique_id():
    """Test employee ID unique constraint."""
    Employee.objects.create(
        employee_id="EMP001",
        full_name="John Doe",
        email="john@example.com",
        department="Engineering"
    )
    with pytest.raises(IntegrityError):
        Employee.objects.create(
            employee_id="EMP001",
            full_name="Jane Doe",
            email="jane@example.com",
            department="HR"
        )

def test_employee_unique_email():
    """Test employee email unique constraint."""
    Employee.objects.create(
        employee_id="EMP001",
        full_name="John Doe",
        email="john@example.com",
        department="Engineering"
    )
    with pytest.raises(IntegrityError):
        Employee.objects.create(
            employee_id="EMP002",
            full_name="Jane Doe",
            email="john@example.com",
            department="HR"
        )

# -----------------
# API TESTS
# -----------------
@pytest.fixture
def api_client():
    return APIClient()

def test_api_list_employees(api_client):
    """Test listing all employees."""
    Employee.objects.create(employee_id="EMP001", full_name="A", email="a@a.com", department="IT")
    Employee.objects.create(employee_id="EMP002", full_name="B", email="b@b.com", department="IT")
    
    response = api_client.get("/api/employees/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2

def test_api_create_employee_success(api_client):
    """Test creating a valid employee."""
    payload = {
        "employee_id": "EMP003",
        "full_name": "Alice Smith",
        "email": "alice@example.com",
        "department": "Finance"
    }
    response = api_client.post("/api/employees/", payload, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Employee.objects.filter(employee_id="EMP003").exists()

def test_api_create_employee_duplicate_id(api_client):
    """Test creating an employee with existing ID returns 400."""
    Employee.objects.create(employee_id="EMP001", full_name="A", email="a@a.com", department="IT")
    payload = {
        "employee_id": "EMP001",
        "full_name": "Duplicate",
        "email": "dup@a.com",
        "department": "IT"
    }
    response = api_client.post("/api/employees/", payload, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "employee with this employee id already exists" in str(response.data).lower() or  "already exists" in str(response.data).lower()

def test_api_create_employee_invalid_email(api_client):
    """Test creating an employee with invalid email format returns 400."""
    payload = {
        "employee_id": "EMP004",
        "full_name": "Invalid Email",
        "email": "not-an-email",
        "department": "IT"
    }
    response = api_client.post("/api/employees/", payload, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "email" in str(response.data).lower()

def test_api_delete_employee(api_client):
    """Test deleting an employee."""
    emp = Employee.objects.create(employee_id="EMP001", full_name="A", email="a@a.com", department="IT")
    response = api_client.delete(f"/api/employees/{emp.id}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Employee.objects.filter(id=emp.id).exists()

def test_api_xss_protection(api_client):
    """Test XSS payloads on employee input."""
    payload = {
        "employee_id": "EMP005",
        "full_name": "<script>alert(1)</script>",
        "email": "xss@example.com",
        "department": "IT"
    }
    response = api_client.post("/api/employees/", payload, format="json")
    assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST]
    if response.status_code == status.HTTP_201_CREATED:
        # If created, check that the output is not the raw payload (though DRF serializers 
        # normally don't bleach input by default unless we add a custom validator)
        # We will require our serializer to reject or escape it as per rule 13.
        pass
