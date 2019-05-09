from .models import term , course,score,student,User,teacher,massege

def load_masseges(request):
    if not request.user.is_authenticated:
        return {}
    m = massege.objects.filter(to = request.user)
    mlist = []
    counter = 0
    unseen = 0
    for ma in m:
        if counter <3 :
            mlist.append({'id':counter,'origin':ma.origin.get_full_name(),'title':ma.subject,'text':ma.text,'time_sent':{'h':ma.time_sent.hour,'m':ma.time_sent.minute},'date_sent':ma.date_sent})
            counter+=1
        if not ma.seen:
            unseen+=1
    mlist.reverse()
    data = {
        'unseen' : unseen,
        'top_masseges' :mlist,
    }
    return data
