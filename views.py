from typing import List, Set, Tuple, Union

from drafter import Argument, Button, Div, Page, PageContent, SelectBox, Span, TextArea, TextBox, route

from courses import Course, CourseListing, Student
from listings import AVAILABLE_MAJORS, UNIVERSITY_CATALOG
from state import State


def make_form_step(internal_content: List[Union[PageContent, str]], proceed_url: str) -> List[Union[PageContent, str]]:
    """Creates page content representing a step in the form.

    Args:
        internal_content (List[Union[PageContent, str]]): The form fields to render
        proceed_url (str): The URL to continue to after submitting the form step

    Returns:
        List[Union[PageContent, str]]: The overall page content
    """
    return [
        Div(
            content=[
                Div(content=["UD StudyPath"], classes="form-step-top-bar"),
                Div(
                    content=[
                        Div(
                            content=[
                                *internal_content,
                                Button("Continue", proceed_url, classes="form-step-continue", id="form-next-button"),
                            ],
                            classes="page-center-box",
                        )
                    ],
                    classes="page-center-box-container",
                ),
            ],
            classes="page-container",
        )
    ]


@route
def select_major(state: State) -> Page:
    """
    Page for selecting a major
    """
    majors: List[str] = [name for name in AVAILABLE_MAJORS]
    return Page(
        state,
        make_form_step(
            [
                "Select your major:",
                SelectBox("major_selected", majors),
            ],
            "enter_taken_courses",
        ),
    )


@route
def enter_taken_courses(state: State, major_selected: str = "") -> Page:
    """
    Page for entering taken courses
    """
    # Process previous form page data
    if major_selected:
        state.student.curriculum = AVAILABLE_MAJORS[major_selected]
        state.major = major_selected
    return Page(
        state,
        make_form_step(
            [
                Span("<h3>Enter the Courses you have already taken:</h3>"),
                Span(
                    'For example, you might write "CISC108,BISC217,MATH243" if you have taken CISC 108, BISC 217, and MATH 243.'
                ),
                Span(
                    "Note that all course codes must be exactly 7 characters long (4 for the department, 3 for the ID)."
                ),
                Span("Any invalid input will send you back to this screen."),
                TextArea("taken_courses", "", width="500"),
            ],
            "enter_desired_timeslots",
        ),
    )


@route
def enter_desired_timeslots(state: State, taken_courses: str) -> Page:
    """
    Page for entering desired timeslots
    """
    # Process the taken courses
    course_strings = [course_code.strip() for course_code in taken_courses.split(",")]
    if course_strings[0] != "":
        for course_code in course_strings:
            if len(course_code) != 7:
                return enter_taken_courses(state)
        state.student.has_taken = course_strings
    else:
        state.student.has_taken = []
    # Return the new form page
    return Page(
        state,
        make_form_step(
            [
                Span("<h3>When are you comfortable taking classes?</h3>"),
                Span("Enter the number of periods from the start of the day:"),
                TextBox("starting_timeslot", "0", kind="number", min="0", max="4"),
                Span("Enter the number of periods before the end of the day:"),
                TextBox("ending_timeslot", "0", kind="number", min="0", max="4"),
            ],
            "enter_desired_credit_load",
        ),
    )


@route
def enter_desired_credit_load(state: State, starting_timeslot: int, ending_timeslot: int) -> Page:
    """
    Page for entering desired credit load
    """
    # Update state from last form
    state.student.distance_from_first_slot = starting_timeslot
    state.student.distance_from_last_slot = ending_timeslot
    # Return new form
    return Page(
        state,
        make_form_step(
            [
                Span("<h3>Enter how many credit hours (0-18) you want for the semester:</h3>"),
                TextBox("credit_load", "16", kind="number", min="12", max="23"),
            ],
            "enter_desired_difficulty_load",
        ),
    )


@route
def enter_desired_difficulty_load(state: State, credit_load: int) -> Page:
    """
    Page for entering desired difficulty load
    """
    # Update state from last form
    state.student.maximum_credit_load = credit_load
    # Return new form
    return Page(
        state,
        make_form_step(
            [
                Span(
                    "<h3>Enter the maximum total difficulty load (averages around 3-4 points per class) for your semester.</h3>"
                ),
                TextBox("difficulty_load", "25", kind="number", min="20", max="40"),
            ],
            "enter_desired_course_tags",
        ),
    )


@route
def enter_desired_course_tags(state: State, difficulty_load: int = -1) -> Page:
    """
    Page for entering desired course type
    """
    # Update state from last form
    if difficulty_load > 0:
        state.student.maximum_difficulty_load = difficulty_load
    return Page(
        state,
        make_form_step(
            [
                Span("<h3>What course tags would you like to take?</h3>"),
                Span("Enter comma-separated course tags."),
                Span(f"Available course tags: {', '.join(UNIVERSITY_CATALOG.get_all_tags())}"),
                TextArea("course_tags", "", width="500"),
            ],
            "process_schedules",
        ),
    )


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


