
#Anzeige-Class
class Display(object):
    def __init__(self, seg, start, end):
        self.seg = seg
        self.start = start
        self.end = end

    def get_all(self):
        return { 'text': self.seg.text[self.start:self.end]}

    def set_text(self, text):
        text_padded = text.rjust(8, ' ')
        self.seg.text[self.start:self.end] = text_padded

    #Methode, um den Text des eigenen Displays zu ändern
    def changeMyDisplay(self, text):
        self.seg.text[self.start:self.end] = text