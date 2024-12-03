import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as tkst
import tkinter.messagebox as messagebox
import sv_ttk
import re+


from track_library import Track

class AddTrackWindow:
    def __init__(self, parent, library):
        self.window = tk.Toplevel(parent)
        self.window.title("➕ Add Track")
        self.window.geometry("600x500")
        self.window.configure(bg='#1E1E1E')
        self.library = library
        sv_ttk.set_theme("dark")
        self.setup_gui()

    def setup_gui(self):
        # Main container with padding
        main_container = ttk.Frame(self.window, padding="20 20 20 20")
        main_container.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = ttk.Label(
            main_container, 
            text="Add New Track", 
            font=("Arial", 18, "bold"),
            foreground="#00B4D8"
        )
        title_label.pack(pady=(0,20))

        # Input frame
        input_frame = ttk.Frame(main_container)
        input_frame.pack(fill=tk.X, expand=True)

        # Input fields with improved layout
        fields = [
            ("Track Name:", "name", "Enter track name", self.validate_name),
            ("Artist:", "artist", "Enter artist name", self.validate_artist),
            ("YouTube URL:", "url", "Enter YouTube URL", self.validate_url),
            ("Rating (0-5):", "rating", "Enter rating (0-5)", self.validate_rating)
        ]

        self.entries = {}
        self.validation_labels = {}
        for label, key, placeholder, validation_func in fields:
            # Field container
            field_container = ttk.Frame(input_frame)
            field_container.pack(fill=tk.X, pady=5)

            # Label
            ttk.Label(
                field_container, 
                text=label, 
                width=20, 
                anchor='w'
            ).pack(side=tk.LEFT, padx=(0,10))

            # Entry with placeholder
            entry = ttk.Entry(field_container, width=40)
            entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
            entry.insert(0, placeholder)
            entry.bind('<FocusIn>', lambda e, entry=entry: self.on_entry_click(e, entry))
            entry.bind('<FocusOut>', lambda e, entry=entry: self.on_entry_leave(e, entry))
            entry.bind('<KeyRelease>', lambda e, key=key, func=validation_func: self.validate_input(e, key, func))
            
            # Validation label
            validation_label = ttk.Label(
                field_container, 
                text="", 
                foreground="red", 
                font=("Arial", 8)
            )
            validation_label.pack(side=tk.LEFT, padx=(10,0))

            self.entries[key] = entry
            self.validation_labels[key] = validation_label

        # Add Track button
        add_btn = ttk.Button(
            main_container,
            text="➕ Add Track",
            command=self.add_track,
            style="Accent.TButton"
        )
        add_btn.pack(pady=20)

    def on_entry_click(self, event, entry):
        """Remove placeholder text when entry is clicked"""
        placeholders = [
            "Enter track name", 
            "Enter artist name", 
            "Enter YouTube URL", 
            "Enter rating (0-5)"
        ]
        if entry.get() in placeholders:
            entry.delete(0, tk.END)
            entry.config(foreground='white')

    def on_entry_leave(self, event, entry):
        """Restore placeholder if no text is entered"""
        if entry.get().strip() == "":
            default_placeholders = {
                "name": "Enter track name",
                "artist": "Enter artist name",
                "url": "Enter YouTube URL",
                "rating": "Enter rating (0-5)"
            }
            key = [k for k, v in self.entries.items() if v == entry][0]
            entry.insert(0, default_placeholders[key])
            entry.config(foreground='gray')

    def validate_name(self, name):
        """Validate track name"""
        if len(name.strip()) < 2:
            return "Name too short"
        return None

    def validate_artist(self, artist):
        """Validate artist name"""
        if len(artist.strip()) < 2:
            return "Artist name too short"
        return None

    def validate_url(self, url):
        """Validate YouTube URL"""
        youtube_regex = (
            r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
        )
        if not re.match(youtube_regex, url):
            return "Invalid YouTube URL"
        return None

    def validate_rating(self, rating):
        """Validate rating"""
        try:
            rating = int(rating)
            if rating < 0 or rating > 5:
                return "Rating must be between 0-5"
        except ValueError:
            return "Rating must be a number"
        return None

    def validate_input(self, event, key, validation_func):
        """Validate input and show/hide validation messages"""
        value = self.entries[key].get()
        
        # Skip validation for placeholders
        placeholders = [
            "Enter track name", 
            "Enter artist name", 
            "Enter YouTube URL", 
            "Enter rating (0-5)"
        ]
        if value in placeholders:
            self.validation_labels[key].config(text="")
            return

        error = validation_func(value)
        if error:
            self.validation_labels[key].config(text=error)
        else:
            self.validation_labels[key].config(text="✓")

    def add_track(self):
        # Validate all fields before adding
        errors = []
        track_data = {}
        for key, entry in self.entries.items():
            value = entry.get()
            
            # Skip placeholders
            placeholders = [
                "Enter track name", 
                "Enter artist name", 
                "Enter YouTube URL", 
                "Enter rating (0-5)"
            ]
            if value in placeholders:
                errors.append(f"{key.capitalize()} is required")
                continue

            # Validate each field
            if key == "name":
                error = self.validate_name(value)
            elif key == "artist":
                error = self.validate_artist(value)
            elif key == "url":
                error = self.validate_url(value)
            elif key == "rating":
                error = self.validate_rating(value)
            
            if error:
                errors.append(error)
            else:
                track_data[key] = value

        # Check for errors
        if errors:
            messagebox.showerror("Validation Error", "\n".join(errors))
            return

        # Add track
        try:
            new_id = str(len(self.library.tracks) + 1).zfill(2)
            self.library.tracks[new_id] = Track(
                track_data["name"], 
                track_data["artist"], 
                track_data["url"], 
                0,  # initial play count
                int(track_data["rating"])
            )
            self.library.save_to_file()
            messagebox.showinfo("Success", "Track added successfully!")
            self.window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add track: {str(e)}")

