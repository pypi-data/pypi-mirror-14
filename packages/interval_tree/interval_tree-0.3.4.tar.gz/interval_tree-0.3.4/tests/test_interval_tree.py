#!/usr/bin/env python
# encoding: utf-8
"""
test_interval_tree.py

Test so that the interval tree behave as expected

Created by Måns Magnusson on 2014-03-12.
Copyright (c) 2014 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import tempfile
import pytest

from interval_tree.interval_tree import IntervalTree


class TestIntervalTree(object):
    """Test class for testing how the interval tree behaves.."""

    def setup_class(self):
        """Setup different interval trees and check if they behave correct"""
        # Setup family with sick kid, sick father and healthy mother:
        # This should behave such that pos 1 and 2 are covered by the interval:
        empty_interval = [0,0,None]
        self.empty_tree = IntervalTree([empty_interval],0,0)
        smallest_interval = [1,1,'id_01']
        self.simplest_tree = IntervalTree([smallest_interval],1, 2)
        small_interval = [1,2,'id_02']
        self.simple_tree = IntervalTree([smallest_interval, small_interval],1, 2)
        interval_3 = [10,20,'id_03']
        interval_4 = [16,40,'id_04']
        self.tree = IntervalTree([interval_3, interval_4],1, 50)
        interval_5 = [10,20,'id_05']
        interval_6 = [10,20,'id_06']
        interval_7 = [10,20,'id_06']
        self.ovelapping_tree = IntervalTree([interval_5, interval_6, interval_7],1, 50)
        interval_8 = (10,20,'id_08')
        self.tuple_tree = IntervalTree([interval_8],1, 50)
         
    
    def test_empty_tree(self):
        """Test if empty trees behave as suspected."""
        assert self.empty_tree.find_range([3,3]) == []
    
    def test_basic_tree_functions(self):
        """Check so that the tree class behave as expected."""
        with pytest.raises(SyntaxError):
            tree = IntervalTree([[2,'id01']],1,2)
        with pytest.raises(SyntaxError):
            self.simplest_tree.find_range([1])
        with pytest.raises(ValueError):
            self.simplest_tree.find_range([1, 'a'])
        
    def test_simplest_tree(self):
        """Test interval_tree with one position."""
        assert self.simplest_tree.find_range([1,1]) == ['id_01']
        assert self.simplest_tree.find_range([2,2]) == []
        
    def test_simple_tree(self):
        """Test interval_tree with one position."""
        assert set(self.simple_tree.find_range([1,1])) == set(['id_01', 'id_02'])
        assert set(self.simple_tree.find_range([1,2])) == set(['id_01', 'id_02'])
        assert set(self.simple_tree.find_range([2,2])) == set(['id_02'])
        assert set(self.simple_tree.find_range([3,3])) == set([])

    def test_tree(self):
        """Test interval_tree with one position."""
        assert set(self.tree.find_range([1,1])) == set([])
        assert set(self.tree.find_range([10,12])) == set(['id_03'])
        assert set(self.tree.find_range([15,15])) == set(['id_03'])
        assert set(self.tree.find_range([16,16])) == set(['id_03', 'id_04'])
        assert set(self.tree.find_range([12,22])) == set(['id_03', 'id_04'])
        assert set(self.tree.find_range([30,30])) == set(['id_04'])
        assert set(self.tree.find_range([30,30])) == set(['id_04'])
        assert set(self.tree.find_range([42,42])) == set([])
    
    def test_overlapping_tree(self):
        """Test interval_tree two almost identical intervals."""
        assert set(self.ovelapping_tree.find_range([15,15])) == set(['id_05', 'id_06'])
    
    def test_tuple_tree(self):
        """Test if tuples are compatible with interval trees."""
        assert set(self.tuple_tree.find_range([15,15])) == set(['id_08'])

    def test_print_tree(self):
        """Test if tuples are compatible with interval trees."""
        print(self.tuple_tree)
        assert True


