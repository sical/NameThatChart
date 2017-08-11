from threading import Thread
import sys
from downloadpeon import Peon
sys.path.append('../')
import imagePrep as pics


class Downloader(Thread):
    def __init__(self, sources, out,color):
        Thread.__init__(self)
        self.sources = sources
        self.output = out
        self.color = color

    def run(self):
        i = 0
        for source in self.sources:
            temp = source.url.split('.')

            ext = str(temp[len(temp) - 1])
            dl = Peon(source.url, self.output + source.type + "_" + str(len(pics.getimgs(self.output))) + "." + ext)
            dl.start()
            print(self.color+"Row : " + str(i) + " on " + str(len(self.sources))+'\x1b[0m')
            i += 1

            dl.join(2)
