from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from app.models import User, Post, Comment

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
posts_bp = Blueprint('posts', __name__, url_prefix='/api/posts')
users_bp = Blueprint('users', __name__, url_prefix='/api/users')


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not all(k in data for k in ['username', 'email', 'password']):
        return {'error': 'Missing fields'}, 400

    if User.query.filter_by(username=data['username']).first():
        return {'error': 'Username exists'}, 409

    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()

    return user.to_dict(), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    if not user or not user.check_password(data['password']):
        return {'error': 'Invalid credentials'}, 401

    token = create_access_token(identity=user.id)
    return {'access_token': token, 'user': user.to_dict()}, 200


@posts_bp.route('', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    return {'posts': [p.to_dict() for p in posts]}, 200


@posts_bp.route('', methods=['POST'])
@jwt_required()
def create_post():
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data or 'title' not in data or 'content' not in data:
        return {'error': 'Missing fields'}, 400

    post = Post(title=data['title'], content=data['content'],
                user_id=user_id)
    db.session.add(post)
    db.session.commit()

    return post.to_dict(), 201


@posts_bp.route('/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return post.to_dict(), 200


@posts_bp.route('/<int:post_id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):
    user_id = get_jwt_identity()
    post = Post.query.get_or_404(post_id)

    if post.user_id != user_id:
        return {'error': 'Unauthorized'}, 403

    data = request.get_json()
    post.title = data.get('title', post.title)
    post.content = data.get('content', post.content)
    db.session.commit()

    return post.to_dict(), 200


@posts_bp.route('/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    user_id = get_jwt_identity()
    post = Post.query.get_or_404(post_id)

    if post.user_id != user_id:
        return {'error': 'Unauthorized'}, 403

    db.session.delete(post)
    db.session.commit()

    return {'deleted': post_id}, 204


@posts_bp.route('/<int:post_id>/comments', methods=['POST'])
@jwt_required()
def add_comment(post_id):
    user_id = get_jwt_identity()
    Post.query.get_or_404(post_id)
    data = request.get_json()

    if not data or 'content' not in data:
        return {'error': 'Missing content'}, 400

    comment = Comment(content=data['content'], user_id=user_id,
                      post_id=post_id)
    db.session.add(comment)
    db.session.commit()

    return comment.to_dict(), 201


@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    user_data = user.to_dict()
    user_data['posts'] = [p.to_dict() for p in user.posts]
    return user_data, 200


@users_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    current_user_id = get_jwt_identity()

    if current_user_id != user_id:
        return {'error': 'Unauthorized'}, 403

    user = User.query.get_or_404(user_id)
    data = request.get_json()

    user.bio = data.get('bio', user.bio)
    db.session.commit()

    return user.to_dict(), 200
