from datetime import datetime
from models.user import User
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Thread:
	id: int
	user_id: int
	course_id: int
	original_id: int
	editor_id: int
	accepted_id: int
	duplicate_id: int
	number: int
	type: str
	title: str
	content: str
	document: str
	category: str
	subcategory: str
	subsubcategory: str
	flag_count: int
	star_count: int
	view_count: int
	unique_view_count: int
	vote_count: int
	reply_count: int
	unresolved_count: int
	is_locked: bool
	is_pinned: bool
	is_private: bool
	is_endorsed: bool
	is_answered: bool
	is_student_answered: bool
	is_staff_answered: bool
	is_archived: bool
	is_anonymous: bool
	is_megathread: bool
	anonymous_comments: bool
	approved_status: str
	created_at: datetime
	updated_at: datetime
	deleted_at: str
	pinned_at: str
	anonymous_id: int
	vote: Optional[int] = None
	is_seen: Optional[bool] = None
	is_starred: Optional[bool] = None
	is_watched: Optional[bool] = None
	glanced_at: Optional[datetime] = None
	new_reply_count: Optional[int] = None
	duplicate_title: Optional[str] = None
	user: Optional[User] = field(default=None)



