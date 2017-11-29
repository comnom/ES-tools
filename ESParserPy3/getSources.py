# getSources.py
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



from .dataFile import DataFile

import os



def GetSources(dataPath, pluginPath=""):
	dataPath = os.path.normpath(dataPath)
	files = []
	
	for file in os.listdir(dataPath):
		fullPath = os.path.normpath(dataPath + "/" + file)
		files.append(DataFile(fullPath))
	
	if pluginPath:
		pluginPath = os.path.normpath(pluginPath)
		for dir in os.listdir(pluginPath):
			pluginDataPath = os.path.normpath(pluginPath + "/" + dir + "/data")
			if not os.path.isdir(pluginDataPath):
				continue
				
			for file in os.listdir(pluginDataPath):
				fullPath = os.path.normpath(pluginDataPath + "/" + file)
				files.append(DataFile(fullPath))
				
	return files

