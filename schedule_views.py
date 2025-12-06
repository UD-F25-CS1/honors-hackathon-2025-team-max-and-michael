from typing import List, Set, Tuple

from drafter import Page, route

from courses import Course, CourseListing, Student
from listings import UNIVERSITY_CATALOG
from state import State


def build_course_pool(student: Student) -> CourseListing:
    """Builds the pool of relevant and constraint-meeting courses for a student.

    Args:
        student (Student): The student to check

    Returns:
        CourseListing: The relevant course pool, based on their selections
    """
    # Get the student's requirements for completing the major
    useful_courses = student.get_useful_courses()
    # Apply the course listing filters
    course_listing = UNIVERSITY_CATALOG.get_course_listing()
    course_listing = course_listing.filter_courses_by_codes(codes=useful_courses)
    course_listing = course_listing.filter_courses_by_prerequisites(student=student)
    course_listing = course_listing.filter_courses_by_bounding_times(student=student)
    # Extract the course pool
    return course_listing


def order_course_pool(course_pool: CourseListing, student: Student) -> CourseListing:
    """Orders the course pool, prioritizing first taking lower-level courses and then courses that meet the tags

    Args:
        course_pool (CourseListing): The unordered course pool
        student (Student): The student whose preferences to consider

    Returns:
        CourseListing: The ordered course pool
    """
    # Tuple: (Course object, course level, number of tags satisfied)
    with_sorting_data: List[Tuple[Course, int, int]] = []
    for course in course_pool.available_courses:
        with_sorting_data.append((course, course.get_course_level(), student.get_tags_satisfied(course)))
    # Used generative AI for syntax to sort by two parameters
    with_sorting_data.sort(key=lambda x: (x[1], x[2]))
    return CourseListing([sorting_data[0] for sorting_data in with_sorting_data])


def build_schedules(student: Student, n_schedules: int = 100) -> List[List[Tuple[str, int]]]:
    """Builds possible schedules for a student based on their preferences.

    Generates a maximum of n_schedules schedules recursively.

    Only generates "complete" schedules; i.e., schedules where the algorithm reached a situation where it couldn't add any more courses

    Args:
        student (Student): The student whose preferences to consider
        n_schedules (int, optional): The maximum number of schedules to generate. Defaults to 100.

    Returns:
        List[List[Tuple[str, int]]]: The list of schedules
    """
    # Get the course pool
    unordered_course_pool = build_course_pool(student)
    course_pool = order_course_pool(unordered_course_pool, student)
    pool_list = course_pool.available_courses

    # Generative AI used to assist with creating the rest of the algorithm
    # i.e., used in the construction of the rest of this function
    found_schedules: Set[Tuple[Tuple[str, int], ...]] = set()
    results: List[List[Tuple[str, int]]] = []

    # Pre-expand courses into individual (course_code, time_slot) offerings
    # e.g. CISC108 with time_slots [1,3,14] becomes:
    #   [("CISC108", 1), ("CISC108", 3), ("CISC108", 14)]
    offerings = []
    for course in pool_list:
        for slot in course.time_slots:
            offerings.append((course.code, slot))

    # Build indexes to avoid repeatedly scanning the catalog
    # Map code → all its times
    course_to_offerings = {}
    for code, slot in offerings:
        course_to_offerings.setdefault(code, []).append((code, slot))

    # Recursive schedule builder
    def backtrack(current_sched: List[Tuple[str, int]]):
        nonlocal results

        if len(results) >= n_schedules:
            return  # stop early

        # Track used time slots and used course codes
        used_slots = {slot for _, slot in current_sched}
        used_codes = {code for code, _ in current_sched}

        # Try to find something new to add
        added_any = False

        for course in pool_list:
            # Skip if code already used
            if course.code in used_codes:
                continue

            # Try each time slot for that course
            for slot in course.time_slots:
                if slot in used_slots:
                    continue  # time conflict

                # Valid addition → recurse
                added_any = True
                new_sched = current_sched + [(course.code, slot)]
                backtrack(new_sched)

                if len(results) >= n_schedules:
                    return

        # If we reached a point where nothing new can be added, store schedule
        if not added_any:
            # Sort schedule to ensure duplicate-free canonical form
            canonical = tuple(sorted(current_sched))

            if canonical not in found_schedules:
                found_schedules.add(canonical)
                results.append(list(canonical))

    # Start recursion with the empty schedule
    backtrack([])

    return results


@route
def process_schedules(state: State, tags_selected: List[str]) -> Page:
    """Builds the schedules for the user and adds them to state

    Args:
        state (State): The application state
        tags_selected (List[str]): The tags the user has selected

    Returns:
        Page: The schedule browsing page, after the user has already built their schedule
    """

    return Page(state, [])


@route
def browse_schedule(state: State):
    pass
