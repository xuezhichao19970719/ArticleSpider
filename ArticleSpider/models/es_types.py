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