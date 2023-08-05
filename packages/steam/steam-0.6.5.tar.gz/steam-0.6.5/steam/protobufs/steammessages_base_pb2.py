# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: steammessages_base.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)


import google.protobuf.descriptor_pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='steammessages_base.proto',
  package='',
  serialized_pb='\n\x18steammessages_base.proto\x1a google/protobuf/descriptor.proto\"\xf8\x03\n\x12\x43MsgProtoBufHeader\x12\x0f\n\x07steamid\x18\x01 \x01(\x06\x12\x18\n\x10\x63lient_sessionid\x18\x02 \x01(\x05\x12\x15\n\rrouting_appid\x18\x03 \x01(\r\x12*\n\x0cjobid_source\x18\n \x01(\x06:\x14\x31\x38\x34\x34\x36\x37\x34\x34\x30\x37\x33\x37\x30\x39\x35\x35\x31\x36\x31\x35\x12*\n\x0cjobid_target\x18\x0b \x01(\x06:\x14\x31\x38\x34\x34\x36\x37\x34\x34\x30\x37\x33\x37\x30\x39\x35\x35\x31\x36\x31\x35\x12\x17\n\x0ftarget_job_name\x18\x0c \x01(\t\x12\x0f\n\x07seq_num\x18\x18 \x01(\x05\x12\x12\n\x07\x65result\x18\r \x01(\x05:\x01\x32\x12\x15\n\rerror_message\x18\x0e \x01(\t\x12\n\n\x02ip\x18\x0f \x01(\r\x12\x1a\n\x12\x61uth_account_flags\x18\x10 \x01(\r\x12\x14\n\x0ctoken_source\x18\x16 \x01(\r\x12\x1b\n\x13\x61\x64min_spoofing_user\x18\x17 \x01(\x08\x12\x1a\n\x0ftransport_error\x18\x11 \x01(\x05:\x01\x31\x12\'\n\tmessageid\x18\x12 \x01(\x04:\x14\x31\x38\x34\x34\x36\x37\x34\x34\x30\x37\x33\x37\x30\x39\x35\x35\x31\x36\x31\x35\x12\x1a\n\x12publisher_group_id\x18\x13 \x01(\r\x12\r\n\x05sysid\x18\x14 \x01(\r\x12\x11\n\ttrace_tag\x18\x15 \x01(\x04\x12\x15\n\rwebapi_key_id\x18\x19 \x01(\r\"8\n\tCMsgMulti\x12\x15\n\rsize_unzipped\x18\x01 \x01(\r\x12\x14\n\x0cmessage_body\x18\x02 \x01(\x0c\"+\n\x13\x43MsgProtobufWrapped\x12\x14\n\x0cmessage_body\x18\x01 \x01(\x0c\"\x8f\x01\n\x0e\x43MsgAuthTicket\x12\x0e\n\x06\x65state\x18\x01 \x01(\r\x12\x12\n\x07\x65result\x18\x02 \x01(\r:\x01\x32\x12\x0f\n\x07steamid\x18\x03 \x01(\x06\x12\x0e\n\x06gameid\x18\x04 \x01(\x06\x12\x14\n\x0ch_steam_pipe\x18\x05 \x01(\r\x12\x12\n\nticket_crc\x18\x06 \x01(\r\x12\x0e\n\x06ticket\x18\x07 \x01(\x0c\"\xf6\x01\n\x14\x43\x43\x44\x44\x42\x41ppDetailCommon\x12\r\n\x05\x61ppid\x18\x01 \x01(\r\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0c\n\x04icon\x18\x03 \x01(\t\x12\x0c\n\x04logo\x18\x04 \x01(\t\x12\x12\n\nlogo_small\x18\x05 \x01(\t\x12\x0c\n\x04tool\x18\x06 \x01(\x08\x12\x0c\n\x04\x64\x65mo\x18\x07 \x01(\x08\x12\r\n\x05media\x18\x08 \x01(\x08\x12\x1f\n\x17\x63ommunity_visible_stats\x18\t \x01(\x08\x12\x15\n\rfriendly_name\x18\n \x01(\t\x12\x13\n\x0bpropagation\x18\x0b \x01(\t\x12\x19\n\x11has_adult_content\x18\x0c \x01(\x08\"\xef\x02\n\rCMsgAppRights\x12\x11\n\tedit_info\x18\x01 \x01(\x08\x12\x0f\n\x07publish\x18\x02 \x01(\x08\x12\x17\n\x0fview_error_data\x18\x03 \x01(\x08\x12\x10\n\x08\x64ownload\x18\x04 \x01(\x08\x12\x15\n\rupload_cdkeys\x18\x05 \x01(\x08\x12\x17\n\x0fgenerate_cdkeys\x18\x06 \x01(\x08\x12\x17\n\x0fview_financials\x18\x07 \x01(\x08\x12\x12\n\nmanage_ceg\x18\x08 \x01(\x08\x12\x16\n\x0emanage_signing\x18\t \x01(\x08\x12\x15\n\rmanage_cdkeys\x18\n \x01(\x08\x12\x16\n\x0e\x65\x64it_marketing\x18\x0b \x01(\x08\x12\x17\n\x0f\x65\x63onomy_support\x18\x0c \x01(\x08\x12\"\n\x1a\x65\x63onomy_support_supervisor\x18\r \x01(\x08\x12\x16\n\x0emanage_pricing\x18\x0e \x01(\x08\x12\x16\n\x0e\x62roadcast_live\x18\x0f \x01(\x08:A\n\x12msgpool_soft_limit\x12\x1f.google.protobuf.MessageOptions\x18\xd0\x86\x03 \x01(\x05:\x02\x33\x32:B\n\x12msgpool_hard_limit\x12\x1f.google.protobuf.MessageOptions\x18\xd1\x86\x03 \x01(\x05:\x03\x33\x38\x34\x42\x05H\x01\x80\x01\x00')


