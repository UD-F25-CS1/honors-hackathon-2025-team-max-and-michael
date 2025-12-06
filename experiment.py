from courses import Student
from listings import CHEMICAL_ENGINEERING_CURRICULUM
from schedule_views import build_schedules

test_student = Student(CHEMICAL_ENGINEERING_CURRICULUM, ["breadth", "chemistry"], 35.0, 18, 0, 0, [])
print(build_schedules(test_student, 5))
