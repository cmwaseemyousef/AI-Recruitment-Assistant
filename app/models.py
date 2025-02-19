class Candidate:
    """Class representing a job candidate."""
    def __init__(self, name, skills, experience, education):
        self.name = name
        self.skills = skills
        self.experience = experience
        self.education = education
    def __repr__(self):
        return f"<Candidate {self.name}>"