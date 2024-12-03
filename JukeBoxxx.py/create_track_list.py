import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as tkst
import sv_ttk

# Import the Track class to manage track objects
from track_library import Track

# Class to handle adding new tracks to the library
class AddTrackWindow:
    def __init__(self, parent, library):
        # Initialize the "Add Track" window
        self.window = tk.Toplevel(parent)
        self.window.title("Add Track")
        self.window.geometry("600x250")  # Set the size of the window
        self.library = library  # Reference to the track library
        sv_ttk.set_theme("dark")  # Set dark theme for consistency
        self.setup_gui()  # Set up the graphical user interface

    def setup_gui(self):
        # Create a frame for form layout
        form_frame = ttk.Frame(self.window)
        form_frame.pack(padx=20, pady=20)

        # Define the input fields for adding a track
        fields = [
            ("Track Name:", "name"),  # Name of the track
            ("Artist:", "artist"),  # Name of the artist
            ("YouTube URL:", "url"),  # YouTube URL for the track
            ("Rating (0-5):", "rating")  # User-defined rating for the track
        ]

        self.entries = {}  # Dictionary to store input widgets
        for i, (label, key) in enumerate(fields):
            # Create a label and entry field for each input
            ttk.Label(form_frame, text=label).grid(row=i, column=0, padx=5, pady=5, sticky="e")
            entry = ttk.Entry(form_frame, width=40)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[key] = entry  # Save entry widget by key

        # Add a button to submit the new track
        ttk.Button(
            form_frame,
            text="Add Track",
            command=self.add_track  # Call add_track method on click
        ).grid(row=len(fields), column=0, columnspan=2, pady=20)

    def add_track(self):
        # Retrieve input values
        name = self.entries["name"].get()
        artist = self.entries["artist"].get()
        url = self.entries["url"].get()
        rating = self.entries["rating"].get()

        # Validate inputs
        if all([name, artist, url, rating]):  # Ensure all fields are filled
            try:
                rating = int(rating)  # Convert rating to integer
                if 0 <= rating <= 5:  # Check if rating is within valid range
                    # Generate a new ID and add track to library
                    new_id = str(len(self.library.tracks) + 1).zfill(2)
                    self.library.tracks[new_id] = Track(name, artist, url, 0, rating)
                    self.library.save_to_file()  # Save updated library to file
                    self.window.destroy()  # Close the window
                else:
                    # Show error if rating is out of range
                    tk.messagebox.showerror("Error", "Rating must be between 0 and 5!")
            except ValueError:
                # Show error if rating is not a number
                tk.messagebox.showerror("Error", "Rating must be a number!")
        else:
            # Show error if any field is left empty
            tk.messagebox.showerror("Error", "Please fill in all fields!")

# Class to handle searching for tracks in the library
class FindTrackWindow:
    def __init__(self, parent, library):
        # Initialize the "Find Track" window
        self.window = tk.Toplevel(parent)
        self.window.title("Find Track")
        self.window.geometry("600x200")  # Set the size of the window
        self.library = library  # Reference to the track library
        sv_ttk.set_theme("dark")  # Set dark theme for consistency
        self.setup_gui()  # Set up the graphical user interface

    def setup_gui(self):
        # Create a frame for the search bar
        search_frame = ttk.Frame(self.window)
        search_frame.pack(padx=20, pady=20, fill=tk.X)

        # Add a label, entry field, and button for searching
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=(0, 10))
        self.search_var = tk.StringVar()  # Variable to hold search query
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=40)
        search_entry.pack(side=tk.LEFT, padx=(0, 10))

        # Add a search button
        ttk.Button(search_frame, text="Search", command=self.search_tracks).pack(side=tk.LEFT)

        # Add a scrollable text area to display results
        self.results_text = tkst.ScrolledText(self.window, height=15)
        self.results_text.pack(padx=20, pady=(10, 20), fill=tk.BOTH, expand=True)

    def search_tracks(self):
        # Get the search query and convert it to lowercase
        query = self.search_var.get().strip().lower()
        results = []  # List to hold search results
        
        # Search through tracks in the library
        for track in self.library.tracks.values():
            if query in track.name.lower() or query in track.artist.lower():
                # Add matching tracks to results list
                results.append(f"{track.name} by {track.artist} (Rating: {track.rating})")
        
        # Clear previous results
        self.results_text.delete(1.0, tk.END)
        if results:
            # Display results if matches are found
            self.results_text.insert(tk.END, "\n".join(results))
        else:
            # Display message if no matches are found
            self.results_text.insert(tk.END, "No matches found.")
