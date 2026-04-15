from flask import Flask, Response, request, jsonify, render_template
import cv2
import numpy as np
import threading
import time
import os

app = Flask(__name__)

@app.after_request
def add_cors(response):
    response.headers["Access-Control-Allow-Origin"]  = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

# ─── HSV FILTER DEFINITIONS ─────────────────────────────────────────────────
HSV_FILTERS = {
    "orange":  {"lower": [10,   215,  230], "upper": [ 30, 240, 255]},
    "red":  {"lower": [10,   215,  230], "upper": [ 30, 240, 255]},
    "blue":   {"lower": [90, 200,  255], "upper": [120, 255, 180]},
    "green": {"lower": [  0, 20,  50], "upper": [ 10, 255, 255]},
    "magenta":{"lower": [150, 10,  10], "upper": [179, 255, 255]},
}

# ─── STREAM STATE ────────────────────────────────────────────────────────────
frames      = {}
frames_lock = threading.Lock()

active_filter = list(HSV_FILTERS.keys())[0]

# test-mode state
test_mode        = False   # True = use uploaded still image instead of camera
test_image_frame = None    # BGR ndarray of the uploaded image

# ─── CAMERA / SOURCE THREAD ──────────────────────────────────────────────────
USE_FAKE = not os.path.exists("/dev/video0") and not os.path.exists("/proc/device-tree/model")

def camera_thread():
    if USE_FAKE:
        _fake_camera_loop()
    else:
        _real_camera_loop()

def _fake_camera_loop():
    while True:
        if test_mode and test_image_frame is not None:
            with frames_lock:
                frames["input"] = test_image_frame.copy()
            time.sleep(0.1)
            continue
        h = np.zeros((480, 640, 3), dtype=np.uint8)
        t = time.time()
        for col in range(640):
            hue = int((col / 640 * 180 + t * 20)) % 180
            h[:, col] = [hue, 200, 200]
        bgr = cv2.cvtColor(h, cv2.COLOR_HSV2BGR)
        cv2.circle(bgr, (160, 240), 80, (0, 180, 0), -1)
        cv2.circle(bgr, (320, 240), 80, (200, 100, 0), -1)
        cv2.circle(bgr, (480, 240), 80, (0, 80, 255), -1)
        with frames_lock:
            frames["input"] = bgr.copy()
        time.sleep(0.01)

def _real_camera_loop():
    try:
        from picamera2 import Picamera2
        picam2 = Picamera2()
        picam2.configure(picam2.create_video_configuration(
            main={"format": "RGB888", "size": (1536, 864)} # Lowest resolution, highest framerate
        ))
        picam2.set_controls({"AfMode": 2, "AeEnable": True, "FrameRate": 60}) # Set autofocus mode to continuous and enable auto exposure
        picam2.start()
        while True:
            if test_mode and test_image_frame is not None:
                with frames_lock:
                    frames["input"] = test_image_frame.copy()
                time.sleep(0.1)
                continue
            frame = picam2.capture_array()
            bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            with frames_lock:
                frames["input"] = bgr
            time.sleep(0.01)
    except Exception as e:
        print(f"Camera error: {e}. Falling back to test pattern.")
        _fake_camera_loop()

# ─── MASK GENERATOR THREAD ───────────────────────────────────────────────────
def mask_thread():
    while True:
        with frames_lock:
            src  = frames.get("input")
            filt = HSV_FILTERS.get(active_filter)
        if src is not None and filt is not None:
            hsv  = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
            lo   = np.array(filt["lower"])
            hi   = np.array(filt["upper"])
            mask = cv2.inRange(hsv, lo, hi)
            mask_bgr = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
            overlay  = src.copy()
            overlay[mask > 0] = (overlay[mask > 0] * 0.4 + np.array([0, 200, 0]) * 0.6)
            with frames_lock:
                frames["mask"]    = mask_bgr
                frames["overlay"] = overlay.astype(np.uint8)

        time.sleep(0.01)

