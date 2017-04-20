import unittest
import sys
import os

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if not path in sys.path:
    sys.path.insert(1, path)
del path

from semigroups import FpSemigroup
from semigroups import FpSemigroupElement
from semigroups import FpMonoid
from semigroups import FpMonoidElement

class TestFpSemigroup(unittest.TestCase):

    def test_valid_init(self):
        FpSemigroup([0,1], [])
        FpSemigroup([0,1], [[[0], [0, 0]]])
        FpSemigroup([0,1,2], [[[1], [0, 0]]])

        FpSemigroup(["a"], [])
        FpSemigroup(["a"], [["a", "aa"]])
        FpSemigroup(["a","b"], [["b", "aa"]])

    def test_alphabet(self):
        with self.assertRaises(ValueError):
            FpSemigroup([], [[[1], [0, 0]]])
        with self.assertRaises(TypeError):
            FpSemigroup(1, [[[1], [0, 0]]])

    def test_rels_int(self):
        with self.assertRaises(TypeError):
            FpSemigroup([0,1], "[[1], [0, 0]]")
        with self.assertRaises(TypeError):
            FpSemigroup([0,1], ["[1], [0, 0]"])
        with self.assertRaises(ValueError):
            FpSemigroup([0,1], [[[1], [0, 0], [1]]])
        with self.assertRaises(TypeError):
            FpSemigroup([0,1], [[[1], "0, 0"]])
        with self.assertRaises(TypeError):
            FpSemigroup([0,1], [[["1"], [0, 0]]])
        with self.assertRaises(ValueError):
            FpSemigroup([0,1], [[[1], [2, 0]]])

    def test_alphabet_str(self):
        with self.assertRaises(ValueError):
            FpSemigroup([], [["a", "aa"]])
        with self.assertRaises(ValueError):
            FpSemigroup(["a"], [["b", "aa"]])
        with self.assertRaises(ValueError):
            FpSemigroup(["a","a"], [["b", "aa"]])

    def test_rels_str(self):
        with self.assertRaises(TypeError):
            FpSemigroup(["a","b"], "['a', 'aa']")
        with self.assertRaises(TypeError):
            FpSemigroup(["a","b"], ["'b', 'aa'"])
        with self.assertRaises(ValueError):
            FpSemigroup(["a","b"], [['a', 'aa', 'b']])
        with self.assertRaises(TypeError):
            FpSemigroup(["a","b"], [['b', ['a','a']]])
        with self.assertRaises(ValueError):
            FpSemigroup(["a","b"], [['b', 'ca']])

    def test_set_report(self):
        S=FpSemigroup([0], [[[0], [0, 0]]])
        S.set_report(True)
        S.set_report(False)
        with self.assertRaises(TypeError):
            S.set_report('False')

    def test_size(self):
        self.assertEqual(FpSemigroup(["a"], [["a", "aa"]]).size(),1)
        self.assertEqual(FpSemigroup(["a","b"], [["a", "aa"],['b','bb'],\
        ['ab','ba']]).size(),3)
        self.assertEqual(FpSemigroup([0], [[[0], [0,0]]]).size(),1)
        self.assertEqual(FpSemigroup([0,1], [[[0], [0,0]],[[1],[1,1]],\
        [[0,1],[1,0]]]).size(),3)

    def test_word_to_class_index(self):
        FpS=FpSemigroup(["a","b"], [["a", "aa"],['b','bb'],['ab','ba']])
        FpS2=FpSemigroup([],[])
        e=FpSemigroupElement(FpS,"aba")
        FpS.word_to_class_index(e)
        with self.assertRaises(TypeError):
            FpS.word_to_class_index(1)
            FpS.word_to_class_index([1,'0'])
            FpS.word_to_class_index(FpSemigroupElement(FpS2,"aba"))
        self.assertEqual(FpS.word_to_class_index(e),
        FpS.word_to_class_index(FpSemigroupElement(FpS,"abaaabb")))

    def test_repr(self):
        self.assertEqual(FpSemigroup([1,2],[[[1,1],[1]],[[2,2,2],[2]],\
        [[1,2],[2,1]]]).__repr__(),"<FpSemigroup <1,2|11=1,222=2,12=21>>")
        self.assertEqual(FpSemigroup(["a","b"],[["aa","a"],["bbb","ab"],\
        ["ab","ba"]]).__repr__(),"<FpSemigroup <a,b|aa=a,bbb=ab,ab=ba>>")
        self.assertEqual(FpSemigroup(["a","b"],[["aa","a"],["bbbbbbbbbbbbbb\
bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb","b"],["ab","ba"]]).__repr__(),\
        "<FpSemigroup with 2 generators and 3 relations>")


