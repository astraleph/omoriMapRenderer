from sheetreader import SheetReader
from PIL import Image
import glob
import json

config = json.load(open('config.json', 'r', encoding="utf-8"))
mapinfos = json.load(open(config['mapinfos'].replace(
    "<www>", config['www']), 'r', encoding='utf-8'))

nameToID = dict(zip([a['name'] for a in mapinfos if a],
                    [a['id'] for a in mapinfos if a]))

invalidTile = Image.open("./sprites/invalidSprite.png")
actorTile = Image.open("./sprites/actorSprite.png")

while True:
    print("\n\nOMORI MAP RENDERER\n---")
    query = input("Search > ")
    validMaps = [(a, nameToID[a])
                 for a in nameToID if query.lower() in a.lower()]
    for x, res in enumerate(validMaps):
        print(f"{x}: \"{res[0]}\"")
    select = input("Select a map > ")
    if not select.isdigit():
        print("Not a number. Try again!")
        continue
    selected = validMaps[int(select)]
    print(f"---\nRendering map \"{selected[0]}\"")

    # load map
    MAP = json.load(
        open(config['www'] + f"\\maps\\map{selected[1]}.json", 'r', encoding="utf-8"))
    DATA = json.load(open(
        config['www'] + f"\\data\\Map{str(selected[1]).zfill(3)}.json", 'r', encoding="utf-8"))

    imageWidth, imageHeight = MAP['tilewidth'] * \
        MAP['width'], MAP['tileheight'] * MAP['height']
    mapWidth, mapHeight = MAP['width'], MAP['height']
    tileWidth, tileHeight = MAP['tilewidth'], MAP['tileheight']

    composite = Image.new("RGBA", (imageWidth, imageHeight))

    # data has important event stuff
    # map has actual map tiles / tilesets
    TILESETS = {}
    for tileset in MAP['tilesets']:
        source = tileset['source']
        fullsource = config['www'] + f"\\maps\\{source}"
        TILEJSON = json.load(open(fullsource))
        iW, iH = TILEJSON['imagewidth'], TILEJSON['imageheight']
        tW, tH = TILEJSON['tilewidth'],  TILEJSON['tileheight']
        rows, cols = iW//tW, iH//tH

        firstgid = tileset['firstgid']
        tilecount = TILEJSON['tilecount']
        imageName = config['www'] + \
            TILEJSON['image'].replace("/", "\\").strip("..")

        TILESETS[range(firstgid, firstgid+tilecount)
                 ] = SheetReader(imageName, tW, tH)

    layerN = 0
    for layer in MAP['layers']:
        if 'data' not in layer:
            continue

        cx, cy = 0, 0
        curLayer = Image.new("RGBA", (imageWidth, imageHeight))

        for tile in layer['data']:
            if tile != 0:  # not empty
                # find responsible tileset
                rtileset = [ts for ts in TILESETS if tile in ts]
                if len(rtileset) != 1:  # no valid tilesets / more than one valid tileset
                    print(f"{tile} - {rtileset} ??")
                SS = TILESETS[rtileset[0]]
                if 'tile_collision' not in SS.imageName.lower() and 'tile_flags' not in SS.imageName.lower() and 'tile_region' not in SS.imageName.lower():
                    firstgid = rtileset[0][0]  # first in range
                    tile = SS.getSprite(tile - firstgid)
                    if not tile:  # something went wrong, show invalid tile
                        tile = invalidTile
                    curLayer.paste(tile, (cx*tileWidth, cy*tileHeight))

            cx += 1
            if cx >= mapWidth:
                cx = 0
                cy += 1
        if curLayer.getbbox():
            curLayer.save(f"./layers/layer_{layerN}.png")
            composite = Image.alpha_composite(composite, curLayer)
        layerN += 1
    composite.save("./layers/composite.png")

    print("Finished rendering map!")
    print("Rendering actors...")
    
    events = DATA['events']
    actorImage = Image.new("RGBA", (imageWidth, imageHeight))
    for event in events:
        if event:
            ex, ey = event['x'] * tileWidth, event['y'] * tileHeight
            actorImage.paste(actorTile, (ex, ey))
    actorImage.save("./layers/actors.png")
    
    print("BGM - " + DATA['bgm']['name'])
    print("BGS - " + DATA['bgs']['name'])
    if DATA['parallaxName']:
        parallax = config['www'] + f"\\img\\parallaxes\\{DATA['parallaxName']}.png"
        I = Image.open(parallax)
        I.save("./layers/parallax.png")
    exit()
