"""Menu-driven course prerequisite system (Question 2).

An edge  Y -> X  means "Y is a prerequisite of X".
  prerequisites of X = incoming edges of X
  courses unlocked by Y = outgoing edges of Y
"""
from course import Course
from graph import Graph

SAMPLE_COURSES = [
    Course("CS101", "Programming Fundamentals", 4, Course.CORE, "Intro to programming in Python."),
    Course("CS102", "Discrete Mathematics", 3, Course.CORE, "Logic, sets, relations and proofs."),
    Course("CS201", "Data Structures", 4, Course.CORE, "Lists, trees, hash tables and graphs."),
    Course("CS202", "Databases", 3, Course.CORE, "Relational model and SQL."),
    Course("CS301", "Advanced Algorithms", 4, Course.CORE, "Complexity, hashing, graphs, concurrency."),
    Course("CS302", "Artificial Intelligence", 3, Course.ELECTIVE, "Search, learning and reasoning."),
    Course("CS303", "Machine Learning", 3, Course.ELECTIVE, "Supervised and unsupervised learning."),
    Course("CS401", "Final Year Project", 6, Course.CORE, "Capstone software project."),
]

# (prerequisite, course that requires it)
SAMPLE_PREREQUISITES = [
    ("CS101", "CS201"), ("CS102", "CS201"), ("CS101", "CS202"),
    ("CS201", "CS301"), ("CS201", "CS302"), ("CS302", "CS303"),
    ("CS301", "CS401"), ("CS202", "CS401"),
]


def build_graph():
    graph = Graph()
    by_code = {}
    for course in SAMPLE_COURSES:
        graph.addVertex(course)
        by_code[course.code] = course
    for pre, course in SAMPLE_PREREQUISITES:
        graph.addEdge(by_code[pre], by_code[course])
    return graph, by_code


def ask_course(by_code, prompt="Enter course code: "):
    code = input(prompt).strip().upper()
    course = by_code.get(code)
    if course is None:
        print(f"  No course with code '{code}'.")
    return course


def print_course_list(courses, empty_msg):
    if not courses:
        print(f"  {empty_msg}")
        return
    for course in sorted(courses, key=lambda c: c.code):
        print(f"  {course}")


# ---------------- mandatory features ----------------
def list_all(graph, by_code):
    print("\nAll courses and their prerequisites:")
    for i, course in enumerate(sorted(graph.vertices(), key=lambda c: c.code), 1):
        prereqs = sorted(p.code for p in graph.listIncomingAdjacentVertex(course))
        print(f"  {i}. {course.name} ({course.code})")
        print(f"     Prerequisites: {', '.join(prereqs) if prereqs else 'None'}")


def view_details(graph, by_code):
    course = ask_course(by_code)
    if course:
        print("\n" + course.details())


def view_prerequisites(graph, by_code):
    course = ask_course(by_code)
    if course:
        print(f"\nPrerequisites of {course}:")
        print_course_list(graph.listIncomingAdjacentVertex(course), "None (no prerequisites)")


def view_unlocked(graph, by_code):
    course = ask_course(by_code)
    if course:
        print(f"\nCourses unlocked by {course}:")
        print_course_list(graph.listOutgoingAdjacentVertex(course), "None (does not unlock any course)")


# ---------------- advanced features ----------------
def add_course(graph, by_code):
    code = input("New course code: ").strip().upper()
    if code in by_code:
        print("  A course with this code already exists.")
        return
    name = input("Course name: ")
    description = input("Description: ")
    level = input("Level (core/elective): ").strip().lower()
    try:
        credits = int(input("Credit hours: "))
        course = Course(code, name, credits, level, description)
    except ValueError as err:
        print(f"  Invalid data: {err}")
        return
    graph.addVertex(course)
    by_code[course.code] = course
    print(f"  Added {course}.")


def view_profile(graph, by_code):
    course = ask_course(by_code)
    if course:
        print("\n" + course.profile())


def add_prerequisite(graph, by_code):
    course = ask_course(by_code, "Course that needs a prerequisite (X): ")
    pre = ask_course(by_code, "Course to add as prerequisite (Y): ") if course else None
    if not (course and pre):
        return
    if course == pre:
        print("  A course cannot be its own prerequisite.")
    elif graph.hasEdge(pre, course):
        print("  That prerequisite already exists.")
    elif graph.hasPath(course, pre):
        print("  Rejected: this would create a circular prerequisite chain.")
    else:
        graph.addEdge(pre, course)
        print(f"  {pre.code} is now a prerequisite of {course.code}.")


def remove_prerequisite(graph, by_code):
    course = ask_course(by_code, "Course to remove a prerequisite from (X): ")
    pre = ask_course(by_code, "Prerequisite to remove (Y): ") if course else None
    if not (course and pre):
        return
    if graph.removeEdge(pre, course):
        print(f"  {pre.code} is no longer a prerequisite of {course.code}.")
    else:
        print(f"  {pre.code} is not a prerequisite of {course.code}.")


MENU = [
    ("List all courses", list_all),
    ("View course details", view_details),
    ("View prerequisites of a course", view_prerequisites),
    ("View courses unlocked by a course", view_unlocked),
    ("Add a new course", add_course),
    ("View course profile (elective details hidden)", view_profile),
    ("Add a prerequisite", add_prerequisite),
    ("Remove a prerequisite", remove_prerequisite),
]


def main():
    graph, by_code = build_graph()
    try:
        while True:
            print("\n==== Course Prerequisite System ====")
            for i, (label, _) in enumerate(MENU, 1):
                print(f"{i}. {label}")
            print("0. Exit")
            choice = input("Enter choice: ").strip()
            if choice == "0":
                break
            if choice.isdigit() and 1 <= int(choice) <= len(MENU):
                MENU[int(choice) - 1][1](graph, by_code)
            else:
                print(f"Invalid choice, please enter 0-{len(MENU)}.")
    except (EOFError, KeyboardInterrupt):
        print()
    print("Goodbye!")


if __name__ == "__main__":
    main()
