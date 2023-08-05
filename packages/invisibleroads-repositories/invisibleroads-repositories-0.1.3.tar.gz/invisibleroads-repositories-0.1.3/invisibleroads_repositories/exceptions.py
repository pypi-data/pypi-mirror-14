from invisibleroads_macros.exceptions import InvisibleRoadsError


class BadCommitHash(InvisibleRoadsError):
    pass


class BadRepository(InvisibleRoadsError):
    pass


class BadRepositoryURL(InvisibleRoadsError):
    pass


class BadURL(InvisibleRoadsError):
    pass
