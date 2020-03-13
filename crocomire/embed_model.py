class TextEmbed:
    def __init__(self, name: str):
        self.name = name
        self.title = None
        self.description = None
        self.footer = None
        self.thumbnail = None
        self.image = None
        self.fields = {}

    def set_title(self, t: str):
        self.title = t

    def set_description(self, d: str):
        self.description = d

    def set_footer(self, f: str):
        self.footer = f

    def set_thumbnail(self, t: str):
        self.thumbnail = t

    def set_image(self, i: str):
        self.image = i

    def set_fields(self, f: dict):
        self.fields = f
