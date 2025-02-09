from datetime import datetime
from user import User
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
	vote: int
	is_seen: bool
	is_starred: bool
	is_watched: bool
	glanced_at: datetime
	new_reply_count: int
	duplicate_title: str
	user: User