def build_schedules(student: Student, n_schedules: int = 25) -> List[List[Tuple[str, int]]]:
    """Builds possible schedules for a student based on their preferences.

    Generates a maximum of n_schedules schedules recursively.

    Only generates "complete" schedules; i.e., schedules where the algorithm reached a situation where it couldn't add any more courses

    Args:
        student (Student): The student whose preferences to consider
        n_schedules (int, optional): The maximum number of schedules to generate. Defaults to 10.

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
def process_schedules(state: State, course_tags: str) -> Page:
    """Builds the schedules for the user and adds them to state

    Args:
        state (State): The application state
        course_tags (str): The tags the user has selected

    Returns:
        Page: The schedule browsing page, after the user has already built their schedule
    """
    # Process the taken courses
    tag_strings = course_tags.split(",")
    if tag_strings[0] != "":
        for tag in tag_strings:
            if tag not in UNIVERSITY_CATALOG.get_all_tags():
                return enter_desired_course_tags(state)
        state.student.interest_tags = tag_strings
    else:
        state.student.interest_tags = []
    # Build schedule options
    state.schedule_options = build_schedules(state.student)
    # Redirect to the schedule browsing page
    return browse_schedule(state)


def generate_period_block(course_code: str = "Unoccupied", classes: str = "blank-period") -> Div:
    """Generates a period display block for a period

    Args:
        course_code (str): The course code being taken at that time (empty if empty)
        classes (str): The classes of the block

    Returns:
        Div: The block Div
    """
    return Div(content=[Span(course_code)], classes=f"period-block {classes}")


@route
def browse_schedule(state: State, index: int = 0) -> Page:
    """Browses the schedule in state at the given index

    Args:
        state (State): The application state
        index (int, optional): The index of the schedule to view. Defaults to 0.

    Returns:
        Page: The page data
    """
    if not state.schedule_options:
        return Page(
            state,
            [
                Div(
                    content=[
                        Div(
                            content=[
                                "<h3>Error</h3>",
                                "You don't have any schedules generated.",
                                Button("Go back to the start", "index"),
                            ],
                            classes="page-center-box",
                        )
                    ],
                    classes="page-container",
                )
            ],
        )
    if index >= len(state.schedule_options) or index < 0:
        index = 0
    schedule = state.schedule_options[index]
    # Build the MWF schedule
    mwf_content: List[Union[PageContent, str]] = []
    # For each of the 12 time slots
    for time_slot in range(0, 12):
        has_course = False
        for course in schedule:
            if course[1] == time_slot:
                mwf_content.append(generate_period_block(course[0], "period-block-mwf"))
                has_course = True
                break
        if not has_course:
            mwf_content.append(generate_period_block(classes="period-block-mwf"))
    # Build the TR schedule
    tr_content: List[Union[PageContent, str]] = []
    # For each of the 10 time slots
    for time_slot in range(12, 22):
        has_course = False
        for course in schedule:
            if course[1] == time_slot:
                tr_content.append(generate_period_block(course[0], "period-block-tr"))
                has_course = True
                break
        if not has_course:
            tr_content.append(generate_period_block(classes="period-block-tr"))
    return Page(
        state,
        [
            Div(
                content=[
                    Div(content=["UD StudyPath"], classes="form-step-top-bar"),
                    Div(
                        content=[
                            Span(f"<h1>Schedule #{index + 1}</h1>"),
                            Div(
                                content=[
                                    Div(
                                        content=[
                                            generate_period_block(course_code="8:00 AM", classes="period-block-time"),
                                            generate_period_block(course_code="9:00 AM", classes="period-block-time"),
                                            generate_period_block(course_code="10:00 AM", classes="period-block-time"),
                                            generate_period_block(course_code="11:00 AM", classes="period-block-time"),
                                            generate_period_block(course_code="12:00 PM", classes="period-block-time"),
                                            generate_period_block(course_code="1:00 PM", classes="period-block-time"),
                                            generate_period_block(course_code="2:00 PM", classes="period-block-time"),
                                            generate_period_block(course_code="3:00 PM", classes="period-block-time"),
                                            generate_period_block(course_code="4:00 PM", classes="period-block-time"),
                                            generate_period_block(course_code="5:00 PM", classes="period-block-time"),
                                            generate_period_block(course_code="6:00 PM", classes="period-block-time"),
                                            generate_period_block(course_code="7:00 PM", classes="period-block-time"),
                                            generate_period_block(course_code="8:00 PM", classes="period-block-time"),
                                            generate_period_block(course_code="9:00 PM", classes="period-block-time"),
                                        ],
                                        classes="schedule-time-markers",
                                    ),
                                    Div(content=mwf_content),
                                    Div(content=tr_content),
                                    Div(content=mwf_content),
                                    Div(content=tr_content),
                                    Div(content=mwf_content),
                                ],
                                classes="schedule-container",
                            ),
                            Div(
                                content=[
                                    Button(
                                        "Previous",
                                        "browse_schedule",
                                        Argument("index", index - 1),
                                        id="previous-button",
                                    ),
                                    Button("Next", "browse_schedule", Argument("index", index + 1)),
                                ],
                                classes="schedule-switching-controls",
                            ),
                        ],
                        classes="center-box",
                    ),
                ],
                classes="page-container",
            )
        ],
    )


@route
def index(state: State):
    return Page(
        state,
        [
            Div(
                content=[
                    Div(content=["UD StudyPath"], classes="form-step-top-bar"),
                    Div(
                        content=[
                            Div(
                                content=[
                                    Span("<h1>Plan your semester</h1>"),
                                    Button(
                                        "I'm ready", "select_major", classes="form-step-continue", id="form-next-button"
                                    ),
                                ],
                                classes="page-center-box",
                            )
                        ],
                        classes="page-center-box-container",
                    ),
                ],
                classes="page-container",
            )
        ],
    )
