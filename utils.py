import sqlite3
from newspaper import Article
import newspaper

def get_all(query):
    conn = sqlite3.connect("SQL/newDB.db")
    data = conn.execute(query).fetchall()
    conn.close()

    return data
def get_news_by_id(news_id):
    conn = sqlite3.connect("SQL/newDB.db")
    sql='''
    
    SELECT N.subject,N.description, N.image,N.original_url,C.name,C.url
    FROM new N INNER JOIN catergory C ON N.category_id=C.id 
    WHERE id=?
    '''
    news = conn.execute(sql, (news_id, )).fetchone()
    conn.close()

    return news

def add_news(conn,url,category_id):
    sql='''
     INSERT INTO new (subject,description, image , original_url , category_id)
     VALUES (?, ?, ?, ? ,?)
    '''
    article = Article(url)
    article.download()
    article.parse()

    return conn.execute(sql, (article.title, article.text, 
    article.top_image, article.url, category_id))

    conn.commit()



def get_news_url():
    cats = get_all("SELECT * FROM category")
    conn = sqlite3.connect("SQL/newDB.db")
    for cat in cats:
        cat_id = cat[0]
        url = cat [2]
        cat_paper = newspaper.build(url)
        for article in cat_paper.articles:
         try:
            print("=== ", article.url)
            add_news(conn, article.url ,cat_id)
         except Exception as ex:
            print ("Error" + str(ex))
            pass
    
    conn.close()


if __name__=="__main__":
    get_news_url ()
    # print(get_all("SELECT * FROM category"))