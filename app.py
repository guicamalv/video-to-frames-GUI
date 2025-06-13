import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import os

class VideoToFramesApp:
    def __init__(self, master):
        self.master = master
        master.title("Video to Frames Converter")
        master.geometry("400x250")
        master.resizable(False, False)

        self.video_path = ""
        self.output_folder = ""
        self.image_format = tk.StringVar(value="jpg")

        self.label = tk.Label(master, text="Convert video to frames", font=("Arial", 14))
        self.label.pack(pady=10)

        self.select_video_btn = tk.Button(master, text="Select Video", command=self.select_video)
        self.select_video_btn.pack(pady=5)

        self.select_output_btn = tk.Button(master, text="Select Output Folder", command=self.select_output)
        self.select_output_btn.pack(pady=5)

        self.format_label = tk.Label(master, text="Select image format:")
        self.format_label.pack(pady=5)

        self.radio_jpg = tk.Radiobutton(master, text="JPG (smaller, lossy)", variable=self.image_format, value="jpg")
        self.radio_png = tk.Radiobutton(master, text="PNG (larger, lossless)", variable=self.image_format, value="png")
        self.radio_jpg.pack()
        self.radio_png.pack()

        self.convert_btn = tk.Button(master, text="Convert", command=self.convert_video)
        self.convert_btn.pack(pady=10)

    def select_video(self):
        self.video_path = filedialog.askopenfilename(
            filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv")]
        )
        if self.video_path:
            messagebox.showinfo("Video Selected", f"Selected:\n{self.video_path}")

    def select_output(self):
        self.output_folder = filedialog.askdirectory()
        if self.output_folder:
            messagebox.showinfo("Output Folder Selected", f"Saving frames to:\n{self.output_folder}")

    def convert_video(self):
        if not self.video_path or not self.output_folder:
            messagebox.showerror("Missing Info", "Please select both a video file and an output folder.")
            return

        try:
            cap = cv2.VideoCapture(self.video_path)
            if not cap.isOpened():
                raise ValueError("Unable to open video file.")

            frame_count = 0
            ext = self.image_format.get().lower()
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                frame_filename = os.path.join(self.output_folder, f"frame_{frame_count:05d}.{ext}")
                cv2.imwrite(frame_filename, frame)
                frame_count += 1

            cap.release()
            messagebox.showinfo("Success", f"Extracted {frame_count} frames as .{ext.upper()} files.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoToFramesApp(root)
    root.mainloop()
