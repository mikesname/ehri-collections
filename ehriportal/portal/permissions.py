"""
Functions that govern user access. Mainly to be used by `user_passes_test`.
"""

def is_staff(user):
    return user.is_staff
