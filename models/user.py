from dataclasses import dataclass

@dataclass
class User:
	id: int
	role: str
	name: str
	avatar: any
	course_role: str
	tutorials: dict[int, str]