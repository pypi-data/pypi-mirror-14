#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import random
import subprocess
import time


def await(command, cap, base, await_fail):
    attempt = 0

    while True:
        failed = False
        print 'Running "{}", attempt: {}'.format(command, attempt)
        try:
            subprocess.check_call(command, shell=True)
        except subprocess.CalledProcessError:
            failed = True

        if (not failed) or (failed and await_fail):
            return
        else:  # Backoff
            sleep_time = random.uniform(0, min(cap, base * pow(2, attempt)))
            attempt += 1
            time.sleep(sleep_time / 1000.0)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', help='The command to run')
    parser.add_argument('-f', '--await-failure',
                        help='Wait for the command to fail instead of succeed')
    parser.add_argument('-c', '--backoff-cap', default=4000, type=int,
                        help='The maximum amount to wait for in backoff, in milliseconds')
    parser.add_argument('-b', '--backoff-base', default=20, type=int,
                        help='The base amount to backoff by (e.g. the first backoff period) in milliseconds')
    args = parser.parse_args()

    await(args.command, args.backoff_cap, args.backoff_base, args.await_failure)


if __name__ == '__main__':
    main()
