from drafter import (  # , hide_debug_information, set_website_framed
    add_website_css,
    hide_debug_information,
    set_site_information,
    set_website_framed,
    set_website_style,
    set_website_title,
    start_server,
)

import views  # noqa: F401
from courses import BLANK_STUDENT
from state import State
from styles import SITE_STYLES

hide_debug_information()
set_website_framed(False)
add_website_css(SITE_STYLES)
set_website_title("UD StudyPath")
set_website_style("none")
set_site_information(
    author="Max Polonlsky and Michael Rothkopf",
    description="""UD StudyPath solves the limitations of Blue Hen Planner, WebReg, and Stellic by considering all aspects of course selection at once.

    It takes into account the courses you should be taking to graduate on time, prerequisites, scheduling, and your personal preferences, allowing you to fully customize all aspects of your academic career at once.

    Begin your UD StudyPath and UD study paths today!
""",
    sources=["Used generative AI for some code generation", "https://gemini.google.com"],
    planning=["https://docs.google.com/presentation/d/18-BhAJuDB6_1G6gx9oXqxJJQq_YlVO1RFA_q8HSKy40/edit?usp=sharing"],
    links=["https://github.com/UD-F25-CS1/honors-hackathon-2025-team-max-and-michael"],
)


start_server(State(BLANK_STUDENT, [], ""))
