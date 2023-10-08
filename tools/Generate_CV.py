# Load website data and change to CV Latex file
# This is only a test version

from markdown_to_json.vendor import CommonMark
from markdown_to_json.markdown_to_json import Renderer, CMarkASTNester
import json,re
from datetime import datetime
import calendar

inp_path='data/metadata_ZH.md'
lang='ZH'

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
# （和实际的latex不一样）
def research():
    content=page_content['Publication']['Research']
    contenttext=''
    for item in content:
        
        authors=content[item]['Author'].split(';')
        authortext=''
        for author in authors:
            ret=re.match('<b>(\w+ \w+)</b>',author)
            if ret is not None:
                authortext+=', \textbf{%s}'%(ret.group(1))
            else:
                authortext+=', %s'%(author)
            contenttext+='\vspace{1mm} \item %s. ``%s,'' \textit{%s}, %s. \href{%s}{\textcolor{link}{\scriptsize{\faLink} Link}}'%(
                authortext,item,content[item]['PubTitle'],content[item]['Date'].split(',')[0],content[item]['Link'])

# ----------------------------
# Patent section
# ----------------------------

def splitauthors(authors,maxnum=2):
    # 提取作者
    langtext={'ZH':['<b>(\S+)</b>','、','等'],
    'EN':['<b>(\w+ \w+)</b>',', ','et al.']}
    authortext=''
    sptext=''
    for author in authors:
        ret=re.match(langtext[lang][0],author)
        if ret is not None:
            authortext+=r'%s\textbf{%s}'%(sptext,ret.group(1))
        else:
            if authors.index(author)>maxnum or author==langtext[lang][2]:
                authortext+=langtext[lang][2]
                break
            authortext+='%s%s'%(sptext,author)
        sptext=langtext[lang][1]
    return authortext

def patents():
    langtext={'ZH':['发明专利','授权专利号：'],
    'EN':['Patents','CN. Patent No. ']}

    content=page_content['Publication']['Patent']
    contenttext=''

    for item in content:
        authortext=splitauthors(content[item]['Author'].split('; '))       
        contenttext+=r"""\vspace{1mm} \item %s. ``%s,''%s\textit{%s}. \href{%s}{\textcolor{link}{\scriptsize{\faLink}}}
        """%(
            authortext,item,langtext[lang][1],content[item]['Index'],content[item]['Link'])#,content[item]['Date'].split(',')[0] #.replace('https://patents.glgoo.top','https://patents.google.com')

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
    """%(langtext[lang][0],contenttext)
    return out

    
def softrights():
    langtext={'ZH':['软件著作权',' 版权登记号：'],
    'EN':['Software Copyright','CN. Copyright No. ']}

    content=page_content['Publication']['Software Copyright']
    contenttext=''

    for item in content:
        authortext=splitauthors(content[item]['Author'].split(';'))        
        contenttext+=r"""\vspace{1mm} \item %s. ``%s,''%s\textit{%s}.
        """%(
            authortext,item,langtext[lang][1],content[item]['Index'])

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
    """%(langtext[lang][0],contenttext)
    return out

# ----------------------------
# Award section
# ----------------------------
# （和实际的latex不一样）
def transdate(content):
    # 日期修正
    date=datetime.strptime(content, '%Y-%m')
    return '%s. %s'%(calendar.month_abbr[date.month],date.year)

def award():
    langtext={'ZH':['获奖荣誉'],
    'EN':['Awards and Honors']}
    contenttext=''
    for item in page_content['Reward']:
        datetext=transdate(page_content['Reward'][item]['Date'])
        item=item.replace(r'<span class="highlight"><b>',r'\textbf{')
        item=item.replace(r'</b></span>',r'}')
        item=item.replace(r'<b>',r'\hlbox{\textbf{')
        item=item.replace(r'</b>',r'}}')
        item=item.replace(r'&nbsp','')
        contenttext+=r"""\cvhonor{%s}{%s}
        """%(item,datetext)

    out=r"""
    \vspace{-4mm} 
    \cvsection{%s}
    \begin{cvhonors}
    %s\end{cvhonors}
    """%(langtext[lang][0],contenttext)
    return out

out=award()

with open('out.txt','wb') as f:
    f.write(out.encode('utf-8'))

# print(out)