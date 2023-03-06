# reporter.py
#   Reporter class
#
# Jiyong Jang, 2012
#
import time
from collections import defaultdict
import common
import patchloader
import sourceloader


class Reporter(object):

    def __init__(self, patch, source):
        self._patch_list = patch.items()
        self._npatch = patch.length()
        self._source_list = source.items()
        self._nsource = source.length()
        self._match_dict = source.match_items()
        self._context_dict = defaultdict(list)

    def _exact_match(self):
        '''
        Exact-matching test to catch Bloom filters errors
        '''
        print '[+] performing an exact matching test'
        start_time = time.time()
        exact_nmatch = 0

        for patch_id, source_id_list in self._match_dict.items():
            patch_norm_lines = self._patch_list[patch_id].norm_lines
            patch_norm_length = len(patch_norm_lines)
            for source_id in source_id_list:
                source_norm_lines = self._source_list[source_id].norm_lines
                source_norm_length = len(source_norm_lines)

                for i in range(0, (source_norm_length-patch_norm_length+1)):
                    patch_line = 0
                    source_line = i
                    while patch_norm_lines[patch_line] == source_norm_lines[source_line]:
                        patch_line += 1
                        source_line += 1

                        if patch_line == patch_norm_length:
                            common.verbose_print('  [-] exact match - %s : %s (line #%d)' % (self._patch_list[patch_id].file_path, self._source_list[source_id].file_path, i+1))
                            self._context_dict[patch_id].append(common.ContextInfo(source_id, max(0, i-common.context_line), i, source_line, min(source_line+common.context_line, source_norm_length-1)))
                            exact_nmatch += 1
                            break

                        while source_line<source_norm_length-patch_norm_length and source_norm_lines[source_line]=='':
                            source_line += 1

                        if source_line == source_norm_length-patch_norm_length:
                            break

        elapsed_time = time.time() - start_time
        print '[+] %d exact matches ... %.1fs\n' % (exact_nmatch, elapsed_time)
        return exact_nmatch

    def _html_escape(self, string):
        '''
        Escape HTML
        '''
        return ''.join(common.html_escape_dict.get(c,c) for c in string)

    def output(self, outfile='output.html'):
        '''
        Perform an exact matching test and generate a report
        '''
        exact_nmatch = self._exact_match()
        if exact_nmatch == 0:
            return exact_nmatch

        print '[+] generating a report'
        start_time = time.time()

        out = open(outfile, 'w')
        # html head - css, javascript
        out.write("""
<!DOCTYPE html>
<html>
<head>
    <title>ReDeBug - Report</title>
    <style type="text/css">
    .container { padding: 3px 3px 3px 3px; font-size: 14px; }
    .patch { background-color: #CCCCCC; border: 2px solid #555555; margin: 0px 0px 5px 0px }
    .source { background-color: #DDDDDD; padding: 3px 3px 3px 3px; margin: 0px 0px 5px 0px }
    .filepath { font-size: small; font-weight: bold; color: #0000AA; padding: 5px 5px 5px 5px; }
    .codechunk { font-family: monospace; font-size: small; white-space: pre-wrap; padding: 0px 0px 0px 50px; }
    .linenumber { font-family: monospace; font-size: small; float: left; color: #777777; }
    </style>
    <script language="javascript">
        function togglePrev(node) {
            var targetDiv = node.previousSibling;
            targetDiv.style.display = (targetDiv.style.display=='none')?'block':'none';
            node.innerHTML = (node.innerHTML=='+ show +')?'- hide -':'+ show +';
        }
        function toggleNext(node) {
            var targetDiv = node.nextSibling;
            targetDiv.style.display = (targetDiv.style.display=='none')?'block':'none';
            node.innerHTML = (node.innerHTML=='+ show +')?'- hide -':'+ show +';
        }
    </script>
</head>
<body>
<div style="width: 100%; margin: 0px auto">""")
        # unpatched code clones
        out.write("""
    <b># <i>unpatched code clones:</i> <font style="color:red">%d</font></b>""" % exact_nmatch)

        for patch_id, context_list in self._context_dict.items():
            p = self._patch_list[patch_id]
            out.write("""
    <div class="container">
        <br />""")
            # patch info
            out.write("""
        <div class="patch">
            <div class="filepath">%s</div>
            <div class="codechunk">%s</div>
        </div>""" % (p.file_path, p.orig_lines))

            for context in context_list:
                s = self._source_list[context.source_id]
                # source info - prev_context
                out.write("""
        <div class="source">
            <div class="filepath">%s</div>
            <div style="display: none">
                <div class="linenumber">""" % s.file_path)

                for i in range(context.prev_context_line, context.start_line):
                    out.write("""
                %d<br />""" % (i+1))

                out.write("""
                </div>
                <div class="codechunk">%s</div>
            </div><a href="javascript:;" onclick="togglePrev(this);">+ show +</a>""" % self._html_escape('\n'.join(s.orig_lines[context.prev_context_line:context.start_line])))
                # source info
                out.write("""
            <div>
                <div class="linenumber">""")

                for i in range(context.start_line, context.end_line):
                    out.write("""
                %d<br />""" % (i+1))

                out.write("""
                </div>
                <div class="codechunk">%s</div>
            </div>""" % self._html_escape('\n'.join(s.orig_lines[context.start_line:context.end_line])))
                # source info - next_context
                out.write("""
            <a href="javascript:;" onclick="toggleNext(this);">+ show +</a><div style="display: none">
                <div class="linenumber">""")

                for i in range(context.end_line, context.next_context_line):
                    out.write("""
                %d<br />""" % (i+1))

                out.write("""
                </div>
                <div class="codechunk">%s</div>
            </div>
        </div>""" % self._html_escape('\n'.join(s.orig_lines[context.end_line:context.next_context_line])))
            out.write("""
    </div>""")

        out.write("""
</div>
</body>
</html>""")
        out.close()

        elapsed_time = time.time() - start_time
        print '[+] \"%s\" ... %.1fs\n' % (outfile, elapsed_time)
        return exact_nmatch

