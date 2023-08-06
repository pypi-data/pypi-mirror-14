class DictDiffer(object):
    """
    Calculate the difference between two dictionaries as:
    (1) keys added
    (2) keys removed
    (3) keys same in both but changed values
    (4) keys same in both and unchanged values
    """

    def __init__(self, current_dict, past_dict):
        self.current_dict, self.past_dict = current_dict, past_dict
        self.set_current, self.set_past = set(current_dict.keys()), set(past_dict.keys())
        self.intersect = self.set_current.intersection(self.set_past)

    def added(self):
        """

        :return: set of keys
        """
        return self.set_current - self.intersect

    def removed(self):
        """

        :return: set of keys
        """
        return self.set_past - self.intersect

    def changed(self):
        """

        :return: set of keys
        """
        return set(o for o in self.intersect if self.past_dict[o] != self.current_dict[o])

    def unchanged(self):
        """

        :return: set of keys
        """
        return set(o for o in self.intersect if self.past_dict[o] == self.current_dict[o])

class ListDiffer(DictDiffer):
    """
    Calculate the difference between two dictionaries as:
    (1) indexes added
    (2) indexes removed
    (3) indexes same in both but changed values
    (4) indexes same in both and unchanged values
    """

    @staticmethod
    def list_to_dict(l):
        return {i: v for i, v in enumerate(l)}

    def __init__(self, current_list, past_list):
        current_dict = self.list_to_dict(current_list)
        past_dict = self.list_to_dict(past_list)
        super(ListDiffer, self).__init__(current_dict, past_dict)
