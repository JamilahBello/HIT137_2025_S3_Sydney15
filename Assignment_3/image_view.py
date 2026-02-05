import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk


class ImageView:
    def __init__(self, controller):
        self.controller = controller

        self.root = tk.Tk()
        self.root.title("Image Editor Group 15 Syd")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)

        # Tk variables (sliders)
        self.brightness_var = tk.DoubleVar(value=1.0)
        self.contrast_var = tk.DoubleVar(value=1.0)
        self.blur_var = tk.DoubleVar(value=0)

        # Widgets need later
        self.canvas = None
        self.status_bar = None
        self.display_photo = None
        self.image_info_label = None

        # Build UI
        self.create_menu()
        self.create_canvas()
        self.create_controls()
        self.create_status_bar()

    # ==================== FILE OPERATIONS ====================

    def open_image(self):  # [4]
        """Open an image file"""
        file_path = filedialog.askopenfilename(
            title="Open Image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp"),
                ("JPEG", "*.jpg *.jpeg"),
                ("PNG", "*.png"),
                ("BMP", "*.bmp"),
            ],
        )

        try:
            self.controller.open(file_path)

            self.brightness_var.set(1.0)
            self.contrast_var.set(1.0)
            self.blur_var.set(0)

            self.refresh_image()
            self.update_status(f"Loaded: {file_path}")
            messagebox.showinfo("Success, Image loaded successfully!")
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Could not open image, file type may be corrupted or unsupported file type:\n{str(e)}",
            )

    def save_image(self):
        # [4]
        """Save to current file"""
        if self.controller.get_display_pil() is None:
            messagebox.showwarning("Warning", "No image found.")
            return

        try:
            self.controller.save()
            messagebox.showinfo("Success", "Image saved!")
            self.update_status(f"Saved")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save:\n{str(e)}")

    def save_as(self):
        # [4]
        """Save to new file"""
        if self.controller.get_display_pil() is None:
            messagebox.showwarning("Warning", "No image found.")
            return
        try:
            self.controller.save()
            messagebox.showinfo("Success", "Image saved!")
            self.update_status(f"Saved")

            file_path = filedialog.askopenfilename(
                title="Open Image",
                filetypes=[
                    ("Image files", "*.jpg *.jpeg *.png *.bmp"),
                    ("JPEG", "*.jpg *.jpeg"),
                    ("PNG", "*.png"),
                    ("BMP", "*.bmp"),
                ],
            )

            if not file_path:
                return
            self.controller.save_as(file_path)
            messagebox.showinfo("Success", "Image saved!")
            self.update_status(f"Saved: {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save:\n{str(e)}")

    def exit_app(self):
        """Exit with confirmation"""
        if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
            self.root.quit()

    def undo(self):
        if self.controller.get_display_pil() is None:
            messagebox.showwarning("Warning", "No image found.")
            return
        self.controller.undo()
        self.refresh_image()
        self.update_status("Undo")  # [5]

    def redo(self):
        if self.controller.get_display_pil() is None:
            messagebox.showwarning("Warning", "No image found.")
            return
        self.controller.redo()
        self.refresh_image()
        self.update_status("Redo")  # [5]

    def apply_reset_image(self):
        """Reset to original image"""
        if self.controller.get_display_pil() is None:
            messagebox.showwarning("Warning", "No image found.")
            return

        if messagebox.askyesno("Reset", "Reset to original image?"):
            self.controller.reset()
            self.brightness_var.set(1.0)
            self.contrast_var.set(1.0)
            self.blur_var.set(0)
            self.refresh_image()
            self.refresh_details()
            self.update_status("Reset to original")  # [6]

    def refresh_image(self):
        """PULL PIL disp;ay image from controller and draw it"""
        pil_img = self.controller.get_display_pil()
        if pil_img is None:
            self.update_status("No image to display")
            return

        # Resize to fit canvas (keep aspect ratio)
        img = pil_img.copy()
        img.thumbnail((580, 580), Image.Resampling.LANCZOS)

        # Convert to PhotoImage
        self.display_photo = ImageTk.PhotoImage(img)

        # Clear canvas and show image
        self.canvas.delete("all")
        self.canvas.create_image(300, 300, image=self.display_photo, anchor=tk.CENTER)

        size = self.controller.get_size()
        if size:
            w, h = size
            self.update_status(f"Size: {w}x{h} pixels")  # [5]

    def update_status(self, message):
        """Update status bar"""
        if self.status_bar is None:
            return
        self.status_bar.config(text=message)

    # ==================== FILTERS ====================

    def apply_grayscale(self):
        if self.controller.get_display_pil() is None:
            messagebox.showwarning("Warning", "No image found.")
            return

        self.controller.grayscale()
        self.refresh_image()

    def update_blur(self, value):
        if self.controller.get_display_pil() is None:
            messagebox.showwarning("Warning", "No image found.")
            return
        intensity = int(float(value))
        self.controller.blur(intensity)
        self.refresh_image()

    def apply_edge_detection(self):
        if self.controller.get_display_pil() is None:
            messagebox.showwarning("Warning", "No image found.")
            return

        self.controller.canny_edges()
        self.refresh_image()

    def apply_rotate_90(self):
        if self.controller.get_display_pil() is None:
            messagebox.showwarning("Warning", "No image found.")
            return

        self.controller.rotate(90)
        self.refresh_image()

    def apply_rotate_180(self):
        if self.controller.get_display_pil() is None:
            messagebox.showwarning("Warning", "No image found.")
            return

        self.controller.rotate(180)
        self.refresh_image()

    def apply_rotate_270(self):
        if self.controller.get_display_pil() is None:
            messagebox.showwarning("Warning", "No image found.")
            return

        self.controller.rotate(270)
        self.refresh_image()

    def apply_flip_x(self):
        if self.controller.get_display_pil() is None:
            messagebox.showwarning("Warning", "No image found.")
            return

        self.controller.flip(1)
        self.refresh_image()

    def apply_flip_y(self):
        if self.controller.get_display_pil() is None:
            messagebox.showwarning("Warning", "No image found.")
            return

        self.controller.flip(0)
        self.refresh_image()

    def update_brightness(self, value):
        if self.controller.get_display_pil() is None:
            messagebox.showwarning("Warning", "No image found.")
            return
        v = float(value)
        beta = int((v - 1.0) * 100)
        self.controller.brightness(beta)
        self.refresh_image()

    def update_contrast(self, value):
        if self.controller.get_display_pil() is None:
            messagebox.showwarning("Warning", "No image found.")
            return
        alpha = float(value)
        self.controller.contrast(alpha)
        self.refresh_image()

    def refresh_details(self):
        if self.image_info_label is None:
            return

        try:
            details = self.controller.get_details()
        except ValueError:
            details = "No image loaded"
        self.image_info_label.config(text=details)

    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)  # [1]
        file_menu.add_command(label="Open", command=self.open_image)
        file_menu.add_command(label="Save", command=self.save_image)
        file_menu.add_command(label="Save As", command=self.save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_app)

        # Edit Menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)

        edit_menu.add_command(label="Undo", command=self.undo)
        edit_menu.add_command(label="Redo", command=self.redo)

    def create_canvas(self):
        """Create image display area"""
        # Frame for canvas
        canvas_frame = tk.Frame(self.root, bg="#1b1b1b")
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Canvas for image
        self.canvas = tk.Canvas(
            canvas_frame,
            bg="#1b1b1b",
            width=600,
            height=600,
            highlightthickness=2,
            highlightbackground="#444",
        )
        self.canvas.pack(padx=10, pady=10)

        # Placeholder text
        self.canvas.create_text(
            300,
            300,
            text="Open an image\n(File → Open)",
            fill="white",
            font=("Arial", 14),
        )  # [1]

    def create_controls(self):
        """Create control panel with buttons and slider"""
        global brightness_variable, brightness_slider, brightness_label

        # Right panel
        control_frame = tk.Frame(self.root, width=250, bg="#52514b")
        control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        control_frame.pack_propagate(False)

        # === FILTERS ===
        tk.Label(
            control_frame,
            text="Image Controls",
            font=("Segoe UI", 11),
            bg="#52514b",
            fg="white",
        ).pack(pady=5)

        # undo_redo_frame = tk.Frame(control_frame, bg="#2d2d2d")
        # undo_redo_frame.pack(pady=6)

        # # Undo button
        # tk.Button(
        #     undo_redo_frame,
        #     text="Undo",
        #     font=("Segoe UI", 10),
        #     bg="#3a3a3a",
        #     fg="white",
        #     command=self.undo,
        #     activebackground="#080807",
        #     activeforeground="white",
        #     relief="flat",
        #     height=2,
        #     width=9,
        # ).pack(side=tk.LEFT, padx=5) # [2]

        # # Redo button
        # tk.Button(
        #     undo_redo_frame,
        #     text="Redo",
        #     font=("Segoe UI", 10),
        #     bg="#3a3a3a",
        #     fg="white",
        #     command=self.redo,
        #     activebackground="#080807",
        #     activeforeground="white",
        #     relief="flat",
        #     height=2,
        #     width=9,
        # ).pack(side=tk.LEFT, padx=5)

        # tk.Button(text="↶ Undo", command=undo).pack(side=tk.LEFT, padx=2)
        # tk.Button(text="↷ Redo", command=redo).pack(side=tk.LEFT, padx=2)

        tk.Button(
            control_frame,
            text="Grayscale Conversion",
            font=("Segoe UI", 10),
            bg="#3a3a3a",
            fg="white",
            command=self.apply_grayscale,
            activebackground="#080807",
            activeforeground="white",
            relief="flat",
            height=2,
            width=20,
        ).pack(
            pady=3
        )  # [2]

        tk.Button(
            control_frame,
            text="Edge Detection",
            font=("Segoe UI", 10),
            bg="#3a3a3a",
            fg="white",
            command=self.apply_edge_detection,
            activebackground="#080807",
            activeforeground="white",
            relief="flat",
            height=2,
            width=20,
        ).pack(
            pady=3
        )  # [2]

        tk.Button(
            control_frame,
            text="Rotate 90°",
            font=("Segoe UI", 10),
            bg="#3a3a3a",
            fg="white",
            command=self.apply_rotate_90,
            activebackground="#080807",
            activeforeground="white",
            relief="flat",
            height=2,
            width=20,
        ).pack(
            pady=3
        )  # [2]
        tk.Button(
            control_frame,
            text="Rotate 180°",
            font=("Segoe UI", 10),
            bg="#3a3a3a",
            fg="white",
            command=self.apply_rotate_180,
            activebackground="#080807",
            activeforeground="white",
            relief="flat",
            height=2,
            width=20,
        ).pack(
            pady=3
        )  # [2]

        tk.Button(
            control_frame,
            text="Rotate 270°",
            font=("Segoe UI", 10),
            bg="#3a3a3a",
            fg="white",
            command=self.apply_rotate_270,
            activebackground="#080807",
            activeforeground="white",
            relief="flat",
            height=2,
            width=20,
        ).pack(
            pady=3
        )  # [2]

        tk.Button(
            control_frame,
            text="Flip Horizontal",
            font=("Segoe UI", 10),
            bg="#3a3a3a",
            fg="white",
            command=self.apply_flip_x,
            activebackground="#080807",
            activeforeground="white",
            relief="flat",
            height=2,
            width=20,
        ).pack(
            pady=3
        )  # [2]

        tk.Button(
            control_frame,
            text="Flip vertical",
            font=("Segoe UI", 10),
            bg="#3a3a3a",
            fg="white",
            command=self.apply_flip_y,
            activebackground="#080807",
            activeforeground="white",
            relief="flat",
            height=2,
            width=20,
        ).pack(
            pady=3
        )  # [2]

        # Separator

        # === BRIGHTNESS SLIDER ===
        tk.Label(
            control_frame,
            text="Brightness",
            font=("Segoe UI", 10),
            bg="#52514b",
            fg="white",
        ).pack(
            pady=5
        )  # [2]

        brightness_slider = tk.Scale(
            control_frame,
            from_=0.0,
            to=2.0,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            variable=self.brightness_var,
            command=self.update_brightness,
            length=200,
            # Styling
            bg="#2d2d2d",
            fg="white",
            troughcolor="#444444",
            activebackground="#f5de0c",
            highlightthickness=0,
            bd=0,
            relief="flat",
            showvalue=False,
        )
        brightness_slider.pack(pady=(10, 4))  # [1]

        brightness_label = tk.Label(
            control_frame, text="1.0", bg="#2d2d2d", fg="white", font=("Segoe UI", 9)
        )

        tk.Label(
            control_frame,
            text="Contrast",
            font=("Segoe UI", 10),
            bg="#52514b",
            fg="white",
        ).pack(pady=5)

        contrast_slider = tk.Scale(
            control_frame,
            from_=0.0,
            to=2.0,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            variable=self.contrast_var,
            command=self.update_contrast,
            length=200,
            # Styling
            bg="#2d2d2d",
            fg="white",
            troughcolor="#444444",
            activebackground="#f5de0c",
            highlightthickness=0,
            bd=0,
            relief="flat",
            showvalue=False,
        )
        contrast_slider.pack(pady=(10, 4))

        tk.Label(
            control_frame,
            text="Blur",
            font=("Segoe UI", 10),
            bg="#52514b",
            fg="white",
        ).pack(pady=5)

        blur_slider = tk.Scale(
            control_frame,
            from_=0.0,
            to=2.0,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            variable=self.blur_var,
            command=self.update_blur,
            length=200,
            # Styling
            bg="#2d2d2d",
            fg="white",
            troughcolor="#444444",
            activebackground="#f5de0c",
            highlightthickness=0,
            bd=0,
            relief="flat",
            showvalue=False,
        )
        blur_slider.pack(pady=(10, 4))

        info_frame = tk.Frame(control_frame, bg="#2d2d2d")
        info_frame.pack(fill=tk.X, padx=10, pady=(15, 5))

        # need to add a function calling
        image_info_label = tk.Label(
            info_frame,
            text=self.refresh_details(),
            justify=tk.LEFT,
            anchor="w",
            font=("Segoe UI", 9),
            bg="#2d2d2d",
            fg="#dddddd",
            padx=10,
            pady=8,
        )
        image_info_label.pack(fill=tk.X)

        # Reset button
        tk.Button(
            control_frame,
            text="Reset to Original",
            font=("Segoe UI", 10),
            bg="#3a3a3a",
            fg="white",
            command=self.apply_reset_image,
            activebackground="#f5de0c",
            activeforeground="white",
            relief="flat",
            height=2,
            width=20,
        ).pack(pady=5)

    def create_status_bar(self):
        """Create status bar at bottom"""
        status_bar = tk.Label(
            self.root,
            text="No image loaded",
            justify=tk.LEFT,
            anchor="w",
            font=("Segoe UI", 9),
            bg="#2d2d2d",
            fg="#dddddd",
            padx=10,
            pady=8,
        )
        status_bar.pack(side=tk.TOP, fill=tk.X)

    def run(self):
        self.root.mainloop()
