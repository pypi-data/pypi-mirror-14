import socket,logging
import select, errno
# from your hokey import app


class GrasshopperEngine:
	def __init__(self):
		try:
			# Create TCP socket
			self.listen_fd = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
		except socket.error, msg:
			print 'Create socket failed'

		try:
			# Set SO_REUSEADDR optional
			self.listen_fd.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		except socket.error, msg:
			print 'setsocketopt SO_REUSEADDR failed'

		try:
			# do bind
			self.listen_fd.bind(('',5555))
		except socket.error, msg:
			print 'bind failed'

		try:
			# set listen number
			self.listen_fd.listen(10)
		except socket.error, msg:
			print 'set listen: ',msg

		try:
			# Create epoll handler
			self.epoll_fd = select.epoll()
			self.epoll_fd.register(self.listen_fd.fileno(), select.EPOLLIN)
		except select.error, msg:
			print 'create epoll info:' ,msg
	
		
	def install(self,app):
		#do_process inside app
		self.app = app
	def run(self):
		connections = {}; addresses = {}; requests = {}; responses = {}
		while True:
			# epoll event ...
			epoll_list = self.epoll_fd.poll(1)

			for fd, events in epoll_list:
#---------------------------------------------------------------------------
				if fd == self.listen_fd.fileno():
					conn, addr = self.listen_fd.accept()
					# set socket fd as nonblocking
					conn.setblocking(0)
					self.epoll_fd.register(conn.fileno(), select.EPOLLIN | select.EPOLLET)
					connections[conn.fileno()] = conn
					addresses[conn.fileno()] = addr
					responses[conn.fileno()] = b''
					requests[conn.fileno()] = b''
#---------------------------------------------------------------------------
				elif select.EPOLLIN & events:
					datas = ''
					while True:
						try:
							data = connections[fd].recv(10)
							if not data and not datas:
								self.epoll_fd.unregister(fd)
								connections[fd].close()
								print '%s, %d closed' % (addresses[fd][0],addresses[fd][1])
								break
							else:
								datas += data
						except socket.error, msg:
							if msg.errno == errno.EAGAIN:
								requests[fd] = datas
								responses[fd]=self.app.process_request(datas)	# For app ................
								self.epoll_fd.modify(fd, select.EPOLLET | select.EPOLLOUT)
								break
							else:
								self.epoll_fd.unregister(fd)
								connections[fd].close()
								break
#---------------------------------------------------------------------------
				elif select.EPOLLOUT & events:
					send_length = 0
					while True:
						#send_length += connections[fd].send(requests[fd][send_length:])
						send_length += connections[fd].send(responses[fd])
						if send_length == len(responses[fd]):
							break

					self.epoll_fd.modify(fd, select.EPOLLIN | select.EPOLLET)
#---------------------------------------------------------------------------
				elif select.EPOLLHUP & events:
					self.epoll_fd.unregister(fd)
					connections[fd].close()
#---------------------------------------------------------------------------
				else:
					continue
