import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkinter.scrolledtext as tkst
import sv_ttk

# Import the Track class to handle track objects
from track_library import Track

# Class for updating track details
class UpdateTrackWindow:
    def __init__(self, parent, library):
        # Initialize the "Update Track" window
        self.window = tk.Toplevel(parent)
        self.window.title("Update Track")
        self.window.geometry("600x300")  # Set size of the window
        self.library = library  # Reference to the track library
        sv_ttk.set_theme("dark")  # Set dark theme for consistency
        self.setup_gui()  # Initialize GUI components

    def setup_gui(self):
        # Create a frame for organizing input fields and buttons
        main_frame = ttk.Frame(self.window, padding="20 20 20 20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Define the fields for track updates
        fields = [
            ("Track ID:", "track_id"),  # ID of the track to be updated
            ("New Track Name:", "name"),  # New name for the track
            ("New Artist:", "artist"),  # New artist name
            ("New YouTube URL:", "url"),  # New YouTube URL
            ("New Rating (0-5):", "rating")  # New rating for the track
        ]

        self.entries = {}  # Dictionary to store input fields
        for i, (label, key) in enumerate(fields):
            # Create a label and entry field for each input
            ttk.Label(main_frame, text=label).grid(row=i, column=0, padx=5, pady=5, sticky="e")
            entry = ttk.Entry(main_frame, width=40)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[key] = entry  # Store entry widget by key

        # Add a button to trigger the update process
        ttk.Button(
            main_frame,
            text="Update Track",
            command=self.update_track
        ).grid(row=len(fields), column=0, columnspan=2, pady=20)

    def update_track(self):
        # Fetch the entered track ID
        track_id = self.entries["track_id"].get().strip()
        
        # Validate if the track ID exists
        if track_id not in self.library.tracks:
            messagebox.showerror("Error", f"No track found with ID {track_id}")
            return

        # Retrieve the track object to be updated
        track = self.library.tracks[track_id]

        # Fetch and update track details if provided
        name = self.entries["name"].get().strip()
        artist = self.entries["artist"].get().strip()
        url = self.entries["url"].get().strip()
        rating = self.entries["rating"].get().strip()

        if name:  # Update track name if not empty
            track.name = name
        if artist:  # Update artist name if not empty
            track.artist = artist
        if url:  # Update YouTube URL if not empty
            track.youtube_url = url
        if rating:  # Update rating if valid
            try:
                rating = int(rating)
                if 0 <= rating <= 5:  # Ensure rating is within valid range
                    track.rating = rating
                else:
                    messagebox.showerror("Error", "Rating must be between 0 and 5!")
                    return
            except ValueError:  # Handle non-numeric ratings
                messagebox.showerror("Error", "Rating must be a number!")
                return

        # Save updated library data to file
        self.library.save_to_file()
        
        # Notify user of successful update
        messagebox.showinfo("Success", f"Track {track_id} updated successfully")
        
        # Close the window after updating
        self.window.destroy()

# Class for removing tracks
class RemoveTrackWindow:
    def __init__(self, parent, library):
        # Initialize the "Remove Track" window
        self.window = tk.Toplevel(parent)
        self.window.title("Remove Track")
        self.window.geometry("300x150")  # Set size of the window
        self.library = library  # Reference to the track library
        sv_ttk.set_theme("dark")  # Set dark theme for consistency
        self.setup_gui()  # Initialize GUI components

    def setup_gui(self):
        # Create a frame for organizing input and button
        main_frame = ttk.Frame(self.window, padding="20 20 20 20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Add a label and entry field for track ID
        ttk.Label(main_frame, text="Enter Track ID to Remove:").pack(pady=(0,10))
        self.track_id_entry = ttk.Entry(main_frame, width=30)
        self.track_id_entry.pack(pady=(0,10))

        # Add a button to trigger the remove process
        remove_button = ttk.Button(
            main_frame, 
            text="Remove Track", 
            command=self.remove_track
        )
        remove_button.pack(pady=(10,0))

    def remove_track(self):
        # Fetch the entered track ID
        track_id = self.track_id_entry.get().strip()

        # Validate if the track ID exists
        if track_id in self.library.tracks:
            # Remove the track from the library
            del self.library.tracks[track_id]
            
            # Save updated library data to file
            self.library.save_to_file()
            
            # Notify user of successful removal
            messagebox.showinfo("Success", f"Track {track_id} removed successfully")
            
            # Close the window after removal
            self.window.destroy()
        else:
            # Show error message if track ID is not found
            messagebox.showerror("Error", f"No track found with ID {track_id}")
