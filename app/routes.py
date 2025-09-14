from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import User
from markupsafe import escape

main_bp = Blueprint("main", __name__)


@main_bp.route("/api/data", methods=["GET"])
@jwt_required()
def get_data():
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)

    return (
        jsonify(
            {
                "user_id": user.id,
                "username": escape(user.username),
                "message": "Добро пожаловать в защищенное API!",
            }
        ),
        200,
    )


@main_bp.route("/api/posts", methods=["POST"])
@jwt_required()
def create_post():
    data = request.get_json()
    title = data.get("title")
    content = data.get("content")

    if not title or not content:
        return jsonify({"msg": "Требуется title и content"}), 400

    return (
        jsonify(
            {"msg": "Пост создан", "title": escape(title), "content": escape(content)}
        ),
        201,
    )
