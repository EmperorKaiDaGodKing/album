# album

Simple sample app with two shareable folders:
- `/home/runner/work/album/album/sample-app/photos`
- `/home/runner/work/album/album/sample-app/videos`

The sample server listens on `0.0.0.0:8000`, so iOS and Android devices on the same Wi-Fi can connect.

## One step at a time (iPad friendly)
1. Open this repo on GitHub in Microsoft Edge.
2. Open `sample-app/photos` or `sample-app/videos`.
3. Tap **Add file** to upload photo/video files.
4. When you can run code, start server: `python3 /home/runner/work/album/album/sample-app/server.py`.
5. Find your local IP (example: `192.168.1.10`).
6. On iPhone/Android browser, open: `http://YOUR_LOCAL_IP:8000`.

## Notes
- This repo structure can be edited fully from iPad on GitHub.
- Running the server requires a device that can execute Python (computer or cloud runtime).
