"""Leo desktop companion for Windows."""

from __future__ import annotations

import ctypes
import math
import os
import sys
import threading
import tkinter as tk
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps, ImageTk
import pystray


APP_NAME = "Leo's Desktop Buddy"
FRAME_COUNT = 6
PET_SIZE = 172
ATTACK_REACH = 78
CATCH_DISTANCE = 112
ESCAPE_DISTANCE = 150
MAX_SPEED = 10.5


def resource_path(relative: str) -> Path:
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    return base / relative


class Point(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]


class LeoPet:
    def __init__(self) -> None:
        if sys.platform != "win32":
            raise RuntimeError("Leo's Desktop Buddy is a Windows app.")

        self.user32 = ctypes.windll.user32
        self.root = tk.Tk()
        self.root.withdraw()
        self.root.title(APP_NAME)
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.configure(bg="#00ff00")
        self.root.wm_attributes("-transparentcolor", "#00ff00")

        self.canvas = tk.Canvas(
            self.root,
            width=PET_SIZE,
            height=PET_SIZE,
            bg="#00ff00",
            bd=0,
            highlightthickness=0,
        )
        self.canvas.pack()
        self.walk_right, self.walk_left = self._load_frames("assets/sprites/leo-walk-v2.png")
        self.fight_right, self.fight_left = self._load_frames("assets/sprites/leo-fight.png")
        self.sprite = self.canvas.create_image(PET_SIZE // 2, PET_SIZE // 2)

        cursor = self._cursor()
        self.x = cursor[0] - PET_SIZE / 2
        self.y = cursor[1] + 30
        self.frame_index = 0
        self.tick_count = 0
        self.facing_right = True
        self.fighting = False
        self.running = True

        self.root.deiconify()
        self.root.update_idletasks()
        self._make_click_through()
        self.tray = self._create_tray()
        threading.Thread(target=self.tray.run, daemon=True).start()
        self._tick()

    def _load_frames(self, filename: str) -> tuple[list[ImageTk.PhotoImage], list[ImageTk.PhotoImage]]:
        sheet = Image.open(resource_path(filename)).convert("RGBA")
        cell_width = sheet.width // FRAME_COUNT
        raw: list[Image.Image] = []
        for index in range(FRAME_COUNT):
            cell = sheet.crop((index * cell_width, 0, (index + 1) * cell_width, sheet.height))
            bbox = cell.getbbox()
            if bbox:
                cell = cell.crop(bbox)
            cell.thumbnail((PET_SIZE - 8, PET_SIZE - 8), Image.Resampling.LANCZOS)
            frame = Image.new("RGBA", (PET_SIZE, PET_SIZE), (0, 0, 0, 0))
            frame.alpha_composite(cell, ((PET_SIZE - cell.width) // 2, PET_SIZE - cell.height - 2))
            raw.append(frame)
        return (
            [ImageTk.PhotoImage(frame) for frame in raw],
            [ImageTk.PhotoImage(ImageOps.mirror(frame)) for frame in raw],
        )

    def _make_click_through(self) -> None:
        hwnd = self.root.winfo_id()
        get_long = self.user32.GetWindowLongW
        set_long = self.user32.SetWindowLongW
        ex_style = get_long(hwnd, -20)
        # WS_EX_LAYERED | WS_EX_TRANSPARENT | WS_EX_TOOLWINDOW | WS_EX_NOACTIVATE
        set_long(hwnd, -20, ex_style | 0x80000 | 0x20 | 0x80 | 0x08000000)

    def _create_tray(self) -> pystray.Icon:
        icon = Image.new("RGBA", (64, 64), (31, 97, 212, 255))
        draw = ImageDraw.Draw(icon)
        draw.rounded_rectangle((8, 8, 56, 56), radius=13, fill=(38, 125, 245, 255))
        draw.ellipse((20, 22, 27, 29), fill="white")
        draw.ellipse((37, 22, 44, 29), fill="white")
        draw.arc((20, 25, 44, 45), 20, 160, fill="white", width=4)
        menu = pystray.Menu(
            pystray.MenuItem("Leo is following your mouse", None, enabled=False),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Exit", self._request_exit),
        )
        return pystray.Icon("leo_desktop_buddy", icon, APP_NAME, menu)

    def _request_exit(self, _icon=None, _item=None) -> None:
        self.running = False
        self.root.after(0, self.root.destroy)
        if self.tray:
            self.tray.stop()

    def _cursor(self) -> tuple[int, int]:
        point = Point()
        self.user32.GetCursorPos(ctypes.byref(point))
        return point.x, point.y

    def _tick(self) -> None:
        if not self.running:
            return

        mouse_x, mouse_y = self._cursor()
        center_x = self.x + PET_SIZE / 2
        center_y = self.y + PET_SIZE / 2
        cursor_dx = mouse_x - center_x
        cursor_dy = mouse_y - center_y
        cursor_distance = math.hypot(cursor_dx, cursor_dy)

        if self.fighting:
            self.fighting = cursor_distance < ESCAPE_DISTANCE
        else:
            self.fighting = cursor_distance < CATCH_DISTANCE

        if not self.fighting and abs(cursor_dx) > 3:
            self.facing_right = cursor_dx > 0

        # Stand just beside and slightly below the pointer so attacks visually
        # connect with it instead of placing the cursor above Leo's head.
        target_center_x = mouse_x - ATTACK_REACH if self.facing_right else mouse_x + ATTACK_REACH
        target_center_y = mouse_y + 28
        dx = target_center_x - center_x
        dy = target_center_y - center_y
        target_distance = math.hypot(dx, dy)
        moving = not self.fighting and target_distance > 7

        if moving:
            speed = min(MAX_SPEED, max(2.2, target_distance * 0.055))
            self.x += dx / target_distance * speed
            self.y += dy / target_distance * speed
            if self.tick_count % 5 == 0:
                self.frame_index = (self.frame_index + 1) % FRAME_COUNT
        elif self.fighting:
            if self.tick_count % 7 == 0:
                self.frame_index = (self.frame_index + 1) % FRAME_COUNT
        else:
            self.frame_index = 1

        # A tiny idle bob keeps Leo feeling alive without being distracting.
        bob = int(math.sin(self.tick_count / 9) * 2) if not moving and not self.fighting else 0
        if self.fighting:
            frames = self.fight_right if self.facing_right else self.fight_left
        else:
            frames = self.walk_right if self.facing_right else self.walk_left
        self.canvas.itemconfigure(self.sprite, image=frames[self.frame_index])
        self.root.geometry(f"{PET_SIZE}x{PET_SIZE}+{round(self.x)}+{round(self.y + bob)}")
        self.root.lift()
        self.tick_count += 1
        self.root.after(16, self._tick)

    def run(self) -> None:
        try:
            self.root.mainloop()
        finally:
            self.running = False
            if getattr(self, "tray", None):
                self.tray.stop()


def already_running() -> bool:
    kernel32 = ctypes.windll.kernel32
    kernel32.CreateMutexW(None, False, "LeoDesktopBuddy_SingleInstance")
    return kernel32.GetLastError() == 183


if __name__ == "__main__":
    if sys.platform == "win32" and not already_running():
        LeoPet().run()
