import pytest
import json
import os
from track_library import Track, TrackLibrary

class TestTrack:
    def test_track_creation_full_params(self):
        track = Track(
            name="Test Song", 
            artist="Test Artist", 
            youtube_url="https://youtube.com/test", 
            play_count=5, 
            rating=4
        )
        assert track.name == "Test Song"
        assert track.artist == "Test Artist"
        assert track.youtube_url == "https://youtube.com/test"
        assert track.play_count == 5
        assert track.rating == 4

    def test_track_creation_default_params(self):
        track = Track(
            name="Default Song", 
            artist="Default Artist", 
            youtube_url="https://youtube.com/default"
        )
        assert track.play_count == 0
        assert track.rating == 0

    def test_track_to_dict(self):
        track = Track(
            name="Dict Song", 
            artist="Dict Artist", 
            youtube_url="https://youtube.com/dict", 
            play_count=10, 
            rating=5
        )
        track_dict = track.to_dict()
        assert track_dict == {
            'name': "Dict Song",
            'artist': "Dict Artist", 
            'youtube_url': "https://youtube.com/dict",
            'play_count': 10,
            'rating': 5
        }

    def test_track_from_dict(self):
        track_data = {
            'name': "FromDict Song",
            'artist': "FromDict Artist",
            'youtube_url': "https://youtube.com/fromdict",
            'play_count': 7,
            'rating': 3
        }
        track = Track.from_dict(track_data)
        assert track.name == "FromDict Song"
        assert track.artist == "FromDict Artist"
        assert track.youtube_url == "https://youtube.com/fromdict"
        assert track.play_count == 7
        assert track.rating == 3

class TestTrackLibrary:
    def setup_method(self):
        # Ensure clean state before each test
        self.library = TrackLibrary()
        if os.path.exists('library.json'):
            os.remove('library.json')

    def test_library_initialization(self):
        assert len(self.library.tracks) == 0

    def test_save_to_file(self):
        # Add some tracks
        track1 = Track("Song1", "Artist1", "https://youtube.com/1")
        track2 = Track("Song2", "Artist2", "https://youtube.com/2", 5, 4)
        
        # Add to library
        self.library.tracks = {
            'track1': track1,
            'track2': track2
        }
        
        # Save to file
        self.library.save_to_file()
        
        # Verify file was created
        assert os.path.exists('library.json')
        
        # Verify file contents
        with open('library.json', 'r') as f:
            saved_data = json.load(f)
        
        assert len(saved_data) == 2
        assert saved_data['track1']['name'] == "Song1"
        assert saved_data['track2']['rating'] == 4

    def test_load_from_file(self):
        # Prepare test data
        test_data = {
            'track1': {
                'name': "LoadSong1",
                'artist': "LoadArtist1",
                'youtube_url': "https://youtube.com/load1",
                'play_count': 3,
                'rating': 2
            }
        }
        
        # Save test data to file
        with open('library.json', 'w') as f:
            json.dump(test_data, f)
        
        # Load from file
        library = TrackLibrary()
        library.load_from_file()
        
        # Verify loaded data
        assert len(library.tracks) == 1
        loaded_track = list(library.tracks.values())[0]
        assert loaded_track.name == "LoadSong1"
        assert loaded_track.artist == "LoadArtist1"
        assert loaded_track.play_count == 3

    def test_load_from_nonexistent_file(self):
        # Ensure no library.json exists
        if os.path.exists('library.json'):
            os.remove('library.json')
        
        # Create library (should trigger load_default_tracks)
        library = TrackLibrary()
        library.load_from_file()
        
        # This test would depend on the implementation of load_default_tracks
        # Since that method is not fully defined in the provided code,
        # you might need to add a specific implementation or modify the test
        assert len(library.tracks) > 0