import base
from mongoengine import ValidationError
from datetime import datetime, timedelta
from bson.objectid import ObjectId

from app.models import Event, User
from mock import Mock, patch

class TestEvents(base.TestingTemplate):

    START = datetime.now()
    END = datetime.now() + timedelta(minutes=1)
    TITLE = 'Some Title'
    LOCATION = 'Some Location'
    SLUG = 'my-cool-event'

    @property
    def USER(self): 
        return User.objects().first()

    def make_event(self):
        return Event(title=self.TITLE,
                     creator=self.USER,
                     location=self.LOCATION,
                     slug=self.SLUG,
                     start_date=self.START.date(),
                     start_time=self.START.time(),
                     end_date=self.END.date(),
                     end_time=self.END.time())

    def setUp(self):
        Event.drop_collection()
        # for e in Event.objects():
        #     e.delete()
        super(TestEvents, self).setUp()

    def test_events_route_logged_in(self):
        """Test the `/admin/events` route, logged in."""
        resp = self.request_with_role('/admin/events', role='user')
        self.assertEqual(resp.status_code, 200)

    def test_events_route_logged_out(self):
        """Test the `/admin/events` route, logged out."""
        resp = self.request_with_role('/admin/events', role='none')
        self.assertEqual(resp.status_code, 302)

    def test_create_event_route_with_correct_privileges(self):
        """Test the `/admin/events/create` route, logged in with correct
        privileges.
        """
        resp = self.request_with_role('/admin/events/create', role='editor')
        self.assertEqual(resp.status_code, 200)

    def test_create_event_route_with_incorrect_privileges(self):
        """Test the `/admin/events/create` route, logged in with
        incorrect privileges.
        """
        resp = self.request_with_role('/admin/events/create', role='user')
        self.assertEqual(resp.status_code, 401)

    def test_create_event_route_logged_out(self):
        """Test the `/admin/events/create` route, logged out."""
        resp = self.request_with_role('/admin/events/create', role='none')
        self.assertEqual(resp.status_code, 302)

    def test_create_event_model_missing_title(self):
        """Test that creating an Event without a title fails."""
        with self.assertRaises(ValidationError):
            e = Event(creator=self.USER)
            e.save()

    def test_create_event_model_missing_creator(self):
        """Test that creating an Event without a creator fails."""
        with self.assertRaises(ValidationError):
            e = Event(title=self.TITLE)
            e.save()

    def test_create_event_model_with_backwards_dates(self):
        """Test creating an event with the start_datetime after the
        end_datetime.
        """
        # Good dates, bad times
        with self.assertRaises(ValidationError):
            e = Event(title=self.TITLE, creator=self.USER,
                      start_date=self.START.date(),
                      start_time=self.END.time(),
                      end_date=self.END.date(),
                      end_time=self.START.time())
            e.save()

        # Bad dates, good times
        with self.assertRaises(ValidationError):
            e = Event(title=self.TITLE, creator=self.USER,
                      start_date=self.END.date() + timedelta(days=1),
                      start_time=self.START.time(),
                      end_date=self.END.date(),
                      end_time=self.END.time())
            e.save()

    def test_event_start_datetimes(self):
        """Test that when events are created with both start_date and
        start_time, start_datetime() is their value combined.
        """
        e = Event(title=self.TITLE, creator=self.USER,
                  start_date=self.START.date(),
                  start_time=self.START.time())
        self.assertEqual(e.start_datetime(), self.START)


    def test_event_end_datetimes(self):
        """Test that when events are created with both end_date and
        end_time, end_datetime() is their value combined.
        """
        e = Event(title=self.TITLE, creator=self.USER,
                  end_date=self.END.date(),
                  end_time=self.END.time())
        self.assertEqual(e.end_datetime(), self.END)


    def test_event_start_datetimes_none_with_incomplete_data(self):
        """Test that when events are created without both of start_date and
        start_time, start_datetime() returns None.
        """
        e = Event(title=self.TITLE, creator=self.USER,
                  start_date=self.START.date())
        self.assertIsNone(e.start_datetime())

        f = Event(title=self.TITLE, creator=self.USER,
                  start_time=self.START.time())
        self.assertIsNone(f.start_datetime())

    def test_event_end_datetimes_none_with_incomplete_data(self):
        """Test that when events are created without both of end_date and
        end_time, end_datetime() returns None.
        """
        e = Event(title=self.TITLE, creator=self.USER,
                  end_date=self.END.date())
        self.assertIsNone(e.end_datetime())

        f = Event(title=self.TITLE, creator=self.USER,
                  end_time=self.END.time())
        self.assertIsNone(f.end_datetime())

    def test_create_event_model(self):
        """Test creating an event with the proper data"""
        self.assertEqual(Event.objects(creator=self.USER).count(), 0)
        e = self.make_event()
        e.save()
        self.assertEqual(Event.objects(creator=self.USER).count(), 1)
        self.assertEqual(Event.objects().get(creator=self.USER), e)

    def test_create_event_model_using_form(self):
        """Test creating an event by POSTing data to the `/admin/events/create`
        route.
        """
        query_string_data = {
            "title": "Test Title",
            "location": "45 Some Location",
            "start_date": "2014-02-15",
            "start_time": "12:15:00",
            "end_date": "2014-02-15",
            "end_time": "13:15:30",
            "short_description": "This is a short description.",
            "long_description": "This is a long description. It is longer"
        }

        self.assertEqual(Event.objects(location="45 Some Location").count(), 0)
        
        resp = self.request_with_role('/admin/events/create',
            method='POST',
            data=query_string_data,
            follow_redirects=True)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(Event.objects(location="45 Some Location").count(), 1)

    def test_create_event_model_using_form_without_title(self):
        """Test that POSTing event data to `/admin/events/create` without a title does
        not result in event creation.
        """

        bad_data = {
            "location": "45 Some Location",
            "start_date": "2014-02-15",
            "start_time": "12:15:00",
            "end_date": "2014-02-15",
            "end_time": "13:15:30",
            "short_description": "This is a short description.",
            "long_description": "This is a long description. It is longer"
        }

        self.assertEqual(Event.objects(location="45 Some Location").count(), 0)
        resp = self.request_with_role('/admin/events/create',
            method='POST',
            data=bad_data,
            follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(Event.objects(location="45 Some Location").count(), 0)

    def test_delete_event_when_event_exists(self):
        """Test that when an event with id `_id` exists in the database and the
        `/admin/events/delete/_id` route is POSTed to, it is deleted.
        """
        __import__('ipdb').set_trace()

        e = self.make_event()
        e.save()
        self.assertEqual(Event.objects(creator=e.creator).count(), 1)
        _id = e.id

        @patch('app.gcal_client')
        def test_initialization(self, mock_A):
        #with patch("app.gcal_client") as fake_gclient:
        # Mock A's do_something method
            mock_A.delete_event.return_value = None
            resp = self.request_with_role('/admin/events/delete/%s' % _id,
                                        method="POST",
                                        follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(Event.objects(creator=e.creator).count(), 0)


    def test_delete_event_when_event_does_not_exist(self):
        """Test that when an event with id `_id` exists in the database and the
        `/admin/events/delete/someotherid` route is POSTed to, it is deleted.
        """

        e = self.make_event()
        e.save()
        other_id = ObjectId()
        resp = self.request_with_role('/admin/events/delete/%s' % other_id, method="POST",
                               follow_redirects=True)
        self.assertIn('Invalid event id', resp.data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(Event.objects(creator=e.creator).count(), 1)

if __name__ == '__main__':
    base.TestingTemplate.main()
