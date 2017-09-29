# dataNode.py
# Copyright (c) 2014 Michael Zahniser
# Copyright (C) 2017 Frederick W. Goy IV
#
# This program is a derivative of the source code from the Endless Sky
# project, which is licensed under the GNU GPLv3.
#
# Endless Sky source: https://github.com/endless-sky/endless-sky
#
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



class DataNode:
	def __init__(self, parent=None, children=None, tokens=None):
		self.parent = parent
		self.children = children or []
		self.tokens = tokens or []
		
		
	def Size(self):
		return len(self.tokens)
		
		
	def Token(self, index):
		return self.tokens[index]
		
		
	def Value(self, index):
		if not self.IsNumber(index):
			message = "Cannot convert " + self.tokens[index] + " to a number."
			return 0.
		
		token = self.tokens[index]
		
		hasDecimalPoint = False
		hasExponent = False
		for it in token:
			if it == ".":
				hasDecimalPoint = True
			elif it == "e" or it == "E":
				hasExponent = True
		
		if hasDecimalPoint or hasExponent:
			value = float(token)
		else:
			value = int(token)
			
		invalid = ("nan", "inf", "+inf", "-inf")
		if value not in invalid:
			return value
		else:
			message = "Cannot convert " + str(value) + " to a number."
			return 0.
			
			
	def IsNumber(self, index):
		if index >= len(self.tokens) or not self.tokens[index]:
			return False
		
		token = self.tokens[index]
		
		hasDecimalPoint = False
		hasExponent = False
		isLeading = True
		for it in token:
			if isLeading:
				isLeading = False
				if it == "-" or it == "+":
					continue
			
			if it == ".":
				if hasDecimalPoint or hasExponent:
					return False
				
				hasDecimalPoint = True
				
			elif it == "e" or it == "E":
				if hasExponent:
					return False
				
				hasExponent = True
				isLeading = True
				
			elif not it.isdigit():
				return False
		
		return True
		
		
	def HasChildren(self):
		if self.children:
			return True
			
		return False
			
			
	def Begin(self):
		for it in self.children[:]:
			yield it
			
			
	def End(self):
		for it in reversed(self.children)[:]:
			yield it
