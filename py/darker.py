# A countdown program for Dark and Darker Goblin Caves

import time
import winsound

# Shrinking Timings: 150, 255, 105, 85
circles = [150, 255, 105, 85]
# circles = [5, 5, 5, 5]
warn_t = 5
filenames = ["ding", "ding", "ding", "Speech Disambiguation"]


def beep(f, t):
    s = time.perf_counter()
    winsound.Beep(f, t)

    time.sleep(1 - (time.perf_counter() - s))


def warn():
    for i, name in enumerate(filenames):
        s = time.perf_counter()
        count = len(filenames) - i - 1
        print("." if count else "Go!", end="" if count else "\r", flush=True)
        winsound.PlaySound(f"C:\Windows\Media\{name}.wav", winsound.SND_FILENAME)
        time.sleep(1 - (time.perf_counter() - s))


def countdown(c=warn_t):
    for i in range(c - 1):
        print(c - i)
        beep(300, 100)

    beep(500, 250)


def main():
    for i, t in enumerate(circles):
        s = time.perf_counter()
        count = len(circles) - i - 1
        round = "Round " + str(i + 1) if count else "Final Round"
        # round = i + 1

        # print("Round", round if count else "Final round!")
        print("                         ", end="\r", flush=True)
        print(round, end="", flush=True)
        warn()
        # countdown(warn_t * 2 if count else warn_t)

        time.sleep(t - (time.perf_counter() - s))

    time.sleep(2)
    print("u ded lol. get guud")


if __name__ == "__main__":
    main()
