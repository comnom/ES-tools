# genAllContent.py
# Copyright (C) 2017 Frederick W. Goy IV
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.



# Generates an all content plugin which optionally includes plugins.
#
# Usage: >>genAllContent.py "games data path" "plugin path"



if __name__ == "__main__":
	from ESParserPy.dataNode import DataNode
	from ESParserPy.getSources import GetSources
	
	import io
	import os
	import sys
	
	args = sys.argv
	
	dataPath = args[1]
	
	if len(args) > 2:
		pluginPath = args[2]
	else:
		pluginPath = ""
	
	files = GetSources(dataPath, pluginPath)
	
	ships = DataNode()
	outfits = DataNode()
	for file in files:
		for node in file.Begin():
			if node.Token(0) == "ship" and node.Size() == 2:
				ships.Append(node)
			elif node.Token(0) == "outfit":
				outfits.Append(node)
	
	shipLicenses = []
	for node in ships.Begin():
		for child in node.Begin():
			if child.Token(0) == "attributes":
				for grandChild in child.Begin():
					if grandChild.Token(0) == "licenses":
						for greatGrandchild in grandChild.Begin():
							shipLicenses.append(greatGrandchild.Token(0))
							
	outfitLicenses = []
	for node in outfits.Begin():
		for child in node.Begin():
			if child.Token(0) == "licenses":
				for grandChild in child.Begin():
					outfitLicenses.append(grandChild.Token(0))
					
	licenses = []
	for license in shipLicenses:
		if license not in licenses:
			licenses.append(license)
			
	for license in outfitLicenses:
		if license not in licenses:
			licenses.append(license)
			
	outFile = io.BytesIO()
	startString = ("start\n" +
		"\tdate 16 11 3013\n" +
		"\tplanet \"New Boston\"\n" +
		"\taccount\n" +
		"\t\tcredits 1000000000\n" +
		"\tset \"license: Pilot's\"\n")
	
	for license in licenses:
		startString += ("\tset \"license: " + license + "\"\n")
		
	outFile.write(startString)
	
	shipString = "shipyard \"Cheater Ships\"\n"
	for ship in ships.Begin():
		shipString += ('\t"' + ship.Token(1) + '"\n')
		
	outFile.write(shipString)
	
	outfitString = "outfitter \"Cheater Outfits\"\n"
	for outfit in outfits.Begin():
		outfitString += ('\t"' + outfit.Token(1) + '"\n')
		
	outFile.write(outfitString)
	
	planetString = ("planet \"New Boston\"\n" +
		"\tshipyard \"Cheater Ships\"\n" +
		"\toutfitter \"Cheater Outfits\"\n")
		
	outFile.write(planetString)
	
	if not os.path.isdir(os.path.normpath("genPlugin/data")):
		os.makedirs(os.path.normpath("genPlugin/data"))
	
	with open(os.path.normpath("genPlugin/data/genOut.txt"), "wb") as saveFile:
		saveFile.write(outFile.getvalue())

