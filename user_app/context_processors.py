from user_app.models import notification, chat_message, chat_conversation
from django.db.models import Q

def notifications_and_chats(request):
    unread_notif_count = 0
    unread_chat_count = 0
    
    if request.session.get('uid'):
        uid = str(request.session['uid'])
        unread_notif_count = notification.objects.filter(recipient_type='user', recipient_id=uid, is_read=False).count()
        unread_chat_count = chat_message.objects.filter(receiver_type='user', receiver_id=uid, is_read=False).count()
    elif request.session.get('bid'):
        bid = str(request.session['bid'])
        unread_notif_count = notification.objects.filter(recipient_type='builder', recipient_id=bid, is_read=False).count()
        unread_chat_count = chat_message.objects.filter(receiver_type='builder', receiver_id=bid, is_read=False).count()
    elif request.session.get('admin'):
        unread_notif_count = notification.objects.filter(recipient_type='admin', is_read=False).count()

    return {
        'unread_notif_count': unread_notif_count,
        'unread_chat_count': unread_chat_count,
    }
