#!/usr/bin/env python3
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import quote
import json

BASE_DIR = Path(__file__).resolve().parent
PHOTOS_DIR = BASE_DIR / "photos"
VIDEOS_DIR = BASE_DIR / "videos"
IMAGE_EXTENSIONS = {".avif", ".gif", ".heic", ".heif", ".jpeg", ".jpg", ".png", ".webp"}
VIDEO_EXTENSIONS = {".m4v", ".mov", ".mp4", ".mpeg", ".mpg", ".webm"}


class AlbumHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_GET(self):
        if self.path == "/api/photos":
            self._json_list(PHOTOS_DIR)
            return
        if self.path == "/api/videos":
            self._json_list(VIDEOS_DIR)
            return
        super().do_GET()

    def _json_list(self, directory: Path):
        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)
        items = [
            self._serialize_media_item(directory, item)
            for item in sorted(directory.rglob("*"))
            if item.is_file() and not item.name.startswith(".")
        ]
        body = json.dumps({"items": items}).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _serialize_media_item(self, root: Path, item: Path):
        relative_path = item.relative_to(root).as_posix()
        suffix = item.suffix.lower()
        if suffix in IMAGE_EXTENSIONS:
            kind = "image"
        elif suffix in VIDEO_EXTENSIONS:
            kind = "video"
        else:
            kind = "file"

        return {
            "name": item.name,
            "path": relative_path,
            "url": f"/{root.name}/{quote(relative_path)}",
            "kind": kind,
        }


def main():
    # Local testing defaults: 0.0.0.0 + open CORS allow iOS/Android devices on same network.
    host = "0.0.0.0"
    port = 8000
    server = ThreadingHTTPServer((host, port), AlbumHandler)
    print(f"Server running at http://{host}:{port}")
    print("On iPhone/Android, open http://<your-local-ip>:8000")
    print("Press Ctrl+C to stop")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