MSGPOOL_SOFT_LIMIT_FIELD_NUMBER = 50000
msgpool_soft_limit = _descriptor.FieldDescriptor(
  name='msgpool_soft_limit', full_name='msgpool_soft_limit', index=0,
  number=50000, type=5, cpp_type=1, label=1,
  has_default_value=True, default_value=32,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)
MSGPOOL_HARD_LIMIT_FIELD_NUMBER = 50001
msgpool_hard_limit = _descriptor.FieldDescriptor(
  name='msgpool_hard_limit', full_name='msgpool_hard_limit', index=1,
  number=50001, type=5, cpp_type=1, label=1,
  has_default_value=True, default_value=384,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)


_CMSGPROTOBUFHEADER = _descriptor.Descriptor(
  name='CMsgProtoBufHeader',
  full_name='CMsgProtoBufHeader',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='steamid', full_name='CMsgProtoBufHeader.steamid', index=0,
      number=1, type=6, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='client_sessionid', full_name='CMsgProtoBufHeader.client_sessionid', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='routing_appid', full_name='CMsgProtoBufHeader.routing_appid', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='jobid_source', full_name='CMsgProtoBufHeader.jobid_source', index=3,
      number=10, type=6, cpp_type=4, label=1,
      has_default_value=True, default_value=18446744073709551615,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='jobid_target', full_name='CMsgProtoBufHeader.jobid_target', index=4,
      number=11, type=6, cpp_type=4, label=1,
      has_default_value=True, default_value=18446744073709551615,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='target_job_name', full_name='CMsgProtoBufHeader.target_job_name', index=5,
      number=12, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='seq_num', full_name='CMsgProtoBufHeader.seq_num', index=6,
      number=24, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='eresult', full_name='CMsgProtoBufHeader.eresult', index=7,
      number=13, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=2,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='error_message', full_name='CMsgProtoBufHeader.error_message', index=8,
      number=14, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ip', full_name='CMsgProtoBufHeader.ip', index=9,
      number=15, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='auth_account_flags', full_name='CMsgProtoBufHeader.auth_account_flags', index=10,
      number=16, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='token_source', full_name='CMsgProtoBufHeader.token_source', index=11,
      number=22, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='admin_spoofing_user', full_name='CMsgProtoBufHeader.admin_spoofing_user', index=12,
      number=23, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='transport_error', full_name='CMsgProtoBufHeader.transport_error', index=13,
      number=17, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='messageid', full_name='CMsgProtoBufHeader.messageid', index=14,
      number=18, type=4, cpp_type=4, label=1,
      has_default_value=True, default_value=18446744073709551615,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='publisher_group_id', full_name='CMsgProtoBufHeader.publisher_group_id', index=15,
      number=19, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sysid', full_name='CMsgProtoBufHeader.sysid', index=16,
      number=20, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='trace_tag', full_name='CMsgProtoBufHeader.trace_tag', index=17,
      number=21, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='webapi_key_id', full_name='CMsgProtoBufHeader.webapi_key_id', index=18,
      number=25, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=63,
  serialized_end=567,
)


_CMSGMULTI = _descriptor.Descriptor(
  name='CMsgMulti',
  full_name='CMsgMulti',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='size_unzipped', full_name='CMsgMulti.size_unzipped', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='message_body', full_name='CMsgMulti.message_body', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=569,
  serialized_end=625,
)


_CMSGPROTOBUFWRAPPED = _descriptor.Descriptor(
  name='CMsgProtobufWrapped',
  full_name='CMsgProtobufWrapped',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='message_body', full_name='CMsgProtobufWrapped.message_body', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=627,
  serialized_end=670,
)


_CMSGAUTHTICKET = _descriptor.Descriptor(
  name='CMsgAuthTicket',
  full_name='CMsgAuthTicket',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='estate', full_name='CMsgAuthTicket.estate', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='eresult', full_name='CMsgAuthTicket.eresult', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=True, default_value=2,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='steamid', full_name='CMsgAuthTicket.steamid', index=2,
      number=3, type=6, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='gameid', full_name='CMsgAuthTicket.gameid', index=3,
      number=4, type=6, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='h_steam_pipe', full_name='CMsgAuthTicket.h_steam_pipe', index=4,
      number=5, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ticket_crc', full_name='CMsgAuthTicket.ticket_crc', index=5,
      number=6, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ticket', full_name='CMsgAuthTicket.ticket', index=6,
      number=7, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=673,
  serialized_end=816,
)


