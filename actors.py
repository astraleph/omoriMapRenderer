# This is a pile of non-functional code I made in an attempt to render Event sprites!
# It does not work properly. If someone can figure out why that'd be cool :) i don't know
# all that much about how RPGMaker calls in sprites which is like 99% of the issue lol
# side note, this all goes after line 95 in main.py


events = DATA['events']
actorImage = Image.new("RGBA", (imageWidth, imageHeight))
for event in events:
	if event:
		ex, ey = event['x'] * tileWidth, event['y'] * tileHeight
		actorImage.paste(actorTile, (ex, ey))

		# var bitmap = ImageManager.loadCharacter(characterName);
		# var big = ImageManager.isBigCharacter(characterName);
		# var pw = bitmap.width / (big ? 3 : 12);
		# var ph = bitmap.height / (big ? 4 : 8);
		# var n = characterIndex;
		# var sx = (n % 4 * 3 + 1) * pw;
		# var sy = (Math.floor(n / 4) * 4) * ph;
		# this.contents.blt(bitmap, sx, sy, pw, ph, x - pw / 2, y - ph);
		tileID = event['pages'][-1]['image']['characterName']
		tileIndex = event['pages'][-1]['image']['characterIndex']
		tileDir = event['pages'][-1]['image']['direction']

		if tileID:
			tileImage = Image.open(
				config['www'] + f"\\img\\characters\\{tileID}.png")
			ttw, tth = tileImage.width, tileImage.height

			big = "$" in tileID
			pw = ttw / (3 if big else 12)
			ph = tth / (4 if big else 8)
			sx = (tileIndex % 4 * 3 + 1) * pw
			sy = ((tileIndex // 4) * 4) * ph

			left = sx
			top = sy
			right = sx+pw
			bottom = sy+ph

			tile = tileImage.crop((left, top, right, bottom))
		else:
			tile = actorTile

		actorImage.paste(tile, (ex, ey))
actorImage.save("./layers/actors.png")