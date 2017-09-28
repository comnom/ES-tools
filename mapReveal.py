# mapReveal.py
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


# Overwrite a save to reveal the entire map. Optionally includes plugins.
#
# Usage: >>mapReveal.py "games data path" "save file path" "optional: plugin path"
#
# This naturally overwrites your save, so if it breaks, you get to keep it.

if __name__ == "__main__":
	from ESParserPy.dataFile import DataFile
	from ESParserPy.dataNode import DataNode
	from ESParserPy.dataWriter import DataWriter
	
	import os
	import sys
	
	args = sys.argv
	
	dataPath = os.path.normpath(args[1])
	
	if len(args) > 3:
		pluginPath = os.path.normpath(args[3])
	else:
		pluginPath = ""
	
	files = []
	
	for file in os.listdir(dataPath):
		fullPath = os.path.normpath(dataPath + "/" + file)
		files.append(DataFile(fullPath))
	
	if pluginPath:
		for dir in os.listdir(pluginPath):
			pluginDataPath = os.path.normpath(pluginPath + "/" + dir + "/data")
			if not os.path.isdir(pluginDataPath):
				continue
				
			for file in os.listdir(pluginDataPath):
				fullPath = os.path.normpath(pluginDataPath + "/" + file)
				files.append(DataFile(fullPath))
	
	systems = []
	planets = []
	for file in files:
		for node in file.Begin():
			if node.Token(0) == "system":
				systems.append(node.Token(1))
			elif node.Token(0) == "planet":
				planets.append(node.Token(1))
	
	newRoot = DataNode()
	
	for token in systems:
		child = DataNode(parent=newRoot, children=None, tokens=["visited", token])
		newRoot.children.append(child)
	
	for token in planets:
		child = DataNode(parent=newRoot, children=None, tokens=["visited planet", token])
		newRoot.children.append(child)
	
	outPath = os.path.normpath(args[2])
	save = DataFile(outPath)
	
	for child in save.Begin():
		if child.Token(0) == "visited" or child.Token(0) == "visited planet":
			save.root.children.remove(child)
	
	for child in newRoot.Begin():
		save.root.children.append(child)
	
	newSave = DataWriter(outPath)
	
	for child in save.Begin():
		newSave.Write(child)
	
	newSave.Save()
