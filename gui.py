import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk
import os
import sys
import pyperclip
from url_validator import is_valid_youtube_url
from video_downloader import download_video

class YouTubeDownloaderApp:
    def __init__(self, master):
        self.master = master
        master.title("YouTube Video Downloader")

        # Determine and create base directory if necessary
        self.base_dir = self.determine_base_directory()
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

        # Setup GUI components
        self.setup_gui_components()

        # Attempt to auto-fill URL from clipboard
        self.prefill_url_from_clipboard()

    def determine_base_directory(self):
        # Check if we are running as a frozen application (like a PyInstaller executable)
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Append "downloaded_videos" to the base directory
        downloaded_videos_path = os.path.join(base_dir, "downloaded_videos")
        return downloaded_videos_path

    def setup_gui_components(self):
        # URL Entry
        self.url_label = tk.Label(self.master, text="YouTube Video URL:")
        self.url_label.pack()
        self.url_entry = tk.Entry(self.master, width=50)
        self.url_entry.pack()

        # Download Folder Selection
        self.folder_path = tk.StringVar(value=self.base_dir)
        self.folder_label = tk.Label(self.master, text="Download Folder:")
        self.folder_label.pack()
        self.folder_entry = tk.Entry(self.master, textvariable=self.folder_path, width=50)
        self.folder_entry.pack()
        self.browse_button = tk.Button(self.master, text="Browse", command=self.browse_folder)
        self.browse_button.pack()

        # Download Button
        self.download_button = tk.Button(self.master, text="Download", command=self.initiate_download)
        self.download_button.pack()

        # Status/Error Display
        self.status_display = scrolledtext.ScrolledText(self.master, width=70, height=10)
        self.status_display.pack()

        # Progress Bar
        self.progress_bar = ttk.Progressbar(self.master, orient='horizontal', length=400, mode='determinate')
        self.progress_bar.pack()

        # Bind Enter key to Download button
        self.master.bind('<Return>', self.initiate_download)

        # Focus window
        self.master.lift()
        self.master.focus_force()

    def prefill_url_from_clipboard(self):
        clipboard_content = pyperclip.paste()
        if is_valid_youtube_url(clipboard_content):
            self.url_entry.insert(0, clipboard_content)
            self.display_message(f"URL: {clipboard_content} has been pasted from your clipboard.")

    def browse_folder(self):
        directory = filedialog.askdirectory(initialdir=self.folder_path.get())
        if directory:
            self.folder_path.set(directory)

    def initiate_download(self, event=None):
        url = self.url_entry.get()
        download_folder = self.folder_path.get()

        if not url or not download_folder:
            self.display_message("Please fill in all fields.")
            return

        success, message = download_video(url, download_folder, self.progress_callback)
        self.display_message(message)
        if success:
            self.reset_progress_bar()

    def progress_callback(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        completion = int((bytes_downloaded / total_size) * 100)
        self.update_progress_bar(completion)

    def update_progress_bar(self, value):
        self.progress_bar['value'] = value
        self.master.update_idletasks()

    def reset_progress_bar(self):
        self.progress_bar['value'] = 0

    def display_message(self, message):
        self.status_display.insert(tk.END, message + "\n")
        self.status_display.see(tk.END)

def main():
    root = tk.Tk()
    app = YouTubeDownloaderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
