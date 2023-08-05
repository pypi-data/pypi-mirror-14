import CoreLocation
import arrow
import plistlib
import time
import tzlocal
import uuid
import os.path
import datetime


class DayOneEntry(object):
    def __init__(self, text=None, starred=False, tags=None):
        self.tags = tags or []
        self.starred = starred
        self.text = text
        # We default to now time. Override it if needed
        self._time = arrow.utcnow().format('YYYY-MM-DDTHH:mm:ssz')
        self.lat = None
        self.lon = None
        self.starred = None
        self.tags = []
        self.text = None
        self._uuid = None
        self._tz = None
        self.location = {}


    @property
    def tz(self):
        """Return the timezone. If none is set use system timezone"""
        if not self._tz:
            self._tz = tzlocal.get_localzone().zone
        return self._tz


    @tz.setter
    def tz(self, timezone):
        self._tz = timezone
    

    def add_tag(self, _tags):
        """Add tag(s) to a DayOneEntry"""
        if isinstance(_tags, list):
            for t in _tags:
                self.tags.append(t)
        else:
            self.tags.append(_tags)

    @property
    def uuid(self):
        """Return _uuid"""
        return self._uuid


    @uuid.setter
    def uuid(self, value):
        """ Set _uuid to specified value"""
        self._uuid = value


    @property
    def time(self):
        """Return the DayOneEntry's time"""
        return self._time


    @time.setter
    def time(self, t):
        """Convert any timestamp into a datetime and save as _time"""
        _time = arrow.get(t).format('YYYY-MM-DDTHH:mm:ss')
        self._time = datetime.datetime.strptime(_time, '%Y-%m-%dT%H:%M:%S')


    def as_dict(self):
        """Return a dict that represents the DayOneEntry"""
        entry_dict = {}
        entry_dict['UUID'] = self.uuid
        entry_dict['Creation Date'] = self.time
        entry_dict['Time Zone'] = self.tz
        entry_dict['Tags'] = self.tags
        entry_dict['Entry Text'] = self.text
        entry_dict['Starred'] = self.starred
        entry_dict['Location'] = self.location
        return entry_dict


class DayOne(object):
    def __init__(self, dayone_journal_path=None):
        self.dayone_journal_path = dayone_journal_path
        self._location_manager = CoreLocation.CLLocationManager.alloc().init()
        self._location_manager.delegate()

    def get_location(self):
        self._location_manager.startUpdatingLocation()
        loc = None
        while loc is None:
            loc = self._location_manager.location()
            time.sleep(0.25)
        coord = loc.coordinate()
        self._location_manager.stopUpdatingLocation()
        lat, lon = coord.latitude, coord.longitude

        loc = {
            "Latitude": lat,
            "Longitude": lon
        }

        return loc


    def save(self, entry, with_location=True, debug=False):
        """Saves a DayOneEntry as a plist"""
        entry_dict = {}
        if isinstance(entry, DayOneEntry):
            # Get a dict of the DayOneEntry
            entry_dict = entry.as_dict()
        else:
            entry_dict = entry
        
        # Set the UUID
        entry_dict['UUID'] = uuid.uuid4().get_hex()
        if with_location and not entry_dict['Location']:
            entry_dict['Location'] = self.get_location()


        # Do we have everything needed?
        if not all ((entry_dict['UUID'], entry_dict['Time Zone'],
                     entry_dict['Entry Text'])):
            print "You must provide: Time zone, UUID, Creation Date, Entry Text"
            return False

        if debug is False:
            file_path = self._file_path(entry_dict['UUID'])
            plistlib.writePlist(entry_dict, file_path)
        else:
            plist = plistlib.writePlistToString(entry_dict)
            print plist

        return True


    def _file_path(self, uid):
        """Create and return full file path for DayOne entry"""
        file_name = '%s.doentry' % (uid)
        return os.path.join(self.dayone_journal_path, file_name)

