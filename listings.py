from typing import Dict

from courses import Catalog, Course, Curriculum, TakenRequirement

# Used generative AI to generate list of requirements
# Does not have to be entirely accurate for prototype
CHEMICAL_ENGINEERING_CURRICULUM = Curriculum(
    requirements=[
        # Core CHEG courses — represent as “must take at least 1 of each” groups
        TakenRequirement(course_codes=["CHEG112"], minimum_count=1),
        TakenRequirement(course_codes=["CHEG231"], minimum_count=1),
        TakenRequirement(course_codes=["CHEG332"], minimum_count=1),
        TakenRequirement(course_codes=["CHEG341"], minimum_count=1),
        TakenRequirement(course_codes=["CHEG342"], minimum_count=1),
        TakenRequirement(course_codes=["CHEG345"], minimum_count=1),
        # Senior-level design / lab (choose at least 1 of two alternatives)
        TakenRequirement(course_codes=["CHEG432", "CHEG431"], minimum_count=1),
        # Chemistry foundation
        TakenRequirement(course_codes=["CHEM111", "CHEM103"], minimum_count=1),
        TakenRequirement(course_codes=["CHEM112", "CHEM104"], minimum_count=1),
        # Quantitative/Analytical Chem + lab
        TakenRequirement(course_codes=["CHEM220"], minimum_count=1),
        TakenRequirement(course_codes=["CHEM221"], minimum_count=1),
        # Physical Chemistry + optional lab or lab alternative
        TakenRequirement(course_codes=["CHEM444"], minimum_count=1),
        # lab optional depending on path
        TakenRequirement(course_codes=["CHEM445", "CHEM333"], minimum_count=0),
        # Organic / Biochemistry / Biology requirement (fulfill via one of several)
        TakenRequirement(course_codes=["CHEM331", "CHEM332", "CHEM527", "BISC207"], minimum_count=1),
        # Math & Physics baseline (simplified as placeholders — your planner likely handles these separately)
        TakenRequirement(course_codes=["MATH242"], minimum_count=1),
        TakenRequirement(course_codes=["MATH243"], minimum_count=1),
        TakenRequirement(course_codes=["PHYS207"], minimum_count=1),
        TakenRequirement(course_codes=["PHYS208"], minimum_count=1),
        # Breadth / General Education / Electives — represent as “take at least X total from list”
        # For simplicity, treat as a large pool: minimum 6 courses from breadthelectives list
        TakenRequirement(
            course_codes=["EGGG101", "ENGL110", "Breadth1", "Breadth2", "Breadth3", "Breadth4", "Breadth5", "Breadth6"],
            minimum_count=6,
        ),
        # Technical / CHEG Electives — at least 3 more CHEG electives (codes placeholder)
        TakenRequirement(
            course_codes=["CHEG electives"],  # this denotes any recognized CHEG elective code
            minimum_count=3,
        ),
    ]
)


