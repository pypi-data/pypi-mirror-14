from rest_framework.throttling import ScopedRateThrottle


class ScopedActionRateThrottle(ScopedRateThrottle):

    def __call__(self, *args, **kwargs):
        return self

    def __init__(self, action, scope):
        self.action = action
        self.scope_attr = 'throttle_{}_{}_scope'.format(action, scope)

    def allow_request(self, request, view):
        if view.action == self.action:
            return super(ScopedActionRateThrottle, self).allow_request(request, view)

        return True
