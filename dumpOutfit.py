# dumpOutfit.py
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



# Create a space separated table of outfits matching attributes.
#
# Usage: >>dumpOutfit.py "games data path" "plugin path or none" "output file" "attr"
#
# Ex. >>dumpOutfit.py "C:\Endless Sky\data" none example.csv cooling "active cooling"
# Will output a table of all outfits with cooling and active cooling attributes.
#
# name, cost, and space(outfit space) are included by default so there is no need to
# explicitly request them.
#
# Does not work with weapons. Use >>EndlessSky.exe -w for that.



def DumpOutfits(dataFiles, keys):
	outfits = []
	for file in dataFiles:
		for node in file.Begin():
			if node.Token(0) == "outfit":
				isMatch = False
				mapping = {"name": node.Token(1), "cost": "", "space": ""}
				for child in node.BeginFlat():
					if child.Token(0) == "cost":
						mapping["cost"] = child.Token(1)
					elif child.Token(0) == "outfit space":
						mapping["space"] = child.Token(1)
					else:
						for key in keys:
							if child.Token(0) == key:
								isMatch = True
								mapping[key] = child.Token(1)
					
				if isMatch:
					outfits.append(mapping)
					
	return outfits



if __name__ == "__main__":
	from ESParserPy.dataNode import DataNode
	from ESParserPy.dataWriter import DataWriter
	from ESParserPy.getSources import GetSources
	
	import sys
	
	args = sys.argv
	
	dataPath = args[1]
	
	pluginPath = args[2]
	if pluginPath == "none":
		pluginPath = ""
		
	files = GetSources(dataPath, pluginPath)
	
	attributes = args[4:]
	outfits = DumpOutfits(files, attributes)
	
	newRoot = DataNode()
	header = ["name", "cost", "space"]
	header += attributes
	newRoot.Append(DataNode(tokens=header))
	
	for outfit in outfits:
		tokenList = []
		for key in header:
			if key in outfit:
				tokenList.append(outfit[key])
			else:
				tokenList.append("0")
		
		newRoot.Append(DataNode(tokens=tokenList))
	
	outPath = args[3]
	outFile = DataWriter(outPath)
	for node in newRoot.Begin():
		outFile.Write(node)
	
	outFile.Save()

