import uuid
import base64
import binascii

class ArcUUID:

    LENGTH = 26

    def __init__(self, str_arc_uuid=None):
        if not str_arc_uuid:
            gen_uuid = uuid.uuid4()
            self.id = str(base64.b32encode(gen_uuid.bytes)).replace('=', '').replace('b\'', '').replace('\'', '') # to remove padding
        else:
            if len(str_arc_uuid) != ArcUUID.LENGTH:
                raise ValueError("This arcUUID doesn't meet the length expectations of an ArcUUID:" + str_arc_uuid)
            try:
                # just to see if string has non-alphabet characters. we already know length is 26 so we pad by 6 ='s to
                # length 32 to meet base32 spec
                base64.b32decode(str_arc_uuid + "======")
            except binascii.Error:
                raise ValueError("This arcUUID has characters that aren't in the Base32 encoding:" + str_arc_uuid)
            self.id = str_arc_uuid

    def __str__(self):
        return self.id

    @staticmethod
    def random_arc_uuid():
        return ArcUUID()

    @staticmethod
    def from_string(str_arc_uuid):
        if not str_arc_uuid:
            raise ValueError("Cannot construct an ArcUUID off a None value!")
        return ArcUUID(str_arc_uuid=str_arc_uuid)

    def __hash__(self):
        hash_code = 5
        hash_code = 43 * hash_code + self.id.__hash__()
        return hash_code

    def __eq__(self, other):
        if not other:
            return False
        if not isinstance(other, ArcUUID):
            return False
        if not self.id == other.id:
            return False
        return True
