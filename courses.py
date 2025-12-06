from dataclasses import dataclass
from typing import List, Optional, Set


@dataclass
class TakenRequirement:
    course_codes: List[str]
    minimum_count: int


@dataclass
class Course:
    # Must be 7-character (e.g. CISC108)
    code: str
    title: str
    credits: int
    # Time slots are tuples with integers numbered for 70 minute blocks (55 min class, 15 minute break) from 8am to 10pm
    # There are 12 time slots on MWF and 10 on TR, so we will use 22 total slots. 0 through 11 are MWF, 12 through 21 are TR
    time_slots: List[int]
    tags: List[str]
    prerequisites: List[TakenRequirement]
    # Difficulty is rated on a scale of 1.0 to 5.0, as in RateMyProfessor.
    # Values pulled from RMP averages over all profs teaching course
    difficulty: float

    def get_course_number(self) -> int:
        """Extracts the course number from the course code

        Returns:
            int: The course number
        """
        return int(self.code[4:])

    def get_course_level(self) -> int:
        """Extracts the course level (100, 200, etc) from the course code

        Returns:
            int: The course level
        """
        return (self.get_course_number() // 100) * 100


@dataclass
class Curriculum:
    requirements: List[TakenRequirement]


@dataclass
class Student:
    curriculum: Curriculum
    interest_tags: List[str]
    maximum_difficulty_load: float
    maximum_credit_load: int
    # The number of time slots away from the first (0) time slot or the last (21) time slot a course must be to be eligible
    # For example, a value of 1 for distance_from_first_slot means that courses could start at slot 1 (MWF) or 13 (TR)
    # A value of 3 for distance_from_last_slot means that courses could end at slot 8 (MWF) or 18 (TR)
    distance_from_first_slot: int
    distance_from_last_slot: int
    # Course codes
    has_taken: List[str]

    def meets_requirement(self, requirement: TakenRequirement) -> bool:
        """Checks whether a student meets a course requirement

        Args:
            requirement (TakenRequirement): The requirement to check the student against

        Returns:
            bool: Whether the student meets the requirement
        """
        count: int = 0
        for course_code in requirement.course_codes:
            if course_code in self.has_taken:
                count += 1
        return count >= requirement.minimum_count

    def can_take(self, course: Course) -> bool:
        """Checks whether a student is eligible to take a given course, based on its prerequisites

        Args:
            course (Course): The course to consider

        Returns:
            bool: Whether the student is allowed to take the course
        """
        for prerequisite in course.prerequisites:
            if not self.meets_requirement(prerequisite):
                return False
        return True

    def get_remaining_requirements(self) -> List[TakenRequirement]:
        """Returns a list of the requirements the student must meet to earn their degree

        Returns:
            List[TakenRequirement]: The list of requirements
        """
        remaining: List[TakenRequirement] = []
        for requirement in self.curriculum.requirements:
            if not self.meets_requirement(requirement):
                remaining.append(requirement)
        return remaining

    def get_useful_courses(self) -> Set[str]:
        """Gets a list of useful courses for the student to take.

        A useful course is a course that helps fulfill a requirement that the student still needs.

        Returns:
            Set[str]: The course codes for the useful courses
        """
        result: Set[str] = set()
        for requirement in self.get_remaining_requirements():
            for course in requirement.course_codes:
                result.add(course)
        return result

    def get_tags_satisfied(self, course: Course) -> int:
        """Gets the number of desired tags that a course satisfies

        Args:
            course (Course): The course to consider

        Returns:
            int: The number of user-selected tags a course satisfies
        """
        count: int = 0
        for tag in self.interest_tags:
            if tag in course.tags:
                count += 1
        return count


@dataclass
class CourseListing:
    available_courses: List[Course]

    def filter_courses_by_codes(self, codes: Set[str]) -> "CourseListing":
        """Returns only those courses that are in the provided list of course codes

        That is to say, intersects the set of "codes" with the "available_courses"

        Args:
            codes (Set[str]): The course codes to include

        Returns:
            CourseListing: The courses available in the codes list
        """
        result: List[Course] = []
        for course in self.available_courses:
            if course.code in codes:
                result.append(course)
        return CourseListing(result)

    def filter_courses_by_time(self, time_slot: int) -> "CourseListing":
        """Returns all of the courses with a course at that time

        Args:
            time_slot (int): The time slot, numbered from 0 to 21 (inclusive)

        Returns:
            CourseListing: The courses available at that time slot
        """
        result: List[Course] = []
        for course in self.available_courses:
            if time_slot in course.time_slots:
                result.append(course)
        return CourseListing(result)

    def filter_courses_by_time_slots(self, time_slots: List[int]) -> "CourseListing":
        """Returns the courses that do NOT take place in ANY of the time slots specified

        Args:
            time_slots (List[int]): The already taken time slots

        Returns:
            CourseListing: The courses that do not conflict
        """
        result: List[Course] = []
        for course in self.available_courses:
            for time_slot in course.time_slots:
                if time_slot not in time_slots:
                    result.append(course)
                    break
        return CourseListing(result)

    def filter_courses_by_difficulty(self, maximum_difficulty: float) -> "CourseListing":
        """Returns the courses below a certain difficulty value

        Args:
            maximum_difficulty (float): The maximum difficulty value (inclusive) that you wish to include

        Returns:
            CourseListing: The courses meeting the difficulty constraint
        """
        result: List[Course] = []
        for course in self.available_courses:
            if course.difficulty <= maximum_difficulty:
                result.append(course)
        return CourseListing(result)

    def filter_courses_by_credits(self, maximum_credits: int) -> "CourseListing":
        """Returns the courses below a certain credit value

        Args:
            maximum_credits (int): The maximum number of credits (inclusive) that you wish to include

        Returns:
            CourseListing: The courses meeting the credit constraint
        """
        result: List[Course] = []
        for course in self.available_courses:
            if course.credits <= maximum_credits:
                result.append(course)
        return CourseListing(result)

    def filter_courses_by_tags(self, desired_tags: List[str]) -> "CourseListing":
        """Returns the courses containing at least one of the desired tags

        Args:
            desired_tags (List[str]): The tags to filter by

        Returns:
            CourseListing: The courses meeting the tag constraint
        """
        result: List[Course] = []
        for course in self.available_courses:
            for tag in desired_tags:
                if tag in course.tags:
                    result.append(course)
        return CourseListing(result)

    def filter_courses_by_prerequisites(self, student: Student) -> "CourseListing":
        """Returns the courses a student meets the prerequisites for

        Args:
            student (Student): The Student to consider

        Returns:
            CourseListing: The courses that meet the prerequisite constraint
        """
        result: List[Course] = []
        for course in self.available_courses:
            if student.can_take(course):
                result.append(course)
        return CourseListing(result)

    def filter_courses_by_bounding_times(self, student: Student) -> "CourseListing":
        """Filters courses by the start and end of day bounds provided by the student.

        Args:
            student (Student): The student whose distances to consider

        Returns:
            CourseListing: The çourses that are within the allowed times
        """
        result: List[Course] = []
        for course in self.available_courses:
            for time_slot in course.time_slots:
                # If MWF time slot
                if time_slot < 12:
                    if (
                        time_slot >= student.distance_from_first_slot
                        and time_slot < 12 - student.distance_from_last_slot
                    ):
                        result.append(course)
                        break
                # TR time slot
                else:
                    if (
                        time_slot - 12
                    ) >= student.distance_from_first_slot and time_slot < 22 - student.distance_from_last_slot:
                        result.append(course)
                        break
        return CourseListing(result)


@dataclass
class Catalog:
    courses_offered: List[Course]

    def get_course_by_code(self, code: str) -> Optional[Course]:
        """Get a specific course by its code

        Args:
            code (str): The course of the code

        Returns:
            Optional[Course]: The Course object, or None if it couldn't be found
        """
        for course in self.courses_offered:
            if course.code == code:
                return course
        return None

    def get_all_tags(self) -> List[str]:
        """Returns all the available tags from offered courses

        Returns:
            List[str]: The tags in the catalog
        """
        result: Set[str] = set()
        for course in self.courses_offered:
            for tag in course.tags:
                result.add(tag)
        return list(result)

    def get_all_course_codes(self, is_sorted: bool = True) -> List[str]:
        """Returns all of the course codes in the catalog

        Args:
            is_sorted (bool, optional): Whether to sort alphabetically. Defaults to True.

        Returns:
            List[str]: The (potentially sorted) course codes
        """
        course_codes = [course.code for course in self.courses_offered]
        if is_sorted:
            course_codes.sort()
        return course_codes

    def get_course_listing(self) -> CourseListing:
        """Gets a course listing from the Catalog

        Returns:
            CourseListing: A CourseListing containing all courses offered in the catalog
        """
        return CourseListing([course for course in self.courses_offered])


BLANK_CURRICULUM = Curriculum([])
BLANK_STUDENT = Student(
    BLANK_CURRICULUM,
    interest_tags=[],
    maximum_difficulty_load=5.0,
    maximum_credit_load=18,
    distance_from_first_slot=0,
    distance_from_last_slot=0,
    has_taken=[],
)
