from sqlalchemy.orm import Session

from app.models.track_events import TrackEvents
from app.schemas.schemas import TrackEvent

def insertTrackEvent(db: Session, track_event: TrackEvent):
    evt = TrackEvents(
        youtube_id=track_event.id,
        requested_by=track_event.requested_by,
        event_type=track_event.event_type,
        timestamp=track_event.timestamp,
        guild_id=track_event.guild_id,
        title=track_event.title,
        url=track_event.webpage_url,
        duration=track_event.duration
    )
    db.add(evt)
    db.commit()
