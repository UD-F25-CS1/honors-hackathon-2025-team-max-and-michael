from drafter import (  # , hide_debug_information, set_website_framed
    set_site_information,
    set_website_title,
    start_server,
)

import views  # noqa: F401
from courses import BLANK_STUDENT
from state import State

# hide_debug_information()
# set_website_framed(False)
set_website_title("UD StudyPath")
set_site_information(
    "author",
    """
Your description can go here.
""",
    [],
    [],
    [],
)


start_server(State(BLANK_STUDENT, []))
