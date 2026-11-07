"""Entity class for a university course (Question 2)."""


class Course:
    CORE = "core"
    ELECTIVE = "elective"

    def __init__(self, code: str, name: str, credit_hours: int, level: str,
                 description: str = ""):
        if not code.strip() or not name.strip():
            raise ValueError("Course code and name cannot be empty")
        if credit_hours <= 0:
            raise ValueError("Credit hours must be positive")
        if level not in (Course.CORE, Course.ELECTIVE):
            raise ValueError("Level must be 'core' or 'elective'")
        self.code = code.strip().upper()
        self.name = name.strip()
        self.credit_hours = credit_hours
        self.level = level
        self.description = description.strip()

    # Equality/hash on the course code lets Course be used as a graph vertex.
    def __eq__(self, other):
        return isinstance(other, Course) and self.code == other.code

    def __hash__(self):
        return hash(self.code)

    def details(self):
        """Full profile, ignoring visibility."""
        return (f"Code        : {self.code}\n"
                f"Name        : {self.name}\n"
                f"Credit Hours: {self.credit_hours}\n"
                f"Level       : {self.level.capitalize()}\n"
                f"Description : {self.description or '-'}")

    def profile(self):
        """Visibility-aware profile: electives show the name only."""
        if self.level == Course.ELECTIVE:
            return f"Name        : {self.name}\n(Elective - other details are hidden)"
        return self.details()

    def __str__(self):
        return f"{self.code} - {self.name}"
