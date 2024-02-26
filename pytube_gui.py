import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk
from pytube import YouTube

class YouTubeDownloaderApp:
    def __init__(self, master):
        self.master = master
        master.title("YouTube Video Downloader")

        # URL Entry
        self.url_label = tk.Label(master, text="YouTube Video URL:")
        self.url_label.pack()
        self.url_entry = tk.Entry(master, width=50)
        self.url_entry.pack()

        # Download Folder Selection
        self.folder_path = tk.StringVar()
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

    def browse_folder(self):
        self.folder_path.set(filedialog.askdirectory())

    def download_video(self):
        url = self.url_entry.get()
        download_folder = self.folder_path.get()

        if not url or not download_folder:
            self.status_display.insert(tk.END, "Please fill in all fields.\n")
            return

        try:
            yt = YouTube(url, on_progress_callback=self.progress_callback)
            video = yt.streams.get_highest_resolution()
            self.status_display.insert(tk.END, f"Starting download of '{yt.title}'\n")
            video.download(download_folder)
            self.status_display.insert(tk.END, f"Downloaded '{yt.title}' successfully to {download_folder}\n")
            self.progress_bar['value'] = 0  # Reset progress bar after download
        except Exception as e:
            self.status_display.insert(tk.END, f"Error occurred: {e}\n")

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
