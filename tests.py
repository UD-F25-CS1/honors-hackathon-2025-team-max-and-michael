# Used generative AI to assist with unit tests

from bakery import assert_equal

from courses import Catalog, Course, Curriculum, Student, TakenRequirement
from views import build_course_pool, build_schedules, order_course_pool


def sample_catalog():
    c1 = Course(
        code="CISC108",
        title="Intro Programming",
        credits=3,
        time_slots=[0, 3],
        tags=["coding"],
        prerequisites=[],
        difficulty=2.0,
    )
    c2 = Course(
        code="CISC181",
        title="Intro CS II",
        credits=3,
        time_slots=[1, 4],
        tags=["coding"],
        prerequisites=[TakenRequirement(["CISC108"], 1)],
        difficulty=3.0,
    )
    c3 = Course(
        code="MATH241",
        title="Calculus I",
        credits=4,
        time_slots=[12],
        tags=["math"],
        prerequisites=[],
        difficulty=3.5,
    )
    return Catalog([c1, c2, c3])


def sample_student():
    curriculum = Curriculum([TakenRequirement(["CISC108", "CISC181"], 2)])
    return Student(
        curriculum=curriculum,
        interest_tags=["coding"],
        maximum_difficulty_load=5.0,
        maximum_credit_load=18,
        distance_from_first_slot=0,
        distance_from_last_slot=0,
        has_taken=["CISC108"],
    )


req = TakenRequirement(["CISC108", "MATH241"], 1)
student = sample_student()
assert_equal(True, student.meets_requirement(req))


catalog = sample_catalog()
c1 = catalog.get_course_by_code("CISC108")
c2 = catalog.get_course_by_code("CISC181")
if c1 and c2:
    assert_equal(True, student.can_take(c1))
    assert_equal(True, student.can_take(c2))


useful = student.get_useful_courses()
assert_equal(["CISC108", "CISC181"], useful)

course = catalog.get_course_by_code("CISC108")
if course:
    assert_equal(108, course.get_course_number())
    assert_equal(100, course.get_course_level())

listing = catalog.get_course_listing()


filtered = listing.filter_courses_by_codes(["CISC108"])
assert_equal(["CISC108"], [c.code for c in filtered.available_courses])


filtered2 = listing.filter_courses_by_prerequisites(student)
assert_equal(set([c.code for c in filtered2.available_courses]), {"CISC108", "CISC181", "MATH241"})


filtered3 = listing.filter_courses_by_time(12)
assert_equal(["MATH241"], [c.code for c in filtered3.available_courses])


pool = build_course_pool(student)


ordered = order_course_pool(pool, student)
assert_equal([], [c.code for c in ordered.available_courses])


schedules = build_schedules(student, n_schedules=10)
possible = [{("CISC181", 1)}, {("CISC181", 4)}]
assert_equal(False, any(set(s) in possible for s in schedules))
