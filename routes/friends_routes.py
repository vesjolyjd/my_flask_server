from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from models import User, Friendship

friends_bp = Blueprint('friends', __name__)

@friends_bp.route('/friends')
@login_required
def friends_list():
    """Страница со списком друзей"""
    friends = current_user.get_friends()
    pending_requests = current_user.get_pending_requests()
    sent_requests = current_user.get_sent_requests()
    
    return render_template('friends.html', 
                         friends=friends,
                         pending_requests=pending_requests,
                         sent_requests=sent_requests)

@friends_bp.route('/search-users')
@login_required
def search_users():
    """Страница поиска пользователей"""
    query = request.args.get('query', '')
    users = []
    
    if query:
        users = User.query.filter(
            User.username.ilike(f'%{query}%'),
            User.id != current_user.id
        ).limit(20).all()
    
    return render_template('search_users.html', 
                         users=users, 
                         query=query)

@friends_bp.route('/send-friend-request/<int:user_id>')
@login_required
def send_friend_request(user_id):
    """Отправка заявки в друзья"""
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        flash('Нельзя отправить заявку самому себе!', 'danger')
        return redirect(url_for('friends.search_users'))
    
    if current_user.is_friends_with(user):
        flash(f'Вы уже друзья с {user.username}!', 'info')
        return redirect(url_for('friends.search_users'))
    
    if current_user.has_sent_request_to(user):
        flash(f'Вы уже отправили заявку {user.username}!', 'warning')
        return redirect(url_for('friends.search_users'))
    
    if current_user.has_pending_request_from(user):
        flash(f'У вас есть входящая заявка от {user.username}!', 'warning')
        return redirect(url_for('friends.friends_list'))
    
    # Создаем заявку
    friendship = Friendship(sender_id=current_user.id, receiver_id=user.id)
    db.session.add(friendship)
    db.session.commit()
    
    flash(f'Заявка в друзья отправлена {user.username}!', 'success')
    return redirect(url_for('friends.search_users'))

@friends_bp.route('/accept-friend-request/<int:request_id>')
@login_required
def accept_friend_request(request_id):
    """Принятие заявки в друзья"""
    friendship = Friendship.query.get_or_404(request_id)
    
    if friendship.receiver_id != current_user.id:
        flash('У вас нет прав для этого действия!', 'danger')
        return redirect(url_for('friends.friends_list'))
    
    friendship.status = 'accepted'
    db.session.commit()
    
    flash(f'Вы теперь друзья с {friendship.sender.username}!', 'success')
    return redirect(url_for('friends.friends_list'))

@friends_bp.route('/reject-friend-request/<int:request_id>')
@login_required
def reject_friend_request(request_id):
    """Отклонение заявки в друзья"""
    friendship = Friendship.query.get_or_404(request_id)
    
    if friendship.receiver_id != current_user.id:
        flash('У вас нет прав для этого действия!', 'danger')
        return redirect(url_for('friends.friends_list'))
    
    db.session.delete(friendship)
    db.session.commit()
    
    flash('Заявка в друзья отклонена.', 'info')
    return redirect(url_for('friends.friends_list'))

@friends_bp.route('/cancel-friend-request/<int:request_id>')
@login_required
def cancel_friend_request(request_id):
    """Отмена отправленной заявки"""
    friendship = Friendship.query.get_or_404(request_id)
    
    if friendship.sender_id != current_user.id:
        flash('У вас нет прав для этого действия!', 'danger')
        return redirect(url_for('friends.friends_list'))
    
    db.session.delete(friendship)
    db.session.commit()
    
    flash('Заявка в друзья отменена.', 'info')
    return redirect(url_for('friends.friends_list'))

@friends_bp.route('/remove-friend/<int:friend_id>')
@login_required
def remove_friend(friend_id):
    """Удаление из друзей"""
    friend = User.query.get_or_404(friend_id)
    
    # Ищем дружбу в обоих направлениях
    friendship1 = Friendship.query.filter_by(
        sender_id=current_user.id, 
        receiver_id=friend.id,
        status='accepted'
    ).first()
    
    friendship2 = Friendship.query.filter_by(
        sender_id=friend.id, 
        receiver_id=current_user.id,
        status='accepted'
    ).first()
    
    friendship = friendship1 or friendship2
    
    if not friendship:
        flash('Этот пользователь не в вашем списке друзей!', 'danger')
        return redirect(url_for('friends.friends_list'))
    
    db.session.delete(friendship)
    db.session.commit()
    
    flash(f'{friend.username} удален из друзей.', 'info')
    return redirect(url_for('friends.friends_list'))