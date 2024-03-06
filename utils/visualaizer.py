from PIL import Image, ImageDraw


class Visualizer:

    def __init__(self, df):
        self.df = df

    def visualize_by_fragment(self):

        white = (255, 255, 255)

        image = Image.new("RGB", (1920, 1080), white)
        draw = ImageDraw.Draw(image)

        for i in range(self.df.shape[0]):
            row = self.df.iloc[i]

            if row.Marker == 'start' or row.Marker == 'stop':
                draw.ellipse([(row.X - 7, row.Y - 7), (row.X + 7, row.Y + 7)], fill='green', outline='green')
                if row.Marker == 'stop':
                    image.show()
                    image = Image.new("RGB", (1920, 1080), white)
                    draw = ImageDraw.Draw(image)
                    yield
            else:
                draw.ellipse([(row.X - 5, row.Y - 5), (row.X + 5, row.Y + 5)], fill='red', outline='green')

            if (i + 1) < self.df.shape[0]:
                next_row = self.df.iloc[i + 1]
                draw.line([row.X, row.Y, next_row.X, next_row.Y], fill='black')

    def visualize_all(self):
        white = (255, 255, 255)

        image = Image.new("RGB", (1920, 1080), white)
        draw = ImageDraw.Draw(image)

        for i in range(self.df.shape[0]):
            row = self.df.iloc[i]

            if row.Marker == 'start' or row.Marker == 'stop':
                draw.ellipse([(row.X - 7, row.Y - 7), (row.X + 7, row.Y + 7)], fill='green', outline='green')
            else:
                draw.ellipse([(row.X - 5, row.Y - 5), (row.X + 5, row.Y + 5)], fill='red', outline='green')

            if (i + 1) < self.df.shape[0]:
                next_row = self.df.iloc[i + 1]
                draw.line([row.X, row.Y, next_row.X, next_row.Y], fill='black')

        return draw
