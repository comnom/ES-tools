# teleport.py
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


# Overwrite a save to teleport the player and all ships to system, planet.
#
# Usage: >>teleport.py "save file path" "system" "planet"
#
# This naturally overwrites your save, so if it breaks, you get to keep it.
# Doesn't do any error checking. ie doesn't care if system/planet are valid.

if __name__ == "__main__":
	from ESParserPy.dataFile import DataFile
	from ESParserPy.dataWriter import DataWriter
	
	import os
	import sys
	
	args = sys.argv
	
	outPath = os.path.normpath(args[1])
	saveFile = DataFile(outPath)
	
	system = args[2]
	planet = args[3]
	
	for node in saveFile.Begin():
		if node.Token(0) == "system":
			node.tokens[1] = system
		elif node.Token(0) == "planet":
			node.tokens[1] = planet
		elif node.Token(0) == "ship":
			for child in node.Begin():
				if child.Token(0) == "system":
					child.tokens[1] = system
				elif child.Token(0) == "planet":
					child.tokens[1] = planet
				elif child.Token(0) == "position":
					child.tokens[1] = "0"
					child.tokens[2] = "0"
					
	newSave = DataWriter(outPath)
	
	for child in saveFile.Begin():
		newSave.Write(child)
		
	newSave.Save()
	