class TestFpSemigroupElement(unittest.TestCase):

    def test_valid_init(self):
        FpS=FpSemigroup(["a","b"],[["aa","a"],["bbb","b"],["ba","ab"]])
        FpSemigroupElement(FpS,"aba")
        FpSemigroupElement(FpS,"a")
        FpS=FpSemigroup(["m","o"],[["ooo","o"]])
        FpSemigroupElement(FpS,"moo")
        FpSemigroupElement(FpS,"ooo")
        FpS=FpSemigroup(list("cowie"),[])
        FpSemigroupElement(FpS,"cowie")
        with self.assertRaises(ValueError):
            FpSemigroupElement(FpS,"")
        with self.assertRaises(TypeError):
            FpSemigroupElement("aba","aba")
        with self.assertRaises(TypeError):
            FpSemigroupElement(FpS,FpS)
        with self.assertRaises(ValueError):
            FpSemigroupElement(FpS,"abc")

    def test_mul(self):
        FpS=FpSemigroup(["a","b"],[["aa","a"],["bbb","b"],["ba","ab"]])
        other = "aa"
        a=FpSemigroupElement(FpS,"aba")
        a*a
        with self.assertRaises(TypeError):
            a*other
        with self.assertRaises(TypeError):
            FpSemigroupElement(FpSemigroup(["a","b"],[]),"aba")*a
        self.assertEqual(a*a,FpS.word_to_class_index( \
                        FpSemigroupElement(FpS,"abaaba")))

    def test_repr(self):
        FpS = FpSemigroup([1,2],[[[1,1],[1]],[[2,2,2],[2]]])
        self.assertEqual(FpSemigroupElement(FpS,[1,2]).__repr__(),
                                        "<FpSemigroup Element '[1, 2]'>")
        FpS = FpSemigroup(["a","b"],[["aa","a"],["bbb","b"],["ab","ba"]])
        self.assertEqual(FpSemigroupElement(FpS,"ab").__repr__(),
                                        "<FpSemigroup Element 'ab'>")


