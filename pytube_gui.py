import os
import pyperclip
import re
import sys
import threading
import tkinter as tk
#if i fit i sit ^

# https://www.youtube.com/watch?v=LJxF-i0kvPM

from tkinter import filedialog, scrolledtext, ttk
from pytube import YouTube

class YouTubeDownloaderApp:
    """Class to house the functionality of the Application Window"""
    def __init__(self, master):
        self.master = master
        master.title("YouTube Video Downloader")
        # Define the base directory based on whether the app is frozen
        if getattr(sys, 'frozen', False):
            #as an executable
            base_dir = os.path.dirname(sys.executable)
        else:
            #as a script
            base_dir = os.path.dirname(os.path.abspath(__file__))

        # URL Entry
        self.url_label = tk.Label(master, text="YouTube Video URL:")
        self.url_label.pack()
        self.url_entry = tk.Entry(master, width=50)
        self.url_entry.pack()

        # Download Folder Selection
        self.folder_path = tk.StringVar()
        self.folder_path.set(base_dir)
        self.folder_label = tk.Label(master, text="Download Folder:")
        self.folder_label.pack()
        self.folder_entry = tk.Entry(master, textvariable=self.folder_path, width=50)
        self.folder_entry.pack()
        self.browse_button = tk.Button(master, text="Browse", command=self.browse_folder)
        self.browse_button.pack()

        # Download Button
        self.download_button = tk.Button(master, text="Download", command=self.download_video)
        self.download_button.pack()

        # Status/Error Display
        self.status_display = scrolledtext.ScrolledText(master, width=70, height=10)
        self.status_display.pack()

        # Progress Bar (Make sure to use ttk.Progressbar for styling compatibility)
        self.progress_bar = ttk.Progressbar(master, orient='horizontal', length=400, mode='determinate')
        self.progress_bar.pack()

        # Bind the enter key to the Download button
        self.master.bind('<Return>', self.download_video)

        # Attempt to force window focus when running the script or executable
        master.lift() # bring to the front
        master.focus_force() #focus the window//jedi powers



        clipboard_content = pyperclip.paste()

        if self. is_valid_youtube_url(clipboard_content):
            self.url_entry.insert(0, clipboard_content)
            self.status_display.insert(tk.END, f"\n\nURL: {clipboard_content}. Imported successfully. Hit Enter or Download to Begin Downloading")
        else:
            self.status_display.insert(tk.END, "\n\nCould not import valid YouTube URL from clipboard, you can prefill the URL by copying the valid 'youtube | youtu.be' link before launching the program, this is optional and just a helpful tip.\n\n Enter your URL above and click Download or Hit Enter to Begin Downloading..")

    def is_valid_youtube_url(self, url):
        """This was fun to learn and you should try too\n
Although I wouldn't wish regex on my worst enemies."""
        youtube_regex = (
            r'(https?://)?(www\.)?'
            '(youtube|youtu|youtube-nocookie)\.(com|be)/'
            '(watch\?v=embed/|v/|.+\?v=)?([^&=%\?]{11})')
        return re.match(youtube_regex, url) is not None

    def browse_folder(self):
        """Opens a dialog for the user to select a new download directory."""
        # Use the current folder path as the initial directory in the dialog
        initial_directory = self.folder_path.get()

        # Open the file dialog starting from the initial directory
        directory = filedialog.askdirectory(initialdir=initial_directory)

        # Update the folder path if a new directory was selected
        if directory:
            self.folder_path.set(directory)


    def download_video(self, event=None):
        self.status_display.insert(tk.END, "\n\nDownload button clicked. Verifying Runtime.")
        self.status_display.see(tk.END)  # Auto-scroll to the end
        self.master.update_idletasks()  # Force the GUI to update

        # Start the download in a separate thread
        threading.Thread(target=self.start_download, daemon=True).start()

    def start_download(self):
        url = self.url_entry.get()
        download_folder = self.folder_path.get()

        if not url or not download_folder:
            self.status_display.insert(tk.END, "\n\nPlease fill in all fields.\n\n")
            return

        try:
            yt = YouTube(url, on_progress_callback=self.progress_callback)
            video = yt.streams.get_highest_resolution()

            download_path = os.path.join(download_folder, video.default_filename)
            
            # Check if the file already exists
            if os.path.exists(download_path):
                self.status_display.insert(tk.END, f"\n\n'{video.title}' already downloaded and exists in the specified folder.\n\n")
                return

            # Ensure GUI updates happen from the main thread
            self.status_display.insert(tk.END, f"\n\nDownload is starting, use the progress bar below to monitor your progress '{yt.title}'")

            self.status_display.see(tk.END)  # Auto-scroll to the end

            video.download(download_folder)

            self.status_display.insert(tk.END, f"\n\nDownloaded '{yt.title}' successfully to {download_folder}\n\n")

            self.progress_bar['value'] = 0  # Reset progress bar after download

        except Exception as e:
            self.status_display.insert(tk.END, f"Error occurred: {e}\n\n")

        # Ensure these GUI updates are visible immediately
        self.status_display.see(tk.END)  # Auto-scroll to the end
        self.master.update_idletasks()

    def progress_callback(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        completion = int((bytes_downloaded / total_size) * 100)
        self.progress_bar['value'] = completion  # Update the progress bar
        self.master.update_idletasks()  # Update the GUI

def main():
    root = tk.Tk()
    app = YouTubeDownloaderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

