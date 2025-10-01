"""
Lingrow - simple GUI to display your PNG mockup and try text suggestions.

Place your PNG file (for example: lingrow_mockup.png) in the same folder as this script.
If the file is not found, the app will ask you to select an image file.

This script uses only the Python standard library. For better image support (scaling),
install Pillow: pip install pillow

Run with:
    python main.py

"""
import json
import os
import time
import io
import tkinter as tk
from tkinter import filedialog, messagebox

SAVE_FILE = "saved_texts.json"
DEFAULT_IMAGE = "lingrow_mockup.png"
ICON_PATHS = {
    'home': 'icons/home.png',
    'explore': 'icons/explore.png',
    'write': 'icons/write.png',
    'profile': 'icons/profile.png',
}


def professional_suggestion(text: str) -> str:
    replacements = {
        "gonna": "going to",
        "wanna": "want to",
        "ok": "okay",
        "yeah": "yes",
        "thanks": "thank you",
    }
    result = text
    for k, v in replacements.items():
        result = result.replace(k, v)
        result = result.replace(k.capitalize(), v.capitalize())
    # Capitalize sentence starts (very simple rule)
    sentences = [s.strip().capitalize() for s in result.split('.')]
    return '. '.join(s for s in sentences if s)


def neutral_suggestion(text: str) -> str:
    t = " ".join(text.split())
    # Very small cleanup
    t = t.replace(' ,', ',').replace(' .', '.')
    return t


def cultural_suggestion(text: str) -> str:
    cultural_map = {
        "buddy": "friend",
        "dude": "person",
        "mate": "friend (UK/AU)",
    }
    t = text
    for k, v in cultural_map.items():
        t = t.replace(k, v)
        t = t.replace(k.capitalize(), v.capitalize())
    return t + "\n\nNote: Consider local greetings depending on the culture."


