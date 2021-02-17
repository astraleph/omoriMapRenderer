from PIL import Image

class SheetReader():
    def __init__(self, imageName, tileWidth, tileHeight = None):
        self.imageName = imageName
        self.image = Image.open(imageName)
        if not tileHeight:
            self.tileWidth = tileWidth
            self.tileHeight = tileWidth # assume square tiles
        else:
            self.tileWidth = tileWidth
            self.tileHeight = tileHeight
        self.rows = self.image.width  // self.tileWidth
        self.cols = self.image.height // self.tileHeight
        self.maxTiles = self.rows * self.cols
    def getSprite(self, localID):
        if localID >= self.maxTiles or localID < 0:
            print(localID)
            return None
        x = localID % self.rows
        y = localID // self.rows
        ix, iy = x * self.tileWidth, y * self.tileHeight
        return self.image.crop((ix,iy,ix+self.tileWidth,iy+self.tileHeight))

if __name__ == "__main__":
    ss = SheetReader("DW_Interior.png", 32)
    ss.getSprite(0).show()