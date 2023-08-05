from action import Action


class ActionManager(object):

    @classmethod
    def get_action(cls, action):
        return cls.action_table.get(action)

    action_table = {'describe-instances': Action.DescribeInstancesAction,
                    'terminate-instances': Action.TerminateInstancesAction,
                    'run-instances': Action.RunInstancesAction}
