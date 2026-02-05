#!/usr/bin/env python3
"""
Simple Image Editor - Functions Only (No Classes)
All requirements met with simple functions
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageFilter, ImageEnhance


# Store images at first there will be no image so we need to make them null
original_photo = None
current_photo = None
display_image = None
filepath = None

# Undo/Redo lists
undo_list = []
redo_list = []

# GUI widgets (we need to access them from different functions)
root = None
canvas = None
status_bar = None
brightness_slider = None
brightness_variable = None
brightness_label = None

contrast_slider =None
contrast_label = None
contrast_variable = None
brightness_var=None

# ==================== FILE OPERATIONS ====================

def open_image():
    """Open an image file"""
    global original_photo, current_photo, filepath, undo_list, redo_list

    file_path = filedialog.askopenfilename(
        title="Open Image",
        filetypes=[
            ("Image files", "*.jpg *.jpeg *.png *.bmp"),
            ("JPEG", "*.jpg *.jpeg"),
            ("PNG", "*.png"),
            ("BMP", "*.bmp"),
            ("All files", "*.*")
        ]
    )

    if file_path:
        try:
            # Load image
            original_photo = Image.open(file_path)
            current_photo = original_photo.copy()
            filepath = file_path

            # Clear undo/redo
            undo_list.clear()
            redo_list.clear()

            # Reset brightness slider
            #brightness_var.set(1.0)

            # Display
            display_image()
            update_status(f"Loaded: {file_path}")

            messagebox.showinfo( "Success","Image loaded successfully!")

        except Exception as e:
            messagebox.showerror("Error",f"Could not open image, file type may be corrupted or unsupported file type:\n{str(e)}")


def save_image():
    """Save to current file"""
    global current_photo, filepath

    if current_photo is None:
        messagebox.showwarning("Warning", "No image found.")
        return

    if filepath is None:
        save_as()
        return

    try:
        current_photo.save(filepath)
        messagebox.showinfo("Success", "Image saved!")
        update_status(f"Saved: {filepath}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not save:\n{str(e)}")


def save_as():
    """Save to new file"""
    global current_photo, filepath

    if current_photo is None:
        messagebox.showwarning("Warning", "No image found!")
        return

    file_path = filedialog.asksaveasfilename(
        title="Save Image As",
        defaultextension=".png",
        filetypes=[
            ("PNG", "*.png"),
            ("JPEG", "*.jpg"),
            ("BMP", "*.bmp"),
            ("All files", "*.*")
        ]
    )

    if file_path:
        try:
            current_photo.save(file_path)
            filepath = file_path
            messagebox.showinfo("Success", "Image saved!")
            update_status(f"Saved: {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save:\n{str(e)}")


def exit_app():
    """Exit with confirmation"""
    if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
        root.quit()


# ==================== UNDO/REDO ====================

def save_for_undo():
    """Save current state before making changes"""
    global current_photo, undo_list, redo_list

    if current_photo:
        undo_list.append(current_photo.copy())
        redo_list.clear()


def undo():
    """Undo last action"""
    global current_photo, undo_list, redo_list

    if not undo_list:
        messagebox.showinfo("Undo", "Nothing to undo")
        return

    # Save current to redo
    redo_list.append(current_photo.copy())

    # Restore previous
    current_photo = undo_list.pop()
    display_image()
    update_status("Undo")


def redo():
    """Redo last undo"""
    global current_photo, undo_list, redo_list

    if not redo_list:
        messagebox.showinfo("Redo", "Nothing to redo")
        return

    # Save current to undo
    undo_list.append(current_photo.copy())

    # Restore redo
    current_photo = redo_list.pop()
    display_image()
    update_status("Redo")


def apply_reset_image():
    """Reset to original image"""
    global original_photo, current_photo

    if original_photo is None:
        messagebox.showwarning("Warning", "No image loaded!")
        return

    if messagebox.askyesno("Reset", "Reset to original image?"):
        save_for_undo()
        original_photo = original_photo.copy()
        brightness_var.set(1.0)
        display_image()
        update_status("Reset to original")


# ==================== DISPLAY ====================

def display_image():
    """Show image on canvas"""
    global current_photo, display_photo, canvas

    if current_photo is None:
        return

    # Resize to fit canvas (keep aspect ratio)
    img = current_photo.copy()
    img.thumbnail((580, 580), Image.Resampling.LANCZOS)

    # Convert to PhotoImage
    display_photo = ImageTk.PhotoImage(img)

    # Clear canvas and show image
    canvas.delete("all")
    canvas.create_image(300, 300, image=display_photo, anchor=tk.CENTER)

    # Update status
    w, h = current_photo.size
    update_status(f"Size: {w}×{h} pixels")


def update_status(message):
    """Update status bar"""
    status_bar.config(text=message)


# ==================== FILTERS ====================

def apply_blur():
    pass



def apply_sharpen():
    pass


def apply_emboss():
    pass


# ==================== BRIGHTNESS SLIDER ====================

def update_brightness(value):
    pass
def update_contrast(value):
    pass

def apply_grayscale():
    pass

def apply_edge_detection():
    pass

def apply_brightness_adjustment():
    pass
def rotate_90():
    pass


def apply_flip_horizontal():
    pass

def apply_flip_vertical():
    pass

def apply_rotate_90():
    pass

def apply_rotate_180():
    pass

def apply_rotate_270():
    pass


def get_details():
    pass
# ==================== GUI SETUP ====================

def create_menu():
    """Create menu bar"""
    menubar = tk.Menu(root)
    root.config(menu=menubar)

    # File Menu
    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Open", command=open_image)
    file_menu.add_command(label="Save", command=save_image)
    file_menu.add_command(label="Save As", command=save_as)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=exit_app)

    # Edit Menu
    edit_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Edit", menu=edit_menu)

    # edit_menu.add_command(label="Undo", command=undo)
    # edit_menu.add_command(label="Redo", command=redo)


def create_canvas():
    """Create image display area"""
    global canvas

    # Frame for canvas
    canvas_frame = tk.Frame(root, bg='#1b1b1b')
    canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Canvas for image
    canvas = tk.Canvas(canvas_frame, bg='#1b1b1b', width=600, height=600,highlightthickness=2,
    highlightbackground="#444")
    canvas.pack(padx=10, pady=10)

    # Placeholder text
    canvas.create_text(
        300, 300,
        text="Open an image\n(File → Open)",
        fill='white',
        font=('Arial', 14)
    )




def create_controls():
    """Create control panel with buttons and slider"""
    global brightness_variable, brightness_slider, brightness_label

    # Right panel
    control_frame = tk.Frame(root, width=250, bg='#52514b')
    control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
    control_frame.pack_propagate(False)

    # === FILTERS ===
    tk.Label(
        control_frame,
        text="Image Controls",
        font=('Segoe UI', 11),
        bg='#52514b',
        fg='white'
    ).pack(pady=5)

    undo_redo_frame = tk.Frame(control_frame, bg="#2d2d2d")
    undo_redo_frame.pack(pady=6)

    # Undo button
    tk.Button(
        undo_redo_frame,
        text="Undo",
        font=("Segoe UI", 10),
        bg="#3a3a3a",
        fg="white",
        command=undo,
        activebackground="#080807",
        activeforeground="white",
        relief="flat",
        height=2,
        width=9
    ).pack(side=tk.LEFT, padx=5)

    # Redo button
    tk.Button(
        undo_redo_frame,
        text="Redo",
        font=("Segoe UI", 10),
        bg="#3a3a3a",
        fg="white",
        command=redo,
        activebackground="#080807",
        activeforeground="white",
        relief="flat",
        height=2,
        width=9
    ).pack(side=tk.LEFT, padx=5)

    # tk.Button(text="↶ Undo", command=undo).pack(side=tk.LEFT, padx=2)
    # tk.Button(text="↷ Redo", command=redo).pack(side=tk.LEFT, padx=2)



    tk.Button(
        control_frame,
        text="Grayscale Conversion",
        font=("Segoe UI", 10),
        bg="#3a3a3a",
        fg="white",
        command=apply_grayscale,
        activebackground='#080807',
        activeforeground="white",
        relief="flat",
        height=2,
        width=20
    ).pack(pady=3)

    tk.Button(
        control_frame,
        text="Blur",
        font=("Segoe UI", 10),
        bg="#3a3a3a",
        fg="white",
        command=apply_blur,
        activebackground='#080807',
        activeforeground="white",
        relief="flat",
        height=2,
        width=20
    ).pack(pady=5)

    tk.Button(
        control_frame,
        text="Edge Detection",
        font=("Segoe UI", 10),
        bg="#3a3a3a",
        fg="white",
        command=apply_edge_detection,
        activebackground='#080807',
        activeforeground="white",
        relief="flat",
        height=2,
        width=20
    ).pack(pady=3)


    tk.Button(
        control_frame,
        text="Rotate 90°",
        font=("Segoe UI", 10),
        bg="#3a3a3a",
        fg="white",
        command=apply_rotate_90,
        activebackground='#080807',
        activeforeground="white",
        relief="flat",
        height=2,
        width=20
    ).pack(pady=3)
    tk.Button(
        control_frame,
        text="Rotate 180°",
        font=("Segoe UI", 10),
        bg="#3a3a3a",
        fg="white",
        command=apply_rotate_180,
        activebackground='#080807',
        activeforeground="white",
        relief="flat",
        height=2,
        width=20
    ).pack(pady=3)

    tk.Button(
        control_frame,
        text="Rotate 270°",
        font=("Segoe UI", 10),
        bg="#3a3a3a",
        fg="white",
        command=apply_rotate_270,
        activebackground='#080807',
        activeforeground="white",
        relief="flat",
        height=2,
        width=20
    ).pack(pady=3)

    tk.Button(
        control_frame,
        text="Flip Horizontal",
        font=("Segoe UI", 10),
        bg="#3a3a3a",
        fg="white",
        command=apply_flip_horizontal,
        activebackground='#080807',
        activeforeground="white",
        relief="flat",
        height=2,
        width=20
    ).pack(pady=3)

    tk.Button(
        control_frame,
        text="Flip vertical",
        font=("Segoe UI", 10),
        bg="#3a3a3a",
        fg="white",
        command=apply_flip_vertical,
        activebackground='#080807',
        activeforeground="white",
        relief="flat",
        height=2,
        width=20
    ).pack(pady=3)

    # Separator

    # === BRIGHTNESS SLIDER ===
    tk.Label(
        control_frame,
        text="Brightness",
        font=('Segoe UI', 10),
        bg='#52514b',
        fg='white'
    ).pack(pady=5)

    brightness_var = tk.DoubleVar(value=1.0)

    brightness_slider = tk.Scale(
        control_frame,
        from_=0.0,
        to=2.0,
        resolution=0.1,
        orient=tk.HORIZONTAL,
        variable=brightness_var,
        command=update_brightness,
        length=200,

        # Styling
        bg="#2d2d2d",
        fg="white",
        troughcolor="#444444",
        activebackground="#f5de0c",
        highlightthickness=0,
        bd=0,
        relief="flat",
        showvalue=False
    )
    brightness_slider.pack(pady=(10, 4))


    brightness_label = tk.Label(
        control_frame,
        text="1.0",
        bg="#2d2d2d",
        fg="white",
        font=("Segoe UI", 9)
    )
    tk.Label(
        control_frame,
        text="Contrast",
        font=('Segoe UI', 10),
        bg='#52514b',
        fg='white'
    ).pack(pady=5)


    contrast_slider = tk.Scale(
        control_frame,
        from_=0.0,
        to=2.0,
        resolution=0.1,
        orient=tk.HORIZONTAL,
        variable=contrast_variable,
        command=update_contrast,
        length=200,

        # Styling
        bg="#2d2d2d",
        fg="white",
        troughcolor="#444444",
        activebackground="#f5de0c",
        highlightthickness=0,
        bd=0,
        relief="flat",
        showvalue=False
    )
    contrast_slider.pack(pady=(10, 4))

    info_frame = tk.Frame(control_frame, bg="#2d2d2d")
    info_frame.pack(fill=tk.X, padx=10, pady=(15, 5))



    #need to add a function calling
    image_info_label = tk.Label(
        info_frame,

        text=get_details(),
        justify=tk.LEFT,
        anchor="w",
        font=("Segoe UI", 9),
        bg="#2d2d2d",
        fg="#dddddd",
        padx=10,
        pady=8
    )
    image_info_label.pack(fill=tk.X)

    # Reset button
    tk.Button(
        control_frame,
        text="Reset to Original",
        font=("Segoe UI", 10),
        bg="#3a3a3a",
        fg="white",
        command=apply_reset_image,
        activebackground='#f5de0c',
        activeforeground="white",
        relief="flat",
        height=2,
        width=20
    ).pack(pady=5)


def create_status_bar():
    """Create status bar at bottom"""
    global status_bar

    status_bar = tk.Label(
        root,
        text="No image loaded",
        justify=tk.LEFT,
        anchor="w",
        font=("Segoe UI", 9),
        bg="#2d2d2d",
        fg="#dddddd",
        padx=10,
        pady=8
    )
    status_bar.pack(side=tk.TOP, fill=tk.X)


def setup_window():
    """Setup main window"""
    global root
    root = tk.Tk()
    root.title("Image Editor Group 15 SYD")
    root.geometry("1200x800")
    root.minsize(800, 600)


# ==================== MAIN ====================

def main():
    """Main function - setup and run"""
    # Create window
    setup_window()
    # Create GUI components
    create_menu()
    create_canvas()
    create_controls()
    create_status_bar()
    # Start GUI
    root.mainloop()


if __name__ == "__main__":
    main()