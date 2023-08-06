from bs4 import BeautifulSoup
from os import listdir
from os.path import dirname, realpath
from re import compile as re_compile
from re import findall, finditer, IGNORECASE, match, MULTILINE, UNICODE, sub, VERBOSE
import pickle
flags = MULTILINE|UNICODE


directory_of_this_file = dirname(realpath(__file__))

# load patterns
directory_of_patterns = directory_of_this_file + "/prep/patterns"
language_pattern = {}
for filename in listdir(directory_of_patterns):
    language = filename.split(".")[0]
    with open(directory_of_patterns + "/" + language + ".txt") as f:
        pattern_as_string = (f.read().decode("utf-8").strip())
        pattern = re_compile(pattern_as_string, flags=flags)
        language_pattern[language] = pattern

def flatten(lst):
    result = []
    for element in lst:
        if hasattr(element, '__iter__'):
            result.extend(flatten(element))
        else:
            result.append(element)
    return result

# cleans statement
# sometimes can input something with a tags in it like
# he said &ldquo;bla bla bla <a href="...">bla</a>&rdquo;
def clean(text):
    if isinstance(text, str):
        text = text.decode("utf-8")
    text = text.replace(u"</a>",u"").replace(u"&#39;",u"'").replace(u"&rsquo;",u"\u2019").replace(u"&nbsp;",u" ").replace(u"&mdash;",u"\u2014").replace(u"&rdquo",u"\u201d").replace(u"\xa0",u" ").replace("&nbsp;",u" ").replace(u"</html>","").replace(u"</div>","").replace(u"</body>","").replace(u"</span>",u" ").replace(u"</footer>",u"").replace(u"</li>",u" ").replace(u"</ul>",u" ").replace(u"</p>",u" ")
    # remove opening a tag
    text = sub("</?(?:a|body|div|span|strong)[^>]*/?>", "", text)
    text = sub("</?(?:footer|form|h1|h2|h3|h4|h5|h6|h7|img|input|p|section|ul|li)[^>]*/?>", "\n", text)

    # remove comments
    text = sub("<!--.*-->", "\n", text)

    return text

def extract_statements(text, language=None):

    if isinstance(text, str):
        text = text.decode("utf-8")

    statements = []

    if language:
        tuples = [language, language_pattern[language]]
    else:
        tuples = language_pattern.iteritems()

    for language, pattern in tuples:
        for matchobject in finditer(pattern, text):
            #print "matchobject.start()", matchobject.start()
            #print "matchobject.end()", matchobject.end()
            dicts = {}
            for key, value in matchobject.groupdict().iteritems():
                if value:
                    k1, k2 = key.split("_")
                    if k2 in dicts:
                        dicts[k2][k1] = value
                    else:
                        dicts[k2] = {k1: value}
            d = [v for k,v in dicts.iteritems() if len(v) >= 3]
            if d:
                d = d[0]
                speaker = d['speaker']
                if speaker.istitle():
                    verbose_name = sorted(findall("(?:[A-Z][a-z]+ )*(?:" + speaker + ")(?: [A-Z][a-z]+)*", text), key=len)[-1]
                    if len(verbose_name) < 50 and verbose_name.count(" ") < 6:
                        speaker = verbose_name
                d = {"end": matchobject.end(), "language": language, "speaker": speaker, "quote": clean(d['quote']), "start": matchobject.start()}
                statements.append(d)

    extract_interview(text)

    return statements

def extract_statement(text):
    return (extract_statements(text) or [None])[0]

