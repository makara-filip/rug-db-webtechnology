from app import db
from app.api import api_blueprint
from app.api.auth import basic_auth, token_auth
from app.models import User

@api_blueprint.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    # flask-httpauth package will automatically set the user, via its config
    user: User = basic_auth.current_user()
    token = user.get_auth_token()
    db.session.commit()
    return { "token": token }

@api_blueprint.route('/tokens/revoke', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    user: User = token_auth.current_user()
    user.revoke_auth_token()
    db.session.commit()
    return None, 204