def load_saved():
    if not os.path.exists(SAVE_FILE):
        return []
    try:
        with open(SAVE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []


def save_entry(title, original, suggestions):
    data = load_saved()
    entry = {
        'title': title,
        'original': original,
        'suggestions': suggestions,
        'timestamp': time.time(),
    }
    data.append(entry)
    with open(SAVE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


class LingrowApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title('Lingrow')
        root.geometry('420x780')
        # Colors inspired by your mockup
        self.bg = '#fde8e8'  # soft pink
        self.card = '#fff6f6'
        self.accent = '#7fa6ad'  # muted teal/blue
        root.configure(bg=self.bg)

        # Image state
        self.image_path = None
        self.tk_image = None
        self.pill_hover = False

        # Main container
        self.container = tk.Frame(root, bg=self.bg)
        self.container.pack(fill='both', expand=True)

        # Two main screens
        self.home_frame = tk.Frame(self.container, bg=self.bg)
        self.profile_frame = tk.Frame(self.container, bg=self.bg)

        self.build_home()
        self.build_profile()

        # Bottom navigation (canvas with icons + rounded center pill)
        self.nav_canvas = tk.Canvas(root, height=80, bg=self.bg, highlightthickness=0)
        self.nav_canvas.pack(side='bottom', fill='x')
        # redraw nav when size changes
        self.nav_canvas.bind('<Configure>', lambda e: self.draw_nav())

        # try to load nav icons from ICON_PATHS (user can add files under icons/)
        self.icon_images = {}
        self.load_nav_icons()

        self.show_home()

    def draw_nav(self):
        c = self.nav_canvas
        c.delete('all')
        w = c.winfo_width()
        h = c.winfo_height()
        if w <= 0:
            return

        # positions for icons (approx)
        xs = [w * 0.15, w * 0.35, w * 0.5, w * 0.85]
        y = h / 2

        # Home icon (left)
        if 'home' in self.icon_images:
            img = self.icon_images['home']
            c.create_image(xs[0], y, image=img, tags=('home',), anchor='center')
        else:
            c.create_text(xs[0], y, text='🏠', font=('Helvetica', 18), tags=('home',), anchor='center')
        c.tag_bind('home', '<Button-1>', lambda e: self.show_home())

        # Explore icon
        if 'explore' in self.icon_images:
            img = self.icon_images['explore']
            c.create_image(xs[1], y, image=img, tags=('explore',), anchor='center')
        else:
            c.create_text(xs[1], y, text='🌍', font=('Helvetica', 18), tags=('explore',), anchor='center')
        c.tag_bind('explore', '<Button-1>', lambda e: messagebox.showinfo('Explore', 'Explore clicked'))

        # Center rounded pill (with shadow and hover effect)
        cx = xs[2]
        pill_w = 120
        pill_h = 52
        left = cx - pill_w / 2
        right = cx + pill_w / 2
        top = y - pill_h / 2
        bottom = y + pill_h / 2
        # shadow (slightly offset)
            # (shadow removed to avoid possible rendering/blocking issues)

        # pick pill color depending on hover state
        pill_color = self._adjust_color(self.accent, -0.06) if self.pill_hover else self.accent
        # create the pill shapes and tag them so we can bind hover/click without extra overlays
        c.create_oval(left, top, left + pill_h, bottom, fill=pill_color, outline='', tags=('pill',))
        c.create_oval(right - pill_h, top, right, bottom, fill=pill_color, outline='', tags=('pill',))
        c.create_rectangle(left + pill_h/2, top, right - pill_h/2, bottom, fill=pill_color, outline='', tags=('pill',))
        # center write icon inside pill
        if 'write' in self.icon_images:
            img = self.icon_images['write']
            c.create_image(cx, y, image=img, tags=('write',), anchor='center')
        else:
            c.create_text(cx, y, text='✍️', font=('Helvetica', 18), fill='white', tags=('write',), anchor='center')
        c.tag_bind('write', '<Button-1>', lambda e: self.open_write_popup())
        # bind the pill shapes for hover and clicks (no transparent overlay needed)
        c.tag_bind('pill', '<Button-1>', lambda e: self.on_pill_click(e))
        c.tag_bind('pill', '<Enter>', lambda e: self.on_pill_enter(e))
        c.tag_bind('pill', '<Leave>', lambda e: self.on_pill_leave(e))

        # Profile icon (right)
        if 'profile' in self.icon_images:
            img = self.icon_images['profile']
            c.create_image(xs[3], y, image=img, tags=('profile',), anchor='center')
        else:
            c.create_text(xs[3], y, text='👤', font=('Helvetica', 18), tags=('profile',), anchor='center')
        c.tag_bind('profile', '<Button-1>', lambda e: self.show_profile())

    def on_pill_enter(self, event=None):
        self.pill_hover = True
        self.draw_nav()

    def on_pill_leave(self, event=None):
        self.pill_hover = False
        self.draw_nav()

    def on_pill_click(self, event=None):
        # quick visual feedback then open write popup
        self.pill_hover = True
        self.draw_nav()
        self.root.after(120, lambda: (setattr(self, 'pill_hover', False), self.draw_nav(), self.open_write_popup()))

    def _adjust_color(self, hex_color, factor: float) -> str:
        """Lighten or darken a hex color by factor (-1.0..1.0)."""
        hex_color = hex_color.lstrip('#')
        if len(hex_color) != 6:
            return hex_color
        try:
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            def clamp(v):
                return max(0, min(255, int(v)))
            r = clamp(r + r * factor)
            g = clamp(g + g * factor)
            b = clamp(b + b * factor)
            return '#{:02x}{:02x}{:02x}'.format(r, g, b)
        except Exception:
            return hex_color

    def load_nav_icons(self, size=(36, 36)):
        """Try to load PNG or SVG icons from ICON_PATHS into PhotoImage objects.
        If cairosvg is installed it will convert SVG to PNG on the fly.
        """
        for key, path in ICON_PATHS.items():
            # Try to set application icon from generated assets (if available)
            try:
                from PIL import Image, ImageTk
                icon_path = os.path.join('assets', 'lingrow_logo.png')
                if os.path.exists(icon_path):
                    img = Image.open(icon_path)
                    img.thumbnail((64, 64))
                    self.app_icon = ImageTk.PhotoImage(img)
                    try:
                        root.iconphoto(False, self.app_icon)
                    except Exception:
                        # some platforms may not support iconphoto
                        pass
            except Exception:
                # Pillow not available or load failed; ignore
                pass
            if not os.path.exists(path):
                continue

            # Try to load with Pillow (preferred) and support SVG via cairosvg if available
            try:
                from PIL import Image, ImageTk
                if path.lower().endswith('.svg'):
                    try:
                        import cairosvg
                        png_bytes = cairosvg.svg2png(url=path)
                        img = Image.open(io.BytesIO(png_bytes))
                    except Exception:
                        # Can't convert SVG here, skip to fallback
                        raise
                else:
                    img = Image.open(path)

                img.thumbnail(size, Image.LANCZOS)
                self.icon_images[key] = ImageTk.PhotoImage(img)
                continue
            except Exception:
                # Pillow / cairosvg failed or not available — try Tk PhotoImage as a last resort
                try:
                    tk_img = tk.PhotoImage(file=path)
                    self.icon_images[key] = tk_img
                except Exception:
                    # give up on this icon
                    continue

    def build_home(self):
        f = self.home_frame
        # Top area: logo and subtitle
        top = tk.Frame(f, bg=self.bg)
        top.pack(fill='x', pady=12)
        logo_frame = tk.Frame(top, bg=self.bg)
        logo_frame.pack(padx=16, anchor='w')
        # small canvas for logo image if present
        self.logo_canvas = tk.Canvas(logo_frame, width=48, height=48, bg=self.bg, highlightthickness=0)
        self.logo_canvas.pack(side='left')
        # Try to load the app logo generated in assets/lingrow_logo.png
        try:
            icon_path = os.path.join('assets', 'lingrow_logo.png')
            if os.path.exists(icon_path):
                try:
                    from PIL import Image, ImageTk
                    img = Image.open(icon_path)
                    img.thumbnail((48, 48))
                    self.app_logo = ImageTk.PhotoImage(img)
                    self.logo_canvas.create_image(24, 24, image=self.app_logo)
                except Exception:
                    # Pillow failed, fallback to Tk PhotoImage
                    tk_img = tk.PhotoImage(file=icon_path)
                    self.app_logo = tk_img
                    self.logo_canvas.create_image(24, 24, image=tk_img)
        except Exception:
            # no logo available or failed to load; ignore
            pass
        tk.Label(logo_frame, text='Lingrow', font=('Helvetica', 20, 'bold'), fg=self.accent, bg=self.bg).pack(side='left', padx=8)
        tk.Label(f, text='Your voice, in any language.', bg=self.bg, fg=self.accent, font=('Helvetica', 12)).pack(anchor='w', padx=18)

        # Mockup image box
        img_card = tk.Frame(f, bg=self.card, bd=1, relief='solid')
        img_card.pack(padx=16, pady=12, fill='x')
        self.canvas = tk.Canvas(img_card, height=200, bg=self.card, highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        tk.Button(img_card, text='Load Image', command=self.ask_image, bg=self.card).pack(pady=6)

        # Buttons like in the mockup
        btns = tk.Frame(f, bg=self.bg)
        btns.pack(padx=16, pady=8, fill='x')
        btn_style = {'bg': self.card, 'relief': 'groove', 'bd': 1, 'padx': 8, 'pady': 10}
        tk.Button(btns, text='✎ Write something', command=self.open_write_popup, **btn_style).pack(fill='x', pady=6)
        tk.Button(btns, text='🌍 Explore cultural expressions', command=lambda: messagebox.showinfo('Explore', 'Explore cultural expressions'), **btn_style).pack(fill='x', pady=6)
        tk.Button(btns, text='💡 Recent improvements', command=lambda: messagebox.showinfo('Recent', 'Recent improvements'), **btn_style).pack(fill='x', pady=6)

        self.home_frame.pack(fill='both', expand=True)

    def build_profile(self):
        f = self.profile_frame
        f.config(bg=self.bg)
        header = tk.Frame(f, bg=self.bg)
        header.pack(fill='x', pady=6)
        tk.Button(header, text='←', command=self.show_home, bg=self.bg, bd=0, fg=self.accent).pack(side='left', padx=8)
        tk.Label(header, text='Create an account', font=('Helvetica', 18, 'bold'), bg=self.bg, fg=self.accent).pack(pady=6)

        # Avatar area
        avatar = tk.Frame(f, bg=self.card, bd=1, relief='solid')
        avatar.pack(padx=16, pady=8, fill='x')
        tk.Label(avatar, text='Image', bg=self.card).pack(pady=10)
        tk.Button(avatar, text='+ Add image', command=self.ask_image, bg=self.card).pack(pady=6)

        form = tk.Frame(f, bg=self.bg)
        form.pack(padx=16, pady=6, fill='x')
        tk.Label(form, text='Email', bg=self.bg).pack(anchor='w')
        self.email_entry = tk.Entry(form)
        self.email_entry.pack(fill='x', pady=4)
        tk.Label(form, text='Password', bg=self.bg).pack(anchor='w')
        self.pass_entry = tk.Entry(form, show='*')
        self.pass_entry.pack(fill='x', pady=4)
        tk.Button(form, text='Sign Up', command=lambda: messagebox.showinfo('Sign Up', 'Account created (demo)'), bg=self.card).pack(pady=8)

        tk.Button(f, text='Add friends', command=lambda: messagebox.showinfo('Add friends', 'Add friends (demo)'), bg=self.card).pack(padx=16, pady=6, fill='x')

    def show_home(self):
        self.profile_frame.pack_forget()
        self.home_frame.pack(fill='both', expand=True)

    def show_profile(self):
        self.home_frame.pack_forget()
        self.profile_frame.pack(fill='both', expand=True)

    def ask_image(self):
        path = filedialog.askopenfilename(title='Select an image', filetypes=[('PNG images', '*.png'), ('All files', '*.*')])
        if path:
            self.load_image(path)

    def load_image(self, path):
        # load and show in both logo canvas (small) and main canvas
        try:
            from PIL import Image, ImageTk
            img = Image.open(path)
            # small logo
            logo = img.copy()
            logo.thumbnail((48, 48))
            self.logo_tk = ImageTk.PhotoImage(logo)
            self.logo_canvas.delete('all')
            self.logo_canvas.create_image(24, 24, image=self.logo_tk)

            # main canvas image
            main_img = img.copy()
            main_img.thumbnail((360, 200))
            self.tk_image = ImageTk.PhotoImage(main_img)
            self.canvas.delete('all')
            self.canvas.create_image(180, 100, image=self.tk_image)
            self.image_path = path
        except Exception:
            try:
                img = tk.PhotoImage(file=path)
                self.logo_canvas.delete('all')
                self.logo_canvas.create_image(24, 24, image=img)
                self.canvas.delete('all')
                self.canvas.create_image(0, 0, anchor='nw', image=img)
                # keep reference
                self.tk_image = img
                self.image_path = path
            except Exception as e:
                messagebox.showerror('Error', f'Could not open image: {e}')

    def open_write_popup(self):
        top = tk.Toplevel(self.root)
        top.title('Write')
        top.geometry('600x400')
        tk.Label(top, text='Write something:', font=('Helvetica', 12, 'bold')).pack(anchor='w', padx=8, pady=6)
        text = tk.Text(top, height=8)
        text.pack(fill='both', expand=True, padx=8, pady=6)

        out = tk.Text(top, height=8, state='disabled')
        out.pack(fill='both', expand=True, padx=8, pady=6)

        def do_and_show(func, label):
            t = text.get('1.0', 'end').strip()
            if not t:
                return
            s = func(t)
            out.config(state='normal')
            out.delete('1.0', 'end')
            out.insert('end', f'--- {label} ---\n')
            out.insert('end', s)
            out.config(state='disabled')

        ctl = tk.Frame(top)
        ctl.pack(fill='x', padx=8, pady=6)
        tk.Button(ctl, text='Professional', command=lambda: do_and_show(professional_suggestion, 'Professional')).pack(side='left', padx=6)
        tk.Button(ctl, text='Neutral', command=lambda: do_and_show(neutral_suggestion, 'Neutral')).pack(side='left', padx=6)
        tk.Button(ctl, text='Cultural', command=lambda: do_and_show(cultural_suggestion, 'Cultural')).pack(side='left', padx=6)
        tk.Button(ctl, text='Save', command=lambda: save_entry(os.path.basename(self.image_path) if self.image_path else 'untitled', text.get('1.0', 'end').strip(), {'preview': out.get('1.0', 'end').strip()})).pack(side='right', padx=6)


if __name__ == '__main__':
    root = tk.Tk()
    app = LingrowApp(root)
    root.mainloop()
