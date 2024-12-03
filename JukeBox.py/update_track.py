import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkinter.scrolledtext as tkst
import sv_ttk

from track_library import Track

class UpdateTrackWindow:
    def __init__(self, parent, library):
        self.window = tk.Toplevel(parent)
        self.window.title("🔧 Update Track")
        self.window.geometry("600x450")
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
            text="Update Track Details", 
            font=("Arial", 18, "bold"),
            foreground="#00B4D8"
        )
        title_label.pack(pady=(0,20))

        # Frame for input fields
        input_frame = ttk.Frame(main_container)
        input_frame.pack(fill=tk.X, expand=True)

        # Input fields with improved layout
        fields = [
            ("Track ID:", "track_id", "Enter the ID of the track to update"),
            ("New Track Name:", "name", "Enter new track name"),
            ("New Artist:", "artist", "Enter new artist name"),
            ("New YouTube URL:", "url", "Enter new YouTube URL"),
            ("New Rating (0-5):", "rating", "Enter new rating between 0-5")
        ]

        self.entries = {}
        for label, key, placeholder in fields:
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
            
            self.entries[key] = entry

        # Update button with custom style
        update_btn = ttk.Button(
            main_container,
            text="🔄 Update Track",
            command=self.update_track,
            style="Accent.TButton"
        )
        update_btn.pack(pady=20)

    def on_entry_click(self, event, entry):
        """Remove placeholder text when entry is clicked"""
        if entry.get() in ["Enter the ID of the track to update", 
                            "Enter new track name", 
                            "Enter new artist name", 
                            "Enter new YouTube URL", 
                            "Enter new rating between 0-5"]:
            entry.delete(0, tk.END)
            entry.config(foreground='white')

    def on_entry_leave(self, event, entry):
        """Restore placeholder if no text is entered"""
        if entry.get().strip() == "":
            default_placeholders = {
                "track_id": "Enter the ID of the track to update",
                "name": "Enter new track name",
                "artist": "Enter new artist name",
                "url": "Enter new YouTube URL",
                "rating": "Enter new rating between 0-5"
            }
            entry.insert(0, default_placeholders[entry.cget('name')])
            entry.config(foreground='gray')

    def update_track(self):
        track_id = self.entries["track_id"].get().strip()
        if track_id not in self.library.tracks:
            messagebox.showerror("Error", f"No track found with ID {track_id}")
            return
        
        if not track_id or track_id.startswith("Enter the ID"):
            messagebox.showerror("Error", "Track ID is invalid.")
            return

        track = self.library.tracks[track_id]

            # Update fields that are not empty or placeholders
        fields = {
                "name": self.entries["name"].get().strip(),
                "artist": self.entries["artist"].get().strip(),
                "url": self.entries["url"].get().strip(),
                "rating": self.entries["rating"].get().strip()
            }

        # Update name if provided and not a placeholder
        if fields["name"] and not fields["name"].startswith("Enter new track name"):
            track.name = fields["name"]

        # Update artist if provided and not a placeholder
        if fields["artist"] and not fields["artist"].startswith("Enter new artist name"):
            track.artist = fields["artist"]

        # Update URL if provided and not a placeholder
        if fields["url"] and not fields["url"].startswith("Enter new YouTube URL"):
            track.youtube_url = fields["url"]

        # Update rating if provided, valid, and not a placeholder
        if fields["rating"] and not fields["rating"].startswith("Enter new rating between 0-5"):
            try:
                rating = int(fields["rating"])
                if 0 <= rating <= 5:
                    track.rating = rating
                else:
                    messagebox.showerror("Error", "Rating must be between 0 and 5!")
                    return
            except ValueError:
                messagebox.showerror("Error", "Rating must be a number!")
                return

        # Save updated library
        self.library.save_to_file()
        
        # Show success message
        messagebox.showinfo("Success", f"Track {track_id} updated successfully")
        
        # Close the window
        self.window.destroy()

class RemoveTrackWindow:
    def __init__(self, parent, library):
        self.window = tk.Toplevel(parent)
        self.window.title("🗑️ Remove Track")
        self.window.geometry("500x300")
        self.window.configure(bg='#1E1E1E')
        self.library = library
        sv_ttk.set_theme("dark")
        self.setup_gui()

    def setup_gui(self):
        main_container = ttk.Frame(self.window, padding="20 20 20 20")
        main_container.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = ttk.Label(
            main_container, 
            text="Remove Track", 
            font=("Arial", 18, "bold"),
            foreground="#00B4D8"
        )
        title_label.pack(pady=(0,20))

        # Track ID Input
        input_frame = ttk.Frame(main_container)
        input_frame.pack(fill=tk.X, expand=True, pady=10)

        ttk.Label(
            input_frame, 
            text="Enter Track ID to Remove:", 
            width=25, 
            anchor='w'
        ).pack(side=tk.LEFT, padx=(0,10))

        self.track_id_entry = ttk.Entry(input_frame, width=30)
        self.track_id_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
        self.track_id_entry.insert(0, "Enter the ID of the track to remove")
        self.track_id_entry.bind('<FocusIn>', self.on_entry_click)
        self.track_id_entry.bind('<FocusOut>', self.on_entry_leave)

        # Remove Button
        remove_button = ttk.Button(
            main_container, 
            text="🗑️ Remove Track", 
            command=self.remove_track,
            style="Destructive.TButton"
        )
        remove_button.pack(pady=(20,0))

    def on_entry_click(self, event):
        """Remove placeholder text when entry is clicked"""
        if self.track_id_entry.get() == "Enter the ID of the track to remove":
            self.track_id_entry.delete(0, tk.END)
            self.track_id_entry.config(foreground='white')

    def on_entry_leave(self, event):
        """Restore placeholder if no text is entered"""
        if self.track_id_entry.get().strip() == "":
            self.track_id_entry.insert(0, "Enter the ID of the track to remove")
            self.track_id_entry.config(foreground='gray')

    def remove_track(self):
        track_id = self.track_id_entry.get().strip()

        # Check if track ID is not a placeholder
        if track_id == "Enter the ID of the track to remove":
            messagebox.showerror("Error", "Please enter a valid Track ID")
            return

        # Check if track ID exists
        if track_id in self.library.tracks:
            # Remove the track
            del self.library.tracks[track_id]
            
            # Save updated library
            self.library.save_to_file()
            
            # Show success message                             
            messagebox.showinfo("Success", f"Track {track_id} removed successfully")
            
            # Close the window
            self.window.destroy()
        else:
            # Show error if track not found
            messagebox.showerror("Error", f"No track found with ID {track_id}")