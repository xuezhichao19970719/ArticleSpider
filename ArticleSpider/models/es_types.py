from elasticsearch_dsl import Text, Date, Keyword, Integer, DocType, Completion
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import analyzer

connections.create_connection(hosts=['localhost'])

my_analyzer = analyzer('ik_smart')

class ArticleType(DocType):
    # 伯乐在线文章类型
    建议 = Completion(analyzer=my_analyzer)
    标题 = Text(analyzer="ik_max_word")
    创建日期 = Date()
    文章url = Keyword()
    文章url_md5 = Keyword()
    文章封面图url = Keyword()
    点赞数 = Integer()
    收藏数 = Integer()
    评论数 = Integer()
    类型列表 = Text(analyzer="ik_max_word")
    文章内容 = Text(analyzer="ik_smart")

    class Meta:
        index = "jobbole"
        doc_type = "article"

if __name__ == "__main__":
    ArticleType.init()

class LagouType(DocType):
    # 伯乐在线文章类型
    建议 = Completion(analyzer=my_analyzer)
    招聘职位名称 = Text(analyzer="ik_max_word")
    招聘页面url = Keyword()
    招聘页面url_md5 = Keyword()
    职位薪水 = Keyword()
    需求工作经验 = Keyword()
    需求学历 = Keyword()
    工作类型 = Keyword()
    工作标签 = Text(analyzer="ik_max_word")
    招聘发布时间 = Date()
    职位描述 = Text(analyzer="ik_smart")
    工作地址 = Text(analyzer="ik_max_word")
    公司名称 = Text(analyzer="ik_max_word")
    公司网址 = Keyword()

    class Meta:
        index = "lagou"
        doc_type = "job"

if __name__ == "__main__":
    LagouType.init()

class ChemicalBookType(DocType):
    # 伯乐在线文章类型
    建议 = Completion(analyzer=my_analyzer)
    CAS = Keyword()
    中文名称 = Text(analyzer="ik_max_word")
    英文名称 = Text(analyzer="ik_max_word")
    化学式 = Keyword()
    化学结构式图片url = Keyword()

    class Meta:
        index = "ChemicalBook"
        doc_type = "chemical"

if __name__ == "__main__":
    ChemicalBookType.init()