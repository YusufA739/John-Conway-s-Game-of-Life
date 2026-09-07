import time
#
# start = time.perf_counter()
# for carrier in range (10000000):
#     if not True:
#         time.sleep(0)
#
# end = time.perf_counter()
# print(end-start)
#
#
# start = time.perf_counter()
# for carrier in range (10000000):
#     time.sleep(0)
#
# end = time.perf_counter()
# print(end-start)
#
#
# start = time.perf_counter()
# for carrier in range (10000000):
#     time.sleep(0)
#
# end = time.perf_counter()
# print(end-start)


print("if 1==0: vs if 1 < 0:")
start = time.perf_counter()
for carrier in range (10000000):
    if 1==0:
        time.sleep(0)

end = time.perf_counter()
print(end-start)


start = time.perf_counter()
for carrier in range (10000000):
    if not 1 > 0:
        time.sleep(0)

end = time.perf_counter()
print(end-start)