# coding:utf-8

import _thread
from time import sleep, ctime

loops = [4,2]


def loop(nloop, nsec, lock):
    print("start loop", nloop, "at:", ctime())
    sleep(nsec)
    print("loop", nloop, "done at:", ctime())
    lock.release() # 每个线程在执行完成的时候都会释放自己的锁对象


def main():
    print("starting at:", ctime())
    locks = []
    nloops = range(len(loops))
    # 创建一个锁的列表
    for i in nloops:
        lock = _thread.allocate_lock() # 取得锁对象
        lock.acquire() # 取得锁，相当于把锁锁上
        print(lock)
        locks.append(lock) # 填加到锁列表locks中

    # 下面这个循环用于派生线程
    for i in nloops:
        _thread.start_new_thread(loop, (i, loops[i], locks[i]))

    # 循序检查锁列表中所有的锁都被释放了，这样执行慢的线程会一直循环等待直至线程执行结束，释放锁对象
    for i in nloops:
        while locks[i].locked():pass

    print("all DONE at:", ctime())

if __name__ == "__main__":
    main()
