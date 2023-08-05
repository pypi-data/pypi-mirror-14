import sys

def fuga():
  print("[hoge] > %s" % (sys.argv[1:]))

if __name__ == "__main__":
  fuga()
