import pytest
from core.models import Employee, Attendance
from datetime import date
from rest_framework.test import APIClient
from rest_framework import status

pytestmark = pytest.mark.django_db

@pytest.fixture
def api_client():
    return APIClient()

def test_dashboard_stats(api_client):
    e1 = Employee.objects.create(employee_id="E1", full_name="A", email="a@a.com", department="IT")
    e2 = Employee.objects.create(employee_id="E2", full_name="B", email="b@b.com", department="HR")
    Attendance.objects.create(employee=e1, date=date(2023, 1, 1), status="Present")
    Attendance.objects.create(employee=e2, date=date(2023, 1, 1), status="Absent")

    response = api_client.get("/api/dashboard/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["total_employees"] == 2
    assert response.data["total_present"] == 1
    assert response.data["total_absent"] == 1
