from typing import List, Union

from drafter import Button, Div, Page, PageContent, SelectBox, route

from listings import AVAILABLE_MAJORS
from state import State
from courses import get_all_tags


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
            [
                Div(["UD StudyPath"], classes="form-step-top-bar"),
                Div(
                    [*internal_content, Button("Continue", proceed_url, classes="form-step-continue")],
                    classes="form-step-center-box",
                ),
            ],
            classes="form-step-container",
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
                SelectBox("major", majors),
            ],
            "/form/enter-taken-courses",
        ),
    )

def add_course(state: State, major: str, taken_course: str) -> None:
    """
    Adds a taken course to the student's curriculum
    """

    if taken_course in state.student.curriculum.available_courses:
        state.student.curriculum.taken_courses.append(taken_course)
    return enter_taken_courses(state, state.student.curriculum.name)

@route
def enter_taken_courses(state: State, major_selected: str ='') -> Page:
    """
    Page for entering taken courses
    """
    if major_selected:
        state.student.curriculum = AVAILABLE_MAJORS[major_selected]


    return Page(
        state,
        make_form_step(
            [
                "Enter the Courses you have already taken:",
                TextBox("taken_course", ''), Button("Add Course", "add_course"),
                Text("Courses Taken: " + ", ".join(state.student.curriculum.taken_courses)),
                Button("Confirm Taken Courses", "/form/enter-desired-timeslots"),

            ],
            "/form/enter-desired-timeslots",
        ),
    )

def confirm_timeslots(state: State, start_timeslot: str, end_timeslot: str) -> None:
    """
    Confirms the desired timeslots for the student
    """
    state.student.distance_from_first_slot = int(start_timeslot)
    state.student.distance_from_last_slot = int(end_timeslot)
    return enter_desired_credit_load(state)

@route
def enter_desired_timeslots(state: State) -> Page:
    """
    Page for entering desired timeslots
    """
    return Page(
        state,
        make_form_step(
            [
                "When are you comfortable taking classes?",
                TextBox("starting_timeslot", ''),
                "Enter the number of periods from the start of the day:",
                TextBox("ending_timeslot", ''),
                "Enter the number of periods before the end of the day:",
                Button("Confirm Timeslots", "confirm_timeslots"),
                
            ],
            "/form/desired-credit-load",
        ),
    )

def confirm_credit_load(state: State, credit_load: str) -> None:
    """
    Confirms the desired credit load for the student
    """
    state.student.desired_credit_load = int(credit_load)
    return enter_desired_course_type(state)

@route
def enter_desired_credit_load(state: State) -> Page:
    """
    Page for entering desired credit load
    """
    return Page(
        state,
        make_form_step(
            [
                "Enter how many credit hours (0-18) you want for the semester:",
                TextBox("credit_load", ''),
                Button("Confirm Credit Load", "confirm_credit_load"),
            ],
            "/form/desired-course-type",
        ),
    )

def add_course_type(state: State, course_type: str) -> None:
    """
    Adds a desired course type to the student's preferences
    """
    if course_type not in state.student.interest_tags:
        state.student.interest_tags.append(course_type)
    return enter_desired_course_type(state)

def confirm_course_types(state: State) -> None:
    """
    Confirms the desired course types for the student
    """
    return 

@route
def enter_desired_course_type(state: State) -> Page:
    """
    Page for entering desired course type
    """
    tags = get_all_tags(state)
    
    return Page(
        state,
        make_form_step(
            [
                "What type of courses do you want to take?",
                SelectBox("course_type", tags, multiple=True),
                Button("Add Course Type", "add_course_type"),
                Button("Confirm Course Types", "confirm_course_types"),

            ],
            "/form/view-schedules,
        ),
    )

@route
def view_schedules(state: State) -> Page:
    """
    Page for viewing generated schedules
    """
    # Placeholder content for generated schedules
    return Page(
        state,
        [
            Div(["Generated Schedules will be displayed here."], classes="schedule-viewer"),
        ],
    )
