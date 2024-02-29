from pytube import YouTube
import os

def download_video(url, download_folder, on_progress_callback):
    """Download a YouTube video to the specified folder."""
    try:
        yt = YouTube(url, on_progress_callback=on_progress_callback)
        video = yt.streams.get_highest_resolution()
        download_path = os.path.join(download_folder, video.default_filename)
        print("Starting download for {video.title} to {download_folder}.")

        # Check if the file already exists to avoid re-downloading
        if os.path.exists(download_path):
            return False, f"'{video.title}' already exists in the specified folder."

        # Download the video
        video.download(download_folder)
        return True, f"Downloaded '{video.title}' successfully to {download_folder}{video.title}.mp4"

    except Exception as e:
        return False, f"An error occurred during the download: {e}"

