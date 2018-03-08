'''
notify_telegram - a simple notification-daemon with telegram backend.
'''

import configparser
import dbus
import dbus.service
import dbus.mainloop.glib
from gi.repository import GLib
import telegram


def read_config(path):
    ''' produce config values from a file '''
    conf = configparser.RawConfigParser()
    conf.read(path)
    return int(conf.get('general', 'recipient')), conf.get('general', 'token')


class NotificationFetcher(dbus.service.Object):
    ''' interface to dbus notifications '''

    def __init__(self, *args, **kwargs):
        ''' constructor '''
        self._id = 0
        self._recipient, self._token = read_config('/etc/notify_telegram.conf')
        self._bot = telegram.Bot(token=self._token)
        super(NotificationFetcher, self).__init__(*args, **kwargs)

    _method = "org.freedesktop.Notifications"
    @dbus.service.method(_method, in_signature='susssasa{ss}i', out_signature='u')
    def Notify(self, app_name, notification_id, app_icon,
               summary, body, actions, hints, expire_timeout):
        # pylint: disable=invalid-name,too-many-arguments
        ''' this is called when we get a new notification '''

        try:
            self._id += 1
            notification_id = self._id

            urgency = int(hints['urgency']) if 'urgency' in hints else 1

            icon = ""
            if hints.get('category', None) == 'error':
                icon = "\U0001F6A8 "
            if hints.get('category', None) == 'success':
                icon = "\U00002705 "

            text = icon + ("%s %s" % (summary, body)).strip()

            if 'document' in hints:
                print(self._bot.sendDocument(
                    self._recipient,
                    open(hints['document'], 'rb'),
                    caption=text,
                    parse_mode=telegram.ParseMode.MARKDOWN,
                    disable_notification=(urgency == 0)))
            else:
                print(self._bot.sendMessage(
                    self._recipient,
                    text,
                    parse_mode=telegram.ParseMode.MARKDOWN,
                    disable_notification=(urgency == 0)))

            return notification_id
        except Exception as e:
            print(e)

    @dbus.service.method(_method, in_signature='', out_signature='ssss')
    def GetServerInformation(self):
        # pylint: disable=invalid-name,no-self-use
        ''' identify our server '''
        return ("notify-telegram", "http://example.com", "0.1", "1")


def main():
    ''' main entry point '''
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    session = dbus.SessionBus()
    _ = dbus.service.BusName("org.freedesktop.Notifications", session)
    NotificationFetcher(session, '/org/freedesktop/Notifications')

    try:
        GLib.MainLoop().run()
    except KeyboardInterrupt:
        GLib.MainLoop().quit()


if __name__ == '__main__':
    main()