# ─── MJPEG STREAMING ─────────────────────────────────────────────────────────
def generate_stream(name):
    while True:
        with frames_lock:
            frame = frames.get(name)
        if frame is not None:
            _, buf = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 75])
            yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n"
                   + buf.tobytes() + b"\r\n")
        time.sleep(0.01)

@app.route("/video/<name>")
def video(name):
    return Response(generate_stream(name),
                    mimetype="multipart/x-mixed-replace; boundary=frame")

# ─── API ENDPOINTS ────────────────────────────────────────────────────────────
@app.route("/api/filters", methods=["GET"])
def get_filters():
    return jsonify(HSV_FILTERS)

@app.route("/api/filters/<name>", methods=["POST"])
def set_filter(name):
    data = request.json
    if name not in HSV_FILTERS:
        HSV_FILTERS[name] = {"lower": [0,0,0], "upper": [179,255,255]}
    HSV_FILTERS[name]["lower"] = data["lower"]
    HSV_FILTERS[name]["upper"] = data["upper"]
    return jsonify({"ok": True})

@app.route("/api/active_filter", methods=["GET","POST"])
def active_filter_ep():
    global active_filter
    if request.method == "POST":
        active_filter = request.json["name"]
        return jsonify({"ok": True})
    return jsonify({"name": active_filter})

@app.route("/api/pixel_hsv", methods=["GET"])
def pixel_hsv():
    x = int(request.args.get("x", 0))
    y = int(request.args.get("y", 0))
    with frames_lock:
        src = frames.get("input")
        
    if src is None:
        return jsonify({"h": 0, "s": 0, "v": 0})
        
    h_img, w_img = src.shape[:2]
    x = max(0, min(x, w_img - 1))
    y = max(0, min(y, h_img - 1))
    
    # PERFORMANCE FIX: Grab the 1-pixel BGR array first, THEN convert it
    pixel_bgr = np.uint8([[src[y, x]]])
    pixel_hsv = cv2.cvtColor(pixel_bgr, cv2.COLOR_BGR2HSV)
    
    h, s, v = pixel_hsv[0, 0]
    return jsonify({"h": int(h), "s": int(s), "v": int(v)})

# ─── TEST MODE ───────────────────────────────────────────────────────────────
@app.route("/api/test_mode", methods=["GET","POST"])
def test_mode_ep():
    global test_mode
    if request.method == "POST":
        test_mode = request.json.get("enabled", False)
        # If disabling and no image is set, just pass; camera loop will take over
        return jsonify({"ok": True, "test_mode": test_mode})
    return jsonify({"test_mode": test_mode})

@app.route("/api/upload_test_image", methods=["POST"])
def upload_test_image():
    global test_image_frame, test_mode
    if "image" not in request.files:
        return jsonify({"ok": False, "error": "No image file"}), 400
    f = request.files["image"]
    data = np.frombuffer(f.read(), dtype=np.uint8)
    img  = cv2.imdecode(data, cv2.IMREAD_COLOR)
    if img is None:
        return jsonify({"ok": False, "error": "Could not decode image"}), 400
    # Resize to reasonable size, keeping aspect ratio
    max_dim = 640
    h, w = img.shape[:2]
    scale = min(max_dim / w, max_dim / h, 1.0)
    if scale < 1.0:
        img = cv2.resize(img, (int(w*scale), int(h*scale)))
    test_image_frame = img
    test_mode = True          # auto-enable test mode on upload
    with frames_lock:
        frames["input"] = test_image_frame.copy()
    return jsonify({"ok": True, "size": [img.shape[1], img.shape[0]]})

# ─── MAIN PAGE ────────────────────────────────────────────────────────────────


@app.route("/")
def index():
    return render_template("index.html")

# ─── STARTUP ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    threading.Thread(target=camera_thread, daemon=True).start()
    threading.Thread(target=mask_thread,   daemon=True).start()
    app.run(host="0.0.0.0", port=5000, threaded=True)