_CCDDBAPPDETAILCOMMON = _descriptor.Descriptor(
  name='CCDDBAppDetailCommon',
  full_name='CCDDBAppDetailCommon',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='appid', full_name='CCDDBAppDetailCommon.appid', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='name', full_name='CCDDBAppDetailCommon.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='icon', full_name='CCDDBAppDetailCommon.icon', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='logo', full_name='CCDDBAppDetailCommon.logo', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='logo_small', full_name='CCDDBAppDetailCommon.logo_small', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='tool', full_name='CCDDBAppDetailCommon.tool', index=5,
      number=6, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='demo', full_name='CCDDBAppDetailCommon.demo', index=6,
      number=7, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='media', full_name='CCDDBAppDetailCommon.media', index=7,
      number=8, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='community_visible_stats', full_name='CCDDBAppDetailCommon.community_visible_stats', index=8,
      number=9, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='friendly_name', full_name='CCDDBAppDetailCommon.friendly_name', index=9,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='propagation', full_name='CCDDBAppDetailCommon.propagation', index=10,
      number=11, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='has_adult_content', full_name='CCDDBAppDetailCommon.has_adult_content', index=11,
      number=12, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=819,
  serialized_end=1065,
)


_CMSGAPPRIGHTS = _descriptor.Descriptor(
  name='CMsgAppRights',
  full_name='CMsgAppRights',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='edit_info', full_name='CMsgAppRights.edit_info', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='publish', full_name='CMsgAppRights.publish', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='view_error_data', full_name='CMsgAppRights.view_error_data', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='download', full_name='CMsgAppRights.download', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='upload_cdkeys', full_name='CMsgAppRights.upload_cdkeys', index=4,
      number=5, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='generate_cdkeys', full_name='CMsgAppRights.generate_cdkeys', index=5,
      number=6, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='view_financials', full_name='CMsgAppRights.view_financials', index=6,
      number=7, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='manage_ceg', full_name='CMsgAppRights.manage_ceg', index=7,
      number=8, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='manage_signing', full_name='CMsgAppRights.manage_signing', index=8,
      number=9, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='manage_cdkeys', full_name='CMsgAppRights.manage_cdkeys', index=9,
      number=10, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='edit_marketing', full_name='CMsgAppRights.edit_marketing', index=10,
      number=11, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='economy_support', full_name='CMsgAppRights.economy_support', index=11,
      number=12, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='economy_support_supervisor', full_name='CMsgAppRights.economy_support_supervisor', index=12,
      number=13, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='manage_pricing', full_name='CMsgAppRights.manage_pricing', index=13,
      number=14, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='broadcast_live', full_name='CMsgAppRights.broadcast_live', index=14,
      number=15, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=1068,
  serialized_end=1435,
)

DESCRIPTOR.message_types_by_name['CMsgProtoBufHeader'] = _CMSGPROTOBUFHEADER
DESCRIPTOR.message_types_by_name['CMsgMulti'] = _CMSGMULTI
DESCRIPTOR.message_types_by_name['CMsgProtobufWrapped'] = _CMSGPROTOBUFWRAPPED
DESCRIPTOR.message_types_by_name['CMsgAuthTicket'] = _CMSGAUTHTICKET
DESCRIPTOR.message_types_by_name['CCDDBAppDetailCommon'] = _CCDDBAPPDETAILCOMMON
DESCRIPTOR.message_types_by_name['CMsgAppRights'] = _CMSGAPPRIGHTS

class CMsgProtoBufHeader(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _CMSGPROTOBUFHEADER

  # @@protoc_insertion_point(class_scope:CMsgProtoBufHeader)

class CMsgMulti(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _CMSGMULTI

  # @@protoc_insertion_point(class_scope:CMsgMulti)

class CMsgProtobufWrapped(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _CMSGPROTOBUFWRAPPED

  # @@protoc_insertion_point(class_scope:CMsgProtobufWrapped)

class CMsgAuthTicket(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _CMSGAUTHTICKET

  # @@protoc_insertion_point(class_scope:CMsgAuthTicket)

class CCDDBAppDetailCommon(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _CCDDBAPPDETAILCOMMON

  # @@protoc_insertion_point(class_scope:CCDDBAppDetailCommon)

class CMsgAppRights(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _CMSGAPPRIGHTS

  # @@protoc_insertion_point(class_scope:CMsgAppRights)

google.protobuf.descriptor_pb2.MessageOptions.RegisterExtension(msgpool_soft_limit)
google.protobuf.descriptor_pb2.MessageOptions.RegisterExtension(msgpool_hard_limit)

DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), 'H\001\200\001\000')
# @@protoc_insertion_point(module_scope)
