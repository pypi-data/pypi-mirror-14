#-*- coding: utf-8 -*-
import unittest
from statement_extractor import extract_statement, extract_statements

class TestMethods(unittest.TestCase):

    def test1(self):
        text = 'She said "I support you."'
        statement = extract_statement(text)
        print "statement is", statement
        self.assertEqual(statement['quote'], "I support you.")
        self.assertEqual(statement['speaker'], "She")

    def test2(self):
        text = """
"If he builds the wall the way he built Trump Towers, he'll be using illegal immigrant labor to do it," Rubio said of Trump, referring to Trump's proposal to build a border wall along the border with Mexico.
"""
        statement = extract_statement(text)
        self.assertEqual(statement['speaker'], "Rubio")
        self.assertEqual(statement['quote'], "If he builds the wall the way he built Trump Towers, he'll be using illegal immigrant labor to do it")

    def test3(self):
        text = """"Such a cute soundbite," Trump said."""
        statement = extract_statement(text)
        self.assertEqual(statement['speaker'], "Trump")
        self.assertEqual(statement['quote'], "Such a cute soundbite")

    def test4(self):
        text = """"I guess there's a statute of limitation on lies," Rubio quipped, to applause from the audience."""
        statement = extract_statement(text)
        self.assertEqual(statement['speaker'], "Rubio")
        self.assertEqual(statement['quote'], "I guess there's a statute of limitation on lies")

    def test5(self):
        text = """"Marco is exactly right that a federal court found Donald guilty of being part of a conspiracy to hire people illegally and entered a $1 million judgment against him," Cruz said."""
        statement = extract_statement(text)
        self.assertEqual(statement['speaker'], "Cruz")
        self.assertEqual(statement['quote'], "Marco is exactly right that a federal court found Donald guilty of being part of a conspiracy to hire people illegally and entered a $1 million judgment against him")

    def test6(self):
        text = """"Donald funded the gang of eight," Cruz said."""
        statement = extract_statement(text)
        self.assertEqual(statement['speaker'], "Cruz")
        self.assertEqual(statement['quote'], "Donald funded the gang of eight")

#    def test7(self):
#        text = """
#"Even today, we saw a report in one of the newspapers that Donald, you've hired a significant number of people from other countries to take jobs that Americans could have filled," Rubio said. "My mom was a maid at a hotel, and instead of hiring an American like her, you have brought in over 1,000 people from all over the world to fill those jobs instead."
#"""
#        statements = extract_statements(text)
#        self.assertEqual(statements[0]['speaker'], "Rubio")
#        self.assertEqual(statements[1]['speaker'], "Rubio")

    def test8(self):
        text = """
“No, no, no. I don’t repeat myself,” Trump insisted, before immediately repeating himself by stating, “I don’t repeat myself.”
"""
        statements = extract_statements(text)
        self.assertEqual(statements[0]['speaker'], "Trump")
        self.assertEqual(statements[0]['quote'], u"""No, no, no. I don\u2019t repeat myself""")

    def test9(self):
        text = """
“You don’t repeat yourself?” Rubio asked in a bewildered tone.
"""
        statement = extract_statement(text)
        self.assertEqual(statement['speaker'], "Rubio")
        self.assertEqual(statement['quote'], u"You don\u2019t repeat yourself?")

    def test10(self):
        text = 'Mark told Jacob "I will protect you."'
        statement = extract_statement(text)
        self.assertEqual(statement['speaker'], "Mark")
        self.assertEqual(statement['quote'], "I will protect you.")

    def test11(self):
        text = 'Mark, the lead on the project, told Jacob "I will make sure you get a promotion."'
        statement = extract_statement(text)
        self.assertEqual(statement['speaker'], "Mark")
        self.assertEqual(statement['quote'], "I will make sure you get a promotion.")

    def test12(self):
        text = '''Tripoli Prime Minister Khalifa Ghwell said in a statement late on Tuesday that the airspace had been closed to "protect the souls of the people following the Presidential Council's inappropriate behaviour".'''
        statement = extract_statement(text)
        self.assertEqual(statement['speaker'], "Tripoli Prime Minister Khalifa Ghwell")
        self.assertEqual(statement['quote'], "protect the souls of the people following the Presidential Council's inappropriate behaviour")

    def test13(self):
        text = """
u'sing deep concern and disappointment at the leaders of Libya who were not able to overcome their differences," Ban urged them to show unity.</p>\n<p class="story-body-text" data-para-word-count="42">"They must address these issues with one government, one voice and with a sense of unity," Ban stressed, saying he has met Monday in Tunis wit'
        """
        statement = extract_statement(text)
        self.assertEqual(statement['speaker'], 'Ban')
        self.assertEqual(statement['quote'], "They must address these issues with one government, one voice and with a sense of unity")

    def test14(self):
        text = """
ded.</p>
<p class="story-body-text" data-para-word-count="25">While expressing deep concern and disappointment at the leaders of Libya who were not able to overcome their differences," Ban urged them to show unity.</p>
<p class="story-body-text" data-para-word-count="42">
        """
        statement = extract_statement(text)
        self.assertEqual(statement, None)
 
    if __name__ == '__main__':
        unittest.main()
