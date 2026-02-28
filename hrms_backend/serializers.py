from rest_framework import serializers
from core.models import Employee, Attendance
import html
import re



class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'employee_id', 'full_name', 'email', 'department', 'date_of_joining']

    def validate_full_name(self, value):
        # Basic XSS protection pattern
        if re.search(r'<[^>]+>', value):
            raise serializers.ValidationError("HTML tags are not allowed.")
        return html.escape(value)

class AttendanceSerializer(serializers.ModelSerializer):
    employee_id = serializers.CharField(source='employee.employee_id')
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)

    class Meta:
        model = Attendance
        fields = ['id', 'employee_id', 'employee_name', 'date', 'status']

    def create(self, validated_data):
        employee_data = validated_data.pop('employee')
        employee = Employee.objects.get(employee_id=employee_data['employee_id'])
        attendance = Attendance.objects.create(employee=employee, **validated_data)
        return attendance

