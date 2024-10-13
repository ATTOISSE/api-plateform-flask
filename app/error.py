from flask import jsonify, make_response

def success_response(data=None, message="Opération réussie", code=200):
    return make_response(jsonify({
        "success": True,
        "data": data,
        "message": message
    }), code)

def error_response(message="Une erreur s'est produite", code=500, details=None):
    return make_response(jsonify({
        "success": False,
        "error": message,
        "details": details
    }), code)

def handle_db_error(e):
    return error_response(message="Erreur serveur interne", details=str(e), code=500)

def handle_validation_error(ve):
    return error_response(message="Données invalides", details=ve.messages, code=400)

