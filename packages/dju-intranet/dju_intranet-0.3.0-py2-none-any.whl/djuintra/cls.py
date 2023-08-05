from collections import namedtuple


Schedule = namedtuple('Schedule', ('title', 'start', 'end', 'depart'))
TimePlace = namedtuple('TimePlace', ('time', 'place'))


class TimeTable(namedtuple('TimeTable', (
                           'grade', 'division', 'code', 'classcode',
                           'classtype', 'classname', 'score', 'time', 'minor',
                           'profname', 'times', 'maxstudents', 'available'))):
    """Named tuple for time table.

    :param grade: Required grade for the course
    :type grade: :class:`int`

    :param division: Liberal or major and somthing else
    :type division: :class:`str`

    :param code: Course code for registration
    :type code: :class:`str`

    :param classcode: Class number for registration
    :type classcode: :class:`str`

    :param classname: Name of the course
    :type classname: :class:`str`

    :param score: Credits
    :type score: :class:`int`

    :param time: how many time costs for this class for one week
    :type time: :class:`int`

    :param minor: Is it need to minor?
    :type minor: :class:`str`

    :param profname: The name of the professor
    :type profname: :class:`str`

    :param times: When is the class
    :type times: A set of :class:`TimePlace`

    :param maxstudents: How many students can listen this class
    :type maxstudents: :class:`int`

    :param available: Is this class available?
    :type available: :class:`str`

    """
    pass


class Scores(namedtuple('Scores', ('averagescore', 'semesters'))):
    """All personal scores.

    :param averagescore: Average score for you
    :type averagescore: :class:`float`

    :param semesters: A set of :class:`Semester`
    :type semesters: :class:`collections.Iterable`

    """
    pass


class Semester(namedtuple('Semester', ('title', 'scores'))):
    """Scores for the semester

    :param title: Title of the semester
    :type title: :class:`str`

    :param scores: A set of :class:`Score`
    :type scores: :class:`collections.Iterable`

    """
    pass


class Score(namedtuple('Score', ('code', 'title', 'point', 'score'))):
    """Personal scores data.

    :param code: Cource code
    :type code: :class:`str`

    :param title: Cource title
    :type title: :class:`str`

    :param point: Credits for course
    :type point: :class:`float`

    :param score: Your score
    :type score: :class:`str`

    """
    pass
