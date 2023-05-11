# Load website data and change to CV Latex file
# This is only a test version

from markdown_to_json.vendor import CommonMark
from markdown_to_json.markdown_to_json import Renderer, CMarkASTNester
import json,re
from datetime import datetime
import calendar

inp_path='data/metadata_EN.md'

nester = CMarkASTNester()
renderer = Renderer()
with open(inp_path,'rb') as f:
    ast = CommonMark.DocParser().parse(f.read().decode('utf-8'))
    nested = nester.nest(ast)
    rendered = renderer.stringify_dict(nested)
pagedata=json.loads(json.dumps(rendered))

page_content=pagedata[list(pagedata.keys())[0]]

# ----------------------------
# Research section
# ----------------------------
# content=page_content['Publication']['Research']
# contenttext=''
# for item in content:
    
#     authors=content[item]['Author'].split(';')
#     authortext=''
#     for author in authors:
#         ret=re.match('<b>(\w+ \w+)</b>',author)
#         if ret is not None:
#             authortext+=', \textbf{%s}'%(ret.group(1))
#         else:
#             authortext+=', %s'%(author)
#         contenttext+='\vspace{1mm} \item %s. ``%s,'' \textit{%s}, %s. \href{%s}{\textcolor{link}{\scriptsize{\faLink} Link}}'%(
#             authortext,item,content[item]['PubTitle'],content[item]['Date'].split(',')[0],content[item]['Link'])

# ----------------------------
# Patent section
# ----------------------------
content=page_content['Publication']['Patent']
contenttext=''

for item in content:
    authors=content[item]['Author'].split('; ')
    authortext=''
    sptext=''
    for author in authors:
        ret=re.match('<b>(\w+ \w+)</b>',author)
        if ret is not None:
            authortext+=r'%s\textbf{%s}'%(sptext,ret.group(1))
        else:
            authortext+='%s%s'%(sptext,author)
        sptext=', '
    contenttext+=r"""\vspace{1mm} \item %s. ``%s,'' CN. Patent No. \textit{%s}, %s. \href{%s}{\textcolor{link}{\scriptsize{\faLink} Link}}
    """%(
        authortext,item,content[item]['Index'],content[item]['Date'].split(',')[0],content[item]['Link'].replace('https://patents.glgoo.top','https://patents.google.com'))

out=r"""
\vspace{1mm}
\cventry
{}
{\faChevronRight \ \ %s}
{\ }
{}
{\vspace{-4mm}
\begin{cvitemize2}
    %s\end{cvitemize2}
}
"""%('Patents',contenttext)
print(out)


# ----------------------------
# Award section
# ----------------------------
# contenttext=''
# for item in page_content['Reward']:
#     date=datetime.strptime(page_content['Reward'][item]['Date'], '%Y-%m')
#     item=item.replace(r'<span class="highlight"><b>',r'\textbf{')
#     item=item.replace(r'</b></span>',r'}')
#     item=item.replace(r'<b>',r'\hlbox{\textbf{')
#     item=item.replace(r'</b>',r'}}')
#     contenttext+=r"""\cvhonor{%s}{%s. %s}
#     """%(item,calendar.month_abbr[date.month],date.year)

# out=r"""
# \vspace{-4mm} 
# \cvsection{Awards and Honors}
# \begin{cvhonors}
# %s\end{cvhonors}
# """%(contenttext)

# print(out)