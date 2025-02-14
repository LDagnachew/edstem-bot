from datetime import datetime
from models.user import User
from dataclasses import dataclass, field
from typing import Optional
from sentence_transformers import SentenceTransformer, util


model = SentenceTransformer("all-MiniLM-L6-v2")

thread_dict = {}

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


# Handles updating the thread pool
def find_duplicate_thread(new_thread=Thread):

	if not thread_dict or len(thread_dict) == 0:
		return None
	
	titles = [new_thread.title] + list(thread_dict.keys())
	embeddings = model.encode(titles);

	similarities = util.pytorch_cos_sim(embeddings[0], embeddings[1:]).squeeze(0)

	if similarities.numel() == 0:
		return None
	
	# Find the highest that is similar
	match_idx = similarities.argmax().item()
	match_score = similarities[match_idx].item()

	# Duplicate Found!
	if match_score >= 0.8:
		return thread_dict[titles[match_idx]]

	return None
	



	
