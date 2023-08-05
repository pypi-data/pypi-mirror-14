import unittest
from judge import error
from judge.parsers import IOGroup, In, Out
from judge.graders import iograder, iorun, iorunonce


#
# Code fragments
#
templ1 = r'''
1; 2; --> "result: 3\n" 

-1; 1; --> "result: 0\n"
'''

src1_ok = '''
x = int(input())
y = int(input())
print('result:', x + y)
'''

src1_presentation = '''
x = int(input())
y = int(input())
print('Result: ', x + y)
''' 

src1_presentation_msg = '''
------------------
Presentation Error
------------------

Expected answer:
    [ 1 ]
    [ 2 ]
    result: 3

Obtained:
    [ 1 ]
    [ 2 ]
    Result:  3
''' 

src1_wrong = '''
x = int(input())
y = int(input())
print('result:', x + y + 1)
'''

src1_wrong_msg = '''
------------
Wrong Answer
------------

Expected answer:
    [ 1 ]
    [ 2 ]
    result: 3

Obtained:
    [ 1 ]
    [ 2 ]
    result: 4
''' 

src1_missing = '''
x = int(input())
print('result:', x + 2)
'''

src1_missing_msg = '''
-----------------
Early Termination
-----------------

Expected answer:
    [ 1 ]
    [ 2 ]
    result: 3

Obtained:
    [ 1 ]
    result: 3

Hint:
    Your program did not used all expected inputs.
''' 

src1_runtime = '''
x = int(input())
y = int(input())
print('result:', x + y + z)
'''

src1_runtime_msg = '''
---------------
Runtime Problem
---------------

Expected answer:
    [ 1 ]
    [ 2 ]
    result: 3

Obtained:
    [ 1 ]
    [ 2 ]

Error message:
    Traceback (most recent call last)
      File "<string>", line 4, in <module>
        print('result:', x + y + z)
    
    NameError: name 'z' is not defined

''' 

src1_extra = '''
x = int(input())
y = int(input())
z = int(input())
print('result:', x + y + z)
'''

src1_extra_msg = '''
-------------
Time Exceeded
-------------

Expected answer:
    [ 1 ]
    [ 2 ]
    result: 3

Obtained:
    [ 1 ]
    [ 2 ]

Hint:
    Your program took more than 10.00 seconds to run.
''' 

src1_timeout = '''
import time
time.sleep(1)
'''

src1_timeout_msg = '''
-------------
Time Exceeded
-------------

Expected answer:
    [ 1 ]
    [ 2 ]
    result: 3

Hint:
    Your program took more than 0.05 seconds to run.
'''


class IOPyGraderTestCase(unittest.TestCase):
    sandbox = False
    
    def test_src1_ok(self):
        grade = iograder(src1_ok, templ1, sandbox=self.sandbox)
        self.assertEqual(grade.value, 1)
        self.assertEqual(grade.feedback, None, grade.feedback)
        
    def test_src1_wrong(self):
        grade = iograder(src1_wrong, templ1, sandbox=self.sandbox)
        self.assertEqual(grade.value, 0)
        self.assertIsInstance(grade.feedback.error, error.WrongAnswer)

    def test_src1_wrong_message(self):
        grade = iograder(src1_wrong, templ1, sandbox=self.sandbox)
        out = str(grade.feedback)
        self.assertEqual(out.strip(), src1_wrong_msg.strip())

    def test_src1_presentation(self):
        grade = iograder(src1_presentation, templ1, sandbox=self.sandbox)
        self.assertEqual(grade.value, 0)
        self.assertIsInstance(grade.feedback.error, error.PresentationError)
        
    def test_src1_presentation_message(self):
        grade = iograder(src1_presentation, templ1, sandbox=self.sandbox)
        out = str(grade.feedback)
        self.assertEqual(out.strip(), src1_presentation_msg.strip())
        
    def test_src1_missing(self):
        grade = iograder(src1_missing, templ1, sandbox=self.sandbox)
        self.assertEqual(grade.value, 0)
        self.assertIsInstance(grade.feedback.error, error.EarlyTermination)
        
    def test_src1_missing_message(self):
        grade = iograder(src1_missing, templ1, sandbox=self.sandbox)
        out = str(grade.feedback)
        self.assertEqual(out.strip(), src1_missing_msg.strip())

    def test_src1_runtime(self):
        grade = iograder(src1_runtime, templ1, sandbox=self.sandbox)
        self.assertEqual(grade.value, 0)
        self.assertIsInstance(grade.feedback.error, error.RuntimeProblem)

    def test_src1_runtime_message(self):
        grade = iograder(src1_runtime, templ1, sandbox=self.sandbox)
        out = str(grade.feedback)
        self.assertEqual(out.strip(), src1_runtime_msg.strip())

    def test_src1_extra(self):
        grade = iograder(src1_extra, templ1, sandbox=self.sandbox)
        self.assertEqual(grade.value, 0)
        self.assertIsInstance(grade.feedback.error, error.TimeExceeded)
    
    def test_src1_extra_message(self):
        grade = iograder(src1_extra, templ1, sandbox=self.sandbox)
        out = str(grade.feedback)
        self.assertEqual(out.strip(), src1_extra_msg.strip())
        
    def test_src1_timeout(self):
        grade = iograder(src1_timeout, templ1, timeout=0.05, sandbox=self.sandbox)
        self.assertEqual(grade.value, 0)
        self.assertIsInstance(grade.feedback.error, error.TimeExceeded)

    def test_src1_timeout_message(self):
        grade = iograder(src1_timeout, templ1, timeout=0.05, sandbox=self.sandbox)
        out = str(grade.feedback)
        self.assertEqual(out.strip(), src1_timeout_msg.strip())

    
class IORunTestCase(unittest.TestCase):
    def test_iorunonce_ok(self):
        templ = IOGroup.fromstring(templ1)
        for atom in templ:
            interaction = iorunonce(src1_ok, atom)
            self.assertEqual(list(atom), list(interaction))
        
    def test_iorunonce_wrong(self):
        interaction = list(iorunonce(src1_wrong, (1, 5)))
        expected = [In('1'), In('5'), Out('result: 7\n')] 
        self.assertEqual(interaction, expected)
        
    def test_iorun_ok(self):
        templ = IOGroup.fromstring(templ1)
        self.assertEqual(iorun(src1_ok, templ), templ)
        
    def test_iorun_from_inputs_ok(self):
        templ = IOGroup.fromstring(templ1)
        inputs = [['1', '2'], ['-1', '1']]
        self.assertEqual(iorun(src1_ok, inputs), templ)


class IOResultCanRenderHtmlTestCase(unittest.TestCase):
    def test_wrong(self):
        iograder(src1_wrong, templ1, format='html')
        
    def test_timeout(self):
        iograder(src1_timeout, templ1, format='html')
        
    def test_presentation(self):
        iograder(src1_presentation, templ1, format='html')

    def test_missing(self):
        iograder(src1_missing, templ1, format='html')
        
    def test_runtime(self):
        iograder(src1_runtime, templ1, format='html')
        
    def test_extra(self):
        iograder(src1_extra, templ1, format='html')


if __name__ == '__main__':
    unittest.main()
    