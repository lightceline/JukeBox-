import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
import webbrowser
import sv_ttk

from track_library import TrackLibrary
from create_track_list import AddTrackWindow
from create_track_list import FindTrackWindow
from update_track import RemoveTrackWindow
from update_track import UpdateTrackWindow

# Main application class for the JukeBox GUI
class MainApplication:
    def __init__(self):
        # Initialize the root window and configure basic settings
        self.root = tk.Tk()
        self.root.title("🎵 JukeBox")
        self.root.geometry("1000x400")
        self.root.configure(bg='#1E1E1E')  # Dark background
        
        # Initialize the track library and load data from file
        self.library = TrackLibrary()
        try:
            self.library.load_from_file()
        except Exception as e:
            print(f"Error loading library: {e}")
            self.library.tracks = []  # Initialize an empty library in case of failure

        # Apply a dark theme using sv_ttk
        sv_ttk.set_theme("dark")
        
        # Set up the user interface
        self.setup_gui()

    def setup_gui(self):
        # Create the main container with padding for the layout
        main_container = ttk.Frame(self.root, padding="20 20 20 20")
        main_container.pack(fill=tk.BOTH, expand=True)
        main_container.columnconfigure(1, weight=1)

        # Create a sidebar for action buttons
        sidebar_frame = ttk.Frame(main_container, width=200)
        sidebar_frame.grid(row=0, column=0, sticky="nsew", padx=(0,20))
        sidebar_frame.grid_propagate(False)

        # App title with custom font
        title_font = tkfont.Font(family="Arial", size=24, weight="bold")
        ttk.Label(
            sidebar_frame, 
            text="JukeBox",
            font=title_font,
            foreground="#00B4D8"
        ).pack(pady=(0,30))

        # Define and add action buttons for managing tracks
        action_buttons = [
            ("➕ ", self.open_add_track),      # Add a new track
            ("➖ ", self.open_remove_track),   # Remove a track
            ("🔍 ", self.open_find_track),    # Find a track
            ("✏️ ", self.open_update_track)   # Update track details
        ]
        for text, command in action_buttons:
            btn = ttk.Button(
                sidebar_frame,
                text=text,
                command=command,
                width=0,
                style="Accent.TButton"  # Highlighted button style
            )
            btn.pack(side=tk.TOP, pady=10)

        # Create a track list section with treeview for displaying tracks
        track_frame = ttk.Frame(main_container)
        track_frame.grid(row=0, column=1, sticky="nsew")

        # Define columns for the track list
        columns = ('Track', 'Artist', 'Rating', 'Play Count')
        self.track_tree = ttk.Treeview(
            track_frame, 
            columns=columns, 
            show='headings', 
            style='Custom.Treeview'
        )
        
        # Configure column headers and alignment
        for col in columns:
            self.track_tree.heading(col, text=col, anchor='center')
            self.track_tree.column(col, width=10, anchor='center')

        # Add a vertical scrollbar for the treeview
        scrollbar = ttk.Scrollbar(track_frame, orient=tk.VERTICAL, command=self.track_tree.yview)
        self.track_tree.configure(yscrollcommand=scrollbar.set)

        # Pack the treeview and scrollbar into the layout
        self.track_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind a double-click event to play the selected track
        self.track_tree.bind('<Double-1>', self.play_selected_track)
        
        # Apply custom styling to the treeview
        style = ttk.Style()
        style.configure('Custom.Treeview', 
                        background='#2C2C2C', 
                        foreground='white', 
                        fieldbackground='#2C2C2C',
                        font=('Arial', 10))
        style.map('Custom.Treeview', 
                  background=[('selected', '#00B4D8')],
                  foreground=[('selected', 'white')])

        # Load tracks into the treeview
        self.update_track_list()

        # Add a status and exit section at the bottom
        status_frame = ttk.Frame(main_container)
        status_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(20,0))

        self.status_label = ttk.Label(
            status_frame,
            text="Ready to rock your music library! 🎧",
            font=("Arial", 10),
            foreground="#00B4D8"
        )
        self.status_label.pack(side=tk.LEFT, expand=True)

        # Exit button to close the application
        exit_btn = ttk.Button(
            status_frame,
            text="Exit",
            command=self.root.destroy,
            style="Destructive.TButton"
        )
        exit_btn.pack(side=tk.RIGHT)

    def update_track_list(self):
        # Refresh the track list in the treeview
        for item in self.track_tree.get_children():
            self.track_tree.delete(item)
        
        for track_id, track in self.library.tracks.items():
            self.track_tree.insert(
                '',
                'end',
                values=(track.name, track.artist, track.rating, track.play_count),
                tags=(track_id,)
            )

    def play_selected_track(self, event):
        # Play the selected track and increment its play count
        if not self.track_tree.selection():
            return
        
        selected_item = self.track_tree.selection()[0]
        track_id = self.track_tree.item(selected_item, "tags")[0]
        track = self.library.tracks[track_id]
        
        track.play_count += 1
        self.update_track_list()
        webbrowser.open(track.youtube_url)
        self.status_label.config(text=f"Playing: {track.name} by {track.artist}")

    # Open the window for adding a new track
    def open_add_track(self):
        add_window = AddTrackWindow(self.root, self.library)
        self.root.wait_window(add_window)
        self.update_track_list()
        self.status_label.config(text="Track added successfully!")

    # Open the window for searching tracks
    def open_find_track(self):
        FindTrackWindow(self.root, self.library)
        self.status_label.config(text="Search mode activated")

    # Open the window for removing a track
    def open_remove_track(self):
        remove_window = RemoveTrackWindow(self.root, self.library)
        self.root.wait_window(remove_window)
        self.update_track_list()
        self.status_label.config(text="Track removed successfully!")

    # Open the window for updating track information
    def open_update_track(self):
        update_window = UpdateTrackWindow(self.root, self.library)
        self.root.wait_window(update_window)
        self.update_track_list()
        self.status_label.config(text="Track updated successfully!")

    # Start the main application loop
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MainApplication()
    app.run()
