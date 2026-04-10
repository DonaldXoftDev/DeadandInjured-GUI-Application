from pathlib import Path
from itertools import cycle
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk, ImageSequence


class AnimatedGif(ttk.Frame):

    """
    A custom ttk Frame that loads and displays an animated GIF by cycling
    through its individual frames at a specified framerate.
    """
    def __init__(self, master):
        super().__init__(master, width=0, height=100)

        # Open the GIF file using pathlib for reliable path resolution
        file_path = Path(__file__).parent / "assets/spinners.gif"
        with Image.open(file_path) as im:
            # Create a sequence of images extracted from the GIF frames
            sequence = ImageSequence.Iterator(im)
            images = [ImageTk.PhotoImage(s) for s in sequence]
            self.image_cycle = cycle(images)

            # Extract the duration/length of each frame to set the refresh rate
            self.framerate = im.info["duration"]

        # Initialize the container with the first frame
        self.img_container = ttk.Label(self, image=next(self.image_cycle))
        self.img_container.pack(fill="both", expand="yes")
        self.after(self.framerate, self.next_frame)

    def next_frame(self):
        """Updates the label's image to the next frame in the cycle and schedules the next update."""
        self.img_container.configure(image=next(self.image_cycle))
        self.after(self.framerate, self.next_frame)


if __name__ == "__main__":

    app = ttk.Window("Animated GIF", themename="superhero")

    gif = AnimatedGif(app)
    gif.pack(fill=BOTH, expand=YES)

    app.mainloop()