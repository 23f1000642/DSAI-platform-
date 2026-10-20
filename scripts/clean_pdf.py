# Remove handwritten annotation layers (highlighter / pen strokes) that some pages of the source PDF carry.
# They live as a trailing "q /CsN cs ... sc /GsN gs" block at the end of a page's content stream.
import pymupdf, re, sys
src, dst = (sys.argv[1:3] + ['pyq.pdf', 'pyq_clean.pdf'][len(sys.argv[1:3]):])[:2]
d = pymupdf.open(src)
cleaned = []
for i, p in enumerate(d):
    for x in p.get_contents():
        s = d.xref_stream(x)
        m = re.search(rb'q /Cs\d+ cs [\d. ]+ sc /Gs\d+ gs', s)
        if m:
            d.update_stream(x, s[:m.start()]); cleaned.append(i)
d.save(dst)
print('cleaned pages:', sorted(set(cleaned)))
