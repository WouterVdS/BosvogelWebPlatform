import rules


@rules.predicate
def test_rule_true():
    return True


@rules.predicate
def test_rule_false():
    return False


# todo if user-app is finished
"""
    To access rent management one must be:
    Leader
    rent manager (can be old-leader)
"""
rules.add_perm('rent.access_rent_management', test_rule_true)

# todo if user-app is finished
"""

    To change pricing one must be:
    Group leader (groepsleider)
    Rental manager (verhuurbeheerder)
"""
rules.add_perm('rent.change_pricing', test_rule_true)
