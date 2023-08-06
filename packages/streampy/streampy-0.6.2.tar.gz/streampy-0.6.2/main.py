from streampy import Stream
#
# element = Stream.range(100000) \
#     .parallel(process=3) \
#     .filter(lambda x: x % 2 == 0) \
#     .map(lambda x: str(x)) \
#     .map(lambda x: 'Hi{0}'.format(x)) \
#     .map(lambda x: x.upper()) \
#     .filter(lambda x: x.endswith('8')) \
#     .limit(10) \
#     .last()
#
# print Stream.file("test").size()

f = open("test")
Stream.file(f).size()

