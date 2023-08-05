"""
Everything that is always needed.

Not sure what that is for now.

Monitoring of method call timing?
"""


class Foo(dict):

    def bayes_update(self, data):

        for hypo in self:
            like = self.likelihood(data, hypo)

            self[hypo] *= like

        self.normalise()

    def normalise(self):

        total = sum(self.values)

        for k, v in self.items():

            self[k] /= total

    def likelihood(self, data, hypo):

        raise NotImplementedError
