# Page generator
# Update:2023/09/09 @LMR multiimages
# Update:2023/05/10 @LMR init
# pip install -r .\requirements.txt

from markdown_to_json.vendor import CommonMark
from markdown_to_json.markdown_to_json import Renderer, CMarkASTNester
import json,re
from datetime import datetime
import calendar

class PageGenerator():
    def __init__(self,inp_path,temp_path='tools/Template.html',lang='ZH',debug=False):
        """inp_path: Page Description(markdown)"""
        self.debug=debug
        self.lang=lang
        self.load_content(inp_path)
        self.load_template(temp_path)

    def _debug(self,text):
         if self.debug:
              print(text)
         
    def load_content(self,inp_path):
        """Load Page Description"""
        nester = CMarkASTNester()
        renderer = Renderer()
        with open(inp_path,'rb') as f:
            ast = CommonMark.DocParser().parse(f.read().decode('utf-8'))
            nested = nester.nest(ast)
            rendered = renderer.stringify_dict(nested)
        pagedata=json.loads(json.dumps(rendered))
        self._debug(pagedata)
        self.page_title=list(pagedata.keys())[0]
        self.page_content=pagedata[self.page_title]
    
    def load_template(self,temp_path):
        """Load HTML Page Template"""
        with open(temp_path,'rb') as f:
            self.pagetemp=f.read().decode('utf-8')
        self.change_languange()
    
    def pagereplace(self,key,value):
        """Replace Variable"""
        self.pagetemp=self.pagetemp.replace(key,value)
    
    def change_languange(self):
        """Language Setting"""
        lang_dict={
              'ZH':{
                r'{DOWNLOAD_LINK}':'下载简历',
                r'{PAGE_INDEX}':'index_EN.html',
                r'{LANGUAGE_VERSION}':'English Version',
                r'{CONTENT_TEXT}':'分栏导航',
                r'{NEWS_TEXT}':'近期动态',
                r'{EDUCATION_TEXT}':'教育背景',
                r'{PUBLICATION_TEXT}':'主要成果',
                r'{REWARD_TEXT}':'获奖荣誉',
                r'{EXPERIENCE_TEXT}':'科研经历',
                r'{RESEARCH_TEXT}':'研究论文',
                r'{PATENT_TEXT}':'专利',
                r'{COPYRIGHT_TEXT}':'软件著作权'
              },
              'EN':
              {
                r'{DOWNLOAD_LINK}':'Download CV',
                r'{PAGE_INDEX}':'index_CN.html',
                r'{LANGUAGE_VERSION}':'访问中文版',
                r'{CONTENT_TEXT}':'QUICK LINKS',
                r'{NEWS_TEXT}':'RECENT NEWS',
                r'{EDUCATION_TEXT}':'EDUCATION',
                r'{PUBLICATION_TEXT}':'PUBLICATION',
                r'{REWARD_TEXT}':'AWARD',
                r'{EXPERIENCE_TEXT}':'EXPERIENCE',
                r'{RESEARCH_TEXT}':'Research',
                r'{PATENT_TEXT}':'Patent',
                r'{COPYRIGHT_TEXT}':'Software Copyright'
              }
         }
        for key in lang_dict[self.lang]:
             self.pagereplace(key,lang_dict[self.lang][key])  
    
    def add_basicinf(self):
        """Add basic information section"""
        self.pagereplace(r'{TITLE}',self.page_title)
        self.pagereplace(r'{NAME}',self.page_content['Basic Information']['Name'])
        self.pagereplace(r'{NAME_TITLE}',self.page_content['Basic Information']['Title'])

        field_items=''
        for item in self.page_content['Basic Information']['Field']:
                field_items+="""
                <p class="text-muted" style="margin-bottom: 5px;text-align:left;"><span
                                class="ace-icon ace-icon-tag"></span>&nbsp;{0}</p>
                """.format(item)
        self.pagereplace(r'{FIELD}',field_items)

        contact_items=''
        for item in self.page_content['Basic Information']['Contact']:
            if item=='GITHUB':
                  urlr=re.compile("[\(](\S+)[\)]")
                  url=urlr.findall(self.page_content['Basic Information']['Contact'][item])[0]
                  unamer=re.compile("[\[](\w+)[\]]")
                  uname=unamer.findall(self.page_content['Basic Information']['Contact'][item])[0]
                  contact_items+="""
                  <li><a href="{0}" title="{0}" target="_blank"><span
                                class="ace-icon ace-icon-github"></span>&nbsp;{1}</a></li>
                  """.format(url,uname)
            elif item=='EMAIL':
                  contact_items+="""
                  <li><a href="mailto: {0}" title="{0}"><span
                                class="ace-icon ace-icon-contact"></span>&nbsp;{0}</a></li>
                    """.format(self.page_content['Basic Information']['Contact'][item])
        self.pagereplace(r'{CONTACT}',contact_items)

        if 'CV' in self.page_content['Basic Information']:
            self.pagereplace(r'{CV_LINK}',self.page_content['Basic Information']['CV'])
            self.pagereplace(r'{CV_CLICK}','')
        else:
            self.pagereplace(r'{CV_LINK}','javascript:void(0)')
            self.pagereplace(r'{CV_CLICK}','window.print()')                                            
    
    def add_education(self):
        """Add education section"""
        school_items=""
        for item in self.page_content['Education']:
            school_items+="""
            <div class="ref-box hreview">
                <div class="ref-avatar">
                    <img alt="" src="./data/media/{0}" class="avatar avatar-54 photo" height="54" width="54">
                </div>
            
                <div class="ref-info">
                    <div class="ref-author">
                        <strong>{1}</strong>
                        <span>{2}</span>
                    </div>
            
                    <blockquote class="ref-cont clear-mrg">
                        <p>
                            {3}
                        </p>
                    </blockquote>
                </div>
            </div><!-- end school -->
                """.format(self.page_content['Education'][item]['Image'],
                        item,
                        self.page_content['Education'][item]['Brief'],
                        self.page_content['Education'][item]['Detail'],
                        )
        self.pagereplace(r'{EDUCATION_DIV}',school_items)

    def add_publication(self,typ='Research'):
        """Add publication section"""
        content=self.page_content['Publication'][typ]
        publication_items=""
        for item in content:
            if typ=='Software Copyright':
                if 'Author' in content[item]:
                    authorinf=content[item]['Author']+r'&nbsp;|&nbsp;'
                else:
                    authorinf=''
                if self.lang=='ZH':
                    publication_items+="""
                                    <div class="ref-author">
                                        <strong><span class="ace-icon ace-icon-bookmark" style="display:inline-block;">&nbsp;&nbsp;<b>{0}</b>&nbsp;|&nbsp;{1}中国版权登记号:<a class="highlight" style="margin-left: 10px;">{2}</a></span></strong>
                                    </div>""".format(item,authorinf,content[item]['Index'])
                else:
                    publication_items+="""<div class="ref-author">
                                        <strong><span class="ace-icon ace-icon-bookmark" style="display:inline-block;"></span>&nbsp;&nbsp;{0}</strong>
                                        <span>{1}CN. Copyright No.<a class="highlight" style="margin-left: 10px;">{2}</a></span>
                                    </div>""".format(item,authorinf,content[item]['Index'])
            else:
                keywords=""
                for subitems in content[item]['Keywords']:
                        keywords+="""
                        <a class="tag">&#35; {0}</a>
                        """.format(subitems)
                actions=""
                for subitems in content[item]['Actions']:
                    tipnotes={'ZH':
                            {'PDF':['阅读论文','论文'],'VIDEO':['观看实验视频','视频'],'CODE':['下载程序代码','代码'],'DOC':['下载专利公告文件','公告文件']},
                            'EN':
                            {'PDF':['Read the paper','Paper'],'VIDEO':['Watch the experiment video','Video'],'CODE':['Download the program code','Code'],'DOC':['Download the document','Document']}
                    }
                    icons={'PDF':'file','VIDEO':'film','CODE':'folder','DOC':'file'}
                    actions+="""
                            <a href="{0}" target="_blank" title="{1}"><span class="ace-icon ace-icon-{2}"></span>{3}</a>
                        """.format(content[item]['Actions'][subitems],
                                    tipnotes[self.lang][subitems][0],icons[subitems],
                                    tipnotes[self.lang][subitems][1])
                if isinstance(content[item]['Image'],list):
                    imagecontent="""
                    <div class="swiper">
                        <div class="swiper-wrapper" style="width:330px;">"""
                    for img in content[item]['Image']:
                        imagecontent+="""
                        <div class="swiper-slide"><a class="post-thumbnail" href="./data/media/{0}" data-lightbox="image" data-title="{1}"> <img class="example-image" src="./data/media/{0}"
                                                                    alt="image" /></a></div>""".format(img,item+'_%d'%(content[item]['Image'].index(img)))
                    imagecontent+="""
                    </div>         
                        <div class="swiper-button-prev"></div>
                        <div class="swiper-button-next"></div>
                    </div>
                    """
                else:
                    imagecontent="""<a class="post-thumbnail" href="./data/media/{0}" data-lightbox="image" data-title="{1}"> <img class="example-image" src="./data/media/{0}"
                                            alt="image" /></a>""".format(content[item]['Image'],item)
                publication_items+="""
                                    <article class="post">
                                        {0}
                                        <div class="post-content">
                                            <h2 class="post-title"><a href="{2}" target="_blank">{1}</a></h2>
                                            <span class="post-date">{3}&nbsp;&nbsp;|&nbsp;&nbsp;{4}</span>
                                            <span class="post-highlight">{5}&nbsp;&nbsp;|&nbsp;&nbsp;{6}</span>
                                            <p>{7}</p>
                                            <div class="page-footer">
                                                <div class="page-tag">
                                                    {8}
                                                </div>
                                                <div class="page-share">
                                                    {9}
                                                </div>
                                            </div>
                                        </div>
                                    </article>
                """.format(
                        imagecontent,item,
                        content[item]['Link'],
                        content[item]['Author'],
                        content[item]['Date'],
                        content[item]['PubTitle'],
                        content[item]['Index'],
                        content[item]['Abstract'],
                        keywords,actions
                )
        if typ=='Research':
            self.pagereplace(r'{RESEARCH_DIV}',publication_items)
        elif typ=='Patent':
            self.pagereplace(r'{PATENT_DIV}',publication_items)
        elif typ=='Software Copyright':
            self.pagereplace(r'{COPYRIGHT_DIV}',publication_items)
    
    def add_timeline(self,typ='Reward'):
        """Add reward section"""
        reward_items=""
        for item in self.page_content[typ]:
            if len(self.page_content[typ][item]['Date'].split('-'))==2:
                date=datetime.strptime(self.page_content[typ][item]['Date'], '%Y-%m')
                daytext=''
            elif len(self.page_content[typ][item]['Date'].split('-'))==3:
                date=datetime.strptime(self.page_content[typ][item]['Date'], '%Y-%m-%d')
                daytext=' %d,'%(date.day)
            else:
                continue
            if 'Image' in self.page_content[typ][item]:
                if self.lang=='ZH':
                    imgcontent="""&nbsp;<a class="post-thumbnail" href="./data/media/{0}" data-lightbox="image" data-title="{1}" title="查看荣誉证书" style="color: rgb(38, 118, 229);">▛证书▟</a>""".format(
                        self.page_content[typ][item]['Image'],item.replace('<span class="highlight"><b>','').replace('</b></span>','')
                    )
                else:
                    imgcontent="""&nbsp;<a class="post-thumbnail" href="./data/media/{0}" data-lightbox="image" data-title="{1}" title="View certificate" style="color: rgb(38, 118, 229);">▛Cert.▟</a>""".format(
                        self.page_content[typ][item]['Image'],item.replace('<span class="highlight"><b>','').replace('</b></span>','')
                    )
            else:
                imgcontent=''

            reward_items+="""
                <div class="education-box">
                    <time class="education-date" datetime="{0}T{0}">
                        <span>{1} <strong class="text-upper">{2}</strong></span>
                    </time>
                    <h5 style="font-weight:inherit">{3}</h5>
                </div>
                """.format(self.page_content[typ][item]['Date'],
                        calendar.month_abbr[date.month]+daytext,
                        date.year,
                        item+imgcontent
                        )
            
        self.pagereplace(r'{%s_DIV}'%(typ.upper()),reward_items)
    
    def add_experiences(self):
        """Add experience section"""
        experience_items=""
        for item in self.page_content['Experience']:
            date_from=datetime.strptime(self.page_content['Experience'][item]['FromDate'], '%Y-%m')
            date_to=datetime.strptime(self.page_content['Experience'][item]['ToDate'], '%Y-%m')
            details=""
            for subitem in self.page_content['Experience'][item]['Detail']:
                details+="""<p><span class="ace-icon ace-icon-bookmark"></span>&nbsp;{0}</p>
                """.format(subitem)

            if 'Video' in self.page_content['Experience'][item]:
                tiptext={'EN':['Watch the Video','Video'],'ZH':['观看视频','观看视频']}
                videolink="""<hr style="margin-top: 15px;"/>
                <span class="highlight"><a href="{0}" target="_blank" title="{1}"><span class="ace-icon ace-icon-film"></span>{2}</a></span>""".format(
                    self.page_content['Experience'][item]['Video'],tiptext[self.lang][0],tiptext[self.lang][1])
            else:
                videolink=''
            
            imagecontent_v=''
            imagecontent_h=''
            imagecontent_e="""
            </div>         
                    <div class="swiper-button-prev"></div>
                    <div class="swiper-button-next"></div>
            </div>
            """

            if 'ImageV' in self.page_content['Experience'][item]:
                style_detail=r'width:60%;float:left;display:inline;'
                imagecontent_v="""
                <div class="swiper" style="width:39%;float:right;display:inline;margin-left:1px;">
                <div class="swiper-wrapper">
                """
                for img in self.page_content['Experience'][item]['ImageV']:
                    imagecontent_v+="""
                        <div class="swiper-slide"><a class="post-thumbnail" href="./data/media/{0}" data-lightbox="image" data-title="{1}"> <img class="example-image" src="./data/media/{0}"
                                                                    alt="image" /></a></div>""".format(img,item+'_%d'%(self.page_content['Experience'][item]['ImageV'].index(img)))
                imagecontent_v+=imagecontent_e
            else:
                style_detail=''
            
            if 'ImageH' in self.page_content['Experience'][item]:
                imagecontent_h="""
                <div class="swiper" style="width:60%;">
                <div class="swiper-wrapper">
                """
                for img in self.page_content['Experience'][item]['ImageH']:
                    imagecontent_h+="""
                        <div class="swiper-slide"><a class="post-thumbnail" href="./data/media/{0}" data-lightbox="image" data-title="{1}"> <img class="example-image" src="./data/media/{0}"
                                                                    alt="image" /></a></div>""".format(img,item+'_%d'%(self.page_content['Experience'][item]['ImageH'].index(img)))
                imagecontent_h+=imagecontent_e
            
            experience_items+="""
                <div class="education-box" id="{6}">
                    <time class="education-date" datetime="{0}T{1}">
                        <span>{2} <strong class="text-upper">{3}</strong> - {4} <strong
                                class="text-upper">{5}</strong></span>
                        {10}
                    </time>
                    <h4>{6}</h4>
                    <span
                        class="education-company">{7}&nbsp;&nbsp;|&nbsp;&nbsp;{8}</span>
                    <div style="{11}">
                        {9}
                        </div>
                        {12}
                        {13}
                </div>
                """.format(self.page_content['Experience'][item]['FromDate'],
                           self.page_content['Experience'][item]['ToDate'],
                           calendar.month_abbr[date_from.month],
                           date_from.year,
                           calendar.month_abbr[date_to.month],
                           date_to.year,
                            item,
                            self.page_content['Experience'][item]['Project'],
                            self.page_content['Experience'][item]['Title'],
                            details,videolink,style_detail,imagecontent_v,imagecontent_h
                        )
        self.pagereplace(r'{EXPERIENCE_DIV}',experience_items)
    
    def generate(self):
        """Generate the page"""
        self.add_basicinf()
        self.add_education()
        self.add_publication('Research')
        self.add_publication('Patent')
        self.add_publication('Software Copyright')
        self.add_timeline('Reward')
        self.add_timeline('News')
        self.add_experiences()
            
    def save(self,out_path):
         """Save the page"""
         self.pagereplace(r'{UPDATE_TIME}',datetime.now().strftime('%Y-%m-%d'))
         with open(out_path,'wb') as f:
            f.write(self.pagetemp.encode('utf-8'))

if __name__=='__main__':
    import sys,shutil,os
    pg=PageGenerator(sys.argv[1],'tools/Template.html',sys.argv[2])
    pg.generate()
    if len(sys.argv)==3:
        if os.path.exists('page')==False:
            os.mkdir('page')
        if sys.argv[2]=='ZH':
            pg.save('page/index_CN.html')
        elif sys.argv[3]=='EN':
            pg.save('page/index_EN.html')
        shutil.copy('index.html','page/index.html')
        if os.path.exists('page/styles')==False:
            shutil.copytree('styles','page/styles')
    else:
        pg.save(sys.argv[3])