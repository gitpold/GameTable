
#Anzeige-Class
class Display(object):
    def __init__(self, seg, start, end):
        self.seg = seg
        self.start = start
        self.end = end

    #Methode, um den Text des eigenen Displays zu ändern
    def changeMyDisplay(self, text):
        self.seg.text[self.start:self.end] = text