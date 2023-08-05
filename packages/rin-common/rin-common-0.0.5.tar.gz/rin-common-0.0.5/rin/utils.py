import socket

class Utils(object):
  @classmethod
  def validate_ipv4(self, addr):
    try:
      socket.inet_aton(addr)
      return True
    except socket.error:
      return False
