from pages.models import ContactMessage, Blog, Service, ReferenceItem

def dashboard_callback(request, context):
    unread_messages = ContactMessage.objects.filter(is_read=False).count()
    total_messages = ContactMessage.objects.count()
    total_blogs = Blog.objects.count()
    total_services = Service.objects.count()
    total_references = ReferenceItem.objects.count()

    context.update({
        "custom_data": {
            "unread_messages": unread_messages,
            "total_messages": total_messages,
            "total_blogs": total_blogs,
            "total_services": total_services,
            "total_references": total_references,
        }
    })
    return context
