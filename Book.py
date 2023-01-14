#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 19:22:50 2022

@author: Stish
"""
class Book:
    def __init__(self,title,author,isbn,publication):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.publication= publication
        
    def __repr__(self):
        return f"{self.title} {self.author}"