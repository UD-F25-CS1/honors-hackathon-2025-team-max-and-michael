from courses import Student
from listings import CHEMICAL_ENGINEERING_CURRICULUM, UNIVERSITY_CATALOG
from schedule_views import build_schedules

test_student = Student(CHEMICAL_ENGINEERING_CURRICULUM, ["breadth", "chemistry"], 35.0, 18, 0, 0, [])
print(build_schedules(test_student, 5))
print(len(UNIVERSITY_CATALOG.get_all_tags()))
