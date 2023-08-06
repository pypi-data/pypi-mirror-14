import logging
import os
import sys

from .scrapers.coursefinder import CourseFinder
from .scrapers.utmtimetable import UTMTimetable
from .scrapers.utsctimetable import UTSCTimetable
from .scrapers.utsgtimetable import UTSGTimetable
from .scrapers.utsgcalendar import UTSGCalendar
from .scrapers.buildings import Buildings
from .scrapers.food import Food
from .scrapers.textbooks import Textbooks

class NullHandler(logging.Handler):
    def emit(self, record):
        pass

logging.getLogger("uoftscrapers").addHandler(NullHandler())
