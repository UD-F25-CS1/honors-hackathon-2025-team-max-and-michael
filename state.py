from dataclasses import dataclass
from typing import List, Tuple

from courses import Student


@dataclass
class State:
    student: Student
    schedule_options: List[List[Tuple[str, int]]]
