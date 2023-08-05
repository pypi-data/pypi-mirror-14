import asyncio
import io
import re
import types
import urllib
from uuid import uuid4

from .log import logger
from asyncio.streams import StreamReader

clients = []


class EventSocket(asyncio.Protocol):

    RETRY_TIME = 120
    peers = {}

    def __init__(self, **kwargs):
        self._loop = kwargs.get("loop", asyncio.get_event_loop())
        self.transport = None
        self._ev = {}
        self.ip = kwargs.get("ip")
        self._is_server = False
        self.last_line = [1,2]
        self._content_type_without_raw_data = ["auth/request", "text/disconnect-notice", "command/reply"]
        self._is_connected = False

    def connection_made(self, transport):
        self.peer, self.port = transport.get_extra_info("peername")
        # logger.info("%s connected" % str(transport.get_extra_info("peername")))

        if self._is_server:
            logger.info("Incoming connection from %s:%s" % (self.peer, self.port))
            self.peers["%s:%s" % (self.peer, self.port)] = self
        else:
            logger.info("Outgoing connection to %s:%s" % (self.peer, self.port))

        self.transport = transport
        self._is_connected = True
        self._reader = StreamReader(loop=self._loop)
        self._reader.set_transport(transport)
        self._reader_f = asyncio.ensure_future(self._reader_coroutine(), loop=self._loop)
        asyncio.ensure_future(self.start_server()) if self._is_server else None

    @asyncio.coroutine
    def _reader_coroutine(self):
        """
        Coroutine which reads input from the stream reader and processes it.
        """
        while self._is_connected:
            try:
                yield from self._handle_item()
            except asyncio.CancelledError:
                pass
            except Exception as e:
                print(e)
                return

    def parse_ev_attr(self, line):
        if line == "\n":
            return {}
        elif ":" in line:
            k, v = line.split(":", 1)
            k = k.strip()
            v = urllib.parse.unquote(v.strip())
            return {k: v}
        else:
            return {}

    def _get_plain_body(self, data):
        out = {}
        for line in data.split("\n"):
            out.update(self.parse_ev_attr(line))

        if out != {}:
            self._ev.update(out)


        # self._content_length_flag = -1
        # self.dispatch_event()

    @asyncio.coroutine
    def _handle_item(self):

        line = yield from self._reader.readline()
        # print(line)
        self.last_line = [self.last_line[-1], line]
        if line == b"\n" and self._ev != {}:
            # print(self.last_line)
            self.dispatch_event()
        else:
            ev_attr = self.parse_ev_attr(line.decode())
            if "Content-Length" in ev_attr.keys():
                raw_lenght = int(ev_attr["Content-Length"])
                content_type = yield from self._reader.readline()
                self._ev.update(self.parse_ev_attr(content_type.decode()))
                self._ev.update({"Content-Length":raw_lenght})

                data = yield from self._reader.readexactly(raw_lenght)
                data = data.decode()
                if self._ev.get("Content-Type") =="text/event-plain":
                    self._get_plain_body(data)
                else:

                    if data.startswith("Event-Name"):
                        self._get_plain_body(data)
                    elif data.startswith("-E"):
                        self._ev.update({"ErrorResponse": data})
                    else:
                        self._ev.update({"DataResponse": data})

                self.dispatch_event()

            else:
                self._ev.update(ev_attr)

    def data_received(self, data):
        # logger.debug("IN ESL>>>>: \n----START----\n%s\n----END----" % data.decode())
        self._reader.feed_data(data)

    def dispatch_event(self):
        # print(">>>>>>>>>>>>>>>>>SEND EVENT:", self._ev)
        ev = self._ev.copy()
        self._ev = {}
        self.event_received(ev)

    def event_received(self, ev):
        pass

    def transport_write(self, s):
        if self.transport is not None:
            self.transport.write(s.encode())
        else:
            logger.error("ESL not connected to %s" % self.ip)

    def send(self, cmd):
        self.transport_write(cmd+"\n\n")

    def send_msg(self, name, arg=None, uuid="", lock=False):
        self.transport_write("sendmsg %s\ncall-command: execute\n" % uuid)
        self.transport_write("execute-app-name: %s\n" % name)
        if arg:
            self.transport_write("execute-app-arg: %s\n" % arg)
        if lock is True:
            self.transport_write("event-lock: true\n")
        self.transport_write("\n\n")

    def raw_send(self, stuff):
        self.transport_write(stuff)

    def connection_lost(self, exc):
        p_peer = "%s:%s" % (self.peer, self.port)
        self.peers[p_peer] = self
        self.peers.pop(p_peer)

        if not self._is_server:
            logger.warning("Host %s. Connection lost. " % (str(self.transport.get_extra_info("peername")[0])))
            asyncio.ensure_future(self.retry_connect(ip=self.peer, port=self.port))

        if exc is None:
            self._reader.feed_eof()
        else:
            logger.info("Connection lost with exec: %s" % exc)
            self._reader.set_exception(exc)

        if self._reader_f:
            self._reader_f.cancel()

        self._is_connected = False
        self.transport = None
        self._reader = None
        self._reader_f = None

    async def retry_connect(self, ip="", port=""):
        self._is_connected = False
        if not self._is_server:
            self._is_connected = False

            if self.transport is not None:
                ip = self.transport.get_extra_info("peername")[0]
                port = self.transport.get_extra_info("peername")[1]

            await asyncio.sleep(self.RETRY_TIME)
            logger.info("Start connection to %s:%s" % (ip, port))
            try:
                await self._loop.create_connection(lambda: self, ip, port)
            except:

                logger.error("Can not connect ESL to %s:%s" % (ip, port))
                asyncio.ensure_future(self.retry_connect(ip=ip, port=port))
        else:
            pass
            # logger.warning("ESL protocol in Server mode.")

    def parse_raw_lines(self, lines):
        lines = lines.split("\n")
        out = {}
        for l in lines:
            if ":" in l:
                t = l.split(": ", maxsplit=1)
                out[t[0]] = t[1]

        return out

    def parse_raw_split(self, split="|", raw="", need_fields=[], kill_fl=False):

        data = []
        raw = raw.get("DataResponse")
        if raw is None:
            return data

        lines = raw.splitlines()
        if kill_fl and len(lines) > 1:
            lines = lines[1:]
            
        if len(lines) > 1:
            keys = lines[0].strip().split(split)
            for line in lines[1:]:
                fields = line.split(split)
                if len(fields) != len(keys):
                    continue
                r = {keys[i]: fields[i] for i in range(0, len(keys)) if keys[i] in need_fields or len(need_fields) == 0}
                data.append(r)

        return data


