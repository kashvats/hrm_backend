from rest_framework import views, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Employee, Attendance
from hrms_backend.serializers import EmployeeSerializer, AttendanceSerializer

class EmployeeListCreateView(views.APIView):

    def get(self, request):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)
        
    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmployeeDetailView(views.APIView):

    def delete(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AttendanceListCreateView(views.APIView):

    def get(self, request):
        date = request.query_params.get('date')
        dept = request.query_params.get('department')
        if not date:
            return Response({"error": "Date parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        attendances = Attendance.objects.filter(date=date)
        if dept:
            attendances = attendances.filter(employee__department=dept)
            
        serializer = AttendanceSerializer(attendances, many=True)
        return Response(serializer.data)

    def post(self, request):
        from datetime import date
        today = date.today().isoformat()
        
        data = request.data
        if not isinstance(data, list):
            data = [data]
        
        results = []
        for item in data:
            emp_id = item.get('employee_id')
            date_val = item.get('date')
            status_val = item.get('status')
            
            if not all([emp_id, date_val, status_val]):
                continue
            
            # Restrict update to today only
            if date_val != today:
                return Response(
                    {"error": f"You can only mark attendance for today ({today}). Past or future updates are restricted."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            employee = get_object_or_404(Employee, employee_id=emp_id)
            attendance, created = Attendance.objects.update_or_create(
                employee=employee,
                date=date_val,
                defaults={'status': status_val}
            )
            results.append(AttendanceSerializer(attendance).data)
            
        return Response(results, status=status.HTTP_201_CREATED)

class DashboardView(views.APIView):

    def get(self, request):
        from datetime import date
        from django.utils import timezone
        
        today = date.today()
        dept = request.query_params.get('department')
        
        employees = Employee.objects.all()
        if dept:
            employees = employees.filter(department=dept)
            
        total_employees = employees.count()
        today_attendance = Attendance.objects.filter(date=today, employee__in=employees)
        
        present_today = today_attendance.filter(status='Present').count()
        absent_today = today_attendance.filter(status='Absent').count()
        
        # Pending means an employee exists but has no record for today
        pending_attendance = total_employees - (present_today + absent_today)
        
        attendance_percentage = 0
        if total_employees > 0:
            attendance_percentage = round((present_today / total_employees) * 100, 1)

        return Response({
            "date": today.isoformat(),
            "total_employees": total_employees,
            "present_today": present_today,
            "absent_today": absent_today,
            "pending_attendance": max(0, pending_attendance),
            "attendance_percentage": attendance_percentage,
            "last_updated": timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        })
