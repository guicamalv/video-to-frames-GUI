import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import cv2
import os

class VideoToFramesApp:
    def __init__(self, master):
        self.master = master
        master.title("Video to Frames Converter")
        master.geometry("460x420")
        master.resizable(False, False)

        self.video_path = ""
        self.output_folder = ""
        self.image_format = tk.StringVar(value="jpg")
        self.use_segment = tk.BooleanVar(value=False)

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

        self.segment_check = tk.Checkbutton(master, text="Extract only a segment of the video", variable=self.use_segment, command=self.toggle_segment_fields)
        self.segment_check.pack(pady=5)

        self.segment_frame = tk.Frame(master)
        self.start_label = tk.Label(self.segment_frame, text="Start time (s):")
        self.start_label.grid(row=0, column=0, padx=5)
        self.start_entry = tk.Entry(self.segment_frame, width=10)
        self.start_entry.grid(row=0, column=1, padx=5)

        self.end_label = tk.Label(self.segment_frame, text="End time (s):")
        self.end_label.grid(row=0, column=2, padx=5)
        self.end_entry = tk.Entry(self.segment_frame, width=10)
        self.end_entry.grid(row=0, column=3, padx=5)

        self.skip_frame_label = tk.Label(master, text="Skip every N frames (0 = no skipping):")
        self.skip_frame_label.pack(pady=5)
        self.skip_frame_entry = tk.Entry(master, width=10)
        self.skip_frame_entry.insert(0, "0")
        self.skip_frame_entry.pack()

        self.progress = ttk.Progressbar(master, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=10)

        self.convert_btn = tk.Button(master, text="Convert", command=self.convert_video)
        self.convert_btn.pack(pady=15)

    def toggle_segment_fields(self):
        if self.use_segment.get():
            self.segment_frame.pack(pady=5)
        else:
            self.segment_frame.pack_forget()

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
            skip_n = int(self.skip_frame_entry.get())
            if skip_n < 0:
                raise ValueError("Skip value cannot be negative.")

            cap = cv2.VideoCapture(self.video_path)
            if not cap.isOpened():
                raise ValueError("Unable to open video file.")

            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            start_sec = float(self.start_entry.get()) if self.use_segment.get() else 0
            end_sec = float(self.end_entry.get()) if self.use_segment.get() else float('inf')

            start_frame = int(start_sec * fps)
            end_frame = int(end_sec * fps) if end_sec != float('inf') else total_frames

            cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
            frame_count = start_frame
            image_count = 0
            ext = self.image_format.get().lower()

            self.progress["maximum"] = end_frame - start_frame

            while cap.isOpened():
                if frame_count > end_frame:
                    break
                ret, frame = cap.read()
                if not ret:
                    break

                if skip_n == 0 or (image_count % (skip_n + 1)) == 0:
                    filename = os.path.join(self.output_folder, f"frame_{image_count:05d}.{ext}")
                    cv2.imwrite(filename, frame)

                image_count += 1
                frame_count += 1
                self.progress["value"] = frame_count - start_frame
                self.master.update_idletasks()

            cap.release()
            messagebox.showinfo("Success", f"Processed {image_count} frames with skip = {skip_n}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoToFramesApp(root)
    root.mainloop()