# find repeated paragraphs
def extract_interview(text):
    #text = clean(text)
    #print "text is", text
    tag = u"(?:</?(?:a|body|div|footer|form|h1|h2|h3|h4|h5|h6|h7|img|input|p|section|span|strong|ul|li)[^>\n\r\t]*/?>)"
    tag_zero_or_one = tag + "?"
    tags_any = tag + "*"
    tags_inline = u"(?:</?(?:a|p|span|strong)[^>\n\r\t]*/?>)*"
    p = u"(?:[^\n]{50,3000})"
    p = tags_any + p + tags_any
    # maybe add in paragraph acceptable text like any character except </div>
    #pattern = "(\n{0,2}" + tags_any + "[A-Z][A-Za-z -]{2,15}" + tags_inline + ":" + tags_inline + ".{50,10000}" + tags_any + "\n{0,2}){5,}"
    #pattern = "(\n{0,2}" + tags_any + "[A-Z][A-Za-z -]{2,15}" + tags_inline + ":" + tags_inline + p + tags_any + "\n{0,2}){5,}"
    pattern = """(?:
                  [\n]{0,2} # new lines between paragraphs
                  (?:<(?:p|div|li)[^>\n\r\t]*>) # open paragraphs
                  (?:[^\n]{5,50})
                  (?::)
                  (?:[^\n]{50,3000})
                  (?:</(?:p|div|li)>) # close paragraphs
                  (?: # second paragraph if there
                      [\n]{0,2}
                      (?:<(?:p|div|li)[^>\n\r\t]*>) # open paragraphs
                      (?:[^\n]{50,3000})
                      (?:</(?:p|div|li)>) # close paragraphs
                  )?
                  [\n]{0,2} # new lines between paragraphs
              ){5,}
              """


                  #(?:[A-Z][A-Za-z -]{5,55})
    pattern = """(?:
                  [\n]{0,2} # new lines between paragraphs
                  (?:<(?:p|div|li)[^>\n\r\t]*>)? # open paragraphs
                  (?:</?(?:a|span|strong)[^>\n\r\t]*/?>){0,2} # any tags
                  (?:[A-Z](?:[A-Za-z -]|&nbsp;){5,50})
                  (?:</?(?:a|span|strong)[^>\n\r\t]*/?>){0,2} # any tags
                  (?::)
                  (?:</?(?:a|span|strong)[^>\n\r\t]*/?>){0,2} # any tags
                  (?:[^\n]{50,3000})
                  (?:</(?:p|div|li)>)? # close paragraphs
                  (?: # second paragraph if there is one
                      [\n]{0,2}
                      (?:<(?:p|div|li)[^>\n\r\t]*>)? # open paragraphs
                      (?:[^\n]{50,3000})
                      (?:</(?:p|div|li)>)? # close paragraphs
                  )?
                  [\n]{0,2} # new lines between paragraphs
              ){5,}
              """
    pattern = """(?:
                  [\n]{0,2} # new lines between paragraphs
                  (?:<(?:p|div|li)[^>\n\r\t]*>)? # open paragraphs
                  (?:</?(?:a|span|strong)[^>\n\r\t]*/?>){0,2} # any tags
                  (?:[A-Z](?:[A-Za-z -]|&nbsp;){5,50})
                  (?:</?(?:a|span|strong)[^>\n\r\t]*/?>){0,2} # any tags
                  (?::)
                  (?:</?(?:a|span|strong)[^>\n\r\t]*/?>){0,2} # any tags
                  (?:[^\n]{50,3000})
                  (?:</(?:p|div|li)>)? # close paragraphs
                  [\n]{0,2} # new lines between paragraphs
                  (?:<(?:p|div|li)[^>\n\r\t]*>)? # open paragraphs
                  (?:</?(?:a|span|strong)[^>\n\r\t]*/?>){0,2} # any tags
                  (?:[A-Z](?:[A-Za-z -]|&nbsp;){5,50})
                  (?:</?(?:a|span|strong)[^>\n\r\t]*/?>){0,2} # any tags
                  (?::)
                  (?:</?(?:a|span|strong)[^>\n\r\t]*/?>){0,2} # any tags
                  (?:[^\n]{50,3000})
                  (?:</(?:p|div|li)>)? # close paragraphs
                  [\n]{0,2} # new lines between paragraphs
              ){1,}
              """

 
 
    #print "pattern is"
    #print [pattern]
    mos =  list(finditer(pattern, text, MULTILINE|UNICODE|VERBOSE))
    #print "mos is", mos
    for mo in mos:
        #print "\n\nmatch object is ", matchobject.group(0)
        #print "\n\nmatch object cleaned is ", clean(matchobject.group(0))
#        print "\n\n\n\nunclean is", mo.group(0)
        #print "text is", mo.group(0)
        text = clean(mo.group(0))
        #print "\ntext is", text

    # replaces non-breaking space
    #text = text.replace(u"\xa0",u" ").replace("&nbsp;",u" ")
    #soup = BeautifulSoup(text, "html5lib")
    #paragraphs = soup.findAll("p")
    #texts = [p.text for p in paragraphs]
    #texts = [t for t in texts if match(".{2,15}:.{20,2000}", t)]
    #print "texts are", texts
#    for mo in finditer("""
#        (?P<question>:[^\r\n]{10,1000})
#        \n?
#        (?P<answer>:[^\r\n]{10,1000})
#    """, text, VERBOSE):
#        print "mo is", mo.groupdict()
    #print "\n\n"


def get_keywords():
    directory_of_keywords = directory_of_this_file + "/prep/keywords"
    language_keywords = {}
    for filename in listdir(directory_of_keywords):
        language = filename.split(".")[0]
        with open(directory_of_keywords + "/" + language + ".txt") as f:
            language_keywords[language] = f.read().decode("utf-8").strip().splitlines()
    return language_keywords
eo=extract_statements
