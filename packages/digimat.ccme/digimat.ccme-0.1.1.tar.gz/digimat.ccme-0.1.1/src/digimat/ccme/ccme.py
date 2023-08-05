import requests

   # 40  -rw-        8160  Aug 20 2004 06:58:00 +02:00  Analog1.raw
   # 41  -rw-        8160  Aug 20 2004 06:58:00 +02:00  Analog2.raw
   # 42  -rw-        5280  Aug 20 2004 06:58:00 +02:00  AreYouThere.raw
   # 43  -rw-        5040  Aug 20 2004 06:58:00 +02:00  AreYouThereF.raw
   # 44  -rw-        8160  Aug 20 2004 06:58:00 +02:00  Bass.raw
   # 45  -rw-        6334   Sep 5 2006 14:38:36 +02:00  BEEPBEEP.RAW
   # 46  -rw-       12240  Aug 20 2004 06:58:00 +02:00  CallBack.raw
   # 47  -rw-       16040  Aug 20 2004 06:58:00 +02:00  Chime.raw
   # 48  -rw-        8160  Aug 20 2004 06:58:00 +02:00  Classic1.raw
   # 49  -rw-       16080  Aug 20 2004 06:58:00 +02:00  Classic2.raw
   # 50  -rw-       10800  Aug 20 2004 06:58:00 +02:00  ClockShop.raw
   # 51  -rw-       10220   Sep 5 2006 14:30:20 +02:00  CTU.RAW
   # 52  -rw-       16080   Sep 5 2006 14:30:16 +02:00  CTU24.RAW
   # 53  -rw-       12966   Sep 5 2006 14:38:48 +02:00  CUCKOO2.RAW
   # 54  -rw-         495  Mar 17 2006 00:27:34 +02:00  DistinctiveRingList.xml
   # 55  -rw-       15243   Sep 5 2006 14:38:54 +02:00  DIVE.RAW
   # 56  -rw-       14000   Sep 5 2006 14:38:58 +02:00  doorbell2.raw
   # 57  -rw-       14256   Sep 5 2006 14:39:04 +02:00  DRAGNET.RAW
   # 58  -rw-        9600  Aug 20 2004 06:58:00 +02:00  Drums1.raw
   # 59  -rw-       13440  Aug 20 2004 06:58:00 +02:00  Drums2.raw
   # 60  -rw-       15840  Aug 20 2004 06:58:00 +02:00  FilmScore.raw
   # 61  -rw-       16080  Aug 20 2004 06:58:00 +02:00  HarpSynth.raw
   # 62  -rw-       16080   Sep 5 2006 14:40:00 +02:00  HOHOHO.RAW
   # 63  -rw-       16080   Sep 5 2006 14:39:30 +02:00  HORN.RAW
   # 64  -rw-        8160  Aug 20 2004 06:58:00 +02:00  Jamaica.raw
   # 65  -rw-       16080  Aug 20 2004 06:58:00 +02:00  KotoEffect.raw
   # 66  -rw-      496521  Mar 29 2004 13:40:48 +02:00  music-on-hold.au
   # 67  -rw-       12720  Aug 20 2004 06:58:00 +02:00  MusicBox.raw
   # 68  -rw-        8160  Aug 20 2004 06:58:00 +02:00  Piano1.raw
   # 69  -rw-       15360  Aug 20 2004 06:58:00 +02:00  Piano2.raw
   # 70  -rw-        9360  Aug 20 2004 06:58:00 +02:00  Pop.raw
   # 71  -rw-        7200  Aug 20 2004 06:58:00 +02:00  Pulse1.raw
   # 72  -rw-        4000  Aug 20 2004 06:58:00 +02:00  Ring1.raw
   # 73  -rw-        4000  Aug 20 2004 06:58:00 +02:00  Ring2.raw
   # 74  -rw-        4000  Aug 20 2004 06:58:00 +02:00  Ring3.raw
   # 75  -rw-        4000  Aug 20 2004 06:58:00 +02:00  Ring4.raw
   # 76  -rw-        4000  Aug 20 2004 06:58:00 +02:00  Ring5.raw
   # 77  -rw-        4000  Aug 20 2004 06:58:00 +02:00  Ring6.raw
   # 78  -rw-        4000  Aug 20 2004 06:58:00 +02:00  Ring7.raw
   # 79  -rw-        4021   Nov 5 2008 16:36:48 +01:00  RingList.xml
   # 80  -rw-       10800  Aug 20 2004 06:58:00 +02:00  Sax1.raw
   # 81  -rw-       14160  Aug 20 2004 06:58:00 +02:00  Sax2.raw
   # 82  -rw-       10648   Sep 5 2006 14:39:46 +02:00  SCOTTIE.RAW
   # 83  -rw-        6720   Sep 5 2006 14:39:50 +02:00  SHEEP.RAW
   # 84  -rw-       16080   Sep 5 2006 14:40:06 +02:00  SLEIGH.RAW
   # 85  -rw-       16080  Aug 20 2004 06:58:00 +02:00  Vibe.raw

class CCME(object):
    def __init__(self, url='http://192.168.0.4/arco/php/lib/cisco/webservice.php'):
        self._url=url

    def request(self, params):
        if params:
            r=requests.get(self._url, params=params, timeout=5.0)
            if r.status_code == requests.codes.ok:
                print r.text
                return r.text

    def play(self, user, sound='chime.raw'):
        params={'action':'play', 'user':user, 'sound':sound}
        return self.request(params)

    def ephones(self):
        params={'command':'ephones'}
        return self.request(params=params)


if __name__ == "__main__":
    pass
