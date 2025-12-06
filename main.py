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
    "author",
    """
Your description can go here.
""",
    [],
    [],
    [],
)


start_server(State(BLANK_STUDENT, [], ""))
