import argparse
import threading
import ast
from url_validator import is_valid_youtube_url
from video_downloader import download_video

def cli_progress_callback(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    completion = int((bytes_downloaded / total_size) * 100)
    print(f"Download Progress: {completion}%", end='\r')

def parse_url_list(arg_value):
    try:
        urls = ast.literal_eval(arg_value)
        if not isinstance(urls, list) or not all(isinstance(url, str) for url in urls):
            raise ValueError
        return urls
    except (ValueError, SyntaxError) as e:
        raise argparse.ArgumentTypeError(f"\nInvalid URL list format. Please provide a valid Python list of URLs as a string. Error:\n{e}")

def download_wrapper(urls, download_folder, max_threads):
    valid_urls = set()  # Use a set to automatically deduplicate URLs
    invalid_urls = []

    # Validate URLs
    for url in urls:
        if is_valid_youtube_url(url):
            valid_urls.add(url)
        else:
            invalid_urls.append(url)
    
    # Early exit if no valid URLs
    if not valid_urls:
        print("\nNo valid YouTube URLs provided.\n")
        if invalid_urls:
            print("\nInvalid URLs:", ", ".join(invalid_urls))
        return
    
    # Download valid URLs
    semaphore = threading.Semaphore(max_threads)
    threads = []
    
    for url in valid_urls:
        semaphore.acquire()
        t = threading.Thread(target=lambda: download_video_and_release(url, download_folder, semaphore), daemon=True)
        t.start()
        threads.append(t)
        if max_threads == 1:
            t.join()  # Sequential download
    
    # Wait for all threads to complete for concurrent downloads
    if max_threads > 1:
        for t in threads:
            t.join()

    # Report invalid URLs if any
    if invalid_urls:
        print("Unable to download the following invalid URLs:", ", ".join(invalid_urls))

def download_video_and_release(url, download_folder, semaphore):
    try:
        success, message = download_video(url, download_folder, cli_progress_callback)
        print(message)
    finally:
        semaphore.release()

def main():
    parser = argparse.ArgumentParser(description='YouTube Video Downloader CLI')
    parser.add_argument('-u', '--url', type=parse_url_list, required=True, help='YouTube video URLs as a Python list')
    parser.add_argument('-d', '--download_folder', type=str, default='./', help='Download destination directory')
    parser.add_argument('-t', '--threads', type=int, default=1, help='Max number of concurrent downloads')
    args = parser.parse_args()

    download_wrapper(args.url, args.download_folder, args.threads)

if __name__ == "__main__":
    main()