class EventProtocol(EventSocket):

    def __init__(self, **kwargs):
        EventSocket.__init__(self, **kwargs)
        self._ev_queue = []
        self._ev_cb = {
            "auth/request": self.auth_request,
            "api/response": self._api_response,
            "command/reply": self._command_reply,
            "text/event-plain": self._plain_event,
            "text/disconnect-notice": self.on_disconnect,
            "text/rude-rejection": self.on_rude_rejection,
        }

    def __protocol_send(self, name, args=""):
        future = asyncio.Future()
        self.send("%s %s" % (name, args))
        self._ev_queue.append((name, future))
        return future

    def __protocol_send_msg(self, name, args=None, uuid="", lock=False):
        future = asyncio.Future()
        self.send_msg(name, args, uuid, lock)
        self._ev_queue.append((name, future))
        return future

    def __protocol_send_raw(self, name, args=""):
        future = asyncio.Future()
        self.raw_send("%s %s" % (name, args))
        self._ev_queue.append((name, future))
        return future

    def event_received(self, ev):
        ct = ev.get("Content-Type", None)
        if ct is not None:
            method = self._ev_cb.get(ct, None)
            if callable(method):
                asyncio.ensure_future(method(ev))
            else:
                print(ct, ev)
                return self.unknown_content_type(ct, ev)

    async def auth_request(self, ev):
        pass

    async def _api_response(self, ev):
        cmd, future = self._ev_queue.pop(0)
        if cmd == "api":
            future.set_result(ev)
        else:
            logger.error("apiResponse on '%s': out of sync?" % cmd)

    async def _command_reply(self, ev):
        # print(ev)
        cmd, future = self._ev_queue.pop(0)
        # print (cmd, future)
        if ev.get("Reply-Text").startswith("+OK"):
            # print(">>>>>>>>>>>>>>>>")
            future.set_result(ev)

        elif ev.get("Reply-Text").startswith("-ERR"):
            future.set_result(ev.get("Reply-Text"))

        elif cmd == "auth":
            print("password error")
        else:
            # deferred.errback(EventError(ctx))
            pass

    async def _plain_event(self, ev):
        name = ev.get("Event-Name")
        method, evname = None, None
        if name is not None:
            evname = "on_" + name.lower().replace("_", "")
            method = getattr(self, evname, None)
        else:
            # if 'verto_host' in ctx.data:
            #     method = getattr(self, "onVertoEvent", None)
            # else:
            #     print "Event_Name not set in ctx.data."
                # print "Event_Name not set in ctx.data \n %s" % str(ctx.data)
            logger.error("Не могу получить метод. Не установлен Event_Name")

        if callable(method):
            return method(ev)
        else:
            return self.unbound_event(ev, evname)

    async def on_disconnect(self, ev):
        # print(" on_disconnect", ev)
        if not self._is_server:
            logger.warning("Host %s. %s " % (str(self.transport.get_extra_info("peername")[0]), ev["raw_data"].replace("\n","")))

    async def on_rude_rejection(self, ev):
        # print(" on_rude_rejection", ev)
        logger.warning("Host %s. %s " % (str(self.transport.get_extra_info("peername")[0]), ev["raw_data"].replace("\n","")))

    def unbound_event(self, ev, evname):
        logger.debug("Метод не определен %s" % evname)

    def unknown_content_type(self, content_type, ctx):
        logger.debug("unknown Content-Type: %s" % content_type)

    async def start_server(self):
        # await self.connect()
        pass

    # EVENT SOCKET COMMANDS

    def auth(self, args):
        """Please refer to http://wiki.freeswitch.org/wiki/Event_Socket#auth

        This method is allowed only for Inbound connections."""
        return self.__protocol_send("auth", args)

    def eventplain(self, args):
        "Please refer to http://wiki.freeswitch.org/wiki/Event_Socket#event"
        return self.__protocol_send('event plain', args)

    def event(self, args):
        "Please refer to http://wiki.freeswitch.org/wiki/Event_Socket#event"
        return self.__protocol_send_msg("event", args, lock=True)

    def connect(self):
        "Please refer to http://wiki.freeswitch.org/wiki/Event_Socket_Outbound#Using_Netcat"
        return self.__protocol_send("connect")

    def api(self, args):
        "Please refer to http://wiki.freeswitch.org/wiki/Event_Socket#api"
        return self.__protocol_send("api", args)

    def sendevent(self, name, args=dict(), body=None):
        "Please refer to http://wiki.freeswitch.org/wiki/Event_Socket#sendevent"
        parsed_args = [name]
        for k,v in args.iteritems():
            parsed_args.append('%s: %s' % (k, v))
        parsed_args.append('')
        if body:
            parsed_args.append(body)
        else:
            parsed_args.append('')
        return self.__protocol_send_raw("sendevent", '\n'.join(parsed_args))

    def bgapi(self, args):
        "Please refer to http://wiki.freeswitch.org/wiki/Event_Socket#bgapi"
        return self.__protocol_send("bgapi", args)

    def exit(self):
        "Please refer to http://wiki.freeswitch.org/wiki/Event_Socket#exit"
        return self.__protocol_send("exit")

    def linger(self, args=None):
        "Please refer to http://wiki.freeswitch.org/wiki/Event_Socket#event"
        return self.__protocol_send("linger", args)

    def filter(self, args):
        """Please refer to http://wiki.freeswitch.org/wiki/Event_Socket#filter

        The user might pass any number of values to filter an event for. But, from the point
        filter() is used, just the filtered events will come to the app - this is where this
        function differs from event().

        >>> filter('Event-Name MYEVENT')
        >>> filter('Unique-ID 4f37c5eb-1937-45c6-b808-6fba2ffadb63')
        """
        return self.__protocol_send('filter', args)

    def filter_delete(self, args):
        """Please refer to http://wiki.freeswitch.org/wiki/Event_Socket#filter_delete

        >>> filter_delete('Event-Name MYEVENT')
        """
        return self.__protocol_send('filter delete', args)

    def verbose_events(self):
        """Please refer to http://wiki.freeswitch.org/wiki/Misc._Dialplan_Tools_verbose_events

        >>> verbose_events()
        """
        return self.__protocol_send_msg('verbose_events', lock=True)

    def auth(self, args):
        """Please refer to http://wiki.freeswitch.org/wiki/Event_Socket#auth

        This method is allowed only for Inbound connections."""
        return self.__protocol_send("auth", args)

    def myevents(self):
        "Please refer to http://wiki.freeswitch.org/wiki/Event_Socket#event"
        return self.__protocol_send("myevents")

    def answer(self):
        "Please refer to http://wiki.freeswitch.org/wiki/Event_Socket_Outbound#Using_Netcat"
        return self.__protocol_send_msg("answer", lock=True)

    def bridge(self, args):
        """Please refer to http://wiki.freeswitch.org/wiki/Event_Socket_Outbound

        >>> bridge("{ignore_early_media=true}sofia/gateway/myGW/177808")
        """
        return self.__protocol_send_msg("bridge", args, lock=True)

    def hangup(self, reason=""):
        """Hangup may be used by both Inbound and Outbound connections.

        When used by Inbound connections, you may add the extra `reason`
        argument. Please refer to http://wiki.freeswitch.org/wiki/Event_Socket#hangup
        for details.

        When used by Outbound connections, the `reason` argument must be ignored.

        Please refer to http://wiki.freeswitch.org/wiki/Event_Socket_Outbound for
        details.
        """
        return self.__protocol_send_msg("hangup", reason, lock=True)

    def sched_api(self, args):
        "Please refer to http://wiki.freeswitch.org/wiki/Mod_commands#sched_api"
        return self.__protocol_send_msg("sched_api", args, lock=True)

    def ring_ready(self):
        "Please refer to http://wiki.freeswitch.org/wiki/Misc._Dialplan_Tools_ring_ready"
        return self.__protocol_send_msg("ring_ready")

    def record_session(self, filename):
        """Please refer to http://wiki.freeswitch.org/wiki/Misc._Dialplan_Tools_record_session

        >>> record_session("/tmp/dump.gsm")
        """
        return self.__protocol_send_msg("record_session", filename, lock=True)

    def read(self, args):
        """Please refer to http://wiki.freeswitch.org/wiki/Misc._Dialplan_Tools_read

        >>> read("0 10 $${base_dir}/sounds/en/us/callie/conference/8000/conf-pin.wav res 10000 #")
        """
        return self.__protocol_send_msg("read", args, lock=True)

    def bind_meta_app(self, args):
        """Please refer to http://wiki.freeswitch.org/wiki/Misc._Dialplan_Tools_bind_meta_app

        >>> bind_meta_app("2 ab s record_session::/tmp/dump.gsm")
        """
        return self.__protocol_send_msg("bind_meta_app", args, lock=True)

    def wait_for_silence(self, args):
        """Please refer to http://wiki.freeswitch.org/wiki/Misc._Dialplan_Tools_wait_for_silence

        >>> wait_for_silence("200 15 10 5000")
        """
        return self.__protocol_send_msg("wait_for_silence", args, lock=True)

    def sleep(self, milliseconds):
        """Please refer to http://wiki.freeswitch.org/wiki/Misc._Dialplan_Tools_sleep

        >>> sleep(5000)
        >>> sleep("5000")
        """
        return self.__protocol_send_msg("sleep", milliseconds, lock=True)

    def vmd(self, args):
        """Please refer to http://wiki.freeswitch.org/wiki/Mod_vmd

        >>> vmd("start")
        >>> vmd("stop")
        """
        return self.__protocol_send_msg("vmd", args, lock=True)

    def set(self, args):
        """Please refer to http://wiki.freeswitch.org/wiki/Misc._Dialplan_Tools_set

        >>> set("ringback=${us-ring}")
        """
        return self.__protocol_send_msg("set", args, lock=True)

    def set_global(self, args):
        """Please refer to http://wiki.freeswitch.org/wiki/Misc._Dialplan_Tools_set_global

        >>> set_global("global_var=value")
        """
        return self.__protocol_send_msg("set_global", args, lock=True)

    def unset(self, args):
        """Please refer to http://wiki.freeswitch.org/wiki/Misc._Dialplan_Tools_unset

        >>> unset("ringback")
        """
        return self.__protocol_send_msg("unset", args, lock=True)

    def start_dtmf(self):
        """Please refer to http://wiki.freeswitch.org/wiki/Misc._Dialplan_Tools_start_dtmf

        >>> start_dtmf()
        """
        return self.__protocol_send_msg("start_dtmf", lock=True)

    def stop_dtmf(self):
        """Please refer to http://wiki.freeswitch.org/wiki/Misc._Dialplan_Tools_stop_dtmf

        >>> stop_dtmf()
        """
        return self.__protocol_send_msg("stop_dtmf", lock=True)

    def start_dtmf_generate(self):
        """Please refer to http://wiki.freeswitch.org/wiki/Misc._Dialplan_Tools_start_dtmf_generate

        >>> start_dtmf_generate()
        """
        return self.__protocol_send_msg("start_dtmf_generate", "true", lock=True)

    def stop_dtmf_generate(self):
        """Please refer to http://wiki.freeswitch.org/wiki/Misc._Dialplan_Tools_stop_dtmf_generate

        >>> stop_dtmf_generate()
        """
        return self.__protocol_send_msg("stop_dtmf_generate", lock=True)

    def queue_dtmf(self, args):
        """Please refer to http://wiki.freeswitch.org/wiki/Misc._Dialplan_Tools_queue_dtmf

        Enqueue each received dtmf, that'll be sent once the call is bridged.

        >>> queue_dtmf("0123456789")
        """
        return self.__protocol_send_msg("queue_dtmf", args, lock=True)

    def flush_dtmf(self):
        """Please refer to http://wiki.freeswitch.org/wiki/Misc._Dialplan_Tools_flush_dtmf

        >>> flush_dtmf()
        """
        return self.__protocol_send_msg("flush_dtmf", lock=True)

    def play_fsv(self, filename):
        """Please refer to http://wiki.freeswitch.org/wiki/Mod_fsv

        >>> play_fsv("/tmp/video.fsv")
        """
        return self.__protocol_send_msg("play_fsv", filename, lock=True)

    def record_fsv(self, filename):
        """Please refer to http://wiki.freeswitch.org/wiki/Mod_fsv

        >>> record_fsv("/tmp/video.fsv")
        """
        return self.__protocol_send_msg("record_fsv", filename, lock=True)

    def record(self, args):
        """Please refer to http://wiki.freeswitch.org/wiki/Mod_record

        >>> record("/tmp/tmp.wav 20 200")
        """
        return self.__protocol_send_msg("record", args, lock=True)

    def playback(self, filename, terminators=None, lock=True):
        """Please refer to http://wiki.freeswitch.org/wiki/Mod_playback

        The optional argument `terminators` may contain a string with
        the characters that will terminate the playback.

        >>> playback("/tmp/dump.gsm", terminators="#8")

        In this case, the audio playback is automatically terminated
        by pressing either '#' or '8'.
        """
        self.set("playback_terminators=%s" % terminators or "none")
        return self.__protocol_send_msg("playback", filename, lock=lock)

    def transfer(self, args):
        """Please refer to https://freeswitch.org/confluence/display/FREESWITCH/mod_dptools%3A+transfer

        >>> transfer("3222 XML default")
        """
        return self.__protocol_send_msg("transfer", args, lock=True)

    def conference(self, args):
        """Please refer to http://wiki.freeswitch.org/wiki/Mod_conference#API_Reference

        >>> conference("myconf")
        """
        return self.__protocol_send_msg("conference", args, lock=True)

    def att_xfer(self, url):
        """Please refer to http://wiki.freeswitch.org/wiki/Misc._Dialplan_Tools_att_xfer

        >>> att_xfer("user/1001")
        """
        return self.__protocol_send_msg("att_xfer", url, lock=True)

    def send_break(self):
        return self.__protocol_send_msg("break", lock=True)

    def endless_playback(self, filename):
        """Please refer to http://wiki.freeswitch.org/wiki/Misc._Dialplan_Tools_endless_playback

        >>> endless_playback("/tmp/dump.gsm")
        """
        return self.__protocol_send_msg("endless_playback", filename, lock=True)

    def execute(self, command, args):
        """Please refer to http://wiki.freeswitch.org/wiki/Event_Socket_Library#execute

        >>> execute('voicemail', 'default $${domain} 1000')
        """
        return self.__protocol_send_msg(command, args, lock=True)

    def play_and_get_digits(self, args):
        """Please refer to https://freeswitch.org/confluence/display/FREESWITCH/mod_dptools%3A+play+and+get+digits

        >>> play_and_get_digits("2 5 3 7000 # $${base_dir}/sounds/en/us/callie/conference/8000/conf-pin.wav /invalid.wav foobar \d+")
        """
        return self.__protocol_send_msg("play_and_get_digits", args, lock=True)

    def displace_session(self, params):
        return self.__protocol_send_msg("displace_session", params, lock=True)

    # API ShortCats

    def uuid_getvar(self, uuid, varname):
        """
        Please refer to https://freeswitch.org/confluence/display/FREESWITCH/mod_commands
        :param args: [channel_uuid, var_name]
        :param lock:
        :return: Fuature
        """
        args = "%s %s %s" % ("uuid_getvar", uuid, varname)
        return self.api(args=args)

    def uuid_displace(self, uuid=None, action="start", file="$", limit="60", mux=""):
        """
        >>> uuid_displace <uuid> [start|stop] <file> [<limit>] [mux]
        :param uuid:
        :param action:
        :param file:
        :param limit:
        :param mux:
        :return:
        """

        params = "uuid_displace {uuid} {action} {file} {limit} {mux}".format(
            uuid=uuid, action=action, file=file, limit=limit, mux=mux)
        print(params)
        return self.api(params)
