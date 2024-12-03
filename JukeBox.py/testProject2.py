import pytest
import tkinter as tk
from unittest.mock import patch, MagicMock
from create_track_list import AddTrackWindow, FindTrackWindow

class MockLibrary:
    def __init__(self):
        self.tracks = {}
    
    def save_to_file(self):
        pass

class MockTrack:
    def __init__(self, name, artist, url, play_count, rating):
        self.name = name
        self.artist = artist
        self.youtube_url = url
        self.play_count = play_count
        self.rating = rating

# AddTrackWindow Tests
def test_validate_name():
    window = AddTrackWindow(tk.Tk(), MockLibrary())
    assert window.validate_name("A") == "Name too short"
    assert window.validate_name("Valid Name") is None

def test_validate_artist():
    window = AddTrackWindow(tk.Tk(), MockLibrary())
    assert window.validate_artist("A") == "Artist name too short"
    assert window.validate_artist("Valid Artist") is None

def test_validate_url():
    window = AddTrackWindow(tk.Tk(), MockLibrary())
    # Valid YouTube URLs
    valid_urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "http://youtube.com/embed/dQw4w9WgXcQ",
        "https://youtu.be/dQw4w9WgXcQ"
    ]
    # Invalid YouTube URLs
    invalid_urls = [
        "invalid url",
        "https://www.google.com",
        ""
    ]
    
    for url in valid_urls:
        assert window.validate_url(url) is None
    
    for url in invalid_urls:
        assert window.validate_url(url) == "Invalid YouTube URL"

def test_validate_rating():
    window = AddTrackWindow(tk.Tk(), MockLibrary())
    # Invalid ratings
    assert window.validate_rating("-1") == "Rating must be between 0-5"
    assert window.validate_rating("6") == "Rating must be between 0-5"
    assert window.validate_rating("abc") == "Rating must be a number"
    
    # Valid ratings
    assert window.validate_rating("0") is None
    assert window.validate_rating("3") is None
    assert window.validate_rating("5") is None

def test_add_track_successful():
    root = tk.Tk()
    library = MockLibrary()
    add_window = AddTrackWindow(root, library)
    
    # Populate entries
    add_window.entries["name"].delete(0, tk.END)
    add_window.entries["name"].insert(0, "Test Track")
    add_window.entries["artist"].delete(0, tk.END)
    add_window.entries["artist"].insert(0, "Test Artist")
    add_window.entries["url"].delete(0, tk.END)
    add_window.entries["url"].insert(0, "https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    add_window.entries["rating"].delete(0, tk.END)
    add_window.entries["rating"].insert(0, "4")
    
    # Mock messagebox to prevent actual popup
    with patch('tkinter.messagebox.showinfo'):
        add_window.add_track()
    
    assert len(library.tracks) == 1
    track = list(library.tracks.values())[0]
    assert track.name == "Test Track"
    assert track.artist == "Test Artist"
    assert track.rating == 4

def test_add_track_validation_errors():
    root = tk.Tk()
    library = MockLibrary()
    add_window = AddTrackWindow(root, library)
    
    # Test various validation scenarios
    test_cases = [
        {"name": "A", "artist": "Valid Artist", "url": "valid_url", "rating": "3", "expected_error": "Name too short"},
        {"name": "Valid Name", "artist": "A", "url": "valid_url", "rating": "3", "expected_error": "Artist name too short"},
        {"name": "Valid Name", "artist": "Valid Artist", "url": "invalid", "rating": "3", "expected_error": "Invalid YouTube URL"},
        {"name": "Valid Name", "artist": "Valid Artist", "url": "valid_url", "rating": "6", "expected_error": "Rating must be between 0-5"}
    ]
    
    for case in test_cases:
        # Reset entries
        for key in ["name", "artist", "url", "rating"]:
            add_window.entries[key].delete(0, tk.END)
            add_window.entries[key].insert(0, case[key])
        
        # Mock messagebox to check error
        with patch('tkinter.messagebox.showerror') as mock_error:
            add_window.add_track()
            mock_error.assert_called_once()
            assert case["expected_error"] in mock_error.call_args[0][1]

# FindTrackWindow Tests
def test_search_tracks_with_matches():
    root = tk.Tk()
    library = MockLibrary()
    # Populate library with test tracks
    library.tracks = {
        "01": MockTrack("Rock Song", "Rock Band", "url1", 10, 4),
        "02": MockTrack("Pop Track", "Pop Artist", "url2", 5, 3)
    }
    
    find_window = FindTrackWindow(root, library)
    
    # Simulate search
    find_window.search_var.set("rock")
    find_window.search_tracks()
    
    # Check results
    results = find_window.results_text.get(1.0, tk.END)
    assert "Rock Song" in results
    assert "Rock Band" in results

def test_search_tracks_no_matches():
    root = tk.Tk()
    library = MockLibrary()
    library.tracks = {
        "01": MockTrack("Rock Song", "Rock Band", "url1", 10, 4),
        "02": MockTrack("Pop Track", "Pop Artist", "url2", 5, 3)
    }
    
    find_window = FindTrackWindow(root, library)
    
    # Simulate search
    find_window.search_var.set("jazz")
    find_window.search_tracks()
    
    # Check results
    results = find_window.results_text.get(1.0, tk.END)
    assert "No matches found" in results