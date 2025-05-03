from app.services.sistema_regras import evaluate_rules

def get_chat_response(message):
    expert_answer = evaluate_rules(message)
    if expert_answer:
        return expert_answer
    return "Desculpe, não entendi. Pode reformular?"