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
	from ESParserPy.getSources import GetSources
	
	import sys
	
	args = sys.argv
	
	dataPath = args[1]
	
	if len(args) > 3:
		pluginPath = args[3]
	else:
		pluginPath = ""
	
	files = GetSources(dataPath, pluginPath)
	
	systems = []
	planets = []
	for file in files:
		for node in file.Begin():
			if node.Token(0) == "system":
				systems.append(node.Token(1))
			elif node.Token(0) == "planet":
				planets.append(node.Token(1))
	
	outPath = args[2]
	save = DataFile(outPath)
	
	for node in save.Begin():
		if node.Token(0) == "visited" or node.Token(0) == "visited planet":
			save.Remove(node)
	
	for token in systems:
		save.Append(DataNode(tokens=["visited", token]))
	
	for token in planets:
		save.Append(DataNode(tokens=["visited planet", token]))
	
	newSave = DataWriter(outPath)
	
	for node in save.Begin():
		newSave.Write(node)
	
	newSave.Save()

