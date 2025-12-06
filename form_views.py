from typing import List, Union

from drafter import Button, Div, Page, PageContent, SelectBox, Span, TextArea, TextBox, route

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
def enter_taken_courses(state: State, major_selected: str) -> Page:
    """
    Page for entering taken courses
    """
    # Process previous form page data
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
    course_strings = taken_courses.split(",")
    for course_code in course_strings:
        if len(course_code) != 7:
            return enter_taken_courses(state.major)
    state.student.has_taken = course_strings
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
def enter_desired_course_tags(state: State, difficulty_load: int) -> Page:
    """
    Page for entering desired course type
    """
    # Update state from last form
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
