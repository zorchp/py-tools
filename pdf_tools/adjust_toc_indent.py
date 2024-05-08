import fitz

"""
the best way to adjust pdf toc is in ipython command line.
"""

doc = fitz.open("test.pdf")

toc = doc.get_toc()

print(toc)
# [[1, 'test', 3]]
# 1 is the depth of toc item
# 'test' is toc name
# 3 is page number

# operate toc (toc as list)
toc[0][1] = "xx"
doc.set_toc(toc)
doc.saveIncr()
