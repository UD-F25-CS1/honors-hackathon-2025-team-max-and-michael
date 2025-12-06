from typing import List, Union

from drafter import Button, Div, PageContent


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
