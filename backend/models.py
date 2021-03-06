from dataclasses import dataclass
from datetime import datetime


def to_cypher_value(value) -> str:
    """Converts value to a valid openCypher type"""
    value_type = type(value)

    if value_type == str and value.lower() == "null":
        return value

    if value_type in [int, float, bool]:
        return str(value)

    if value_type in [list, set, tuple]:
        return f"[{', '.join(map(to_cypher_value, value))}]"

    if value_type == dict:
        lines = ", ".join(f"{k}: {to_cypher_value(v)}" for k, v in value.items())
        return f"{{{lines}}}"

    if value is None:
        return "null"

    if value.lower() in ["true", "false"]:
        return value

    return f"'{value}'"


@dataclass
class Track:
    LABEL = "Track"
    artist_name: str
    track_uri: str
    artist_uri: str
    track_name: str
    album_uri: str
    duration_ms: int
    album_name: str

    @staticmethod
    def create_from_data(data):
        return Track(
            data.properties["artist_name"],
            data.properties["track_uri"],
            data.properties["artist_uri"],
            data.properties["track_name"],
            data.properties["album_uri"],
            data.properties["duration_ms"],
            data.properties["album_name"],
        )

    def to_cypher(self):
        return (
            f"artist_name: {self.artist_name}, track_uri: {self.track_uri}, artist_uri:"
            f" {self.artist_uri}, track_name: {self.track_name}, album_uri: {self.album_uri},"
            f" duration_ms: {to_cypher_value(self.duration_ms)}, album_name: {self.album_name}"
        )

    @staticmethod
    def create_from_dict(data):
        return Track(
            data["artist_name"],
            data["track_uri"],
            data["artist_uri"],
            data["track_name"],
            data["album_uri"],
            data["duration_ms"],
            data["album_name"],
        )


@dataclass
class Playlist:
    LABEL = "Playlist"

    name: str
    collaborative: bool = False
    pid: int = 0
    modified_at: datetime = ""
    num_albums: int = 0
    num_tracks: int = 0
    num_followers: int = 0
    num_edits: int = 0
    duration_ms: int = 0
    num_artists: int = 0

    @staticmethod
    def create_from_data(data):
        return Playlist(
            data.properties["name"],
            data.properties["collaborative"],
            data.properties["pid"],
            data.properties["modified_at"],
            data.properties["num_albums"],
            data.properties["num_tracks"],
            data.properties["num_followers"],
            data.properties["num_edits"],
            data.properties["duration_ms"],
            data.properties["num_artists"],
        )

    @staticmethod
    def create_from_dict(data):
        return Playlist(
            data["name"],
            data["collaborative"],
            data["pid"],
            data["modified_at"],
            data["num_albums"],
            data["num_tracks"],
            data["num_followers"],
            data["num_edits"],
            data["duration_ms"],
            data["num_artists"],
        )

    def to_cypher(self):
        return (
            f"name: {self.name}, collaborative: {to_cypher_value(self.collaborative)},"
            f" pid: {to_cypher_value(self.pid)}, modified_at:"
            f" {to_cypher_value(self.modified_at)}, num_albums:"
            f" {to_cypher_value(self.num_albums)}, num_tracks:"
            f" {to_cypher_value(self.num_tracks)}, num_followers:"
            f" {to_cypher_value(self.num_followers)}, num_edits:"
            f" {to_cypher_value(self.num_edits)}, duration_ms:"
            f" {to_cypher_value(self.duration_ms)}, num_artists:"
            f" {to_cypher_value(self.num_artists)}"
        )

    def to_map(self):
        return self.__dict__
