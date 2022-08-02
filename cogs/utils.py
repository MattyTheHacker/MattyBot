def has_role(self, user, role_id):
    return role_id in [role.id for role in user.roles]
