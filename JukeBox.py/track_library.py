import json  # Thư viện này dùng để đọc và ghi dữ liệu dưới dạng tệp JSON.

# Lớp Track: Dùng để lưu thông tin về một bài hát.
class Track:
    def __init__(self, name, artist, youtube_url, play_count=0, rating=0):
        self.name = name
        self.artist = artist
        self.youtube_url = youtube_url
        self.play_count = play_count
        self.rating = rating

    def to_dict(self):
        return {
            'name': self.name,
            'artist': self.artist,
            'youtube_url': self.youtube_url,
            'play_count': self.play_count,
            'rating': self.rating
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data['name'],
            data['artist'],
            data['youtube_url'],
            data['play_count'],
            data['rating']
        )

class TrackLibrary:
    def __init__(self):
        self.tracks = {}

    def save_to_file(self):
        with open('library.json', 'w') as f:
            json_data = {k: v.to_dict() for k, v in self.tracks.items()}
            json.dump(json_data, f, indent=4)

    def load_from_file(self):
        try:
            with open('library.json', 'r') as f:
                data = json.load(f)
                self.tracks = {k: Track.from_dict(v) for k, v in data.items()}
        except FileNotFoundError:
            self.tracks = {}

            

