from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Item, ClaimRequest
from .forms import ItemForm, ClaimForm, ItemSearchForm


def home(request):
    """Landing page with recent items."""
    recent_lost = Item.objects.filter(item_type='lost', status='active')[:4]
    recent_found = Item.objects.filter(item_type='found', status='active')[:4]
    total_items = Item.objects.count()
    total_lost = Item.objects.filter(item_type='lost').count()
    total_found = Item.objects.filter(item_type='found').count()
    total_claimed = Item.objects.filter(status='claimed').count()
    context = {
        'recent_lost': recent_lost,
        'recent_found': recent_found,
        'total_items': total_items,
        'total_lost': total_lost,
        'total_found': total_found,
        'total_claimed': total_claimed,
    }
    return render(request, 'home.html', context)


def item_list(request):
    """Browse all items with search and filter."""
    form = ItemSearchForm(request.GET)
    items = Item.objects.filter(status='active')

    if form.is_valid():
        q = form.cleaned_data.get('q')
        category = form.cleaned_data.get('category')
        item_type = form.cleaned_data.get('item_type')

        if q:
            items = items.filter(Q(title__icontains=q) | Q(description__icontains=q) | Q(location__icontains=q))
        if category:
            items = items.filter(category=category)
        if item_type:
            items = items.filter(item_type=item_type)

    paginator = Paginator(items, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'form': form,
        'total_results': items.count(),
    }
    return render(request, 'items/item_list.html', context)


def item_detail(request, pk):
    """View full item details."""
    item = get_object_or_404(Item, pk=pk)
    user_has_claimed = False
    if request.user.is_authenticated:
        user_has_claimed = item.claims.filter(claimant=request.user).exists()

    context = {
        'item': item,
        'user_has_claimed': user_has_claimed,
    }
    return render(request, 'items/item_detail.html', context)


@login_required
def item_create(request):
    """Post a new lost/found item."""
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            messages.success(request, 'Item posted successfully!')
            return redirect('item_detail', pk=item.pk)
    else:
        form = ItemForm()
    return render(request, 'items/item_form.html', {'form': form, 'action': 'Post'})


@login_required
def item_edit(request, pk):
    """Edit own item."""
    item = get_object_or_404(Item, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item updated successfully!')
            return redirect('item_detail', pk=item.pk)
    else:
        form = ItemForm(instance=item)
    return render(request, 'items/item_form.html', {'form': form, 'action': 'Edit'})


@login_required
def item_delete(request, pk):
    """Delete own item."""
    item = get_object_or_404(Item, pk=pk, user=request.user)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Item deleted successfully!')
        return redirect('my_items')
    return render(request, 'items/item_confirm_delete.html', {'item': item})


@login_required
def my_items(request):
    """Dashboard of user's own items."""
    items = Item.objects.filter(user=request.user)
    context = {'items': items}
    return render(request, 'items/my_items.html', context)


@login_required
def submit_claim(request, pk):
    """Submit a claim on an item."""
    item = get_object_or_404(Item, pk=pk)

    if item.user == request.user:
        messages.error(request, 'You cannot claim your own item!')
        return redirect('item_detail', pk=pk)

    if item.status != 'active':
        messages.error(request, 'This item is no longer active.')
        return redirect('item_detail', pk=pk)

    if item.claims.filter(claimant=request.user).exists():
        messages.warning(request, 'You have already submitted a claim for this item.')
        return redirect('item_detail', pk=pk)

    if request.method == 'POST':
        form = ClaimForm(request.POST)
        if form.is_valid():
            claim = form.save(commit=False)
            claim.item = item
            claim.claimant = request.user
            claim.save()
            messages.success(request, 'Claim submitted successfully! The owner will review your claim.')
            return redirect('item_detail', pk=pk)
    else:
        form = ClaimForm()

    context = {'form': form, 'item': item}
    return render(request, 'items/submit_claim.html', context)


@login_required
def manage_claims(request, pk):
    """Item owner views claims on their item."""
    item = get_object_or_404(Item, pk=pk, user=request.user)
    claims = item.claims.all()
    context = {'item': item, 'claims': claims}
    return render(request, 'items/manage_claims.html', context)


@login_required
def update_claim(request, pk):
    """Approve or reject a claim."""
    claim = get_object_or_404(ClaimRequest, pk=pk)

    if claim.item.user != request.user:
        messages.error(request, 'You are not authorized to manage this claim.')
        return redirect('home')

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            claim.status = 'approved'
            claim.save()
            claim.item.status = 'claimed'
            claim.item.save()
            # Reject all other pending claims
            claim.item.claims.filter(status='pending').exclude(pk=claim.pk).update(status='rejected')
            messages.success(request, f'Claim by {claim.claimant.username} has been approved!')
        elif action == 'reject':
            claim.status = 'rejected'
            claim.save()
            messages.success(request, f'Claim by {claim.claimant.username} has been rejected.')

    return redirect('manage_claims', pk=claim.item.pk)
