from fresco.util.cache import LRUCache


class TestLRUCache(object):

    lrucache = LRUCache

    def test_it_expires_least_recently_inserted(self):
        c = self.lrucache(3)
        c[0] = 0
        c[1] = 1
        c[2] = 2
        c[3] = 3
        assert set(c.keys()) == {1, 2, 3}

    def test_it_expires_least_recently_accessed(self):
        c = self.lrucache(3)
        c.update([(0, 0), (1, 1), (2, 2)])
        c.get(2)
        c.get(1)
        c.get(0)
        c[3] = 3
        assert set(c.keys()) == {0, 1, 3}

    def test_it_resizes_upwards(self):
        c = self.lrucache(2)
        c.update([(0, 0), (1, 1)])
        c.max_size = 4
        c.update([(2, 2), (3, 3), (4, 4)])
        assert set(c.keys()) == {1, 2, 3, 4}

    def test_it_resizes_downwards(self):
        c = self.lrucache(4)
        c.update([(0, 0), (1, 1), (2, 2), (3, 3)])
        c.max_size = 2
        assert set(c.keys()) == {2, 3}
