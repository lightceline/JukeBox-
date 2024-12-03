import pytest
import tkinter as tk
from unittest.mock import MagicMock, patch
from update_track import UpdateTrackWindow, RemoveTrackWindow

class MockLibrary:
    def __init__(self):
        self.tracks = {
            "1": MockTrack("Track 1", "Artist 1", "url1", 3),
            "2": MockTrack("Track 2", "Artist 2", "url2", 4)
        }
    
    def save_to_file(self):
        pass

class MockTrack:
    def __init__(self, name, artist, url, rating):
        self.name = name
        self.artist = artist
        self.youtube_url = url
        self.rating = rating

# UpdateTrackWindow Tests
def test_update_track_name():
    root = tk.Tk()
    library = MockLibrary()
    update_window = UpdateTrackWindow(root, library)
    
    update_window.entries["track_id"].delete(0, tk.END)
    update_window.entries["track_id"].insert(0, "1")
    update_window.entries["name"].delete(0, tk.END)
    update_window.entries["name"].insert(0, "Updated Track Name")
    
    with patch('tkinter.messagebox.showinfo'):
        update_window.update_track()
    
    assert library.tracks["1"].name == "Updated Track Name"

def test_update_track_invalid_id():
    root = tk.Tk()
    library = MockLibrary()
    update_window = UpdateTrackWindow(root, library)
    
    update_window.entries["track_id"].delete(0, tk.END)
    update_window.entries["track_id"].insert(0, "999")
    
    with patch('tkinter.messagebox.showerror') as mock_error:
        update_window.update_track()
        mock_error.assert_called_once_with("Error", "No track found with ID 999")

def test_update_track_invalid_rating():
    root = tk.Tk()
    library = MockLibrary()
    update_window = UpdateTrackWindow(root, library)
    
    update_window.entries["track_id"].delete(0, tk.END)
    update_window.entries["track_id"].insert(0, "1")
    update_window.entries["rating"].delete(0, tk.END)
    update_window.entries["rating"].insert(0, "6")
    
    with patch('tkinter.messagebox.showerror') as mock_error:
        update_window.update_track()
        mock_error.assert_called_once_with("Error", "Rating must be between 0 and 5!")

def test_update_track_non_numeric_rating():
    root = tk.Tk()
    library = MockLibrary()
    update_window = UpdateTrackWindow(root, library)
    
    update_window.entries["track_id"].delete(0, tk.END)
    update_window.entries["track_id"].insert(0, "1")
    update_window.entries["rating"].delete(0, tk.END)
    update_window.entries["rating"].insert(0, "abc")
    
    with patch('tkinter.messagebox.showerror') as mock_error:
        update_window.update_track()
        mock_error.assert_called_once_with("Error", "Rating must be a number!")

def test_update_track_entry_click_and_leave():
    root = tk.Tk()
    library = MockLibrary()
    update_window = UpdateTrackWindow(root, library)
    
    # Test placeholders for each entry
    entries_to_test = [
        ("track_id", "Enter the ID of the track to update"),
        ("name", "Enter new track name"),
        ("artist", "Enter new artist name"),
        ("url", "Enter new YouTube URL"),
        ("rating", "Enter new rating between 0-5")
    ]
    
    for key, placeholder in entries_to_test:
        entry = update_window.entries[key]
        
        # Simulate focus in (should clear placeholder)
        event_mock = MagicMock()
        update_window.on_entry_click(event_mock, entry)
        assert entry.get() == ""
        
        # Simulate focus out with empty entry (should restore placeholder)
        entry.delete(0, tk.END)
        update_window.on_entry_leave(event_mock, entry)
        assert entry.get() == placeholder

# RemoveTrackWindow Tests
def test_remove_track_successful():
    root = tk.Tk()
    library = MockLibrary()
    remove_window = RemoveTrackWindow(root, library)
    
    remove_window.track_id_entry.delete(0, tk.END)
    remove_window.track_id_entry.insert(0, "1")
    
    with patch('tkinter.messagebox.showinfo'):
        remove_window.remove_track()
    
    assert "1" not in library.tracks

def test_remove_track_invalid_id():
    root = tk.Tk()
    library = MockLibrary()
    remove_window = RemoveTrackWindow(root, library)
    
    remove_window.track_id_entry.delete(0, tk.END)
    remove_window.track_id_entry.insert(0, "999")
    
    with patch('tkinter.messagebox.showerror') as mock_error:
        remove_window.remove_track()
        mock_error.assert_called_once_with("Error", "No track found with ID 999")

def test_remove_track_entry_click_and_leave():
    root = tk.Tk()
    library = MockLibrary()
    remove_window = RemoveTrackWindow(root, library)
    
    # Simulate focus in (should clear placeholder)
    event_mock = MagicMock()
    remove_window.on_entry_click(event_mock)
    assert remove_window.track_id_entry.get() == ""
    
    # Simulate focus out with empty entry (should restore placeholder)
    remove_window.track_id_entry.delete(0, tk.END)
    remove_window.on_entry_leave(event_mock)
    assert remove_window.track_id_entry.get() == "Enter the ID of the track to remove"