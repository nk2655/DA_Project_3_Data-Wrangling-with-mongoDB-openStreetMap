# Calculate the percentage of contribution and find the tup N suers.
from pymongo import MongoClient

client = MongoClient()
db=client.project
number_document = db.doc.find().count()

def topn_contrib(n, user=False):
    if user==True:
        topuser=db.doc.aggregate([{'$group':{'_id':'$created.user', 'count':{'$sum':1}}}, 
                                 {'$sort':{'count':-1}}, {'$limit':n}
                                 ])
        top_n_users=[]
        for res in topuser:
            top_n_users.append(res['_id'])

    top_n_contrib=db.doc.aggregate([{'$group':{'_id':'$created.user', 'count':{'$sum':1}}}, 
                         {'$sort':{'count':-1}}, {'$limit':n},
                         {'$group':{'_id':'$created.user','total':{'$sum':'$count'}}}
                        ])

    for res in top_n_contrib:
        top_n_contrib_count=res['total']

    percent_contrib_topn=(top_n_contrib_count*100)/number_document
    
    if user==True:
        return top_n_users,percent_contrib_topn
    else:
        return percent_contrib_topn