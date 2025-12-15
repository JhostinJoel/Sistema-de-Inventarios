from .models import AuditLog

def get_client_ip(request):
    """Get the client IP address from the request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def log_action(user, action, model_name='', object_id='', description='', request=None):
    """
    Log a user action to the audit log.
    
    Args:
        user: User instance
        action: Action type (CREATE, UPDATE, DELETE, etc.)
        model_name: Name of the model being acted upon
        object_id: ID of the object
        description: Additional description
        request: HTTP request object (for IP address)
    """
    ip_address = None
    if request:
        ip_address = get_client_ip(request)
    
    AuditLog.objects.create(
        user=user,
        action=action,
        model_name=model_name,
        object_id=str(object_id),
        description=description,
        ip_address=ip_address
    )
