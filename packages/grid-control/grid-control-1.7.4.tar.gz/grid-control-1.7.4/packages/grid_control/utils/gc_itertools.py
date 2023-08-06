# | Copyright 2016 Karlsruhe Institute of Technology
# |
# | Licensed under the Apache License, Version 2.0 (the "License");
# | you may not use this file except in compliance with the License.
# | You may obtain a copy of the License at
# |
# |     http://www.apache.org/licenses/LICENSE-2.0
# |
# | Unless required by applicable law or agreed to in writing, software
# | distributed under the License is distributed on an "AS IS" BASIS,
# | WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# | See the License for the specific language governing permissions and
# | limitations under the License.

import itertools

try: # Python <= 2.6
	ichain = itertools.chain.from_iterable
except Exception:
	ichain = lambda iterables: itertools.chain(*iterables)

def lchain(iterables):
	return list(ichain(iterables))

def tchain(iterables, timeout = None): # Combines multiple, threaded generators into single generator
	import time
	from grid_control.utils.thread_tools import start_thread, GCQueue
	threads = []
	result = GCQueue()
	for idx, it in enumerate(iterables):
		def generator_thread(iterator):
			try:
				for item in iterator:
					result.put(item)
			finally:
				result.put(GCQueue) # Use GCQueue as end-of-generator marker
		threads.append(start_thread('generator thread %d' % idx, generator_thread, it))

	if timeout is not None:
		t_end = time.time() + timeout
	while len(threads):
		try:
			if timeout is not None:
				timeout = max(0, t_end - time.time())
			tmp = result.get(timeout)
		except IndexError:
			break
		if tmp == GCQueue:
			threads.pop() # which thread is irrelevant - only used as counter
		else:
			yield tmp
