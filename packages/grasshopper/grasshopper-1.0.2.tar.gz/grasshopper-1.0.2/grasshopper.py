import socket,logging
import select, errno
# from your hokey import app


class GrasshopperEngine:
	def __init__(self,host='',port=5555):
		self.host = host
		self.port = port
		self.app = None
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
			if self.host:
				host = self.host
			else:
				host = ''

			if self.port:
				port = self.port
			else:
				port = 5555
			self.listen_fd.bind((host,port))
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
	

		
	def install(self,app=None):
		#do_process inside app
		self.app = app
	def run(self):
		if not self.app:
			raise RuntimeError('please install your application!\nExample# engine.install(app)\n')
		
		connections = {}; addresses = {}; requests = {}; responses = {}; device_name = {} ; socket_map = {}

		while True:
			#///////////////////////////
			#print 'device_name{}	:',device_name,'\n'
			#print 'socket_map{}		:',socket_map ,'\n'
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
					device_name[conn.fileno()] = b''	# device_name..
#---------------------------------------------------------------------------
				elif select.EPOLLIN & events:
					datas = ''
					while True:
						try:
							data = connections[fd].recv(10)
							if not data and not datas:
								# Delete socket map 
								device_id = device_name[fd]
								del device_name[fd]
								del socket_map[device_id]
								#-----------------------
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
								if fd in device_name and device_name[fd]:
									print 'Already have key...'
								else:
									device_name[fd] = self.app.set_key()	# Should be the device-id
									device_id = device_name[fd]	# Get the device id ..
									socket_map[device_id] = fd	# Get a name of socket fd ..
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
