import csv
import io
import json
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from core.database import get_db
from models.user_model import User
from models.profile_model import Profile
from models.track_model import Track
from models.album_models import Album
from models.playlists_model import Playlist
from models.likes_model import Like
from models.genre_models import TrackGenre
from models.listening_history_model import ListeningHistory
from models.album_models import AlbumRating
from models.track_model import TrackRatings

router = APIRouter()

def serialize(obj):
    if hasattr(obj, '__dict__'):
        data = obj.__dict__.copy()
        data.pop('_sa_instance_state', None)
        for k, v in data.items():
            if hasattr(v, 'strftime'):
                data[k] = v.isoformat()
            elif hasattr(v, 'hex'):
                data[k] = str(v)
            elif hasattr(v, 'value'):
                data[k] = v.value
        return data
    elif hasattr(obj, 'value'):
        return obj.value
    return str(obj)

@router.get("/export/all/json")
def export_all_to_json(db: Session = Depends(get_db)):
    data = {
        "users": [serialize(u) for u in db.query(User).all()],
        "profiles": [serialize(p) for p in db.query(Profile).all()],
        "tracks": [serialize(t) for t in db.query(Track).all()],
        "albums": [serialize(a) for a in db.query(Album).all()],
        "playlists": [serialize(p) for p in db.query(Playlist).all()],
        "likes": [serialize(l) for l in db.query(Like).all()],
        "track_genres": [serialize(tg) for tg in db.query(TrackGenre).all()],
        "listening_history": [serialize(lh) for lh in db.query(ListeningHistory).all()],
        "track_ratings": [serialize(tr) for tr in db.query(TrackRatings).all()],
        "album_ratings": [serialize(ar) for ar in db.query(AlbumRating).all()],
    }
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    return StreamingResponse(
        io.BytesIO(json_str.encode("utf-8")),
        media_type="application/json",
        headers={"Content-Disposition": "attachment; filename=database_export.json"}
    )

@router.get("/export/all/csv")
def export_all_to_csv(db: Session = Depends(get_db)):
    output = io.StringIO()
    writer = csv.writer(output)

    tables = [
        ("users", User, ["id", "email", "username"]),
        ("profiles", Profile, ["id", "nickname", "bio", "user_id", "is_verified"]),
        ("tracks", Track, ["id", "title", "music_file_url", "owner"]),
        ("albums", Album, ["id", "title", "owner_id"]),
        ("playlists", Playlist, ["id", "owner_id", "title", "description"]),
        ("likes", Like, ["id", "track_id", "user_id"]),
        ("track_genres", TrackGenre, ["id", "track_id", "genre"]),
        ("listening_history", ListeningHistory, ["id", "user_id", "track_id", "played_at"]),
        ("track_ratings", TrackRatings, ["id", "track_id", "user_id", "rating"]),
        ("album_ratings", AlbumRating, ["id", "album_id", "user_id", "rating"]),
    ]

    for table_name, model, columns in tables:
        writer.writerow([f"=== {table_name.upper()} ==="])
        writer.writerow(columns)
        for row in db.query(model).all():
            writer.writerow([str(getattr(row, col, "")) for col in columns])
        writer.writerow([])

    output.seek(0)
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode("utf-8-sig")),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=database_export.csv"}
    )
