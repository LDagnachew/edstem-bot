from datetime import datetime
from models.user import User
from dataclasses import dataclass, field
from services import post_mark_review_comment
from typing import Optional
from sentence_transformers import SentenceTransformer, util


model = SentenceTransformer("all-MiniLM-L6-v2")

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

thread_dict = {}
declined_threads_id = []

# Handles updating the thread pool
def find_duplicate_thread(new_thread: Thread):
    if not thread_dict:
        return None

    titles = [new_thread.title.lower()] + [t.title.lower() for t in thread_dict.values()]
    embeddings = model.encode(titles)

    similarities = util.pytorch_cos_sim(embeddings[0], embeddings[1:]).squeeze(0)

    if similarities.numel() == 0:
        return None

    match_idx = similarities.argmax().item()
    match_score = similarities[match_idx].item()

    # If similarity exceeds threshold, return the matching thread
    if match_score >= 0.85:
        duplicate_thread = list(thread_dict.values())[match_idx]
        return duplicate_thread
    
    # For these cases, its best to notify an instructor before declining
    if match_score >= 0.65:
        potential_duplicate_thread = list(thread_dict.values())[match_idx]
        post_mark_review_comment(potential_duplicate_thread)
        return None

    # No duplicate → Add the new thread to the pool
    thread_dict[new_thread.title.lower()] = new_thread
    return None





	
