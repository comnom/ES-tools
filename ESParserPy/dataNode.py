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



class DataNode(object):
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
			message = "Cannot convert token at " + str(index) + " to a number."
			print(message)
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
			return float(token)
		else:
			return int(token)
			
			
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
			
			
	def BeginFlat(self):
		for it in self.Begin():
			yield it
			
			for itb in it.BeginFlat():
				yield itb
				
				
	def End(self):
		for it in reversed(self.children)[:]:
			yield it
			
			
	def Append(self, node):
		node.parent = self
		self.children.append(node)
		
		
	def Remove(self, node):
		node.parent = None
		self.children.remove(node)
		
		
	def Copy(self):
		newTokens = []
		for token in self.tokens:
			newTokens.append(token)
			
		newNode = DataNode(tokens=newTokens)
		if self.HasChildren():
			for node in self.Begin():
				newNode.Append(node.Copy())
				
		return newNode
		
		
	def Delete(self):
		if self.parent:
			self.parent.Remove(self)
		else:
			self.parent = None
			
		self.tokens = None
		
		for node in self.Begin():
			node.Delete()
			
		self.children = None
			
