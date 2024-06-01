import time
import subprocess
import re
import sys

URL = 'google.com'
PATTERN_PACKETS_LOST = r'Lost\s*=\s*(\d+)\s*\((\d+%)\s*loss\)'
PATTERN_PING_AVG = r'Average\s*=\s*(\d+ms)'


def ping(url: str = URL):
    while True:
        process = subprocess.Popen(
            f'ping {url}',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        for char in '|/-\\' * 8:
            print(
                '\r' + f'Пожалуйста, подождите... {char} ', end='', flush=True
            )
            time.sleep(0.1)

        stdout, stderr = process.communicate()
        text_stdout = stdout.decode().strip()

        packets_lost_match = re.search(PATTERN_PACKETS_LOST, text_stdout)
        ping_avg_match = re.search(PATTERN_PING_AVG, text_stdout)

        if packets_lost_match and ping_avg_match:
            packets_lost = packets_lost_match.group()
            ping_avg = ping_avg_match.group()

            time_local = time.localtime()
            time_str = time.strftime('%H:%M:%S', time_local)

            print(
                '\r' + f'>>> {time_str} -> '
                f'{ping_avg}, '
                f'{packets_lost}'
            )
        else:
            print('Ошибка: Шаблон не найден.')


def main():
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        print('Введите URL (по умолчанию google.com):')
        url = input()

    url = url if url else URL
    ping(url)


if __name__ == '__main__':
    main()