class TestFpMonoid(unittest.TestCase):

    def test_valid_init(self):
        FpMonoid([1,2], [])
        FpMonoid([1,2], [[[1], [1, 1]]])
        FpMonoid([1,2,3], [[[2], [1, 1]]])

        FpMonoid([], [])
        FpMonoid(["a"], [])
        FpMonoid(["a"], [["a", "aa"]])
        FpMonoid(["a","b"], [["b", "aa"]])

    def test_alphabet(self):
        with self.assertRaises(ValueError):
            FpMonoid([], [[[1], [2, 2]]])
        with self.assertRaises(TypeError):
            FpMonoid(1, [[[1], [2, 2]]])

    def test_rels_int(self):
        with self.assertRaises(TypeError):
            FpMonoid([1,2], "[[1], [2, 2]]")
        with self.assertRaises(TypeError):
            FpMonoid([1,2], ["[1], [2, 2]"])
        with self.assertRaises(ValueError):
            FpMonoid([1,2], [[[1], [2, 2], [1]]])
        with self.assertRaises(TypeError):
            FpMonoid([1,2], [[[1], "2, 2"]])
        with self.assertRaises(TypeError):
            FpMonoid([1,2], [[["1"], [2, 2]]])
        with self.assertRaises(ValueError):
            FpMonoid([1,2], [[[1], [3, 2]]])

    def test_alphabet_str(self):
        with self.assertRaises(ValueError):
            FpMonoid([], [["a", "aa"]])
        with self.assertRaises(ValueError):
            FpMonoid(["a"], [["b", "aa"]])
        with self.assertRaises(ValueError):
            FpMonoid(["a","a"], [["b", "aa"]])

    def test_rels_str(self):
        with self.assertRaises(TypeError):
            FpMonoid(["a","b"], "['a', 'aa']")
        with self.assertRaises(TypeError):
            FpMonoid(["a","b"], ["'b', 'aa'"])
        with self.assertRaises(ValueError):
            FpMonoid(["a","b"], [['a', 'aa', 'b']])
        with self.assertRaises(TypeError):
            FpMonoid(["a","b"], [['b', ['a','a']]])
        with self.assertRaises(ValueError):
            FpMonoid(["a","b"], [['b', 'ca']])

    def test_set_report(self):
        M=FpMonoid([1], [[[1], [1, 1]]])
        M.set_report(True)
        M.set_report(False)
        with self.assertRaises(TypeError):
            M.set_report('False')

    def test_size(self):
        self.assertEqual(FpMonoid(["a"], [["a", "aa"]]).size(),2)
        self.assertEqual(FpMonoid(["a","b"], [["a", "aa"],['b','bb'],
        ['ab','ba']]).size(),4)
        self.assertEqual(FpMonoid([1], [[[1], [1,1]]]).size(),2)
        self.assertEqual(FpMonoid([1,2], [[[2], [2,2]],[[1],[1,1]],
        [[2,1],[1,2]]]).size(),4)

    def test_word_to_class_index(self):
        FpM=FpMonoid(["a","b"], [["a", "aa"],['b','bb'],['ab','ba']])
        FpM2=FpMonoid([],[])
        FpM.word_to_class_index(FpSemigroupElement(FpM,"aba"))
        a=FpMonoidElement(FpM,"aba")
        FpM.word_to_class_index(a)
        with self.assertRaises(TypeError):
            FpM.word_to_class_index(1)
        with self.assertRaises(TypeError):
            FpM.word_to_class_index([2,'1'])
        with self.assertRaises(ValueError):
            FpM.word_to_class_index(FpSemigroupElement(FpM2,"aba"))
        self.assertEqual(FpM.word_to_class_index(a),
        FpM.word_to_class_index(FpMonoidElement(FpM,"abaaabb")))

    def test_repr(self):
        self.assertEqual(FpMonoid([1,2],[[[1,1],[1]],[[2,2,2],[2]],\
        [[1,2],[2,1]]]).__repr__(),"<FpMonoid <1,2|11=1,222=2,12=21>>")
        self.assertEqual(FpMonoid(["a","b"],[["aa","a"],["bbb","ab"],\
        ["ab","ba"]]).__repr__(),"<FpMonoid <a,b|aa=a,bbb=ab,ab=ba>>")
        self.assertEqual(FpMonoid(["a","b"],[["aa","a"],["bbbbbbbbbbbbbb\
bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb","b"],["ab","ba"]]).__repr__(),\
        "<FpMonoid with 2 generators and 3 relations>")

class TestFpMonoidElement(unittest.TestCase):

    def test_valid_init(self):
        FpM=FpMonoid(["a","b"],[["aa","a"],["bbb","b"],["ba","ab"]])
        FpMonoidElement(FpM,"aba")
        FpMonoidElement(FpM,"a")
        FpM=FpMonoid(["m","o"],[["ooo","o"]])
        FpMonoidElement(FpM,"moo")
        FpMonoidElement(FpM,"")
        with self.assertRaises(TypeError):
            FpMonoidElement("aba","aba")
        with self.assertRaises(TypeError):
            FpMonoidElement(FpM,FpM)
        with self.assertRaises(ValueError):
            FpMonoidElement(FpM,"abc")

    def test_mul(self):
        FpM=FpMonoid(["a","b"],[["aa","a"],["bbb","b"],["ba","ab"]])
        other = "aa"
        a=FpMonoidElement(FpM,"aba")
        a*a
        e=FpMonoidElement(FpM,"")
        with self.assertRaises(TypeError):
            a*other
        with self.assertRaises(TypeError):
            FpMonoidElement(FpMonoid(["a","b"],[]),"aba")*a
        self.assertEqual(a*a,FpM.word_to_class_index(FpMonoidElement(FpM,"abaaba")))
        self.assertEqual(a*e,FpM.word_to_class_index(a))

if __name__ == '__main__':
    unittest.main()
