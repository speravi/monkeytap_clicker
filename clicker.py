import win32api, win32con
import time
import pyautogui
import keyboard
import tkinter as tk
import threading

# Grid config
start_x = 745
start_y = 415
offset = 140
tile_size = 10
target_color = (209, 183, 28)
# target_color = (146, 128, 20)


# Overlay setup
overlay_visible = False
overlay_root = None
overlay_canvas = None

# Click function
def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    time.sleep(0.05)

# Setup overlay window
def init_overlay():
    global overlay_root, overlay_canvas
    overlay_root = tk.Tk()
    overlay_root.title("Overlay")
    overlay_root.attributes('-topmost', True)
    overlay_root.attributes('-alpha', 0.3)
    overlay_root.overrideredirect(True)
    screen_width = overlay_root.winfo_screenwidth()
    screen_height = overlay_root.winfo_screenheight()
    overlay_canvas = tk.Canvas(overlay_root, width=screen_width, height=screen_height, bg='black')
    overlay_canvas.pack()

    for row in range(4):
        for col in range(4):
            x = start_x + col * offset
            y = start_y + row * offset
            overlay_canvas.create_rectangle(
                x, y, x + tile_size, y + tile_size,
                outline='red', width=2
            )

    overlay_root.withdraw()  # Start hidden
    overlay_root.mainloop()

# Toggle visibility without destroying
def toggle_overlay():
    global overlay_visible, overlay_root
    if overlay_root is None:
        return  # Not initialized yet
    if overlay_visible:
        overlay_root.withdraw()
        overlay_visible = False
    else:
        overlay_root.deiconify()
        overlay_visible = True

# Start overlay in background thread
threading.Thread(target=init_overlay, daemon=True).start()

# Listen for key to toggle overlay
def overlay_toggle_listener():
    while True:
        if keyboard.is_pressed('v'):
            toggle_overlay()
            time.sleep(0.4)  # debounce
        time.sleep(0.05)

threading.Thread(target=overlay_toggle_listener, daemon=True).start()

# Main loop – hold SPACE to click
print("Hold SPACE to auto-click. Press 'v' to toggle overlay. Press ESC to quit.")
try:
    while not keyboard.is_pressed('esc'):
        if keyboard.is_pressed('space'):
            for row in range(4):
                for col in range(4):
                    x = start_x + col * offset
                    y = start_y + row * offset
                    try:
                        pixel = pyautogui.pixel(x, y)
                        if pixel == target_color:
                            click(x, y)
                    except Exception:
                        pass  # In case window moves or monitor changes
        else:
            time.sleep(0.05)
except KeyboardInterrupt:
    pass
