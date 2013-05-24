#!/usr/bin/env python
# -*- coding: utf8 -*-

import random

class SkipNode(object):
    '''
    SkipList Node
    '''
    def __init__(self, level=1, elem=None):
        self.elem = elem
        self.next = [None] * level

class SkipList(object):
    '''
    SkipList
    '''
    def __init__(self, maximum=15):
        self.maximum = maximum
        self.head = SkipNode(maximum)
        self.level = 1

    def updateList(self, elem):
        '''
        update[i]保存在该层搜索指定elem时，elem的前一个节点
        '''
        update = [None] * len(self.head.next)
        x = self.head
        for i in reversed(range(len(self.head.next))):
            while x.next[i] != None and x.next[i].elem < elem:
                x = x.next[i]
            update[i] = x
        return update

    def randomGenerator(self):
        newLevel = 1
        while (newLevel < self.maximum and random.random() < 0.5):
            newLevel += 1
        return newLevel

    def find(self, elem, update=None):
        if update == None:
            update = self.updateList(elem)

        if len(update) > 0:
            candidate = update[0].next[0]
            if candidate != None and candidate.elem == elem:
                return candidate
        return None
    
    def insert(self, elem):
        level = self.randomGenerator()
        node = SkipNode(level, elem)

        if (level > self.level):
            self.level = level

        update = self.updateList(elem)

        if self.find(elem, update) == None:
            for i in range(len(node.next)):
                node.next[i] = update[i].next[i]
                update[i].next[i] = node

    def delete(self, elem):
        update = self.updateList(elem)

        node = self.find(elem, update)
        
        if node != None:
            for i in range(len(node.next)):
                update[i].next[i] = node.next[i]

            while self.level > 1 and \
                    self.head.next[self.level-1] == None:
                self.level -= 1
            
    def dump(self):
        print "Maximum Level: %d" % len(self.head.next)
        print "Level: %d" % self.level
        for i in reversed(range(len(s.head.next))):
            x = s.head.next[i]
            buf = ["@"]
            while x != None:
                buf.append(str(x.elem) + "(" + str(len(x.next)) + ")")
                x = x.next[i]
            buf.append("|")
            print "->".join(buf)

s = SkipList(10)
s.insert(3)
s.insert(26)
s.insert(25)
s.insert(6)
s.insert(19)
s.insert(21)
s.insert(12)
s.insert(9)
s.insert(7)
s.dump()
print s.find(12).elem
print s.find(13)
s.delete(12)
s.dump()
print s.find(12)
