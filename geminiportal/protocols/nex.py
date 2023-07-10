from __future__ import annotations

from geminiportal.protocols.base import BaseRequest, BaseResponse


class NexRequest(BaseRequest):
    """
    Encapsulates a nex:// request.
    """

    async def fetch(self) -> NexResponse:
        reader, writer = await self.open_connection()

        selector = self.url.path
        writer.write(f"{selector}\r\n".encode())
        await writer.drain()

        return NexResponse(self, reader, writer)


class NexResponse(BaseResponse):
    STATUS_CODES = {"": "SUCCESS"}

    def __init__(self, request, reader, writer):
        self.request = request
        self.reader = reader
        self.writer = writer
        self.status = ""
        self.meta = ""

        if not self.url.path or self.url.path.endswith("/"):
            self.mimetype = "text/nex"
        else:
            self.mimetype = self.url.guess_mimetype() or "text/plain"

        self.charset = "UTF-8"
        self.lang = None

    def is_success(self):
        return True
