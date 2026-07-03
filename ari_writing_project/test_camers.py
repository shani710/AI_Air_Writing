import cv2

print("Testing cameras with different backends...")

# Try different backends
backends = [
    ('DEFAULT', cv2.CAP_ANY),
    ('DSHOW', cv2.CAP_DSHOW),  # DirectShow - best for Windows
    ('MSMF', cv2.CAP_MSMF),    # Media Foundation
]

for backend_name, backend in backends:
    print(f"\n--- Testing with {backend_name} backend ---")
    for i in range(3):
        try:
            cap = cv2.VideoCapture(i, backend)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret and frame is not None:
                    print(f"✓ Camera {i} WORKS with {backend_name} backend!")
                    cap.release()
                    break
                else:
                    print(f"  Camera {i} opens but no frame")
            else:
                print(f"  Camera {i} not available")
            cap.release()
        except Exception as e:
            print(f"  Camera {i} error: {e}")