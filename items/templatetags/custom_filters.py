from django import template

register = template.Library()


@register.filter
def badge_class(value):
    """Return CSS badge class based on item type, status, or claim status."""
    badge_map = {
        'lost': 'badge-lost',
        'found': 'badge-found',
        'active': 'badge-active',
        'claimed': 'badge-claimed',
        'closed': 'badge-closed',
        'pending': 'badge-pending',
        'approved': 'badge-approved',
        'rejected': 'badge-rejected',
    }
    return badge_map.get(value, '')


@register.filter
def item_icon(category):
    """Return an emoji icon for item categories."""
    icon_map = {
        'electronics': '📱',
        'documents': '📄',
        'clothing': '👕',
        'accessories': '⌚',
        'keys': '🔑',
        'bags': '👜',
        'others': '📦',
    }
    return icon_map.get(category, '📦')
