import rules


@rules.predicate
def test_rule():
    return True


# todo if user-app is finished. access restricted to active leaders and rent-managers
rules.add_perm('rent.access_rent_management', test_rule)

# todo if user-app is finished; access restricted to group leader and rental managers
rules.add_perm('rent.change_pricing', test_rule)
