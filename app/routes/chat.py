from flask import Blueprint, request, jsonify
from app.services.chat_service import get_chat_response

bp = Blueprint("chat", __name__, url_prefix="/chat")

# recebe a mensagem do usuário e retorna a resposta do modelo

@bp.route("", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message")
    response = get_chat_response(message)
    return jsonify({'response': response})