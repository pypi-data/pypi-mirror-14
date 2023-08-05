import unittest
from judge import error
from judge.graders import iograder


#
# Code fragments
#
templ1 = r'''
1; 2; --> "result: 3"  

-1; 2; --> "result: 1"
'''

src1_ok = r'''
#include <stdio.h>

void main() {
    int x=0, y=0;
    scanf("%i", &x);
    scanf("%i", &y);
    printf("result: %i\n", x + y);
}
''' 

src1_presentation = r'''
#include <stdio.h>

void main() {
    int x=0, y=0;
    scanf("%i", &x);
    scanf("%i", &y);
    printf("Result:%i\n", x + y);
}
''' 

src1_wrong = r'''
#include <stdio.h>

void main() {
    int x=0, y=0;
    scanf("%i", &x);
    scanf("%i", &y);
    printf("result: %i\n", x + y + 1);
}
'''

src1_missing = r'''
#include <stdio.h>

void main() {
    int x=0, y=0;
    scanf("%i", &x);
    printf("result: %i\n", x + y);
}

'''

src1_runtime = r'''
#include <stdio.h>

void main() {
    int x=0, y=0;
    scanf("%i", &x);
    scanf("%i", &y);
    printf("result: %i\n");
}
'''

src1_extra = r'''
#include <stdio.h>

void main() {
    int x=0, y=0, z=1;
    scanf("%i", &x);
    scanf("%i", &y);
    scanf("%i", &z);
    printf("result: %i\n", x + y + z);
}
'''

src1_timeout = r'''
#include <unistd.h>

void main() {
    sleep(10000);
}
'''


class IOCGraderTestCase(unittest.TestCase):
    sandbox = False
    lang = 'tcc'
    
    def test_src1_ok(self):
        grade = iograder(src1_ok, templ1, sandbox=self.sandbox, lang=self.lang)
        self.assertEqual(grade.value, 1)
        self.assertEqual(grade.feedback, None)

    def test_src1_wrong(self):
        grade = iograder(src1_wrong, templ1, sandbox=self.sandbox, lang=self.lang)
        self.assertEqual(grade.value, 0)
        self.assertIsInstance(grade.feedback.error, error.WrongAnswer)

    def test_src1_presentation(self):
        grade = iograder(src1_presentation, templ1, sandbox=self.sandbox, lang=self.lang)
        self.assertEqual(grade.value, 0)
        self.assertIsInstance(grade.feedback.error, error.PresentationError)
        
    def test_src1_missing(self):
        grade = iograder(src1_missing, templ1, sandbox=self.sandbox, lang=self.lang)
        self.assertEqual(grade.value, 0)
        self.assertIsInstance(grade.feedback.error, error.EarlyTermination)

    def test_src1_runtime(self):
        grade = iograder(src1_runtime, templ1, sandbox=self.sandbox, lang=self.lang)
        self.assertEqual(grade.value, 0)
        #self.assertIsInstance(grade.feedback.error, error.RuntimeConditionError)
        self.assertIsInstance(grade.feedback.error, error.WrongAnswer)
        
    def test_src1_extra(self):
        grade = iograder(src1_extra, templ1, sandbox=self.sandbox, lang=self.lang)
        self.assertEqual(grade.value, 0)
        self.assertIsInstance(grade.feedback.error, error.TimeExceeded)
        
    def test_src1_timeout(self):
        grade = iograder(src1_timeout, templ1, timeout=0.05, sandbox=self.sandbox, lang=self.lang)
        self.assertEqual(grade.value, 0)
        self.assertIsInstance(grade.feedback.error, error.TimeExceeded)


    
if __name__ == '__main__':
    unittest.main()