class FindTrackWindow:
    def __init__(self, parent, library):
        self.window = tk.Toplevel(parent)
        self.window.title("🔍 Find Track")
        self.window.geometry("600x500")
        self.window.configure(bg='#1E1E1E')
        self.library = library
        sv_ttk.set_theme("dark")
        self.setup_gui()

    def setup_gui(self):
        # Main container
        main_container = ttk.Frame(self.window, padding="20 20 20 20")
        main_container.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = ttk.Label(
            main_container, 
            text="Find Tracks", 
            font=("Arial", 18, "bold"),
            foreground="#00B4D8"
        )
        title_label.pack(pady=(0,20))

        # Search frame
        search_frame = ttk.Frame(main_container)
        search_frame.pack(fill=tk.X, pady=(0,10))

        ttk.Label(
            search_frame, 
            text="Search:", 
            width=10, 
            anchor='w'
        ).pack(side=tk.LEFT, padx=(0,10))

        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(
            search_frame, 
            textvariable=self.search_var, 
            width=40
        )
        search_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0,10))

        search_btn = ttk.Button(
            search_frame, 
            text="🔍 Search", 
            command=self.search_tracks,
            style="Accent.TButton"
        )
        search_btn.pack(side=tk.LEFT)

        # Results area
        self.results_text = tkst.ScrolledText(
            main_container, 
            height=15, 
            wrap=tk.WORD,
            font=("Consolas", 10)
        )
        self.results_text.pack(fill=tk.BOTH, expand=True, pady=(10,0))

    def search_tracks(self):
        query = self.search_var.get().strip().lower()
        results = []
        for track_id, track in self.library.tracks.items():
            if query in track.name.lower() or query in track.artist.lower():
                results.append(
                    f"ID: {track_id} | {track.name} by {track.artist}\n"
                )
        
        self.results_text.delete(1.0, tk.END)
        if results:
            self.results_text.insert(tk.END, "Search Results:\n\n")
            self.results_text.insert(tk.END, "".join(results))
        else:
            self.results_text.insert(tk.END, "No matches found.")