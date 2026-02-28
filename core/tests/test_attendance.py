import pytest
from core.models import Employee, Attendance
from django.db.utils import IntegrityError
from datetime import date
from rest_framework.test import APIClient
from rest_framework import status

pytestmark = pytest.mark.django_db

@pytest.fixture
def employee():
    return Employee.objects.create(
        employee_id="EMP100",
        full_name="Bob Test",
        email="bob@example.com",
        department="HR"
    )

@pytest.fixture
def api_client():
    return APIClient()

def test_create_attendance_success(employee):
    att = Attendance.objects.create(
        employee=employee,
        date=date(2023, 10, 1),
        status="Present"
    )
    assert att.employee == employee
    assert att.status == "Present"

def test_attendance_unique_per_day(employee):
    Attendance.objects.create(
        employee=employee,
        date=date(2023, 10, 1),
        status="Present"
    )
    with pytest.raises(IntegrityError):
        Attendance.objects.create(
            employee=employee,
            date=date(2023, 10, 1),
            status="Absent"
        )

def test_api_mark_attendance(api_client, employee):
    payload = {
        "employee_id": employee.employee_id,
        "date": "2023-10-02",
        "status": "Absent"
    }
    response = api_client.post("/api/attendance/", payload, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Attendance.objects.count() == 1

def test_api_list_attendance(api_client, employee):
    Attendance.objects.create(
        employee=employee,
        date=date(2023, 10, 3),
        status="Present"
    )
    response = api_client.get("/api/attendance/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1

def test_api_list_attendance_filter_by_date(api_client, employee):
    Attendance.objects.create(
        employee=employee,
        date=date(2023, 10, 4),
        status="Present"
    )
    Attendance.objects.create(
        employee=employee,
        date=date(2023, 10, 5),
        status="Absent"
    )
    response = api_client.get("/api/attendance/?date=2023-10-4")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['date'] == "2023-10-04"