# Used generative AI to generate Catalog list
# Catalog literal for UD ChemE (simplified, hackathon-friendly)
# Catalog with multi-section courses (time_slots list = available sections)
UNIVERSITY_CATALOG = Catalog(
    courses_offered=[
        # ---------------- Math sequence (many sections because high demand) ----------------
        Course(
            code="MATH241",
            title="Calculus I",
            credits=4,
            time_slots=[1, 3, 5, 13, 15],  # several MWF + TR sections
            tags=["math", "core"],
            prerequisites=[],
            difficulty=2.8,
        ),
        Course(
            code="MATH242",
            title="Calculus II",
            credits=4,
            time_slots=[2, 4, 6, 14, 16],
            tags=["math", "core"],
            prerequisites=[TakenRequirement(course_codes=["MATH241"], minimum_count=1)],
            difficulty=3.1,
        ),
        Course(
            code="MATH243",
            title="Calculus III",
            credits=4,
            time_slots=[7, 9, 17],  # fewer sections (upper-level)
            tags=["math", "core"],
            prerequisites=[TakenRequirement(course_codes=["MATH242"], minimum_count=1)],
            difficulty=3.4,
        ),
        Course(
            code="MATH260",
            title="Differential Equations",
            credits=3,
            time_slots=[8, 18],
            tags=["math", "core"],
            prerequisites=[TakenRequirement(course_codes=["MATH242"], minimum_count=1)],
            difficulty=3.3,
        ),
        # ---------------- Physics sequence ----------------
        Course(
            code="PHYS207",
            title="General Physics I",
            credits=4,
            time_slots=[0, 2, 14],  # students can pick MWF or TR
            tags=["physics", "core"],
            prerequisites=[TakenRequirement(course_codes=["MATH241"], minimum_count=1)],
            difficulty=3.2,
        ),
        Course(
            code="PHYS208",
            title="General Physics II",
            credits=4,
            time_slots=[4, 6, 16],
            tags=["physics", "core"],
            prerequisites=[TakenRequirement(course_codes=["PHYS207"], minimum_count=1)],
            difficulty=3.4,
        ),
        # ---------------- Chemistry sequence ----------------
        Course(
            code="CHEM111",
            title="General Chemistry I",
            credits=3,
            time_slots=[1, 3, 13, 15],
            tags=["chemistry", "core"],
            prerequisites=[],
            difficulty=2.7,
        ),
        Course(
            code="CHEM112",
            title="General Chemistry II",
            credits=3,
            time_slots=[2, 5, 14],
            tags=["chemistry", "core"],
            prerequisites=[TakenRequirement(course_codes=["CHEM111"], minimum_count=1)],
            difficulty=3.0,
        ),
        Course(
            code="CHEM220",
            title="Quantitative Chemical Analysis",
            credits=3,
            time_slots=[6, 8, 18],
            tags=["chemistry", "lab"],
            prerequisites=[TakenRequirement(course_codes=["CHEM112"], minimum_count=1)],
            difficulty=3.6,
        ),
        Course(
            code="CHEM331",
            title="Organic Chemistry I",
            credits=3,
            time_slots=[7, 9, 17],
            tags=["chemistry", "organic"],
            prerequisites=[TakenRequirement(course_codes=["CHEM112"], minimum_count=1)],
            difficulty=3.8,
        ),
        Course(
            code="CHEM332",
            title="Organic Chemistry II",
            credits=3,
            time_slots=[10, 16],
            tags=["chemistry", "organic"],
            prerequisites=[TakenRequirement(course_codes=["CHEM331"], minimum_count=1)],
            difficulty=3.9,
        ),
        Course(
            code="CHEM444",
            title="Physical Chemistry I (Thermo/Kinetics)",
            credits=3,
            time_slots=[11, 19],
            tags=["chemistry", "physical"],
            prerequisites=[
                TakenRequirement(course_codes=["MATH242", "MATH243"], minimum_count=1),
                TakenRequirement(course_codes=["CHEM112"], minimum_count=1),
            ],
            difficulty=4.0,
        ),
        # ---------------- Intro / General ----------------
        Course(
            code="EGGG101",
            title="Intro to Engineering",
            credits=1,
            time_slots=[0, 12],
            tags=["engineering", "core"],
            prerequisites=[],
            difficulty=2.2,
        ),
        Course(
            code="ENGL110",
            title="Composition",
            credits=3,
            time_slots=[1, 3, 4, 13, 15],
            tags=["writing", "core"],
            prerequisites=[],
            difficulty=2.5,
        ),
        # ---------------- Core CHEG sequence ----------------
        Course(
            code="CHEG112",
            title="Introduction to Chemical Engineering",
            credits=3,
            time_slots=[2, 4, 14],
            tags=["cheg", "core"],
            prerequisites=[TakenRequirement(course_codes=["CHEM111", "MATH241"], minimum_count=1)],
            difficulty=3.0,
        ),
        Course(
            code="CHEG231",
            title="Material & Energy Balances",
            credits=3,
            time_slots=[5, 7, 15],
            tags=["cheg", "core"],
            prerequisites=[TakenRequirement(course_codes=["CHEG112", "CHEM112", "MATH242"], minimum_count=1)],
            difficulty=3.6,
        ),
        Course(
            code="CHEG332",
            title="Transport Phenomena I",
            credits=3,
            time_slots=[8, 18],  # TR/advanced course: fewer sections
            tags=["cheg", "core"],
            prerequisites=[TakenRequirement(course_codes=["MATH243", "PHYS207"], minimum_count=1)],
            difficulty=4.0,
        ),
        Course(
            code="CHEG341",
            title="Thermodynamics for CHEG",
            credits=3,
            time_slots=[9, 19],
            tags=["cheg", "core"],
            prerequisites=[TakenRequirement(course_codes=["CHEM444", "MATH243"], minimum_count=1)],
            difficulty=4.1,
        ),
        Course(
            code="CHEG342",
            title="Unit Operations Lab",
            credits=3,
            time_slots=[10, 20],
            tags=["cheg", "lab"],
            prerequisites=[TakenRequirement(course_codes=["CHEG231"], minimum_count=1)],
            difficulty=4.2,
        ),
        Course(
            code="CHEG345",
            title="Reaction Engineering",
            credits=3,
            time_slots=[11, 21],
            tags=["cheg", "core"],
            prerequisites=[TakenRequirement(course_codes=["CHEG231", "MATH260"], minimum_count=1)],
            difficulty=4.0,
        ),
        Course(
            code="CHEG431",
            title="Senior Design I",
            credits=3,
            time_slots=[12],  # single TR capstone section
            tags=["cheg", "capstone"],
            prerequisites=[TakenRequirement(course_codes=["CHEG332", "CHEG341", "CHEG345"], minimum_count=2)],
            difficulty=4.4,
        ),
        Course(
            code="CHEG432",
            title="Senior Design II",
            credits=3,
            time_slots=[13],  # single TR capstone section (paired with 431)
            tags=["cheg", "capstone"],
            prerequisites=[TakenRequirement(course_codes=["CHEG431"], minimum_count=1)],
            difficulty=4.5,
        ),
        # --------------- Additional CHEG electives (limited set) ---------------
        Course(
            code="CHEG422",
            title="Process Control",
            credits=3,
            time_slots=[6, 16],
            tags=["cheg", "elective"],
            prerequisites=[TakenRequirement(course_codes=["MATH260", "CHEG332"], minimum_count=1)],
            difficulty=4.0,
        ),
        Course(
            code="CHEG451",
            title="Biochemical Engineering",
            credits=3,
            time_slots=[7],
            tags=["cheg", "elective", "bio"],
            prerequisites=[TakenRequirement(course_codes=["CHEM331", "CHEG231"], minimum_count=1)],
            difficulty=4.1,
        ),
        Course(
            code="CHEG460",
            title="Polymer Engineering",
            credits=3,
            time_slots=[9],
            tags=["cheg", "elective"],
            prerequisites=[TakenRequirement(course_codes=["CHEM331"], minimum_count=1)],
            difficulty=4.0,
        ),
        # ---------------- Supporting technical electives from chemistry/biology ----------------
        Course(
            code="BISC207",
            title="Molecular and Cellular Biology",
            credits=4,
            time_slots=[0, 14],
            tags=["bio", "core"],
            prerequisites=[],
            difficulty=3.3,
        ),
        Course(
            code="CHEM527",
            title="Biochemistry (Intro)",
            credits=3,
            time_slots=[10, 16],
            tags=["chemistry", "bio"],
            prerequisites=[TakenRequirement(course_codes=["CHEM331"], minimum_count=1)],
            difficulty=4.0,
        ),
        # ---------------- Typical electives / technical support courses ----------------
        Course(
            code="ENGR201",
            title="Statics (example elective)",
            credits=3,
            time_slots=[1, 3],
            tags=["engineering", "elective"],
            prerequisites=[TakenRequirement(course_codes=["MATH242"], minimum_count=1)],
            difficulty=3.2,
        ),
        Course(
            code="STAT200",
            title="Intro to Statistics",
            credits=3,
            time_slots=[2, 4, 14],
            tags=["math", "elective"],
            prerequisites=[TakenRequirement(course_codes=["MATH241"], minimum_count=1)],
            difficulty=2.9,
        ),
        # ---------------- Breadth / GenEd options ----------------
        Course(
            code="HIST103",
            title="World History (Breadth)",
            credits=3,
            time_slots=[5, 15],
            tags=["breadth", "humanities"],
            prerequisites=[],
            difficulty=2.3,
        ),
        Course(
            code="PHIL101",
            title="Intro to Philosophy (Breadth)",
            credits=3,
            time_slots=[6, 16],
            tags=["breadth", "humanities"],
            prerequisites=[],
            difficulty=2.4,
        ),
        Course(
            code="ECON101",
            title="Principles of Economics (Breadth)",
            credits=3,
            time_slots=[8, 18],
            tags=["breadth", "social"],
            prerequisites=[],
            difficulty=2.7,
        ),
        # ---------------- Labs / Analytical courses ----------------
        Course(
            code="CHEM221",
            title="Quantitative Chemical Analysis Lab",
            credits=1,
            time_slots=[11, 19],
            tags=["chemistry", "lab"],
            prerequisites=[TakenRequirement(course_codes=["CHEM220"], minimum_count=1)],
            difficulty=3.8,
        ),
        Course(
            code="CHEM333",
            title="Analytical Techniques",
            credits=3,
            time_slots=[0, 12],
            tags=["chemistry", "elective"],
            prerequisites=[TakenRequirement(course_codes=["CHEM220"], minimum_count=1)],
            difficulty=3.6,
        ),
        # ---------------- CHEG Elective pool placeholders (few concrete options) ----------------
        Course(
            code="CHEG877",
            title="Process Safety",
            credits=3,
            time_slots=[17, 19],
            tags=["cheg", "elective"],
            prerequisites=[TakenRequirement(course_codes=["CHEG231"], minimum_count=1)],
            difficulty=3.9,
        ),
        Course(
            code="CHEG999",
            title="Chemistry or something",
            credits=3,
            time_slots=[18, 20],
            tags=["cheg", "elective"],
            prerequisites=[TakenRequirement(course_codes=["CHEM112"], minimum_count=1)],
            difficulty=3.7,
        ),
    ]
)


AVAILABLE_MAJORS: Dict[str, Curriculum] = {
    "Chemical Engineering": CHEMICAL_ENGINEERING_CURRICULUM,
}
