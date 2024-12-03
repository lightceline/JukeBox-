from tkinter import Tk, Label, Listbox, Button, Scrollbar, Frame, END, VERTICAL, Toplevel, messagebox

def display_tracks_gui(library):
    root = Tk()
    root.title("Track Viewer")
    root.geometry("800x400")
    root.resizable(False, False)

    # Create a frame for the track list
    list_frame = Frame(root, bd=2, relief="groove")
    list_frame.place(x=10, y=10, width=600, height=350)

    Label(list_frame, text="Track List", font=("Arial", 14, "bold")).pack(anchor="n", pady=5)
    scrollbar_y = Scrollbar(list_frame, orient=VERTICAL)
    scrollbar_y.pack(side="right", fill="y")
    tracks_list = Listbox(list_frame, yscrollcommand=scrollbar_y.set, font=("Arial", 12), width=80, height=20)
    tracks_list.pack(fill="both", expand=True)
    scrollbar_y.config(command=tracks_list.yview)

    # Function to display all tracks
    def list_all_tracks():
        tracks_list.delete(0, END)
        for track in library.list_all_tracks():
            tracks_list.insert(END, f"{track['IdTrack']} - {track['nameTrack']} by {track['artist']} (Genre: {track['genre']}, Rating: {track.get('rating', 'N/A')})")


    # Function to display detailed information
    def show_track_details(event):
        selected_index = tracks_list.curselection()
        if selected_index:
            track = library.list_all_tracks()[selected_index[0]]
            details_window = Toplevel(root)
            details_window.title("Track Details")
            details_window.geometry("600x300")
            details = (
                f"ID: {track['IdTrack']}\n"
                f"Name: {track['nameTrack']}\n"
                f"Artist: {track['artist']}\n"
                f"Genre: {track['genre']}\n"
                f"Rating: {track.get('rating', 'N/A')}\n"
                f"File Path / YouTube Link: {track['file_path']}"
            )
            Label(details_window, text=details, font=("Arial", 12), justify="left", padx=10, pady=10).pack()

    # Attach a double-click event to display details
    tracks_list.bind("<Double-Button-1>", show_track_details)

    # Button to list all tracks
    Button(root, text="List All Tracks", font=("Arial", 12), width=15, command=list_all_tracks).place(x=650, y=150)

    root.mainloop()
